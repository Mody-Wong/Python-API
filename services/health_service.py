from schemas.health import HealthResponse


def get_health_status() -> HealthResponse:
    return HealthResponse(status="ok", message="API is healthy")


def get_database_health_status() -> HealthResponse:
    from database.session import check_database_connection

    check_database_connection()
    return HealthResponse(status="ok", message="Database connection is healthy")
