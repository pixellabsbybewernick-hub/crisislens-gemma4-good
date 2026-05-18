from pathlib import Path
import re

p = Path("app.py")
s = p.read_text(encoding="utf-8")

# Remove broken emoji / mojibake artifacts in Streamlit Cloud UI
s = re.sub(r'page_icon="[^"]*"', 'page_icon="C"', s)
s = re.sub(r'#\s*[^A-Za-z\r\n]*CrisisLens', '# CrisisLens', s)

replacements = {
    "›°ï¸": "",
    "ðŸ”­": "",
    "ðŸš¨": "",
    "â†’": "->",
    "â€”": "-",
    "â€“": "-",
    "EspaÃ±ol": "Spanish",
    "FranÃ§ais": "French",
    "Evidence image â€”": "Evidence image -",
}

for old, new in replacements.items():
    s = s.replace(old, new)

# Make public hosted demo fast instead of waiting for unavailable localhost Ollama
s = re.sub(
    r'(\["auto", "gemma only", "demo fallback only"\],)\s*help=',
    r'\1 index=2, help=',
    s
)

# Replace sidebar caption with a clear hosted-demo note
s = re.sub(
    r'st\.caption\("For the strongest Kaggle video:.*?"\)',
    'st.caption("Hosted demo runs in fast demo mode. Full local Gemma 4 E2B / Ollama mode is shown in the video and reproducible from GitHub.")',
    s
)

p.write_text(s, encoding="utf-8")
