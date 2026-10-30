"""
Integration anti-regression tests for ML Core Orchestrator and FastAPI Server.
Verifies complete pipeline wiring, SQLite persistence, and API endpoint contracts.
"""
import pytest
from fastapi.testclient import TestClient
import server
from ml_core.orchestrator import analyze_incident


@pytest.fixture
def client():
    return TestClient(server.app)


def test_server_app_routes(client):
    """Verify that core routes respond with 200 OK."""
    root_res = client.get("/")
    assert root_res.status_code == 200
    data = root_res.json()
    assert "status" in data
    assert data["status"] == "ok"

    incidents_res = client.get("/api/incidents")
    assert incidents_res.status_code == 200
    assert isinstance(incidents_res.json(), list)


def test_server_create_and_fetch_incident(client):
    """Test creating an incident and fetching it back via SQLite persistence."""
    payload = {
        "title": "Integration Test Case",
        "statements": [
            "The suspect was wearing a black jacket at 3 PM on Main Street.",
            "The suspect wore a yellow raincoat at 3 PM on Main Street."
        ]
    }
    create_res = client.post("/api/incidents", json=payload)
    assert create_res.status_code == 200
    res_data = create_res.json()
    assert "id" in res_data
    assert "summary" in res_data
    assert res_data["summary"]["title"] == "Integration Test Case"

    # Fetch incident detail
    inc_id = res_data["id"]
    detail_res = client.get(f"/api/incidents/{inc_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert "statements" in detail
    assert len(detail["statements"]) == 2
    assert "contradictions" in detail


def test_orchestrator_empty_statements():
    """Verify orchestrator handles empty statements list gracefully."""
    result = analyze_incident([])
    assert isinstance(result, dict)
    assert result["metrics"]["total_contradictions"] == 0
    assert result["contradictions"] == []
    assert result["events"] == []
    assert result["entities"] == []
    assert result["temporals"] == []
    assert result["spatials"] == []


def test_orchestrator_pipeline_with_mocked_llm(monkeypatch):
    """Verify complete ML pipeline execution end-to-end with mocked LLM."""
    def mock_llm_response(prompt: str, error_msg=None) -> str:
        prompt_lower = prompt.lower()
        if "extract all events" in prompt_lower or "events/actions" in prompt_lower:
            return '[{"subject": "suspect", "action": "entered", "object": "bank", "is_explicit_denial": false, "source_span": [0, 0]}]'
        if "contradict" in prompt_lower or "compare these two" in prompt_lower:
            return '{"contradiction": true, "confidence": 0.85}'
        return '{"rationale": "Witness A stated suspect drove red car whereas Witness B stated blue bike."}'

    monkeypatch.setattr("ml_core.llm_client.call_local_llm", mock_llm_response)
    monkeypatch.setattr("ml_core.orchestrator.call_local_llm", mock_llm_response)

    statements = [
        "At 10:00 AM on MG Road, the suspect entered the bank wearing a blue jacket.",
        "At 10:00 AM on MG Road, the suspect entered the bank wearing a bright red coat."
    ]

    result = analyze_incident(statements)
    assert isinstance(result, dict)
    assert "contradictions" in result
    assert "events" in result
    assert "entities" in result
    assert "temporals" in result
    assert "spatials" in result
    assert len(result["events"]) >= 1


def test_server_feedback_endpoint(client):
    """Test human-in-the-loop feedback submission endpoint."""
    feedback_payload = {
        "detection_result_id": "c1",
        "reviewer_verdict": "confirmed",
        "note": "Verified against CCTV footage."
    }
    res = client.post("/api/feedback", json=feedback_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "feedback" in data
    assert data["feedback"]["detection_result_id"] == "c1"
    assert data["feedback"]["reviewer_verdict"] == "confirmed"
