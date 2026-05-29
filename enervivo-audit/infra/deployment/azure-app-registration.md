# Azure — App Registration EnerVivo Audit

L'application a **deux usages** distincts mais peut se contenter d'**une seule** App Registration :

1. **SSO utilisateur** (login web via NextAuth) — permission *delegated* `User.Read`
2. **SharePoint app-only** (worker Celery lit les dossiers projet) — permissions *application* `Sites.Read.All` + `Files.Read.All`

---

## 1. Créer l'App Registration

1. Portail Azure → **Microsoft Entra ID** → **App registrations** → **+ New registration**
2. Nom : `EnerVivo Audit`
3. **Supported account types** : **Single tenant** (EnerVivo uniquement)
4. **Redirect URI** : *Web* →
   ```
   http://localhost:11118/api/auth/callback/microsoft-entra-id
   ```
   (En prod, ajouter aussi `https://audit.enervivo.fr/api/auth/callback/microsoft-entra-id` plus tard.)
5. → **Register**

Une fois créée, noter :
- **Application (client) ID** → variable `AZURE_AD_CLIENT_ID`
- **Directory (tenant) ID** → variable `AZURE_AD_TENANT_ID`

---

## 2. Permissions API

**API permissions** → **+ Add a permission** → **Microsoft Graph** :

### Delegated permissions (auth utilisateur)
- `User.Read` — déjà ajouté par défaut, OK.
- *(optionnel)* `email`, `openid`, `profile`

### Application permissions (SharePoint app-only)
- `Sites.Read.All`
- `Files.Read.All`

→ **Grant admin consent for EnerVivo** (bouton bleu, requiert un admin du tenant).

---

## 3. Client secret

**Certificates & secrets** → **+ New client secret** :
- Description : `enervivo-audit-prod-2026`
- Expiration : **6 months** (rappel à mettre dans le calendrier — secret à renouveler 2× par an)

→ **Add**

Copier **immédiatement** la valeur (`Value`, pas `Secret ID`) — elle ne sera plus visible.
→ variable `AZURE_AD_CLIENT_SECRET` dans `.env`.

---

## 4. Test rapide

Une fois `.env` rempli :

```bash
make up
# Ouvrir http://localhost:11118
# Clique "Se connecter avec Outlook EnerVivo"
# → redirige sur login.microsoftonline.com → callback NextAuth
# → si email se termine par @enervivo.fr → /projects
# → sinon, redirige vers /login?error=domain
```

Côté worker (audit), au premier audit réel :
```bash
make logs s=worker
# Doit afficher : INFO [audit engine] starting...
# Si "MSAL token error" → vérifier permissions Graph + admin consent
```

---

## 5. Tester le SharePoint (mode real)

```bash
# Mettre SHAREPOINT_MODE=real dans .env, puis :
make restart
```

Si tu obtiens un `403 Forbidden` sur `/sites/...` :
- Admin consent pas validé ? Recommencer §2
- Vérifier que le **tenant ID** dans `issuer` correspond
- Tester l'auth seule : `curl` un token MSAL via `tools/msal_test.py` (à écrire si besoin)
