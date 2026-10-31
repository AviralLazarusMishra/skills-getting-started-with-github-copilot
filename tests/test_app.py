import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


def test_unregister_participant_successfully():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    activity = app_module.activities[activity_name]

    if email in activity["participants"]:
        activity["participants"].remove(email)

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_participant_missing_email_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
