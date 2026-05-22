from repositories.training_plan_repository import TrainingPlanRepository
from schemas.training_plan import TrainingPlanCreate, TrainingPlanResponse


def create_training_plan(
    request: TrainingPlanCreate,
    repository: TrainingPlanRepository,
) -> TrainingPlanResponse:
    training_plan = TrainingPlanResponse(
        id=repository.next_id(),
        race_type=request.race_type,
        race_date=request.race_date,
        experience_level=request.experience_level,
        days_per_week=request.days_per_week,
        status="draft",
    )

    return repository.save(training_plan)


def get_training_plan(
    plan_id: str,
    repository: TrainingPlanRepository,
) -> TrainingPlanResponse | None:
    return repository.get_by_id(plan_id)
