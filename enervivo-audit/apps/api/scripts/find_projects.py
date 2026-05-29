"""Cherche récursivement des dossiers par nom sous /09-Projets et affiche leur chemin complet.

Usage (depuis enervivo-audit/) :

    .venv/bin/python apps/api/scripts/find_projects.py DMUZZOLINI DDESCUNS

Sortie : pour chaque nom recherché, affiche le path complet + item_id + webUrl,
prêts à coller dans projects_seed.json.
"""

from __future__ import annotations

import os
import sys
from collections import deque
from pathlib import Path

import httpx
from msal import ConfidentialClientApplication

GRAPH = "https://graph.microsoft.com/v1.0"


def load_dotenv_if_present() -> None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        env = parent / ".env"
        if env.exists():
            for line in env.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


def get_token() -> str:
    app = ConfidentialClientApplication(
        client_id=os.environ["AZURE_AD_CLIENT_ID"],
        client_credential=os.environ["AZURE_AD_CLIENT_SECRET"],
        authority=f"https://login.microsoftonline.com/{os.environ['AZURE_AD_TENANT_ID']}",
    )
    r = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if not r or "access_token" not in r:
        raise SystemExit(f"[X] MSAL : {r}")
    return r["access_token"]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    needles = {n.lower() for n in sys.argv[1:]}

    load_dotenv_if_present()
    drive_id = os.environ.get("SHAREPOINT_DRIVE_ID")
    root_path = os.environ.get("SHAREPOINT_FOLDER_PATH", "/09-Projets")
    if not drive_id:
        raise SystemExit("[X] SHAREPOINT_DRIVE_ID manquant dans .env")

    headers = {"Authorization": f"Bearer {get_token()}"}
    found: dict[str, dict] = {}
    visited = 0

    with httpx.Client(base_url=GRAPH, headers=headers, timeout=60.0) as cli:
        # Résout l'id du dossier racine /09-Projets
        r = cli.get(f"/drives/{drive_id}/root:{root_path}")
        r.raise_for_status()
        root_id = r.json()["id"]
        print(f"[i] Racine résolue : {root_path} -> item_id {root_id}")
        print(f"[i] Recherche de : {', '.join(sorted(needles))}")
        print()

        # BFS dans l'arbre — on s'arrête quand tous les noms sont trouvés
        queue: deque[tuple[str, str]] = deque([(root_id, root_path)])
        while queue and len(found) < len(needles):
            item_id, prefix = queue.popleft()
            url: str | None = f"/drives/{drive_id}/items/{item_id}/children?$top=200&$select=id,name,folder,webUrl"
            while url:
                r = cli.get(url)
                if r.status_code != 200:
                    print(f"[!] {r.status_code} sur {url} : {r.text[:200]}")
                    break
                data = r.json()
                for it in data.get("value", []):
                    visited += 1
                    if "folder" not in it:
                        continue
                    name = it["name"]
                    child_path = f"{prefix}/{name}"
                    if name.lower() in needles and name.lower() not in found:
                        found[name.lower()] = {
                            "name": name,
                            "path": child_path,
                            "item_id": it["id"],
                            "webUrl": it.get("webUrl", ""),
                        }
                        print(f"[OK] TROUVÉ : {name}")
                        print(f"       path    : {child_path}")
                        print(f"       item_id : {it['id']}")
                        print(f"       webUrl  : {it.get('webUrl', '')}")
                        print()
                    queue.append((it["id"], child_path))
                url = data.get("@odata.nextLink", "").replace(GRAPH, "") or None

    print(f"[i] {visited} entrées visitées au total")
    missing = needles - set(found)
    if missing:
        print(f"[!] Introuvables sous {root_path} : {sorted(missing)}")
        return 1
    print("[OK] Tous les projets trouvés.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
