from datetime import date

from schemas.training_plan import ExperienceLevel, RaceType, TrainingPlanCreate
from services.training_plan_service import create_training_plan


def test_create_training_plan_returns_draft_plan():
    request = TrainingPlanCreate(
        race_type=RaceType.half_marathon,
        race_date=date(2026, 9, 20),
        experience_level=ExperienceLevel.beginner,
        days_per_week=4,
    )

    response = create_training_plan(request)

    assert response.id == 1
    assert response.race_type == RaceType.half_marathon
    assert response.race_date == date(2026, 9, 20)
    assert response.experience_level == ExperienceLevel.beginner
    assert response.days_per_week == 4
    assert response.status == "draft"
