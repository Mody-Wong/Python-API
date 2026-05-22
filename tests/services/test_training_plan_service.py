from datetime import date

from schemas.training_plan import ExperienceLevel, RaceType, TrainingPlanCreate
from services.training_plan_service import create_training_plan, get_training_plan


class FakeTrainingPlanRepository:
    def __init__(self) -> None:
        self.training_plans = {}
        self.next_id_value = "plan-1"

    def next_id(self):
        return self.next_id_value

    def save(self, training_plan):
        self.training_plans[training_plan.id] = training_plan
        return training_plan

    def get_by_id(self, plan_id):
        return self.training_plans.get(plan_id)


def test_create_training_plan_returns_draft_plan():
    repository = FakeTrainingPlanRepository()
    request = TrainingPlanCreate(
        race_type=RaceType.half_marathon,
        race_date=date(2026, 9, 20),
        experience_level=ExperienceLevel.beginner,
        days_per_week=4,
    )

    response = create_training_plan(request, repository)

    assert response.id == "plan-1"
    assert response.race_type == RaceType.half_marathon
    assert response.race_date == date(2026, 9, 20)
    assert response.experience_level == ExperienceLevel.beginner
    assert response.days_per_week == 4
    assert response.status == "draft"


def test_get_training_plan_returns_existing_plan():
    repository = FakeTrainingPlanRepository()
    created_plan = create_training_plan(
        TrainingPlanCreate(
            race_type=RaceType.half_marathon,
            race_date=date(2026, 9, 20),
            experience_level=ExperienceLevel.beginner,
            days_per_week=4,
        ),
        repository,
    )

    response = get_training_plan(created_plan.id, repository)

    assert response is not None
    assert response.id == created_plan.id
    assert response.race_type == RaceType.half_marathon
    assert response.status == "draft"


def test_get_training_plan_returns_none_when_missing():
    repository = FakeTrainingPlanRepository()

    response = get_training_plan("missing-plan-id", repository)

    assert response is None
