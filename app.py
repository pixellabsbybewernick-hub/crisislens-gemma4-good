from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import streamlit as st
from PIL import Image

from gemma_client import DEFAULT_MODEL, DEFAULT_OLLAMA_HOST, analyze_crisis, route_incident

APP_DIR = Path(__file__).resolve().parent
ASSET_DIR = APP_DIR / "assets"

st.set_page_config(
    page_title="CrisisLens - Local AI Field Reports",
    page_icon="›°ï¸",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root { --card: rgba(255,255,255,0.06); --muted: rgba(255,255,255,0.65); }
.block-container { padding-top: 1.3rem; }
.hero {
  padding: 1.4rem 1.6rem;
  border-radius: 1.4rem;
  background: linear-gradient(135deg, rgba(43,88,255,.18), rgba(25,160,120,.16));
  border: 1px solid rgba(255,255,255,.12);
  margin-bottom: 1rem;
}
.hero h1 { margin: 0; font-size: 2.45rem; letter-spacing: -0.04em; }
.hero p { color: var(--muted); font-size: 1.03rem; margin: .35rem 0 0 0; max-width: 70rem; }
.metric-card {
  padding: 1rem; border-radius: 1rem; background: var(--card); border: 1px solid rgba(255,255,255,.10);
}
.metric-card b { display: block; font-size: .85rem; color: var(--muted); margin-bottom: .3rem; }
.urgency-low { color: #8ddf8d; font-weight: 800; }
.urgency-medium { color: #ffd166; font-weight: 800; }
.urgency-high { color: #ff9f1c; font-weight: 800; }
.urgency-critical { color: #ff4d6d; font-weight: 900; }
.small-muted { color: var(--muted); font-size: .9rem; }
.report-box { padding: 1rem; border-radius: 1rem; background: rgba(255,255,255,.055); border: 1px solid rgba(255,255,255,.10); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def read_image_bytes(path: Path) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def show_list(title: str, items: list[str]) -> None:
    st.markdown(f"**{title}**")
    if not items:
        st.caption("No items reported.")
        return
    for item in items:
        st.markdown(f"- {item}")


def urgency_class(level: str) -> str:
    level = (level or "medium").lower()
    return f"urgency-{level if level in ['low','medium','high','critical'] else 'medium'}"


def report_to_markdown(report: Dict[str, Any], routing: Dict[str, Any]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    bullets = lambda xs: "\n".join([f"- {x}" for x in xs]) if xs else "- None"
    return f"""# CrisisLens Field Report

Generated: {now}

## Summary
{report.get('summary')}

## Classification
- Incident type: {report.get('incident_type')}
- Urgency: {str(report.get('urgency')).upper()}
- Affected people: {report.get('affected_people_estimate')}

## Evidence
{bullets(report.get('evidence', []))}

## Detected risks
{bullets(report.get('detected_risks', []))}

## Missing information
{bullets(report.get('missing_information', []))}

## Recommended actions
{bullets(report.get('recommended_actions', []))}

## Routing recommendation
- Team: {routing.get('recommended_team')}
- Channel: {routing.get('routing_channel')}
- Target review time: {routing.get('target_review_time')}
- Human gate required: {routing.get('human_gate_required')}

## Field message
{report.get('field_message')}

## Structured report
```text
{report.get('structured_report')}
```

## Safety notes
{bullets(report.get('safety_notes', []))}
"""


def hero() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>›°ï¸ CrisisLens</h1>
          <p><b>Local-first AI field reports with Gemma 4.</b> Turn photos and messy field notes into structured crisis reports, routing suggestions, SMS-ready summaries, and explicit uncertainty for human coordinators.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sample_selector() -> tuple[Optional[bytes], str, str]:
    samples = {
        "Flooded bridge / water shortage": {
            "image": ASSET_DIR / "sample_flooded_bridge.png",
            "note": "Bridge blocked after heavy flooding. Around 40 people are isolated near the school. No clean water since yesterday. Road access unknown.",
        },
        "Shelter capacity pressure": {
            "image": ASSET_DIR / "sample_shelter_queue.png",
            "note": "Village school is being used as temporary shelter. About 75 people arrived, including families with children. Need blankets, drinking water, and registration support.",
        },
        "Damaged road after landslide": {
            "image": ASSET_DIR / "sample_landslide_road.png",
            "note": "Road partially covered by mud and rocks after landslide. One bus route blocked. No injuries reported yet. Need access assessment before sending supplies.",
        },
    }
    choice = st.selectbox("Load a polished demo scenario", list(samples.keys()))
    scenario = samples[choice]
    try:
        image_bytes = read_image_bytes(scenario["image"])
    except FileNotFoundError:
        image_bytes = None
    return image_bytes, scenario["note"], choice


def render_report(report: Dict[str, Any], result_backend: str, latency: float, used_fallback: bool) -> None:
    routing = route_incident(report)
    urgency = str(report.get("urgency", "medium")).lower()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><b>Urgency</b><span class='{urgency_class(urgency)}'>{urgency.upper()}</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><b>Incident</b>{str(report.get('incident_type')).replace('_', ' ').title()}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><b>Backend</b>{result_backend}</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-card'><b>Latency</b>{latency:.2f}s</div>", unsafe_allow_html=True)

    if used_fallback:
        st.warning("Demo fallback was used because the local Gemma backend was unavailable or fallback mode was selected. For final recording, run Ollama + Gemma 4 if possible.")

    st.markdown("### Executive summary")
    st.markdown(f"<div class='report-box'>{report.get('summary')}</div>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("### Dispatch report")
        st.code(report.get("structured_report", ""), language="text")
        st.markdown("### SMS / radio message")
        st.success(report.get("field_message", ""))
        st.markdown("### Routing tool output")
        st.json(routing)
    with right:
        show_list("Detected risks", report.get("detected_risks", []))
        show_list("Missing information", report.get("missing_information", []))
        show_list("Recommended actions", report.get("recommended_actions", []))
        show_list("Uncertainties", report.get("uncertainties", []))
        show_list("Safety notes", report.get("safety_notes", []))

    export_payload = {
        "report": report,
        "routing": routing,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "app": "CrisisLens",
    }
    st.download_button(
        "Download JSON report",
        data=json.dumps(export_payload, indent=2, ensure_ascii=False),
        file_name="crisislens_report.json",
        mime="application/json",
    )
    st.download_button(
        "Download Markdown report",
        data=report_to_markdown(report, routing),
        file_name="crisislens_report.md",
        mime="text/markdown",
    )


def batch_demo() -> None:
    st.markdown("### Batch triage demo")
    st.caption("Shows how multiple incoming field notes can be ranked for a coordinator dashboard.")
    data_path = APP_DIR / "demo_inputs" / "field_notes.csv"
    df = pd.read_csv(data_path)
    rows = []
    for _, row in df.iterrows():
        result = analyze_crisis(
            image_bytes=None,
            field_note=row["field_note"],
            language="English",
            backend_mode="demo fallback only",
        )
        report = result.report
        routing = route_incident(report)
        rows.append(
            {
                "id": row["id"],
                "urgency": report["urgency"],
                "incident_type": report["incident_type"],
                "affected": report["affected_people_estimate"],
                "target_review_time": routing["target_review_time"],
                "message": report["field_message"],
            }
        )
    out = pd.DataFrame(rows)
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    out["sort"] = out["urgency"].map(order).fillna(4)
    out = out.sort_values(["sort", "id"]).drop(columns=["sort"])
    st.dataframe(out, use_container_width=True, hide_index=True)


def main() -> None:
    hero()

    with st.sidebar:
        st.header("Gemma backend")
        backend_mode = st.radio(
            "Backend mode",
            ["auto", "gemma only", "demo fallback only"],
            help="auto tries local Ollama/Gemma first and falls back to deterministic demo mode.",
        )
        model = st.text_input("Ollama model", value=DEFAULT_MODEL)
        host = st.text_input("Ollama host", value=DEFAULT_OLLAMA_HOST)
        st.divider()
        st.header("Demo assets")
        use_sample = st.toggle("Use sample scenario", value=True)
        output_language = st.selectbox("Output language", ["English", "Deutsch", "EspaÃ±ol", "FranÃ§ais", "Arabic", "Hindi", "Swahili"])
        st.caption("For the strongest Kaggle video: run local Gemma 4, show image + note -> report -> routing -> SMS export.")

    tab1, tab2, tab3, tab4 = st.tabs(["Analyze field report", "Coordinator batch view", "Submission story", "Data & prize fit"])

    with tab1:
        left, right = st.columns([0.95, 1.05])
        sample_bytes = None
        default_note = ""
        if use_sample:
            sample_bytes, default_note, scenario_name = sample_selector()
        else:
            scenario_name = "custom"

        with left:
            st.markdown("### 1) Evidence")
            uploaded = st.file_uploader("Upload field photo", type=["png", "jpg", "jpeg", "webp"])
            image_bytes = uploaded.read() if uploaded else sample_bytes
            if image_bytes:
                st.image(image_bytes, caption=f"Evidence image - {scenario_name}", use_container_width=True)
            else:
                st.info("No image selected. The app will analyze the note only.")
            field_note = st.text_area("Field note", value=default_note, height=160)
            run = st.button("Generate crisis report", type="primary", use_container_width=True)

        with right:
            st.markdown("### 2) Gemma 4 analysis + routing")
            if run:
                with st.spinner("Generating structured report..."):
                    try:
                        result = analyze_crisis(
                            image_bytes=image_bytes,
                            field_note=field_note,
                            language=output_language,
                            model=model,
                            host=host,
                            backend_mode=backend_mode,
                        )
                        render_report(result.report, result.backend, result.latency_seconds, result.used_fallback)
                    except Exception as exc:
                        st.error(f"Analysis failed: {exc}")
                        st.info("Switch Backend mode to 'auto' or 'demo fallback only' to keep the demo running without a local model.")
            else:
                st.markdown(
                    """
                    <div class='report-box'>
                    Upload a photo or load a sample scenario, add a short field note, then generate a crisis report. The output is deliberately structured: classification, urgency, uncertainty, missing information, recommended actions, and a compact SMS/radio message.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with tab2:
        batch_demo()

    with tab3:
        st.markdown(
            """
            ### Why this is built for the Gemma 4 Good Hackathon

            **Impact:** CrisisLens targets **Global Resilience**: crisis teams often receive photos and short messages that are hard to triage quickly, especially when connectivity is weak or language varies.

            **Gemma 4 fit:** The app uses multimodal understanding for photo + text, multilingual output for local teams, structured JSON for downstream tooling, and a deterministic routing function that keeps humans in control.

            **Safety & Trust:** The system does not identify people, does not make diagnoses, preserves uncertainty, asks for missing information, and requires human verification before action.

            **Ollama / local ops angle:** CrisisLens is designed to run through a local Ollama backend so the demo can show Gemma 4 operating without sending sensitive crisis reports to a cloud service.

            **Demo arc:** messy evidence -> Gemma analysis -> structured report -> deterministic routing -> SMS export -> human gate.
            """
        )

    with tab4:
        st.markdown("### Data-page alignment")
        st.info("The hackathon provides no official dataset, so CrisisLens ships with synthetic crisis scenarios for safe, repeatable judging and avoids real victim data.")
        st.markdown("### Prize targeting")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Target": "Main Track", "Why CrisisLens fits": "Complete product prototype with human story, demo, code, and operational workflow."},
                    {"Target": "Global Resilience", "Why CrisisLens fits": "Floods, landslides, shelter pressure, blocked roads, water shortage, and field triage."},
                    {"Target": "Safety & Trust", "Why CrisisLens fits": "Uncertainty, no person identification, no diagnosis, human verification gate, auditable routing."},
                    {"Target": "Ollama / Local Ops", "Why CrisisLens fits": "Local Gemma backend for privacy-sensitive, low-connectivity field reporting."},
                ]
            ),
            use_container_width=True,
        )
        st.markdown("### What the judges should notice")
        st.markdown(
            """
            - This is not a generic chatbot; it is an end-to-end crisis-report workflow.
            - Gemma produces structured evidence; deterministic logic handles routing.
            - The output is practical: JSON for systems, Markdown for reports, SMS/radio for low connectivity.
            - The safety layer is visible in the UI, not hidden in a paragraph.
            """
        )


if __name__ == "__main__":
    main()


