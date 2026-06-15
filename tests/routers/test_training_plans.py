import pytest
from fastapi.testclient import TestClient

from core.auth import require_auth
from main import app
from services.training_plan_service import reset_training_plans


@pytest.fixture
def client():
    reset_training_plans()
    app.dependency_overrides[require_auth] = lambda: {"sub": "auth0|test-user"}

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    reset_training_plans()


def test_create_training_plan(client):
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
    response_body = response.json()

    assert response_body["id"] == 1
    assert response_body["race_type"] == "half_marathon"
    assert response_body["race_date"] == "2026-09-20"
    assert response_body["experience_level"] == "beginner"
    assert response_body["days_per_week"] == 4
    assert response_body["status"] == "draft"


def test_create_training_plan_accepts_status(client):
    response = client.post(
        "/training-plans",
        json={
            "race_type": "half_marathon",
            "race_date": "2026-09-20",
            "experience_level": "beginner",
            "days_per_week": 4,
            "status": "active",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "active"


def test_get_training_plan(client):
    create_response = client.post(
        "/training-plans",
        json={
            "race_type": "half_marathon",
            "race_date": "2026-09-20",
            "experience_level": "beginner",
            "days_per_week": 4,
        },
    )
    plan_id = create_response.json()["id"]

    response = client.get(f"/training-plans/{plan_id}")

    assert response.status_code == 200
    assert response.json()["id"] == plan_id
    assert response.json()["status"] == "draft"


def test_list_training_plans(client):
    first_response = client.post(
        "/training-plans",
        json={
            "race_type": "half_marathon",
            "race_date": "2026-09-20",
            "experience_level": "beginner",
            "days_per_week": 4,
        },
    )
    second_response = client.post(
        "/training-plans",
        json={
            "race_type": "10k",
            "race_date": "2026-07-05",
            "experience_level": "intermediate",
            "days_per_week": 3,
        },
    )

    response = client.get("/training-plans")

    assert response.status_code == 200
    assert [plan["id"] for plan in response.json()] == [
        first_response.json()["id"],
        second_response.json()["id"],
    ]


def test_list_training_plans_requires_authorization_token():
    reset_training_plans()
    app.dependency_overrides.clear()

    try:
        with TestClient(app) as test_client:
            response = test_client.get("/training-plans")
    finally:
        reset_training_plans()

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing authorization token"}


def test_get_training_plan_returns_404_when_not_found(client):
    response = client.get("/training-plans/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Training plan not found"}


def test_get_training_plan_returns_404_for_different_owner(client):
    create_response = client.post(
        "/training-plans",
        json={
            "race_type": "half_marathon",
            "race_date": "2026-09-20",
            "experience_level": "beginner",
            "days_per_week": 4,
        },
    )
    plan_id = create_response.json()["id"]
    app.dependency_overrides[require_auth] = lambda: {"sub": "auth0|other-user"}

    response = client.get(f"/training-plans/{plan_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Training plan not found"}


def test_create_training_plan_requires_authorization_token():
    reset_training_plans()
    app.dependency_overrides.clear()

    try:
        with TestClient(app) as test_client:
            response = test_client.post(
                "/training-plans",
                json={
                    "race_type": "half_marathon",
                    "race_date": "2026-09-20",
                    "experience_level": "beginner",
                    "days_per_week": 4,
                },
            )
    finally:
        reset_training_plans()

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing authorization token"}


def test_create_training_plan_rejects_invalid_days_per_week(client):
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
