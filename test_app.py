from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_unregister_participant_removes_email():
    original = app_module.activities["Chess Club"]["participants"][:]
    try:
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
        assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
    finally:
        app_module.activities["Chess Club"]["participants"] = original


def test_unregister_unknown_participant_returns_404():
    original = app_module.activities["Chess Club"]["participants"][:]
    try:
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "ghost@mergington.edu"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found in activity"
    finally:
        app_module.activities["Chess Club"]["participants"] = original
