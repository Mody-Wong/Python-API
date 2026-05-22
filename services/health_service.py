from schemas.health import HealthResponse


def get_health_status() -> HealthResponse:
    return HealthResponse(status="ok", message="API is healthy")


def get_database_health_status() -> HealthResponse:
    from repositories.training_plan_repository import check_dynamodb_connection

    check_dynamodb_connection()
    return HealthResponse(status="ok", message="DynamoDB connection is healthy")
