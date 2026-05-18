# CrisisLens Kaggle demo script
# This lightweight script demonstrates the core report-generation workflow without Streamlit.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gemma_client import analyze_crisis, route_incident

field_note = "Bridge blocked after heavy flooding. Around 40 people are isolated near the school. No clean water since yesterday. Road access unknown."

result = analyze_crisis(
    image_bytes=None,
    field_note=field_note,
    language="English",
    backend_mode="demo fallback only",  # switch to auto/gemma only when local Gemma 4 is available
)

print("BACKEND:", result.backend)
print("REPORT:")
print(result.report)
print("ROUTING:")
print(route_incident(result.report))
