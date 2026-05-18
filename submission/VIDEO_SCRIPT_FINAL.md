# 3-minute video script — CrisisLens

## 0:00–0:20 — Hook

"In a disaster, the problem is often not that nobody has information. The problem is that the information is messy: photos, short messages, different languages, missing locations, and unclear urgency. CrisisLens turns that messy field evidence into a structured report that a human coordinator can verify and route."

## 0:20–0:40 — Why Gemma 4

"We built CrisisLens for the Gemma 4 Good Hackathon because Gemma 4 is exactly the kind of model that makes this workflow possible: multimodal understanding, local inference, multilingual output, and structured reasoning for agentic workflows."

## 0:40–1:35 — Live demo

Show the app.

1. Select `Flooded bridge / water shortage`.
2. Show the image and field note.
3. Click `Generate crisis report`.
4. Show urgency: HIGH.
5. Show dispatch report.
6. Show detected risks and missing information.
7. Show SMS/radio message.

Narration:

"Here we have a blocked bridge after flooding. The note says around 40 people are isolated near a school and there has been no clean water since yesterday. CrisisLens turns this into an incident type, urgency level, evidence list, missing questions, and an SMS-ready message."

## 1:35–2:05 — Routing and safety

Show routing JSON and safety notes.

"The model does not directly trigger emergency actions. Gemma 4 proposes the structured report. A deterministic routing tool recommends the team and review time. The system always keeps a human coordinator in the loop, and it explicitly shows uncertainty. It does not identify people and does not make medical diagnoses."

## 2:05–2:35 — Data and prize fit

Switch to `Data & prize fit` tab.

"The hackathon provides no dataset, so we use synthetic crisis scenarios to avoid real victim data and keep judging repeatable. The main target is Global Resilience, with strong Safety & Trust and Ollama/local-first alignment."

## 2:35–3:00 — Closing

"CrisisLens is not a generic chatbot. It is a local-first crisis reporting workflow: photo plus note, Gemma 4 analysis, structured dispatch report, auditable routing, SMS export, and human verification. When connectivity fails, communities still need clear information. CrisisLens helps make that possible."
