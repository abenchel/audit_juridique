"""Interface SharePointClient — abstrait mock vs real."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from models.document import FileMetadata


class SharePointClient(ABC):
    @abstractmethod
    async def list_files(self, project_sharepoint_url: str) -> AsyncIterator[FileMetadata]:
        """Liste récursivement les fichiers d'un dossier projet."""
        raise NotImplementedError

    @abstractmethod
    async def download_file(self, file: FileMetadata) -> bytes:
        """Télécharge le contenu (en RAM uniquement, jamais sur disque)."""
        raise NotImplementedError
