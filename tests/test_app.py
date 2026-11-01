import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def test_health_endpoint_reports_model_state():
    response = app.test_client().get("/health")

    assert response.status_code == 200
    payload = response.get_json()
    assert "ready" in payload
    assert "error" in payload


def test_empty_question_is_rejected():
    response = app.test_client().post("/ask", json={"question": "   "})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Please enter a question."


def test_non_string_question_is_rejected():
    response = app.test_client().post("/ask", json={"question": 123})

    assert response.status_code == 400
