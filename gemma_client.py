"""Gemma client and safety-preserving fallback logic for CrisisLens.

The primary integration target is Ollama's local API, which supports Gemma-family
models and multimodal payloads. If a local model is unavailable, the app can still
run in deterministic demo mode so the Kaggle video/demo does not fail.
"""

from __future__ import annotations

import base64
import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests

from prompts import SYSTEM_PROMPT, build_user_prompt


DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "gemma4:e2b"


@dataclass
class ModelCallResult:
    report: Dict[str, Any]
    raw_response: str
    backend: str
    latency_seconds: float
    used_fallback: bool


class GemmaClientError(RuntimeError):
    """Raised when the Gemma backend fails and fallback is disabled."""


def _image_to_base64(image_bytes: Optional[bytes]) -> Optional[str]:
    if not image_bytes:
        return None
    return base64.b64encode(image_bytes).decode("utf-8")


def _extract_json(text: str) -> Dict[str, Any]:
    """Robustly parse JSON even if the model accidentally wraps it in prose."""
    text = text.strip()
    if not text:
        raise ValueError("Empty model response")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model response")
    return json.loads(match.group(0))


def _normalize_report(report: Dict[str, Any], language: str) -> Dict[str, Any]:
    """Ensure all expected keys exist and values are display-safe."""
    defaults = {
        "incident_type": "other",
        "urgency": "medium",
        "summary": "Potential crisis-related field report requiring human verification.",
        "affected_people_estimate": "unknown",
        "location_clues": [],
        "detected_risks": [],
        "evidence": [],
        "uncertainties": [],
        "missing_information": [],
        "recommended_actions": [],
        "priority_reasoning": "Insufficient evidence; human verification required.",
        "field_message": "FIELD REPORT: Situation requires verification and coordinator review.",
        "structured_report": "Situation report pending verification.",
        "safety_notes": [
            "Verify conditions on the ground before taking action.",
            "Do not treat this output as an official emergency instruction.",
        ],
        "language": language,
    }
    normalized = {**defaults, **(report or {})}
    for key in [
        "location_clues",
        "detected_risks",
        "evidence",
        "uncertainties",
        "missing_information",
        "recommended_actions",
        "safety_notes",
    ]:
        value = normalized.get(key)
        if isinstance(value, str):
            normalized[key] = [value]
        elif value is None:
            normalized[key] = []
        elif not isinstance(value, list):
            normalized[key] = [str(value)]
    normalized["urgency"] = str(normalized.get("urgency", "medium")).lower()
    if normalized["urgency"] not in {"low", "medium", "high", "critical"}:
        normalized["urgency"] = "medium"
    return normalized


def call_ollama_gemma(
    *,
    image_bytes: Optional[bytes],
    field_note: str,
    language: str,
    model: str = DEFAULT_MODEL,
    host: str = DEFAULT_OLLAMA_HOST,
    timeout: int = 120,
) -> ModelCallResult:
    """Call a local Gemma model through Ollama's /api/generate endpoint."""
    started = time.time()
    prompt = f"{SYSTEM_PROMPT}\n\n{build_user_prompt(field_note, language)}"
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
            "num_ctx": 8192,
        },
    }
    image_b64 = _image_to_base64(image_bytes)
    if image_b64:
        payload["images"] = [image_b64]

    url = f"{host.rstrip('/')}/api/generate"
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    raw = data.get("response", "")
    parsed = _extract_json(raw)
    report = _normalize_report(parsed, language)
    return ModelCallResult(
        report=report,
        raw_response=raw,
        backend=f"Ollama / {model}",
        latency_seconds=time.time() - started,
        used_fallback=False,
    )


