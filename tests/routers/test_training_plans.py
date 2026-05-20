from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_training_plan():
    response = client.post(
        "/training-plans",
        json={
            "race_type": "half_marathon",
            "race_date": "2026-09-20",
            "experience_level": "beginner",
            "days_per_week": 4,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "race_type": "half_marathon",
        "race_date": "2026-09-20",
        "experience_level": "beginner",
        "days_per_week": 4,
        "status": "draft",
    }


def test_create_training_plan_rejects_invalid_days_per_week():
    response = client.post(
        "/training-plans",
        json={
            "race_type": "half_marathon",
            "race_date": "2026-09-20",
            "experience_level": "beginner",
            "days_per_week": 8,
        },
    )

    assert response.status_code == 422
