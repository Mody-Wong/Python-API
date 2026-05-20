from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.base import Base
from models.training_plan import TrainingPlan
from schemas.training_plan import ExperienceLevel, RaceType, TrainingPlanCreate
from services.training_plan_service import create_training_plan, get_training_plan


@pytest.fixture
def db_session():
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

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_training_plan_returns_draft_plan(db_session):
    request = TrainingPlanCreate(
        race_type=RaceType.half_marathon,
        race_date=date(2026, 9, 20),
        experience_level=ExperienceLevel.beginner,
        days_per_week=4,
    )

    response = create_training_plan(request, db_session)

    assert response.id == 1
    assert response.race_type == RaceType.half_marathon
    assert response.race_date == date(2026, 9, 20)
    assert response.experience_level == ExperienceLevel.beginner
    assert response.days_per_week == 4
    assert response.status == "draft"


def test_get_training_plan_returns_existing_plan(db_session):
    training_plan = TrainingPlan(
        race_type="half_marathon",
        race_date=date(2026, 9, 20),
        experience_level="beginner",
        days_per_week=4,
        status="draft",
    )
    db_session.add(training_plan)
    db_session.commit()
    db_session.refresh(training_plan)

    response = get_training_plan(training_plan.id, db_session)

    assert response is not None
    assert response.id == training_plan.id
    assert response.race_type == RaceType.half_marathon
    assert response.status == "draft"


def test_get_training_plan_returns_none_when_missing(db_session):
    response = get_training_plan(999, db_session)

    assert response is None
