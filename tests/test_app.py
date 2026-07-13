from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


def test_unregister_participant():
    client = TestClient(app)
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(email_to_remove)}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email_to_remove} from {activity_name}"
    }

    activities_response = client.get("/activities")
    assert email_to_remove not in activities_response.json()[activity_name]["participants"]
