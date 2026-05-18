# CrisisLens — Local AI Field Reports with Gemma 4

## Summary

CrisisLens is a local-first crisis reporting assistant built for the Gemma 4 Good Hackathon. It turns a photo and a short, messy field note into a structured dispatch report, deterministic routing recommendation, and SMS/radio-ready message for human coordinators.

The core workflow is:

```text
field photo + note → Gemma 4 structured analysis → deterministic routing → human verification → SMS / JSON / Markdown export
```

CrisisLens is designed for low-connectivity disaster response scenarios where teams need clear, compact, multilingual information but cannot rely on always-on cloud infrastructure.

## Problem

During floods, landslides, fires, shelter operations, water shortages, and infrastructure failures, responders often receive information in unstructured formats:

- phone photos
- short text messages
- radio notes
- translated messages
- partial location descriptions
- uncertain numbers of affected people

The operational problem is not only getting information. The harder problem is turning messy evidence into a structured, verifiable report quickly enough for humans to act on it.

## Solution

CrisisLens provides a coordinator dashboard that:

1. Accepts a photo and field note.
2. Uses Gemma 4 to extract a structured JSON report.
3. Classifies incident type and urgency.
4. Lists detected risks, evidence, uncertainties, and missing information.
5. Generates recommended actions and a compact SMS/radio message.
6. Runs a deterministic routing function to recommend the review team and response channel.
7. Exports JSON and Markdown for dispatch or audit workflows.

## Why Gemma 4

The project is built around Gemma 4 strengths:

- **Multimodal understanding:** a crisis report often includes both image evidence and text.
- **Multilingual output:** local teams may need reports in different languages.
- **Structured reasoning:** the app asks for strict JSON that can feed downstream tools.
- **Local-first deployment:** the app can run through Ollama so sensitive field information can remain on local hardware.
- **Agentic workflow:** Gemma proposes structured evidence; deterministic code routes; humans verify.

## Data strategy

The hackathon provides no official dataset, so CrisisLens uses synthetic but realistic crisis scenarios for safe and repeatable judging. This avoids exposing real victim data or sensitive locations.

Included scenarios cover:

- flooded bridge and clean-water shortage
- shelter capacity pressure
- landslide road obstruction
- wildfire smoke and evacuation risk
- medical supply refrigeration failure
- remote drinking-water shortage
- rural school roof damage
- sparse radio reports

The goal is not to claim field validation. The goal is to demonstrate a realistic product workflow that could later be adapted with humanitarian partners and real operating procedures.

## Architecture

```text
Streamlit UI
  ├─ image upload / sample scenario
  ├─ field note input
  ├─ Gemma 4 via Ollama /api/generate
  ├─ strict JSON report parser
  ├─ deterministic routing tool
  ├─ coordinator dashboard
  └─ JSON + Markdown + SMS export
```

## Safety and trust design

CrisisLens is intentionally conservative:

- It does not identify people in images.
- It does not make medical diagnoses.
- It preserves uncertainty instead of hiding it.
- It asks missing-information questions.
- It requires human verification before action.
- It uses deterministic routing logic rather than letting the model directly trigger emergency actions.
- It labels demo fallback mode clearly.

The key design principle is:

> The model proposes. A deterministic tool routes. A human verifies.

## Impact area fit

### Global Resilience

CrisisLens directly targets disaster response, access constraints, water shortages, temporary shelters, and local coordination after extreme events.

### Safety & Trust

The system is built around uncertainty, auditability, human gates, and conservative outputs.

### Ollama / Local Ops

When run with Ollama, CrisisLens demonstrates local Gemma 4 usage for privacy-sensitive, low-connectivity environments.

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Optional local Gemma 4:

```bash
ollama pull gemma4
ollama serve
streamlit run app.py
```

## What to test

1. Open the app.
2. Choose `Flooded bridge / water shortage`.
3. Generate a report.
4. Inspect urgency, evidence, missing information, routing, SMS/radio message, and exports.
5. Try batch triage mode.
6. Open the `Data & prize fit` tab to see the intended hackathon alignment.

## Limitations

CrisisLens is a proof-of-concept, not an official emergency dispatch system. It must not be used to make real emergency decisions without trained human review and institutional validation. Model quality depends on the Gemma 4 variant, image quality, and hardware. The included scenarios are synthetic and intended for safe demonstration.

## Future work

- Partner with emergency-response organizations for workflow validation.
- Add offline speech-to-text for radio/voice notes.
- Add local map/GPS support.
- Add secure incident queues for teams.
- Evaluate with historical public disaster reports.
- Add mobile/wearable deployment using edge runtimes.
