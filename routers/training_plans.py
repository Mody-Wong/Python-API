from fastapi import APIRouter, status

from schemas.training_plan import TrainingPlanCreate, TrainingPlanResponse
from services.training_plan_service import create_training_plan

router = APIRouter(prefix="/training-plans", tags=["training-plans"])


@router.post(
    "",
    response_model=TrainingPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plan(request: TrainingPlanCreate):
    return create_training_plan(request)
