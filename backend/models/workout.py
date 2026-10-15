from datetime import date
from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")

    workout_date: date

    exercise_name: str
    muscle_group: str

    sets: int
    reps: int
    weight_kg: float

    rpe: Optional[float] = None

    # Individual set data
    sets_data: Optional[list[dict]] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True)
    )