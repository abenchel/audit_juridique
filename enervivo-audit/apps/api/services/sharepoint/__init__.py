"""Service SharePoint — client Microsoft Graph (real)."""

from __future__ import annotations

from .base import SharePointClient
from .real import RealSharePointClient


def get_sharepoint_client() -> SharePointClient:
    return RealSharePointClient()


__all__ = ["SharePointClient", "get_sharepoint_client"]
