from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    auth0_domain: str = ""
    auth0_audience: str = ""
    auth0_authority: str = ""
    auth0_algorithms: str = "RS256"

@lru_cache
def get_settings() -> Settings:
    return Settings(
        auth0_domain=getenv("AUTH0_DOMAIN", ""),
        auth0_audience=getenv("AUTH0_AUDIENCE", ""),
        auth0_authority=getenv("AUTH0_AUTHORITY", ""),
        auth0_algorithms=getenv("AUTH0_ALGORITHMS", "RS256"),
    )

