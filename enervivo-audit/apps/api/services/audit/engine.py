"""Moteur d'audit — orchestre listing + classification + matching + rapport.

Flow (cahier des charges + prompt) :
  1. UPDATE audits SET status='running'
  2. SharePoint listing → list[FileMetadata]
  3. Pour chaque fichier en parallèle (max 10) :
     - Téléchargement (RAM)
     - Hash SHA-256
     - Check cache Postgres par hash → réutiliser classification existante
     - Sinon : cache MinIO put, extraction texte, appel LLM, INSERT classified_documents
     - Publier event SSE Redis "progress: X/N"
  4. Charger référentiel V11 → documents attendus pour les jalons demandés
  5. Matcher : tier confidence → present / ambiguous / missing
  6. Construire AuditReport (JSONB)
  7. UPDATE audits SET status='completed', result=..., totaux
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Audit, ClassifiedDocument
from db.repositories.audits import get_audit
from db.repositories.classifications import find_by_hash
from db.repositories.projects import get_project
from db.session import AsyncSessionLocal
from models.audit import (
    AuditReport,
    ErrorFile,
    IgnoredFile,
    JalonReport,
    UnclassifiedFile,
)
from models.document import FileMetadata
from services.audit.matcher import match_classified_to_expected
from services.audit.plan_masse import reassign_plans_de_masse
from services.audit.tadd import reassign_tadd
from services.audit.types import get_handler
from services.extraction import extract_text, is_image
from services.extraction.base import ExtractionError, ScanNoTextError
from services.extraction.pdf import render_pdf_pages_to_png
from services.extraction.registry import get_extractor
from services.llm.classifier import classify, classify_vision
from services.llm.type_snap import snap_type_to_referential
from services.sharepoint import get_sharepoint_client
from services.storage.cache import PDFCache

log = logging.getLogger(__name__)
# 5 parallèles : équilibre speed/stability. Les gros PDFs (PADD 200pages) coûtent 30-40s d'extraction.
# 5 parallèles = 5 PDFs en extraction simultanée, soit ~150-200s d'extraction pure + LLM calls.
# Réduire davantage (3) = plus lent mais moins de pics mémoire.
# Augmenter (10+) = pics OpenRouter/Bedrock (RemoteProtocolError).
CONCURRENCY = 5
# Skip les fichiers énormes (plans cadastraux, scans HD) — pdfplumber explose la RAM
# au-delà de ~80MB et le worker se fait SIGKILL. 80 MB couvre tous les docs juridiques.
MAX_FILE_SIZE_BYTES = 80 * 1024 * 1024


def _classify_ignored_reason(mime: str, name: str, path: str = "") -> str | None:
    """Renvoie une raison d'ignorer le fichier, ou None s'il doit être traité.

    Politique 2026-05-21 : on TENTE de classer tout ce qui peut contenir des
    infos juridiques (PDF, DOCX, PPTX, XLSX, **emails** .eml/.msg, **images**
    via vision LLM). On n'ignore QUE les types vraiment non-classifiables :
      - vidéos, audio (pas de signal exploitable)
      - archives (.zip, .rar) — il faudrait unzip d'abord
      - CAD (.dwg, .dxf) — format binaire CAO, pas de texte exploitable

    On préfère le mime (fiable côté Graph) mais on fallback sur l'extension
    pour les cas où Graph renvoie 'application/octet-stream'.
    """
    mime = (mime or "").lower()
    name = (name or "").lower()
    path_lc = (path or "").lower()
    ext = "." + name.rsplit(".", 1)[-1] if "." in name else ""

    if mime.startswith("video/") or ext in {".mp4", ".mov", ".avi", ".mkv", ".wmv"}:
        return "video"
    if ext in {".mp3", ".wav", ".m4a", ".aac"} or mime.startswith("audio/"):
        return "audio"
    if ext in {".zip", ".rar", ".7z", ".tar", ".gz"} or "compressed" in mime or "zip" in mime:
        return "archive"
    if ext in {".dwg", ".dxf", ".dgn", ".step", ".stp", ".iges",
               # SketchUp (modèles 3D + layouts) — pas de contenu juridique
               ".skp", ".skb", ".layout",
               # AutoCAD fichiers auxiliaires (verrou, backup, log)
               ".dwl", ".dwl2", ".bak",
               # Liz (autre format projet CAD propriétaire vu sur DIBOS)
               ".liz"}:
        return "cad"
    # Binaires SIG/QGIS — pas de contenu juridique exploitable
    if ext in {".qgz", ".qgs", ".shp", ".shx", ".dbf", ".prj", ".geojson",
               ".las", ".laz", ".asc", ".tab", ".kml", ".kmz",
               # QGIS metadata/sidecar (vu sur DMONFLANQUIN)
               ".cpg", ".qml", ".qpj", ".qmd", ".idx", ".gpkg"}:
        return "gis"
    # Outils techniques métier (PVsyst, MS Project, D5Render, ContextCapture…)
    if ext in {".pvc", ".pvp", ".mpp", ".mpx",
               # PVsyst data / meteo / inverter / project versions
               ".met", ".ond", ".pvsettings",
               # D5Render scene/mesh/save/HDR/EXR/cube LUT
               ".drs", ".d5mesh", ".save", ".hdr", ".exr", ".cube",
               # Modèles financiers Python métier (pas du code à auditer)
               ".py",
               # AVIF : stock images décoratives ; rarement utilisé pour des docs
               ".avif"}:
        return "technique_binary"
    # PVsyst versions de projet : .VC0 / .VC1 / ... / .VC9
    if len(ext) == 4 and ext.startswith(".vc") and ext[3].isdigit():
        return "technique_binary"
    # Nuages de points / sortie photogrammétrie / D5Render scenes.
    # `.bin` / `.json` étant trop génériques, on combine NOM + DOSSIER PARENT
    # pour éviter de zapper un `metadata.json` business légitime hors zone 3D.
    _3d_names = {"hierarchy.bin", "octree.bin", "metadata.json",
                 "syncmesh.json", "renderqueueinfo.json", "videoinfo.json"}
    _3d_folders = ("/3d/", "/3 - 3d", "/render", "/d5render", "/d5 render",
                   "/pointcloud", "/point cloud", "/nuage", "/photogrammetrie",
                   "/photogrammétrie", "/orthomosaic", "/insertion paysag")
    if name in _3d_names and any(f in path_lc for f in _3d_folders):
        return "point_cloud"
    # HTML : rarement un document juridique ; généralement export web ou page
    # d'erreur. Si besoin un jour, ajouter un HtmlExtractor (BeautifulSoup).
    if ext in {".html", ".htm"} or mime in {"text/html", "application/xhtml+xml"}:
        return "web"
    return None  # à traiter (PDF/DOCX/PPTX/XLSX/CSV/DOTX/EML/MSG/image)


async def _publish_progress(audit_id: uuid.UUID, payload: dict) -> None:
    """Pub-sub Redis channel `audit:{id}` pour SSE."""
    try:
        from redis.asyncio import Redis  # local import (évite charge si SSE off)

        from config.settings import get_settings

        s = get_settings()
        redis = Redis.from_url(s.redis_url, decode_responses=True)
        await redis.publish(f"audit:{audit_id}", json.dumps(payload, default=str))
        await redis.close()
    except Exception as e:  # pragma: no cover
        log.debug("SSE publish skip: %s", e)


async def _process_file(
    file: FileMetadata,
    audit_id: uuid.UUID,
    audit_type: str,
    reference: dict[str, Any],
    cache: PDFCache,
    session: AsyncSession,
) -> dict[str, Any]:
    """Traite un fichier : download → cache → extract → classify (ou cache hit)."""
    sp_client = get_sharepoint_client()
    result: dict[str, Any] = {
        "file": file,
        "classified_type": None,
        "confidence": None,
        "reason": None,
        "file_hash": None,
        "status_extraction": "ok",
        "error": None,
        "llm_model": None,
    }

    try:
        # Skip fichiers trop volumineux pour éviter SIGKILL OOM du worker
        if file.size and file.size > MAX_FILE_SIZE_BYTES:
            result["status_extraction"] = "error"
            result["error"] = f"fichier trop volumineux ({file.size // (1024 * 1024)} MB > {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB) — skip"
            log.warning("Skip %s : %s", file.path, result["error"])
            return result

        content = await sp_client.download_file(file)
        file_hash = hashlib.sha256(content).hexdigest()
        result["file_hash"] = file_hash

        # Cache cross-audit Postgres : si même hash déjà classifié, réutilise.
        # ⚠️ On re-passe le type caché par snap_type_to_referential : une entrée
        # classifiée sous un ANCIEN référentiel (ex. V12 "DICT - DICT résumé") doit
        # être ramenée vers le type EXACT du référentiel courant (V13 "DT / DICT -
        # resume"), sinon le matcher la voit comme orpheline. Le snap au moment de
        # classer (classify/classify_vision) ne s'applique PAS aux cache-hits — ce
        # garde-fou couvre tout décalage cache ↔ référentiel sans purge ni re-appel
        # LLM. No-op si le type est déjà valide.
        cached = await find_by_hash(session, file_hash)
        if cached:
            # Snap UNIQUEMENT si un type non-vide est caché : un cache à type
            # NULL/"" provient d'un fichier jadis ignoré — le snapper le
            # transformerait à tort en "Autre / Non identifié" (régression). On
            # le conserve tel quel.
            cached_type = cached.classified_type
            result["classified_type"] = (
                snap_type_to_referential(cached_type, reference)
                if cached_type
                else cached_type
            )
            result["confidence"] = cached.confidence
            # Marqueur « (cache) » = info d'AFFICHAGE, pas une donnée. On le
            # rend idempotent : un ré-audit relit une reason qui contient DÉJÀ
            # « (cache) » (car re-persistée telle quelle au passage précédent) →
            # sans nettoyage, le suffixe s'empile (« (cache) (cache) (cache) »).
            # On retire toute occurrence résiduelle puis on en remet exactement
            # une.
            base_reason = (cached.reason or "").replace(" (cache)", "").rstrip()
            result["reason"] = f"{base_reason} (cache)" if base_reason else "(cache)"
            result["llm_model"] = cached.llm_model
        else:
            # Cache MinIO pour éviter re-download SharePoint si re-classification
            await cache.put(file_hash, content, file.mime_type)

            # --- Branche IMAGE : .jpg / .png / .heic etc. → vision LLM direct ---
            # Couvre les cas CNI scannée, RIB photo, attestations en JPEG…
            if is_image(file.mime_type, file.name):
                try:
                    from services.extraction.image import normalize_image_for_vision
                    img_bytes, img_mime = normalize_image_for_vision(
                        content, file.mime_type or "image/jpeg"
                    )
                    classification, model = await classify_vision(
                        file.name,
                        [(img_bytes, img_mime)],
                        audit_type,
                        reference,
                        file_path=file.path,
                    )
                    result["classified_type"] = classification.type
                    result["confidence"] = classification.confidence
                    result["reason"] = classification.reason
                    result["llm_model"] = model
                    return result
                except Exception as ve:
                    result["status_extraction"] = "error"
                    result["error"] = f"image vision échec : {ve}"
                    return result
                finally:
                    content = None  # type: ignore[assignment]

            # --- Branche TEXTE : PDF / DOCX / PPTX / XLSX ---
            # Si aucun extracteur ne supporte le type, on émet une erreur claire
            # (engine.py listing-side ne devrait pas laisser passer ces cas, mais
            # ceinture + bretelles).
            if get_extractor(file.mime_type, file.name) is None:
                result["status_extraction"] = "error"
                result["error"] = f"Aucun extracteur pour {file.mime_type or file.name}"
                content = None  # type: ignore[assignment]
                return result

            # Extraction + LLM
            # ★ to_thread : pdfplumber est synchrone et CPU/IO bound. Sans to_thread
            # il bloque l'event loop → les 4 autres slots du sémaphore attendent
            # (CONCURRENCY=5 devient =1 pendant l'extraction). Avec to_thread, les
            # LLM calls des autres fichiers tournent en vraie parallèle.
            # Fallback vision+OCR PyMuPDF — utilisé quand l'extraction texte
            # échoue, que ce soit parce que le PDF est un scan sans couche texte
            # (ScanNoTextError) OU parce que pdfplumber a planté sur un PDF
            # abîmé/ré-encodé (ExtractionError, ex. "ATTESTATION_STANDARD.pdf (9)").
            # PyMuPDF est bien plus tolérant que pdfplumber : il rend souvent les
            # pages là où pdfplumber refuse de parser. Le fichier ne tombe en
            # `error` que si PyMuPDF échoue AUSSI. Renvoie un dict result rempli
            # en cas de succès, ou None pour laisser l'appelant marquer l'erreur.
            async def _try_pdf_vision_fallback() -> dict | None:
                try:
                    images = await asyncio.to_thread(render_pdf_pages_to_png, content)
                    if not images:
                        return None
                    # PyMuPDF rend à la résolution native du PDF — un scan 300 DPI
                    # peut dépasser 8000px et faire rejeter l'image par Bedrock/Claude
                    # (cas CNI DMONFLANQUIN). On normalise (cap 2048px, JPEG ≤4 MB).
                    from services.extraction.image import normalize_image_for_vision
                    normalized: list[tuple[bytes, str]] = []
                    for png in images:
                        try:
                            normalized.append(normalize_image_for_vision(png, "image/png"))
                        except Exception:
                            normalized.append((png, "image/png"))  # fail-open
                    # OCR de toutes les pages (≤15, scans >2 p. seulement) via
                    # Tesseract → joint au prompt vision pour couvrir le contenu
                    # des pages NON rendues en image. Fail-open : Tesseract absent
                    # ou plante → ocr_text = "" → vision seule.
                    from services.extraction.ocr import ocr_pdf_pages
                    try:
                        ocr_text = await asyncio.to_thread(ocr_pdf_pages, content)
                    except Exception:  # noqa: BLE001
                        ocr_text = ""  # fail-open
                    classification, model = await classify_vision(
                        file.name,
                        normalized,
                        audit_type,
                        reference,
                        file_path=file.path,
                        ocr_text=ocr_text,
                    )
                    result["classified_type"] = classification.type
                    result["confidence"] = classification.confidence
                    result["reason"] = classification.reason
                    result["llm_model"] = model
                    return result
                except Exception:  # noqa: BLE001
                    return None

            try:
                sample = await asyncio.to_thread(
                    extract_text, content, file.mime_type, file.name
                )
            except (ScanNoTextError, ExtractionError) as e:
                # `content` est libéré par l'outer finally après ce retour.
                is_pdf = (file.mime_type or "").lower() == "application/pdf" or (
                    file.name or ""
                ).lower().endswith(".pdf")
                scan_no_text = isinstance(e, ScanNoTextError)
                if not is_pdf:
                    # Non-PDF : pas de rendu PyMuPDF possible → error directe.
                    result["status_extraction"] = "error"
                    result["error"] = (
                        "Fichier sans texte (non-PDF, vision non disponible)"
                        if scan_no_text
                        else str(e)
                    )
                    return result
                # PDF : on tente le fallback vision+OCR dans TOUS les cas (scan
                # OU plantage pdfplumber).
                fallback = await _try_pdf_vision_fallback()
                if fallback is not None:
                    return fallback
                # Le fallback a échoué aussi → error, en gardant la cause d'origine.
                result["status_extraction"] = "error"
                result["error"] = (
                    "scan sans texte + échec vision"
                    if scan_no_text
                    else f"{e} + échec fallback vision"
                )
                return result
            finally:
                # Libère les bytes du PDF dès que possible (uploadé MinIO + sample extrait)
                content = None  # type: ignore[assignment]

            classification, model = await classify(
                file.name, sample, audit_type, reference, file_path=file.path
            )
            result["classified_type"] = classification.type
            result["confidence"] = classification.confidence
            result["reason"] = classification.reason
            result["llm_model"] = model

    except Exception as e:
        log.exception("Échec traitement %s : %s", file.path, e)
        result["status_extraction"] = "error"
        result["error"] = str(e)

    return result


async def _rebuild_partial_report(
    audit_id: uuid.UUID,
    project: Any,
    audit: Any,
    reference: dict[str, Any],
    handler: Any,
    total_files_listed: int,
    ignored_files: list[IgnoredFile] | None = None,
) -> None:
    """Reconstruit `audit.result` à partir des classifications déjà en DB.

    Tourne en parallèle de l'audit (toutes les 30s). Le status reste 'running' —
    on met juste à jour le JSONB. Permet à l'UI d'afficher un rapport partiel
    sans attendre la fin. Tolère toutes les erreurs (best-effort).
    """
    from sqlalchemy import select, update

    try:
        async with AsyncSessionLocal() as session:
            r = await session.execute(
                select(ClassifiedDocument).where(ClassifiedDocument.audit_id == audit_id)
            )
            rows = r.scalars().all()
            if not rows:
                return

            classified = [
                {
                    "file": FileMetadata(
                        name=d.file_name,
                        path=d.sharepoint_path,
                        url=d.sharepoint_url,
                        size=d.file_size,
                        mime_type=d.mime_type,
                        drive_item_id=None,
                    ),
                    "classified_type": d.classified_type,
                    "confidence": d.confidence,
                    "reason": d.reason,
                    "file_hash": d.file_hash,
                    "status_extraction": "error" if d.status == "error" else "ok",
                    "error": d.reason if d.status == "error" else None,
                    "llm_model": d.llm_model,
                }
                for d in rows
            ]

            jalons = audit.jalons or [j["jalon"] for j in reference["jalons"]]
            expected = handler.expected_for_jalons(reference, jalons)
            matched_docs, _ = match_classified_to_expected(
                classified, expected, project_type=project.type
            )

            docs_by_jalon: dict[str, list] = defaultdict(list)
            expected_by_code: dict[str, str] = {e["code"]: e["_jalon"] for e in expected}
            for d in matched_docs:
                docs_by_jalon[expected_by_code.get(d.code, "Autre")].append(d)

            jalon_reports: list[JalonReport] = []
            tot_exp = tot_pres = tot_amb = tot_miss = 0
            for j in jalons:
                docs = docs_by_jalon.get(j, [])
                pres = sum(1 for d in docs if d.status == "present")
                amb = sum(1 for d in docs if d.status == "ambiguous")
                miss = sum(1 for d in docs if d.status == "missing")
                exp_count = sum(1 for d in docs if d.status != "not_applicable")
                comp = round(100 * (pres + 0.5 * amb) / exp_count) if exp_count else 0
                jalon_reports.append(
                    JalonReport(
                        jalon=j,
                        total_expected=exp_count,
                        total_present=pres,
                        total_ambiguous=amb,
                        total_missing=miss,
                        completion_pct=comp,
                        documents=docs,
                    )
                )
                tot_exp += exp_count
                tot_pres += pres
                tot_amb += amb
                tot_miss += miss

            overall_pct = round(100 * (tot_pres + 0.5 * tot_amb) / tot_exp) if tot_exp else 0

            unclassified_list: list[UnclassifiedFile] = []
            errors_list: list[ErrorFile] = []
            for c in classified:
                f = c["file"]
                if c["status_extraction"] == "error":
                    errors_list.append(
                        ErrorFile(
                            file_name=f.name,
                            sharepoint_url=f.url,
                            sharepoint_path=f.path,
                            error=c["error"] or "Erreur inconnue",
                        )
                    )
                elif not any(
                    c["file"].path == ff.sharepoint_path
                    for d in matched_docs
                    for ff in d.found_files
                ):
                    unclassified_list.append(
                        UnclassifiedFile(
                            file_name=f.name,
                            sharepoint_url=f.url,
                            sharepoint_path=f.path,
                            classified_type=c["classified_type"],
                            confidence=c["confidence"],
                            reason=c["reason"],
                        )
                    )

            top_missing = [
                d.name
                for jr in jalon_reports
                for d in jr.documents
                if d.status == "missing" and d.propriete == "Obligatoire"
            ][:3]
            model_used = next((c["llm_model"] for c in classified if c["llm_model"]), None)

            partial = AuditReport(
                audit_id=str(audit_id),
                project_code=project.code,
                project_name=project.name,
                project_type=project.type,
                audit_type=audit.audit_type,
                jalons_audited=jalons,
                started_at=audit.started_at,
                completed_at=datetime.utcnow(),  # juste pour la sérialisation
                model_used=model_used,
                total_files_scanned=len(classified),
                total_expected=tot_exp,
                total_present=tot_pres,
                total_ambiguous=tot_amb,
                total_missing=tot_miss,
                overall_completion_pct=overall_pct,
                top_critical_missing=top_missing,
                jalons=jalon_reports,
                unclassified=unclassified_list,
                errors=errors_list,
                ignored=ignored_files or [],
            )

            await session.execute(
                update(Audit)
                .where(Audit.id == audit_id)
                .values(result=json.loads(partial.model_dump_json()))
            )
            await session.commit()
            log.info("Partial report : %d/%d fichiers", len(classified), total_files_listed)
    except Exception as e:
        log.warning("Partial report KO : %s", e)


async def run_audit(audit_id: uuid.UUID) -> None:
    """Point d'entrée appelé par la tâche Celery."""
    async with AsyncSessionLocal() as session:
        audit = await get_audit(session, audit_id)
        if not audit:
            log.error("Audit %s introuvable", audit_id)
            return
        project = await get_project(session, audit.project_code)
        if not project:
            audit.status = "failed"
            audit.error_message = "Projet introuvable"
            await session.commit()
            return

        # Status → running
        audit.status = "running"
        await session.commit()
        await _publish_progress(audit_id, {"event": "started", "audit_id": str(audit_id)})

        try:
            handler = get_handler(audit.audit_type)
            reference = handler.load_reference()
            sp_client = get_sharepoint_client()
            cache = PDFCache()

            # 1) Listing — sépare immédiatement les fichiers classifiables des
            # types non supportés (vidéos, images, pptx, xlsx, etc.) pour
            # économiser bande passante + RAM + coût LLM.
            files: list[FileMetadata] = []
            ignored_files: list[IgnoredFile] = []
            async for f in sp_client.list_files(project.sharepoint_url):
                reason = _classify_ignored_reason(f.mime_type, f.name, f.path)
                if reason is None:
                    files.append(f)
                else:
                    ignored_files.append(
                        IgnoredFile(
                            file_name=f.name,
                            sharepoint_url=f.url,
                            sharepoint_path=f.path,
                            mime_type=f.mime_type,
                            size=f.size or 0,
                            reason=reason,
                        )
                    )
            log.info(
                "Listing : %d fichiers à classifier, %d ignorés (vidéos/images/etc.)",
                len(files),
                len(ignored_files),
            )
            await _publish_progress(
                audit_id,
                {
                    "event": "listed",
                    "total": len(files),
                    "ignored": len(ignored_files),
                },
            )
            # Persiste le total dans Redis (TTL 24h) → utilisé par GET /audits/{id}
            # pour reconstituer la progression après un refresh de la page.
            try:
                from redis.asyncio import Redis

                from config.settings import get_settings

                _s = get_settings()
                _r = Redis.from_url(_s.redis_url, decode_responses=True)
                await _r.set(f"audit:{audit_id}:total", str(len(files)), ex=86400)
                await _r.close()
            except Exception as _e:
                log.debug("Redis total snapshot skip: %s", _e)

            # 2) Process en parallèle (sémaphore)
            sem = asyncio.Semaphore(CONCURRENCY)
            counter = {"done": 0}

            async def _is_cancelled() -> bool:
                """Lit le flag Redis posé par POST /audits/{id}/cancel."""
                try:
                    from redis.asyncio import Redis

                    from config.settings import get_settings

                    r = Redis.from_url(get_settings().redis_url, decode_responses=True)
                    val = await r.get(f"audit:{audit_id}:cancel")
                    await r.close()
                    return val == "1"
                except Exception:
                    return False

            async def _wrapped(f: FileMetadata) -> dict[str, Any]:
                async with sem:
                    # Vérifie l'annulation avant d'engager du temps/coût LLM
                    if await _is_cancelled():
                        raise asyncio.CancelledError("audit annulé par l'utilisateur")
                    res = await _process_file(f, audit_id, audit.audit_type, reference, cache, session)
                    counter["done"] += 1
                    # ★ Stream-write : on persiste la classification IMMÉDIATEMENT
                    # dans une session indépendante. Si le worker meurt après, on
                    # garde le travail déjà fait. Plus de "tout perdu sur crash".
                    try:
                        async with AsyncSessionLocal() as sub_session:
                            doc = ClassifiedDocument(
                                audit_id=audit_id,
                                sharepoint_url=f.url,
                                sharepoint_path=f.path,
                                file_name=f.name,
                                file_size=f.size,
                                file_hash=res["file_hash"] or "",
                                mime_type=f.mime_type,
                                classified_type=res["classified_type"],
                                confidence=res["confidence"],
                                reason=res["reason"],
                                status="error" if res["status_extraction"] == "error" else "present",
                                llm_model=res["llm_model"],
                            )
                            sub_session.add(doc)
                            await sub_session.commit()
                    except Exception as e:
                        log.warning("Stream-persist KO pour %s : %s", f.name, e)

                    await _publish_progress(
                        audit_id,
                        {"event": "progress", "done": counter["done"], "total": len(files), "file": f.name},
                    )
                    # Snapshot Redis pour refresh-friendly UI (GET /audits/{id} lit cette clé)
                    try:
                        from redis.asyncio import Redis

                        from config.settings import get_settings

                        _r = Redis.from_url(get_settings().redis_url, decode_responses=True)
                        await _r.set(f"audit:{audit_id}:done", str(counter["done"]), ex=86400)
                        await _r.set(f"audit:{audit_id}:current_file", f.name, ex=86400)
                        await _r.close()
                    except Exception:
                        pass
                    return res

            # ★ Tâche périodique : rebuild un rapport PARTIEL toutes les 30s à
            # partir des classifications déjà persistées en DB. Permet à l'UI
            # de montrer un rapport en cours sans attendre la fin de l'audit.
            async def _periodic_partial() -> None:
                while True:
                    await asyncio.sleep(30)
                    await _rebuild_partial_report(
                        audit_id, project, audit, reference, handler, len(files),
                        ignored_files=ignored_files,
                    )

            partial_task = asyncio.create_task(_periodic_partial())
            cancelled = False
            try:
                classified = await asyncio.gather(*[_wrapped(f) for f in files])
            except asyncio.CancelledError:
                # _wrapped a vu le flag Redis et a raise CancelledError.
                # On sort proprement — le status='failed' a déjà été posé en DB
                # par l'endpoint POST /audits/{id}/cancel.
                cancelled = True
                classified = []
                log.info("Audit %s annulé par l'utilisateur", audit_id)
            finally:
                partial_task.cancel()
                try:
                    await partial_task
                except (asyncio.CancelledError, Exception):
                    pass

            if cancelled:
                # On rebuild une dernière fois le rapport partiel avec ce qui a
                # été fait avant l'annulation, puis on sort. Le status reste 'failed'.
                await _rebuild_partial_report(
                    audit_id, project, audit, reference, handler, len(files)
                )
                await _publish_progress(
                    audit_id,
                    {"event": "failed", "audit_id": str(audit_id), "error": "annulé par l'utilisateur"},
                )
                return

            # ⚠️ Les classified_documents sont DÉJÀ persistés au fil de l'eau
            # par _wrapped (stream-write). Plus de bulk insert ici — éviterait
            # des doublons.

            # 3.bis) PASSE 2 — désambiguïsation des plans de masse par jalon.
            # En passe 1 le LLM voit chaque fichier isolément et ne peut pas
            # deviner si un plan de masse est la version J1/J2a/J2b/J3/J4 (le
            # jalon n'est jamais dans le nom). On rassemble ici TOUS les plans
            # de masse et on fait UN seul appel LLM avec le contexte global
            # (noms + dates + dossiers) pour les répartir. Fail-open : toute
            # erreur conserve la classification passe 1, jamais de régression.
            try:
                reassigned = await reassign_plans_de_masse(classified, audit_id)
                if reassigned:
                    await _publish_progress(
                        audit_id,
                        {"event": "plan_masse_pass", "reassigned": reassigned},
                    )
            except Exception as _e:
                log.warning("Passe 2 plans de masse ignorée : %s", _e)

            # 3.ter) PASSE 2 — désambiguïsation des TADD par jalon.
            # Même principe que les plans de masse, mais la logique TADD diffère :
            # le jalon est souvent EXPLICITE dans le nom (`_J1_`, `_J2B_`…). On
            # rassemble tous les TADD, on retient l'unique version officielle par
            # jalon (départage version interne puis date), on écarte les versions
            # antérieures (→ "Autre"), et on laisse intacts les TADD sans jalon
            # dans le nom. Fail-open : toute erreur conserve la passe 1.
            try:
                tadd_changed = await reassign_tadd(classified, audit_id)
                if tadd_changed:
                    await _publish_progress(
                        audit_id,
                        {"event": "tadd_pass", "changed": tadd_changed},
                    )
            except Exception as _e:
                log.warning("Passe 2 TADD ignorée : %s", _e)

            # 4) Matching
            jalons = audit.jalons or [j["jalon"] for j in reference["jalons"]]
            expected = handler.expected_for_jalons(reference, jalons)
            matched_docs, orphans = match_classified_to_expected(
                classified, expected, project_type=project.type
            )

            # 5) Build rapport par jalon
            docs_by_jalon: dict[str, list] = defaultdict(list)
            expected_by_code: dict[str, str] = {e["code"]: e["_jalon"] for e in expected}
            for d in matched_docs:
                docs_by_jalon[expected_by_code.get(d.code, "Autre")].append(d)

            jalon_reports: list[JalonReport] = []
            tot_exp = tot_pres = tot_amb = tot_miss = 0
            for j in jalons:
                docs = docs_by_jalon.get(j, [])
                pres = sum(1 for d in docs if d.status == "present")
                amb = sum(1 for d in docs if d.status == "ambiguous")
                miss = sum(1 for d in docs if d.status == "missing")
                exp_count = sum(1 for d in docs if d.status != "not_applicable")
                comp = round(100 * (pres + 0.5 * amb) / exp_count) if exp_count else 100
                jalon_reports.append(
                    JalonReport(
                        jalon=j,
                        total_expected=exp_count,
                        total_present=pres,
                        total_ambiguous=amb,
                        total_missing=miss,
                        completion_pct=comp,
                        documents=docs,
                    )
                )
                tot_exp += exp_count
                tot_pres += pres
                tot_amb += amb
                tot_miss += miss

            overall_pct = round(100 * (tot_pres + 0.5 * tot_amb) / tot_exp) if tot_exp else 100

            unclassified_list: list[UnclassifiedFile] = []
            errors_list: list[ErrorFile] = []
            for c in classified:
                f = c["file"]
                if c["status_extraction"] == "error":
                    errors_list.append(
                        ErrorFile(
                            file_name=f.name,
                            sharepoint_url=f.url,
                            sharepoint_path=f.path,
                            error=c["error"] or "Erreur inconnue",
                        )
                    )
                # Non rattaché ?
                elif not any(c["file"].path == ff.sharepoint_path for d in matched_docs for ff in d.found_files):
                    unclassified_list.append(
                        UnclassifiedFile(
                            file_name=f.name,
                            sharepoint_url=f.url,
                            sharepoint_path=f.path,
                            classified_type=c["classified_type"],
                            confidence=c["confidence"],
                            reason=c["reason"],
                        )
                    )

            # Top critical missing : Obligatoires manquants
            top_missing = [
                d.name for jr in jalon_reports for d in jr.documents
                if d.status == "missing" and d.propriete == "Obligatoire"
            ][:3]

            model_used = next((c["llm_model"] for c in classified if c["llm_model"]), None)

            report = AuditReport(
                audit_id=str(audit_id),
                project_code=project.code,
                project_name=project.name,
                project_type=project.type,
                audit_type=audit.audit_type,
                jalons_audited=jalons,
                started_at=audit.started_at,
                completed_at=datetime.utcnow(),
                model_used=model_used,
                total_files_scanned=len(files),
                total_expected=tot_exp,
                total_present=tot_pres,
                total_ambiguous=tot_amb,
                total_missing=tot_miss,
                overall_completion_pct=overall_pct,
                top_critical_missing=top_missing,
                jalons=jalon_reports,
                unclassified=unclassified_list,
                errors=errors_list,
                ignored=ignored_files,
            )

            audit.result = json.loads(report.model_dump_json())
            audit.status = "completed"
            audit.completed_at = datetime.utcnow()
            audit.total_expected = tot_exp
            audit.total_found = tot_pres
            audit.total_ambiguous = tot_amb
            audit.total_missing = tot_miss
            await session.commit()

            await _publish_progress(audit_id, {"event": "completed", "audit_id": str(audit_id)})

        except Exception as e:
            log.exception("Audit %s failed", audit_id)
            audit.status = "failed"
            audit.error_message = str(e)[:500]
            audit.completed_at = datetime.utcnow()
            await session.commit()
            await _publish_progress(audit_id, {"event": "failed", "error": str(e)[:200]})
