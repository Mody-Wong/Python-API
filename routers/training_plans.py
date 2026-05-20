from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.session import get_db
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
    db: Session = Depends(get_db),
):
    return create_training_plan(request, db)


@router.get(
    "/{plan_id}",
    response_model=TrainingPlanResponse,
    responses={404: {"description": "Training plan not found"}},
)
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
):
    training_plan = get_training_plan(plan_id, db)
    if training_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training plan not found",
        )

    return training_plan
