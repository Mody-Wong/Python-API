from functools import lru_cache
from os import getenv

from pydantic import BaseModel


class Settings(BaseModel):
    aws_region: str = "eu-west-2"
    dynamodb_endpoint_url: str | None = None
    training_plans_table_name: str = "training-plans"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        aws_region=getenv("AWS_REGION", Settings().aws_region),
        dynamodb_endpoint_url=getenv("DYNAMODB_ENDPOINT_URL"),
        training_plans_table_name=getenv(
            "TRAINING_PLANS_TABLE_NAME",
            Settings().training_plans_table_name,
        ),
    )