def route_incident(report: Dict[str, Any]) -> Dict[str, Any]:
    """A deterministic function-calling style routing tool.

    In the video/writeup, this demonstrates how Gemma's structured output can be
    converted into operational actions without letting the model execute anything.
    """
    incident = str(report.get("incident_type", "other")).lower()
    urgency = str(report.get("urgency", "medium")).lower()

    agency_by_type = {
        "flooding": "Emergency coordination + water/sanitation team",
        "infrastructure_damage": "Public works + search/access team",
        "shelter_need": "Shelter coordinator + logistics team",
        "medical_supply_gap": "Medical logistics + licensed health professional",
        "food_water_shortage": "Relief logistics + water/sanitation team",
        "fire_smoke": "Fire service / evacuation coordinator",
        "landslide": "Search/access team + geotechnical/public works review",
        "other": "Human dispatcher review",
    }
    channel_by_urgency = {
        "low": "Queue for routine verification",
        "medium": "Send to local coordinator within the next operational cycle",
        "high": "Notify duty coordinator and request field verification immediately",
        "critical": "Escalate to emergency channel and request immediate human confirmation",
    }
    sla_by_urgency = {
        "low": "24 hours",
        "medium": "8 hours",
        "high": "1 hour",
        "critical": "15 minutes",
    }

    return {
        "recommended_team": agency_by_type.get(incident, agency_by_type["other"]),
        "routing_channel": channel_by_urgency.get(urgency, channel_by_urgency["medium"]),
        "target_review_time": sla_by_urgency.get(urgency, "8 hours"),
        "human_gate_required": True,
        "tool_reason": "Routing is deterministic and auditable; Gemma proposes the report, a rule-based tool routes it.",
    }


def _language_pack(language: str) -> Dict[str, str]:
    lang = language.lower()
    if "de" in lang or "german" in lang or "deutsch" in lang:
        return {
            "summary_prefix": "MÃ¶glicher Krisenbericht",
            "verify": "Vor Ort verifizieren, bevor MaÃŸnahmen ausgelÃ¶st werden.",
            "no_diag": "Keine medizinische Diagnose; medizinische Angaben mÃ¼ssen fachlich geprÃ¼ft werden.",
            "sms": "DRINGENDER FELDBERICHT",
        }
    if "es" in lang or "span" in lang or "spanisch" in lang:
        return {
            "summary_prefix": "Posible informe de crisis",
            "verify": "Verificar en terreno antes de actuar.",
            "no_diag": "No es un diagnÃ³stico mÃ©dico; verificar con personal cualificado.",
            "sms": "INFORME URGENTE DE CAMPO",
        }
    if "fr" in lang or "french" in lang or "franz" in lang:
        return {
            "summary_prefix": "Rapport de crise potentiel",
            "verify": "VÃ©rifier sur le terrain avant d'agir.",
            "no_diag": "Pas de diagnostic mÃ©dical; faire vÃ©rifier par du personnel qualifiÃ©.",
            "sms": "RAPPORT TERRAIN URGENT",
        }
    return {
        "summary_prefix": "Potential crisis report",
        "verify": "Verify on the ground before action is taken.",
        "no_diag": "No medical diagnosis; health-related details require qualified review.",
        "sms": "URGENT FIELD REPORT",
    }


