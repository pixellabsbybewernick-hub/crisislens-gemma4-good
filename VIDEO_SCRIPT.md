# CrisisLens 3-minute demo video script

## Required video goal

The judges must understand in the first 30 seconds that this is not a generic chatbot. It is a local-first crisis reporting workflow powered by Gemma 4.

## 0:00–0:20 — Human problem

"In a disaster, local teams often do not receive perfect reports. They receive a photo, a short message, a translated note, or a radio update. The problem is turning that messy evidence into something a human coordinator can actually verify and route."

## 0:20–0:40 — Product intro

"This is CrisisLens: a local-first field reporting assistant built with Gemma 4. It converts a crisis photo and short field note into a structured dispatch report, urgency level, missing-information checklist, routing recommendation, and SMS-ready message."

## 0:40–1:25 — Main demo

Screen recording:

1. Open Streamlit app.
2. Sidebar: show backend mode and model name.
3. Select `Flooded bridge / water shortage`.
4. Show image and field note.
5. Click `Generate crisis report`.
6. Show urgency = HIGH.
7. Show dispatch report and SMS/radio message.

Narration:

"Here the field note says a bridge is blocked after flooding, around 40 people are isolated near a school, and there has been no clean water since yesterday. CrisisLens turns that into a high-priority field report with evidence, risks, missing details, and a compact message that can be sent over SMS or radio."

## 1:25–2:00 — Safety and routing

Screen recording:

1. Show Routing tool output.
2. Show Uncertainties.
3. Show Safety notes.
4. Download JSON report.

Narration:

"Gemma 4 does not directly trigger emergency actions. The model proposes a structured report, a deterministic routing tool recommends the team and review time, and a human coordinator remains in control. CrisisLens also refuses to identify people, avoids medical diagnosis, and makes uncertainty visible."

## 2:00–2:30 — Batch and data page fit

Screen recording:

1. Switch to `Coordinator batch view`.
2. Show ranked incoming reports.
3. Switch to `Data & prize fit`.

Narration:

"The hackathon provides no official dataset, so we use synthetic crisis scenarios for safe, repeatable judging instead of real victim data. The batch view shows how a coordinator could triage multiple incoming field notes."

## 2:30–3:00 — Closing / prize positioning

"CrisisLens fits Global Resilience because it supports disaster response and access constraints. It fits Safety & Trust because it preserves uncertainty and requires human verification. And with Ollama, it shows how Gemma 4 can run locally when privacy and connectivity matter. CrisisLens is simple: photo plus note, Gemma 4 analysis, auditable routing, SMS export, human verification."
