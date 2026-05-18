from gemma_client import demo_analysis, route_incident


def test_high_flood_routes_to_emergency_team():
    report = demo_analysis(
        "Bridge blocked after flooding. 40 people isolated and no clean water.",
        "English",
        has_image=True,
    )
    route = route_incident(report)
    assert report["urgency"] == "high"
    assert "water" in route["recommended_team"].lower() or "emergency" in route["recommended_team"].lower()
    assert route["human_gate_required"] is True


def test_medical_note_adds_safety_caveat():
    report = demo_analysis("Medication supply missing for 12 elderly residents.", "English", has_image=False)
    assert any("medical" in note.lower() or "health" in note.lower() for note in report["safety_notes"])


def test_landslide_routes_to_access_team():
    report = demo_analysis(
        "Road partially covered by mud and rocks after landslide. One bus route blocked.",
        "English",
        has_image=True,
    )
    route = route_incident(report)
    assert report["incident_type"] == "landslide"
    assert "access" in route["recommended_team"].lower() or "works" in route["recommended_team"].lower()


def test_smoke_report_preserves_human_gate():
    report = demo_analysis(
        "Smoke visible near village edge. Two elderly residents report breathing difficulty. Need evacuation guidance.",
        "English",
        has_image=False,
    )
    route = route_incident(report)
    assert report["urgency"] == "high"
    assert route["human_gate_required"] is True
    assert any("diagnosis" in note.lower() or "qualified" in note.lower() for note in report["safety_notes"])