def demo_analysis(field_note: str, language: str, has_image: bool) -> Dict[str, Any]:
    """Deterministic fallback for demos when Gemma is not running locally."""
    note = field_note.lower()
    lang = _language_pack(language)

    incident_type = "other"
    detected_risks: List[str] = []
    recommended: List[str] = []

    if any(word in note for word in ["flood", "water", "Ã¼berflut", "flooded", "rain", "bridge"]):
        incident_type = "flooding"
        detected_risks += ["possible blocked access route", "possible unsafe water exposure"]
        recommended += ["Confirm whether people are trapped or isolated.", "Route clean water and access assessment to the area."]
    if any(word in note for word in ["landslide", "mud", "rocks", "rockfall", "erdrutsch"]):
        incident_type = "landslide"
        detected_risks += ["possible slope instability", "blocked or unsafe access route"]
        recommended += ["Request an access and public-works assessment before sending vehicles."]
    if any(word in note for word in ["smoke", "wildfire", "fire", "evacuation", "burning", "rauch", "feuer"]):
        incident_type = "fire_smoke" if incident_type == "other" else incident_type
        detected_risks += ["possible smoke exposure or evacuation risk"]
        recommended += ["Confirm wind direction, evacuation routes, and whether vulnerable people need transport."]
    if any(word in note for word in ["bridge", "road", "collapsed", "blocked", "building", "damage", "brÃ¼cke", "straÃŸe", "roof"]):
        if incident_type == "other":
            incident_type = "infrastructure_damage"
        detected_risks += ["possible infrastructure damage", "access limitations for responders"]
        recommended += ["Ask public works or an access team to verify passability."]
    if any(word in note for word in ["injur", "wound", "medical", "medicine", "medication", "hospital", "verletz", "arzt"]):
        incident_type = "medical_supply_gap" if incident_type == "other" else incident_type
        detected_risks += ["possible medical need that requires qualified verification"]
        recommended += ["Escalate health-related details to a licensed professional."]
    if any(word in note for word in ["water", "food", "clean", "hunger", "wasser", "essen"]):
        if incident_type == "other":
            incident_type = "food_water_shortage"
        detected_risks += ["possible shortage of basic supplies"]
        recommended += ["Verify supply needs, quantities, and delivery access."]
    if any(word in note for word in ["shelter", "school", "famil", "people", "evacu", "unterkunft"]):
        if incident_type == "other":
            incident_type = "shelter_need"
        detected_risks += ["possible shelter or evacuation support need"]
        recommended += ["Confirm number of affected people and shelter capacity."]

    # Estimate urgency from words and approximate people counts.
    numbers = [int(x) for x in re.findall(r"\b\d{1,5}\b", field_note)]
    max_people = max(numbers) if numbers else 0
    urgency = "medium"
    if any(word in note for word in ["critical", "trapped", "missing", "life-threatening", "lebensgefahr"]):
        urgency = "critical"
    elif max_people >= 30 or any(word in note for word in ["blocked", "no clean water", "isolated", "high", "smoke", "refrigeration", "generator not working", "power failure"]):
        urgency = "high"
    elif max_people <= 5 and max_people > 0:
        urgency = "medium"

    if not recommended:
        recommended = ["Assign a human dispatcher to verify the report.", "Ask for exact location and current risk level."]
    detected_risks = list(dict.fromkeys(detected_risks)) or ["insufficient information; potential local safety issue"]
    evidence = [
        "Field note provided by user.",
        "Image evidence available." if has_image else "No image evidence was provided.",
    ]

    affected = "unknown"
    if max_people:
        affected = f"approximately {max_people} mentioned in field note"

    summary = f"{lang['summary_prefix']}: {incident_type.replace('_', ' ')} with {urgency} urgency; human verification required."
    sms = f"{lang['sms']}: {incident_type.replace('_', ' ')} / {urgency.upper()}. {affected}. Verify location, injuries, access, and immediate needs."

    return _normalize_report(
        {
            "incident_type": incident_type,
            "urgency": urgency,
            "summary": summary,
            "affected_people_estimate": affected,
            "location_clues": ["location not confirmed; ask for GPS, landmark, or administrative area"],
            "detected_risks": detected_risks,
            "evidence": evidence,
            "uncertainties": [
                "Visual assessment is limited in demo fallback mode." if has_image else "No image available for visual confirmation.",
                "Exact location and number of affected people need confirmation.",
            ],
            "missing_information": [
                "Exact location or landmark",
                "Are there injured or trapped people?",
                "Is the access route passable for responders?",
                "What supplies are immediately needed?",
            ],
            "recommended_actions": recommended,
            "priority_reasoning": "Urgency is derived from reported isolation, infrastructure/access risk, and number of affected people.",
            "field_message": sms,
            "structured_report": (
                f"INCIDENT: {incident_type.replace('_', ' ')}\n"
                f"URGENCY: {urgency.upper()}\n"
                f"AFFECTED: {affected}\n"
                f"EVIDENCE: field note{' + image' if has_image else ''}\n"
                f"ACTION: verify location, safety status, access route, and immediate needs."
            ),
            "safety_notes": [lang["verify"], lang["no_diag"], "Keep a human coordinator in the loop."],
            "language": language,
        },
        language,
    )


def analyze_crisis(
    *,
    image_bytes: Optional[bytes],
    field_note: str,
    language: str = "English",
    model: str = DEFAULT_MODEL,
    host: str = DEFAULT_OLLAMA_HOST,
    backend_mode: str = "auto",
) -> ModelCallResult:
    """Analyze a crisis report with Gemma 4, with optional deterministic fallback."""
    started = time.time()
    backend_mode = backend_mode.lower()

    if backend_mode == "demo fallback only":
        report = demo_analysis(field_note, language, bool(image_bytes))
        return ModelCallResult(report, json.dumps(report, indent=2), "Deterministic demo fallback", time.time() - started, True)

    try:
        return call_ollama_gemma(
            image_bytes=image_bytes,
            field_note=field_note,
            language=language,
            model=model,
            host=host,
        )
    except Exception as exc:
        if backend_mode == "gemma only":
            raise GemmaClientError(str(exc)) from exc
        report = demo_analysis(field_note, language, bool(image_bytes))
        report["safety_notes"].append(f"Gemma backend unavailable during this run; deterministic fallback used. Backend error: {exc}")
        return ModelCallResult(report, json.dumps(report, indent=2), "Deterministic demo fallback", time.time() - started, True)

