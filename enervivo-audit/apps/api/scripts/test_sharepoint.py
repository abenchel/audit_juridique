"""Test de connexion SharePoint — résout un sharing link via Microsoft Graph.

Usage (depuis enervivo-audit/) :

    # Charge automatiquement .env (variables AZURE_AD_* + sharing link en argv)
    .venv/bin/python apps/api/scripts/test_sharepoint.py \
        "https://enervivo.sharepoint.com/:f:/g/IgA2DjzQs9hrRIxcSeMYKrwAAR33JG7RxyNyn3YmelTkZi4?e=UzeQAh"

Ou en passant les credentials directement (sans .env) :

    AZURE_AD_TENANT_ID=... AZURE_AD_CLIENT_ID=... AZURE_AD_CLIENT_SECRET=... \
        python apps/api/scripts/test_sharepoint.py "<sharing_url>"

Ce script :
  1) obtient un token app-only via MSAL (scope Graph .default)
  2) résout le sharing link en driveItem -> donne drive_id, site_id, path
  3) liste les enfants pour prouver que la lecture marche
  4) affiche les valeurs à coller dans .env (SHAREPOINT_SITE_ID / SHAREPOINT_DRIVE_ID)

Prérequis App Registration :
  - permissions APPLICATION : Sites.Read.All + Files.Read.All
  - admin consent accordé (bouton vert dans Azure portal)
"""

from __future__ import annotations

import base64
import os
import sys
from pathlib import Path

import httpx
from msal import ConfidentialClientApplication

GRAPH = "https://graph.microsoft.com/v1.0"


def load_dotenv_if_present() -> None:
    """Charge .env à la racine d'enervivo-audit/ si présent. Pas de dépendance externe."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        env = parent / ".env"
        if env.exists():
            for line in env.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                os.environ.setdefault(k, v)
            print(f"[i] .env chargé depuis {env}")
            return
    print("[!] Aucun .env trouvé — les variables doivent être exportées manuellement")


def encode_share_url(url: str) -> str:
    """Encode une URL de partage SharePoint en sharingToken Graph (préfixe u!, base64url no padding)."""
    b = base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")
    return f"u!{b}"


def get_token(tenant: str, client_id: str, secret: str) -> str:
    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=secret,
        authority=f"https://login.microsoftonline.com/{tenant}",
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if not result or "access_token" not in result:
        raise SystemExit(f"[X] MSAL : impossible d'obtenir le token : {result}")
    print("[OK] Token Graph app-only obtenu")
    return result["access_token"]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    share_url = sys.argv[1]

    load_dotenv_if_present()

    tenant = os.environ.get("AZURE_AD_TENANT_ID", "")
    client_id = os.environ.get("AZURE_AD_CLIENT_ID", "")
    secret = os.environ.get("AZURE_AD_CLIENT_SECRET", "")
    if not (tenant and client_id and secret):
        print("[X] AZURE_AD_TENANT_ID / AZURE_AD_CLIENT_ID / AZURE_AD_CLIENT_SECRET manquants")
        return 2

    token = get_token(tenant, client_id, secret)
    headers = {"Authorization": f"Bearer {token}"}

    sharing_token = encode_share_url(share_url)
    print(f"[i] Sharing token Graph : {sharing_token[:40]}...")

    with httpx.Client(base_url=GRAPH, headers=headers, timeout=30.0) as cli:
        # 1) Résolution du share → driveItem
        # On demande explicitement le driveItem ET parentReference + path via $expand=driveItem
        r = cli.get(f"/shares/{sharing_token}/driveItem")
        if r.status_code == 403:
            print(
                "[X] 403 Forbidden — l'App Registration n'a pas les permissions "
                "Sites.Read.All + Files.Read.All (Application) ou l'admin consent n'est pas accordé."
            )
            print(r.text)
            return 1
        if r.status_code != 200:
            print(f"[X] Échec /shares/.../driveItem : HTTP {r.status_code}")
            print(r.text)
            return 1
        item = r.json()

        item_id = item.get("id", "")
        name = item.get("name", "")
        is_folder = "folder" in item
        web_url = item.get("webUrl", "")
        parent = item.get("parentReference", {}) or {}
        drive_id = parent.get("driveId", "")
        site_id = parent.get("siteId", "")
        parent_path = parent.get("path", "")  # ex : "/drives/<drive_id>/root:/EnerVivo/Documents/09-Project"

        print()
        print("=" * 70)
        print("RÉSULTAT — Sharing link résolu")
        print("=" * 70)
        print(f"  name           : {name}")
        print(f"  is_folder      : {is_folder}")
        print(f"  item_id        : {item_id}")
        print(f"  drive_id       : {drive_id}")
        print(f"  site_id        : {site_id}")
        print(f"  parent.path    : {parent_path}")
        print(f"  webUrl         : {web_url}")

        # 2) Listing pour prouver la lecture
        if is_folder:
            r2 = cli.get(f"/drives/{drive_id}/items/{item_id}/children?$top=20")
            if r2.status_code != 200:
                print(f"[!] Listing enfants : HTTP {r2.status_code} {r2.text}")
            else:
                children = r2.json().get("value", [])
                print()
                print(f"[OK] Listing : {len(children)} entrée(s) directes (top 20)")
                for it in children[:20]:
                    kind = "DIR" if "folder" in it else "FILE"
                    size = it.get("size", 0)
                    print(f"   - [{kind}] {it.get('name'):<50} {size:>10} octets")

        # 3) Vérifie le path vs garde-fou attendu
        expected_root = os.environ.get("SHAREPOINT_ALLOWED_ROOT_PATH", "/EnerVivo/Documents/09-Project")
        # parent.path est de la forme "/drives/<id>/root:/EnerVivo/Documents/09-Project"
        # On extrait la partie après "root:"
        resolved_site_path = parent_path.split("root:", 1)[1] if "root:" in parent_path else parent_path
        full_path = f"{resolved_site_path}/{name}".replace("//", "/")
        print()
        print("=" * 70)
        print("GARDE-FOU — vérification ALLOWED_ROOT_PATH")
        print("=" * 70)
        print(f"  attendu (préfixe)  : {expected_root}")
        print(f"  chemin résolu      : {full_path}")
        if full_path.startswith(expected_root):
            print("  [OK] Le sharing link pointe bien dans la racine autorisée.")
        else:
            print("  [!] Le sharing link N'EST PAS sous la racine autorisée — à vérifier.")

        # 4) Récap .env
        print()
        print("=" * 70)
        print("À COLLER DANS .env (si différent de ce que tu as déjà)")
        print("=" * 70)
        print(f"SHAREPOINT_SITE_ID={site_id}")
        print(f"SHAREPOINT_DRIVE_ID={drive_id}")
        print(f"SHAREPOINT_FOLDER_PATH={resolved_site_path}/{name}")
        print(f"SHAREPOINT_ALLOWED_ROOT_PATH={expected_root}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
