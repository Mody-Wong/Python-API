from fastapi import APIRouter

from schemas.health import HealthResponse
from services.health_service import get_health_status

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health_check():
    return get_health_status()
