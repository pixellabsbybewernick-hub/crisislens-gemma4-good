"""Prompt templates and output schema for CrisisLens.

CrisisLens is intentionally conservative: it turns unstructured field evidence into
triage-ready reports while preserving uncertainty and human verification.
"""

CRISIS_REPORT_SCHEMA = {
    "incident_type": "flooding | infrastructure_damage | shelter_need | medical_supply_gap | food_water_shortage | fire_smoke | landslide | other",
    "urgency": "low | medium | high | critical",
    "summary": "one-sentence human-readable summary",
    "affected_people_estimate": "string; use unknown if not provided",
    "location_clues": ["visible or stated location clues; never invent exact coordinates"],
    "detected_risks": ["concrete risks observed or stated"],
    "evidence": ["facts grounded in image/text evidence"],
    "uncertainties": ["what the model is unsure about"],
    "missing_information": ["questions a dispatcher should ask next"],
    "recommended_actions": ["safe, practical next steps for a human coordinator"],
    "priority_reasoning": "short explanation for urgency level",
    "field_message": "short message suitable for WhatsApp/radio/SMS",
    "structured_report": "compact dispatch-style report",
    "safety_notes": ["verification and safety caveats"],
    "language": "language used in generated text",
}

SYSTEM_PROMPT = """
You are CrisisLens, a local-first crisis-reporting assistant for field teams, community coordinators, NGOs, and disaster-response volunteers.

Your task is to convert messy field evidence into a safe, structured, action-oriented crisis report.

Rules:
1. Ground every claim in the provided image and/or user note. Do not invent facts.
2. Do not identify people, faces, license plates, or private information.
3. Do not make medical diagnoses. For medical issues, recommend professional verification.
4. Use uncertainty explicitly. If evidence is weak, say so.
5. Prioritize human safety, de-escalation, and verification on the ground.
6. Keep recommendations practical for low-connectivity and resource-limited settings.
7. Return strict JSON only. No markdown. No prose outside JSON.
8. Write all human-readable fields in the requested output language.
9. Use the urgency scale: low, medium, high, critical.
10. If the image is missing, analyze the note only and state that image evidence is unavailable.
""".strip()

USER_PROMPT_TEMPLATE = """
Analyze this field report.

Requested output language: {language}

Field note:
{field_note}

Context:
- This tool is a proof-of-concept for the Gemma 4 Good Hackathon.
- It is designed for disaster response, global resilience, and low-connectivity coordination.
- The output must help a human coordinator triage, verify, and route the report.

Return JSON using this schema exactly:
{schema}
""".strip()


def build_user_prompt(field_note: str, language: str) -> str:
    """Build the user prompt with the schema embedded as a compact contract."""
    import json

    return USER_PROMPT_TEMPLATE.format(
        field_note=field_note.strip() or "No field note provided.",
        language=language,
        schema=json.dumps(CRISIS_REPORT_SCHEMA, indent=2, ensure_ascii=False),
    )
