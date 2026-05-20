from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class RaceType(str, Enum):
    five_k = "5k"
    ten_k = "10k"
    half_marathon = "half_marathon"
    marathon = "marathon"


class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class TrainingPlanCreate(BaseModel):
    race_type: RaceType
    race_date: date
    experience_level: ExperienceLevel
    days_per_week: int = Field(ge=1, le=7)


class TrainingPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    race_type: RaceType
    race_date: date
    experience_level: ExperienceLevel
    days_per_week: int
    status: str
