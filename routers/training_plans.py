from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import require_auth
from schemas.training_plan import TrainingPlanCreate, TrainingPlanResponse
from services.training_plan_service import (
    create_training_plan,
    delete_training_plan,
    get_training_plan,
    list_training_plans,
)

router = APIRouter(prefix="/training-plans", tags=["training-plans"])


@router.post(
    "",
    response_model=TrainingPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plan(
    request: TrainingPlanCreate,
    user: dict = Depends(require_auth),
):
    return create_training_plan(request, owner_sub=user["sub"])


@router.get("", response_model=list[TrainingPlanResponse])
def list_plans(
    user: dict = Depends(require_auth),
):
    return list_training_plans(owner_sub=user["sub"])


@router.get(
    "/{plan_id}",
    response_model=TrainingPlanResponse,
    responses={404: {"description": "Training plan not found"}},
)
def get_plan(
    plan_id: int,
    user: dict = Depends(require_auth),
):
    training_plan = get_training_plan(plan_id, owner_sub=user["sub"])
    if training_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training plan not found",
        )

    return training_plan


@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Training plan not found"}},
)
def delete_plan(
    plan_id: int,
    user: dict = Depends(require_auth),
):
    was_deleted = delete_training_plan(plan_id, owner_sub=user["sub"])
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training plan not found",
        )
