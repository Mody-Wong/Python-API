import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.base import Base
from database.session import get_db
from main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
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

    assert response_body["id"] == 1
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
    response = client.get("/training-plans/999")

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
