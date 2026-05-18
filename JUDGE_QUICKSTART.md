# Judge Quickstart

CrisisLens is a local-first crisis reporting workflow for the Gemma 4 Good Hackathon.

Full local Gemma 4 / Ollama mode:

1. Install Python dependencies

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

2. Install and test Gemma 4 E2B with Ollama

ollama pull gemma4:e2b
ollama run gemma4:e2b "Return exactly: CrisisLens ready."

Expected response:

CrisisLens ready.

3. Start CrisisLens

streamlit run app.py

Open:

http://localhost:8501

Use these settings in the sidebar:

Backend mode: auto
Ollama model: gemma4:e2b
Ollama host: http://localhost:11434
Use sample scenario: off

Test field note:

Bridge blocked after heavy flooding. Around 40 people are isolated near the school. No clean water since yesterday. Road access unknown.

Expected result:

Backend: Ollama / gemma4:e2b

Hosted demo note:

The hosted Streamlit demo is provided for fast judge access to the interface and workflow. The full local Gemma 4 E2B / Ollama workflow is demonstrated in the video and reproducible from this repository.

Safety note:

CrisisLens is designed for human decision support, not autonomous emergency response. The model proposes, a deterministic routing tool routes, and a human verifies.
