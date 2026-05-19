from fastapi import APIRouter

from schemas.health import HealthResponse
from services.health_service import get_database_health_status, get_health_status

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health_check():
    return get_health_status()


@router.get("/db", response_model=HealthResponse)
def database_health_check():
    return get_database_health_status()
