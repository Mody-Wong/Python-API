from typing import Protocol
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError

from core.config import get_settings
from schemas.training_plan import TrainingPlanResponse


class TrainingPlanRepository(Protocol):
    def next_id(self) -> str:
        pass

    def save(self, training_plan: TrainingPlanResponse) -> TrainingPlanResponse:
        pass

    def get_by_id(self, plan_id: str) -> TrainingPlanResponse | None:
        pass


class DynamoDBTrainingPlanRepository:
    def __init__(self) -> None:
        settings = get_settings()
        resource_kwargs = {"region_name": settings.aws_region}
        if settings.dynamodb_endpoint_url is not None:
            resource_kwargs["endpoint_url"] = settings.dynamodb_endpoint_url

        dynamodb = boto3.resource("dynamodb", **resource_kwargs)
        self.table = dynamodb.Table(settings.training_plans_table_name)

    def next_id(self) -> str:
        return str(uuid4())

    def save(self, training_plan: TrainingPlanResponse) -> TrainingPlanResponse:
        self.table.put_item(Item=training_plan.model_dump(mode="json"))
        return training_plan

    def get_by_id(self, plan_id: str) -> TrainingPlanResponse | None:
        response = self.table.get_item(Key={"id": plan_id})
        item = response.get("Item")
        if item is None:
            return None

        return TrainingPlanResponse.model_validate(item)

    def check_connection(self) -> bool:
        self.table.load()
        return True


def get_training_plan_repository() -> TrainingPlanRepository:
    return DynamoDBTrainingPlanRepository()


def check_dynamodb_connection() -> bool:
    try:
        return DynamoDBTrainingPlanRepository().check_connection()
    except ClientError:
        raise
