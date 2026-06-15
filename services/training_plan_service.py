from dataclasses import dataclass

from schemas.training_plan import TrainingPlanCreate, TrainingPlanResponse


@dataclass
class StoredTrainingPlan:
    owner_sub: str
    plan: TrainingPlanResponse


_training_plans: dict[int, StoredTrainingPlan] = {}
_next_training_plan_id = 1


def create_training_plan(
    request: TrainingPlanCreate,
    owner_sub: str,
) -> TrainingPlanResponse:
    global _next_training_plan_id

    training_plan = TrainingPlanResponse(
        id=_next_training_plan_id,
        race_type=request.race_type,
        race_date=request.race_date,
        experience_level=request.experience_level,
        days_per_week=request.days_per_week,
        status="draft",
    )

    _training_plans[training_plan.id] = StoredTrainingPlan(
        owner_sub=owner_sub,
        plan=training_plan,
    )
    _next_training_plan_id += 1

    return training_plan


def get_training_plan(
    plan_id: int,
    owner_sub: str,
) -> TrainingPlanResponse | None:
    stored_training_plan = _training_plans.get(plan_id)
    if stored_training_plan is None:
        return None

    if stored_training_plan.owner_sub != owner_sub:
        return None

    return stored_training_plan.plan


def reset_training_plans() -> None:
    global _next_training_plan_id

    _training_plans.clear()
    _next_training_plan_id = 1
