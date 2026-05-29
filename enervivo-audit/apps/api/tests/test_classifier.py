"""Tests LLM classifier — mock OpenRouter via respx."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from services.llm.classifier import classify
from services.llm.openrouter import _parse_json_lenient

V11_REF = {
    "version": "V11",
    "jalons": [
        {
            "jalon": "J1",
            "documents": [
                {"name": "PDB signee", "code": "pdb_signee"},
                {"name": "LOI signee", "code": "loi_signee"},
            ],
        }
    ],
}


def test_parse_lenient_with_fence() -> None:
    assert _parse_json_lenient('```json\n{"type":"X","confidence":80,"reason":"ok"}\n```') == {
        "type": "X",
        "confidence": 80,
        "reason": "ok",
    }


def test_parse_lenient_plain() -> None:
    assert _parse_json_lenient('{"type":"X","confidence":80,"reason":"ok"}') == {
        "type": "X",
        "confidence": 80,
        "reason": "ok",
    }


@pytest.mark.asyncio
async def test_classify_mocked_openrouter(respx_mock: respx.MockRouter) -> None:
    respx_mock.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "type": "PDB signee",
                                    "confidence": 92,
                                    "reason": "Promesse de bail signée",
                                }
                            )
                        }
                    }
                ]
            },
        )
    )
    res, model = await classify(
        file_name="PDB_signee_v2_def.pdf",
        text_sample="PROMESSE DE BAIL EMPHYTEOTIQUE signée…",
        audit_type="juridique",
        documents_v11=V11_REF,
    )
    assert res.type == "PDB signee"
    assert res.confidence == 92
    assert "anthropic" in model or "claude" in model


@pytest.mark.asyncio
async def test_classify_clamps_confidence(respx_mock: respx.MockRouter) -> None:
    respx_mock.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": json.dumps({"type": "X", "confidence": 200, "reason": ""})}}
                ]
            },
        )
    )
    res, _ = await classify("f.pdf", "text", "juridique", V11_REF)
    assert res.confidence == 100
