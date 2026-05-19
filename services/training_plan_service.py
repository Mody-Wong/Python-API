from schemas.training_plan import TrainingPlanCreate, TrainingPlanResponse


def create_training_plan(request: TrainingPlanCreate) -> TrainingPlanResponse:
    return TrainingPlanResponse(
        id=1,
        race_type=request.race_type,
        race_date=request.race_date,
        experience_level=request.experience_level,
        days_per_week=request.days_per_week,
        status="draft",
    )
