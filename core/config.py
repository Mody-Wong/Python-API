from functools import lru_cache
from os import getenv

from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = (
        "postgresql+psycopg://running_user:running_password"
        "@localhost:5432/running_plan_db"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_url=getenv("DATABASE_URL", Settings().database_url),
    )
