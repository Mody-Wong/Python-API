from fastapi import APIRouter, Depends, HTTPException, status

from repositories.training_plan_repository import (
    TrainingPlanRepository,
    get_training_plan_repository,
)
from schemas.training_plan import TrainingPlanCreate, TrainingPlanResponse
from services.training_plan_service import create_training_plan, get_training_plan

router = APIRouter(prefix="/training-plans", tags=["training-plans"])


@router.post(
    "",
    response_model=TrainingPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plan(
    request: TrainingPlanCreate,
    repository: TrainingPlanRepository = Depends(get_training_plan_repository),
):
    return create_training_plan(request, repository)


@router.get(
    "/{plan_id}",
    response_model=TrainingPlanResponse,
    responses={404: {"description": "Training plan not found"}},
)
def get_plan(
    plan_id: str,
    repository: TrainingPlanRepository = Depends(get_training_plan_repository),
):
    training_plan = get_training_plan(plan_id, repository)
    if training_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training plan not found",
        )

    return training_plan
