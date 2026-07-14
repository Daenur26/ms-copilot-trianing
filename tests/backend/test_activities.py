import uuid
from urllib.parse import quote

from src.app import activities


def test_root_redirect(client):
    # Arrange
    # client fixture provided by conftest.py

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_duplicate(client):
    # Arrange
    activity = "Programming Class"
    unique_email = f"tester+{uuid.uuid4().hex}@mergington.edu"

    # Act - first signup
    resp1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": unique_email})

    # Assert - first signup success
    assert resp1.status_code == 200
    assert resp1.json()["message"] == f"Signed up {unique_email} for {activity}"

    # Act - duplicate signup
    resp2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": unique_email})

    # Assert - duplicate rejected
    assert resp2.status_code == 400


def test_unregister_participant(client):
    # Arrange
    activity = "Chess Club"
    unique_email = f"tester+{uuid.uuid4().hex}@mergington.edu"

    # Ensure the participant exists first
    signup_resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": unique_email})
    assert signup_resp.status_code == 200

    # Act - unregister
    del_resp = client.delete(f"/activities/{quote(activity)}/participants/{quote(unique_email)}")

    # Assert
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == f"Removed {unique_email} from {activity}"

    # Confirm removal
    activities_resp = client.get("/activities")
    assert unique_email not in activities_resp.json()[activity]["participants"]


def test_activity_not_found(client):
    # Arrange
    activity = "This Activity Does Not Exist"
    email = f"tester+{uuid.uuid4().hex}@mergington.edu"

    # Act
    signup_resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    del_resp = client.delete(f"/activities/{quote(activity)}/participants/{quote(email)}")

    # Assert
    assert signup_resp.status_code == 404
    assert del_resp.status_code == 404
