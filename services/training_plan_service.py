from sqlalchemy.orm import Session

from models.training_plan import TrainingPlan
from schemas.training_plan import TrainingPlanCreate, TrainingPlanResponse


def create_training_plan(
    request: TrainingPlanCreate,
    db: Session,
) -> TrainingPlanResponse:
    training_plan = TrainingPlan(
        race_type=request.race_type.value,
        race_date=request.race_date,
        experience_level=request.experience_level.value,
        days_per_week=request.days_per_week,
        status="draft",
    )
    db.add(training_plan)
    db.commit()
    db.refresh(training_plan)

    return TrainingPlanResponse.model_validate(training_plan)


def get_training_plan(
    plan_id: int,
    db: Session,
) -> TrainingPlanResponse | None:
    training_plan = db.get(TrainingPlan, plan_id)
    if training_plan is None:
        return None

    return TrainingPlanResponse.model_validate(training_plan)
