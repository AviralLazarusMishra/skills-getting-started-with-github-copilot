from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app

client = TestClient(app)


def test_unregister_participant_successfully():
    activity_name = "Chess Club"
    email = "student@example.com"

    activity = app_module.activities[activity_name]
    if email in activity["participants"]:
        activity["participants"].remove(email)

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_participant_missing_email_returns_404():
    response = client.delete("/activities/Chess Club/unregister?email=missing@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
