import pytest
from fastapi.testclient import TestClient

from main import app
from repositories.training_plan_repository import get_training_plan_repository


class FakeTrainingPlanRepository:
    def __init__(self) -> None:
        self.training_plans = {}
        self.next_id_value = 1

    def next_id(self):
        plan_id = str(self.next_id_value)
        self.next_id_value += 1
        return plan_id

    def save(self, training_plan):
        self.training_plans[training_plan.id] = training_plan
        return training_plan

    def get_by_id(self, plan_id):
        return self.training_plans.get(plan_id)


@pytest.fixture
def client():
    repository = FakeTrainingPlanRepository()

    def override_get_training_plan_repository():
        return repository

    app.dependency_overrides[get_training_plan_repository] = (
        override_get_training_plan_repository
    )
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


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

    assert response_body["id"] == "1"
    assert response_body["race_type"] == "half_marathon"
    assert response_body["race_date"] == "2026-09-20"
    assert response_body["experience_level"] == "beginner"
    assert response_body["days_per_week"] == 4
    assert response_body["status"] == "draft"


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


def test_get_training_plan_returns_404_when_not_found(client):
    response = client.get("/training-plans/missing-plan-id")

    assert response.status_code == 404
    assert response.json() == {"detail": "Training plan not found"}


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
