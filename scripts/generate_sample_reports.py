"""Generate sample CrisisLens reports from demo scenarios.

This script uses deterministic demo fallback so it can run in CI or Kaggle without
local Ollama. For the final video, run the Streamlit app with local Gemma 4.
"""

from __future__ import annotations

import json
from pathlib import Path

from gemma_client import analyze_crisis, route_incident

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "data" / "demo_scenarios.jsonl"
OUT = ROOT / "sample_reports"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for line in SCENARIOS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        scenario = json.loads(line)
        result = analyze_crisis(
            image_bytes=None,
            field_note=scenario["field_note"],
            language="English",
            backend_mode="demo fallback only",
        )
        payload = {
            "scenario": scenario,
            "report": result.report,
            "routing": route_incident(result.report),
            "backend": result.backend,
        }
        (OUT / f"{scenario['id']}_report.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    print(f"Wrote reports to {OUT}")


if __name__ == "__main__":
    main()
