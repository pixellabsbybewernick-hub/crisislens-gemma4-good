# CrisisLens model and safety card

## Intended use

CrisisLens is a proof-of-concept assistant for turning unstructured field evidence into triage-ready crisis reports. It is intended for demos, research, prototyping, and community-response workflow exploration.

## Out-of-scope use

CrisisLens is not an official emergency-response system and must not be used as the sole basis for life-critical decisions.

## Model role

Gemma 4 is used to interpret image/text evidence and produce a structured report. The model does not execute actions, send alerts, or make final decisions.

## Human role

A human coordinator must verify every report before operational action.

## Key safeguards

- No identity inference.
- No face recognition.
- No medical diagnosis.
- Explicit uncertainty field.
- Missing-information prompts.
- Deterministic routing with human gate.
- Downloadable reports for audit and review.

## Known limitations

- Visual understanding depends on model quality and image clarity.
- The app does not verify geolocation.
- The app does not connect to official dispatch systems by default.
- The fallback mode is a deterministic demo mode, not AI analysis.
