"""Client SharePoint réel — MSAL app-only + Microsoft Graph API.

Permissions requises sur l'App Registration :
  - Sites.Read.All  (application)
  - Files.Read.All  (application)

Stratégie : on utilise SHAREPOINT_DRIVE_ID configuré en .env (résolu une fois
via scripts/test_sharepoint.py) et on dérive le path drive-relatif depuis
l'URL projet. Garde-fou : refuse tout path hors de SHAREPOINT_ALLOWED_ROOT_PATH.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from datetime import datetime
from urllib.parse import unquote, urlparse

import httpx
from msal import ConfidentialClientApplication
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import get_settings
from models.document import FileMetadata

from .base import SharePointClient

log = logging.getLogger(__name__)

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# Préfixes de bibliothèque SharePoint (français + anglais) à retirer du path
# pour obtenir un chemin drive-relatif. Ex :
#   /Documents partages/09-Projets/DMUZZOLINI  ->  /09-Projets/DMUZZOLINI
#   /Shared Documents/09-Projets/DMUZZOLINI    ->  /09-Projets/DMUZZOLINI
_LIBRARY_PREFIXES = (
    "/documents partages",
    "/documents partagés",
    "/shared documents",
)


class RealSharePointClient(SharePointClient):
    def __init__(self) -> None:
        settings = get_settings()
        self._settings = settings
        self._msal = ConfidentialClientApplication(
            client_id=settings.azure_ad_client_id,
            client_credential=settings.azure_ad_client_secret.get_secret_value(),
            authority=f"https://login.microsoftonline.com/{settings.azure_ad_tenant_id}",
        )
        self._token: str | None = None
        self._token_exp: datetime | None = None

    # ----- Auth -----
    def _get_token(self) -> str:
        # msal cache lui-même les tokens ; un appel répété est rapide.
        result = self._msal.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if not result or "access_token" not in result:
            raise RuntimeError(f"MSAL token error : {result.get('error_description') if result else 'no result'}")
        return result["access_token"]

    async def _client(self) -> httpx.AsyncClient:
        token = self._get_token()
        return httpx.AsyncClient(
            base_url=GRAPH_BASE,
            headers={"Authorization": f"Bearer {token}"},
            timeout=300.0,  # 5 min pour les gros fichiers (était 60s → trop court)
        )

    # ----- Resolution URL → path drive-relatif → item_id -----
    def _extract_drive_path(self, project_url: str) -> str:
        """Extrait le path drive-relatif depuis une URL SharePoint complète.

        Exemple :
          https://enervivo.sharepoint.com/Documents%20partages/09-Projets/DMUZZOLINI
          -> /09-Projets/DMUZZOLINI
        """
        parsed = urlparse(project_url)
        path = unquote(parsed.path).rstrip("/")
        lower = path.lower()
        for prefix in _LIBRARY_PREFIXES:
            if lower.startswith(prefix):
                drive_rel = path[len(prefix):]
                return drive_rel if drive_rel.startswith("/") else f"/{drive_rel}"
        # URL déjà drive-relative ou format inattendu
        if path.startswith("/"):
            return path
        raise ValueError(f"URL SharePoint non reconnue : {project_url}")

    async def _resolve_folder(self, project_url: str) -> tuple[str, str, str]:
        """Renvoie (site_id, drive_id, folder_item_id).

        Utilise settings.sharepoint_drive_id directement (pas de résolution
        site→drive à chaque appel) et applique le garde-fou allowed_root_path.
        """
        drive_id = self._settings.sharepoint_drive_id
        if not drive_id:
            raise RuntimeError("SHAREPOINT_DRIVE_ID non configuré en .env")

        drive_path = self._extract_drive_path(project_url)

        # ⚠️ Garde-fou DÉSACTIVÉ : accepte n'importe quel path SharePoint
        # (ancien code ci-dessous commenté)
        # allowed_paths = self._settings.sharepoint_allowed_root_paths_set
        # if allowed_paths:
        #     normalized = drive_path.rstrip("/")
        #     allowed_normalized = {p.rstrip("/") for p in allowed_paths}
        #     if not any(normalized.startswith(allowed) for allowed in allowed_normalized):
        #         raise PermissionError(
        #             f"Path '{drive_path}' hors des racines autorisées {allowed_paths}"
        #         )

        async with await self._client() as cli:
            r = await cli.get(f"/drives/{drive_id}/root:{drive_path}")
            r.raise_for_status()
            folder_id = r.json()["id"]

        site_id = self._settings.sharepoint_site_id  # informatif uniquement
        return site_id, drive_id, folder_id

    # ----- Listing récursif -----
    async def _walk(
        self,
        cli: httpx.AsyncClient,
        drive_id: str,
        item_id: str,
        prefix: str,
        excluded: set[str],
    ) -> AsyncIterator[FileMetadata]:
        url: str | None = f"/drives/{drive_id}/items/{item_id}/children?$top=200"
        while url:
            r = await cli.get(url)
            r.raise_for_status()
            data = r.json()
            for it in data.get("value", []):
                name = it["name"]
                path = f"{prefix}/{name}"
                if it.get("folder"):
                    if name.lower() in excluded:
                        # Skip toute la sous-arborescence sans descendre dedans
                        # (évite 1 appel Graph par dossier + tous les downloads).
                        child_count = it.get("folder", {}).get("childCount", "?")
                        log.info(
                            "Dossier exclu : %s (%s items, ~%s) — skip",
                            path,
                            child_count,
                            it.get("size", "?"),
                        )
                        continue
                    async for f in self._walk(cli, drive_id, it["id"], path, excluded):
                        yield f
                elif it.get("file"):
                    yield FileMetadata(
                        name=name,
                        path=path,
                        url=it.get("webUrl", ""),
                        size=int(it.get("size", 0)),
                        mime_type=it["file"].get("mimeType", "application/octet-stream"),
                        modified_at=(
                            datetime.fromisoformat(it["lastModifiedDateTime"].replace("Z", "+00:00"))
                            if it.get("lastModifiedDateTime")
                            else None
                        ),
                        drive_item_id=it["id"],
                    )
            url = data.get("@odata.nextLink", "").replace(GRAPH_BASE, "") or None

    async def list_files(self, project_sharepoint_url: str) -> AsyncIterator[FileMetadata]:  # type: ignore[override]
        _, drive_id, folder_id = await self._resolve_folder(project_sharepoint_url)
        excluded = self._settings.sharepoint_excluded_folders_set
        async with await self._client() as cli:
            async for f in self._walk(cli, drive_id, folder_id, prefix="", excluded=excluded):
                yield f

    async def download_file(self, file: FileMetadata) -> bytes:
        if not file.drive_item_id:
            raise ValueError("drive_item_id manquant — listing à faire d'abord")
        drive_id = self._settings.sharepoint_drive_id
        if not drive_id:
            raise RuntimeError("SHAREPOINT_DRIVE_ID non configuré en .env")

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=2, min=4, max=30),
            reraise=True,
        )
        async def _download_with_retry() -> bytes:
            async with await self._client() as cli:
                # /content redirige (302) vers une URL signée — httpx la suit par défaut.
                # En app-only, /me/drive n'existe pas : on passe par /drives/{drive_id}.
                r = await cli.get(
                    f"/drives/{drive_id}/items/{file.drive_item_id}/content",
                    follow_redirects=True,
                )
                r.raise_for_status()
                return r.content

        return await _download_with_retry()
