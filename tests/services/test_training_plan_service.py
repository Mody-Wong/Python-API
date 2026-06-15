from datetime import date

import pytest

from schemas.training_plan import ExperienceLevel, RaceType, TrainingPlanCreate
from services.training_plan_service import (
    create_training_plan,
    get_training_plan,
    list_training_plans,
    reset_training_plans,
)


@pytest.fixture
def training_plan_store():
    reset_training_plans()
    yield
    reset_training_plans()


def test_create_training_plan_returns_draft_plan(training_plan_store):
    request = TrainingPlanCreate(
        race_type=RaceType.half_marathon,
        race_date=date(2026, 9, 20),
        experience_level=ExperienceLevel.beginner,
        days_per_week=4,
    )

    response = create_training_plan(request, owner_sub="auth0|test-user")

    assert response.id == 1
    assert response.race_type == RaceType.half_marathon
    assert response.race_date == date(2026, 9, 20)
    assert response.experience_level == ExperienceLevel.beginner
    assert response.days_per_week == 4
    assert response.status == "draft"


def test_get_training_plan_returns_existing_plan(training_plan_store):
    request = TrainingPlanCreate(
        race_type=RaceType.half_marathon,
        race_date=date(2026, 9, 20),
        experience_level=ExperienceLevel.beginner,
        days_per_week=4,
    )
    training_plan = create_training_plan(request, owner_sub="auth0|test-user")

    response = get_training_plan(training_plan.id, owner_sub="auth0|test-user")

    assert response is not None
    assert response.id == training_plan.id
    assert response.race_type == RaceType.half_marathon
    assert response.status == "draft"


def test_get_training_plan_returns_none_when_missing(training_plan_store):
    response = get_training_plan(999, owner_sub="auth0|test-user")

    assert response is None


def test_get_training_plan_returns_none_for_different_owner(training_plan_store):
    request = TrainingPlanCreate(
        race_type=RaceType.half_marathon,
        race_date=date(2026, 9, 20),
        experience_level=ExperienceLevel.beginner,
        days_per_week=4,
    )
    training_plan = create_training_plan(request, owner_sub="auth0|owner")

    response = get_training_plan(training_plan.id, owner_sub="auth0|other-user")

    assert response is None


def test_list_training_plans_returns_only_owner_plans(training_plan_store):
    request = TrainingPlanCreate(
        race_type=RaceType.half_marathon,
        race_date=date(2026, 9, 20),
        experience_level=ExperienceLevel.beginner,
        days_per_week=4,
    )
    owner_plan = create_training_plan(request, owner_sub="auth0|owner")
    create_training_plan(request, owner_sub="auth0|other-user")

    response = list_training_plans(owner_sub="auth0|owner")

    assert [plan.id for plan in response] == [owner_plan.id]
