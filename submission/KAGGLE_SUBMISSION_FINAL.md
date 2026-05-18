# CrisisLens — Local AI Field Reports with Gemma 4

## One-line summary

CrisisLens turns a field photo and a messy crisis note into a structured, auditable dispatch report, routing recommendation, and SMS/radio-ready message using Gemma 4 in a local-first workflow.

## Problem

In floods, landslides, fires, shelter operations, and rural infrastructure failures, local teams often receive critical information as photos, voice notes, WhatsApp messages, or short multilingual field reports. These messages are difficult to prioritize quickly. They may lack exact location, number of affected people, road access information, supply needs, or safety context.

The result is not only an information shortage. It is an information-shaping problem: field evidence must become a compact, structured, verified report before it can support action.

## Solution

CrisisLens is a prototype for a crisis-reporting assistant that helps coordinators transform unstructured evidence into operational summaries.

The workflow is:

1. A responder uploads a photo or selects a field scenario.
2. The responder adds a short field note.
3. Gemma 4 analyzes the image and text and returns strict structured JSON.
4. A deterministic routing tool maps the report to a review channel and team.
5. The app exports a human-readable dispatch report, JSON payload, and SMS/radio message.
6. A human coordinator remains the decision-maker.

## Why Gemma 4

CrisisLens is designed around Gemma 4 capabilities that matter in field conditions:

- multimodal interpretation of photos and text notes
- multilingual output for local teams
- structured JSON generation for downstream tools
- local-first deployment through Ollama
- agentic workflow pattern: model proposes, deterministic tool routes, human verifies

## Data

The hackathon provides no official dataset. CrisisLens therefore ships with synthetic but realistic crisis scenarios and sample images for safe, repeatable judging. This avoids using real victim data while still demonstrating the operational workflow.

The included scenarios cover floods, landslides, shelter pressure, smoke/fire risk, health-supply gaps, rural water shortage, and education infrastructure damage.

## Architecture

```text
Field photo + note
      ↓
Gemma 4 multimodal analysis
      ↓
Strict JSON report
      ↓
Deterministic routing tool
      ↓
Human coordinator review
      ↓
SMS / radio / JSON / Markdown export
```

## Safety and trust

CrisisLens deliberately avoids unsafe automation:

- no person identification
- no medical diagnosis
- explicit uncertainty fields
- missing-information questions
- human verification required before action
- deterministic routing instead of model-triggered emergency action
- transparent fallback mode for demo stability

## Impact area fit

### Global Resilience

The primary use case is disaster response and local resilience: floods, blocked bridges, landslides, temporary shelters, water shortages, and access constraints.

### Safety & Trust

The system makes uncertainty visible and avoids pretending that model output is ground truth. It separates probabilistic model reasoning from deterministic routing and human approval.

### Ollama / Local Ops

CrisisLens can run with Gemma 4 through Ollama, making it suitable for privacy-sensitive or low-connectivity environments where cloud APIs are unavailable or inappropriate.

## Limitations

This is a proof-of-concept, not an official emergency dispatch system. Field decisions must be made by trained humans. Model quality depends on the local Gemma 4 variant and hardware. The synthetic demo scenarios are not a replacement for field validation with humanitarian partners.

## What to test

Run the app, load the `Flooded bridge / water shortage` sample, generate a report, and inspect:

- urgency classification
- evidence and uncertainty
- missing information
- recommended actions
- deterministic routing output
- SMS/radio message
- JSON and Markdown export
