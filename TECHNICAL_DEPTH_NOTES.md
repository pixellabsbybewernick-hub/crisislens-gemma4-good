# Technical depth notes for judges

## Components

1. **Streamlit UI** — single-page coordinator workflow.
2. **Gemma/Ollama client** — calls local Ollama `/api/generate` with optional image payload and JSON mode.
3. **Strict prompt schema** — asks Gemma 4 to produce operational fields rather than generic prose.
4. **JSON parser/normalizer** — robustly extracts and normalizes model JSON.
5. **Deterministic routing tool** — maps incident type + urgency to team/channel/SLA.
6. **Safety layer** — uncertainty fields, missing-information list, medical/person-identification constraints.
7. **Exports** — JSON for systems, Markdown for documentation, SMS/radio summary for low connectivity.

## Why deterministic routing matters

Emergency-like workflows should not let a language model directly dispatch resources. CrisisLens separates probabilistic interpretation from deterministic routing logic. This makes the system more auditable and safer:

- Gemma 4 interprets evidence.
- Python rules route the report.
- A human coordinator approves action.

## Gemma prompt contract

The model is instructed to return fields such as:

- `incident_type`
- `urgency`
- `evidence`
- `uncertainties`
- `missing_information`
- `recommended_actions`
- `field_message`
- `structured_report`
- `safety_notes`

The app validates/normalizes these fields before display.

## Demo fallback

A deterministic fallback is included for demo stability and CI tests. It is visibly labeled in the UI and should not be presented as Gemma output. Its purpose is to keep the app testable when a local model is unavailable.
