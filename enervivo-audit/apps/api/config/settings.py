"""Settings — pydantic-settings, toutes vars validées au démarrage."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- App ---
    environment: Literal["development", "production", "test"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    cors_origins: str = "http://localhost:3000"

    # --- Database ---
    postgres_user: str = "enervivo"
    postgres_password: SecretStr = SecretStr("changeme")
    postgres_db: str = "enervivo_audit"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    # --- Redis ---
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_password: SecretStr | None = None

    # --- MinIO ---
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "enervivo"
    minio_secret_key: SecretStr = SecretStr("changeme")
    minio_secure: bool = False
    minio_bucket: str = "pdf-cache"
    minio_retention_days: int = 30
    minio_quota_gb: int = 5

    # --- OpenRouter (LLM) ---
    openrouter_api_key: SecretStr = SecretStr("")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_default_model: str = "google/gemini-2.5-flash-lite"
    # Modèle dédié à la VISION (PDF scannés, images). Vide → utilise
    # openrouter_default_model (comportement actuel : Haiku partout). À remplir
    # le jour où l'on veut SPLITTER : ex. garder un modèle vision soigné ici et
    # mettre un modèle texte moins cher dans openrouter_default_model.
    openrouter_vision_model: str = ""
    llm_max_retries: int = 3
    llm_timeout_seconds: int = 60

    # Provider abstraction (permet de switcher vers Anthropic direct ensuite)
    llm_provider: Literal["openrouter", "anthropic"] = "openrouter"
    anthropic_api_key: SecretStr | None = None

    # --- Microsoft Entra ID / Graph (SharePoint app-only + auth user) ---
    azure_ad_tenant_id: str = ""
    azure_ad_client_id: str = ""
    azure_ad_client_secret: SecretStr = SecretStr("")
    sharepoint_site_id: str = ""
    sharepoint_drive_id: str = ""
    # Dossier racine des projets à auditer (path drive-relatif). Pour l'audit juridique : /09-Projets.
    sharepoint_folder_path: str = "/09-Projets"
    # Garde-fou : refuse tout chemin résolu hors de ces racines autorisées (CSV).
    # Ex: /09-Projets,/18-Comités internes
    sharepoint_allowed_root_paths: str = "/09-Projets"
    # Dossiers à skipper au listing (case-insensitive, match par nom exact).
    # Visuels = renders 3D / photomontages, hors-scope juridique.
    # Format CSV dans .env, parsé via @property sharepoint_excluded_folders_list.
    sharepoint_excluded_folders: str = "Visuels"

    # --- NextAuth (clé partagée pour vérifier le JWT côté API) ---
    nextauth_secret: SecretStr = SecretStr("changeme")
    nextauth_url: str = "http://localhost:3000"
    allowed_email_domain: str = "enervivo.fr"

    # --- Admins ---
    # Liste CSV d'emails qui ont le rôle admin (changelog, etc.). Source de
    # vérité du rôle : un email présent ici → admin, sinon user. Modifiable
    # dans .env sans toucher la DB. Parsé via @property admin_emails_set.
    admin_emails: str = ""

    # --- Audit thresholds ---
    confidence_threshold_present: int = 70
    confidence_threshold_ambiguous: int = 40

    @property
    def database_url(self) -> str:
        pw = self.postgres_password.get_secret_value()
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{pw}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def alembic_database_url(self) -> str:
        # Alembic env utilise la version sync pour les migrations
        pw = self.postgres_password.get_secret_value()
        return (
            f"postgresql+psycopg://{self.postgres_user}:{pw}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        auth = ""
        if self.redis_password:
            auth = f":{self.redis_password.get_secret_value()}@"
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/0"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def sharepoint_excluded_folders_set(self) -> set[str]:
        return {f.strip().lower() for f in self.sharepoint_excluded_folders.split(",") if f.strip()}

    @property
    def sharepoint_allowed_root_paths_set(self) -> set[str]:
        return {p.strip() for p in self.sharepoint_allowed_root_paths.split(",") if p.strip()}

    @property
    def admin_emails_set(self) -> set[str]:
        return {e.strip().lower() for e in self.admin_emails.split(",") if e.strip()}

    @field_validator("confidence_threshold_present", "confidence_threshold_ambiguous")
    @classmethod
    def _validate_thresholds(cls, v: int) -> int:
        if not 0 <= v <= 100:
            raise ValueError("Seuil de confiance doit être 0-100")
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
