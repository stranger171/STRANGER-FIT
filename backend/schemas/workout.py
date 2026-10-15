from datetime import date
from pydantic import BaseModel


class WorkoutSet(BaseModel):
    set_number: int
    reps: int
    weight_kg: float
    rpe: float | None = None


class WorkoutCreate(BaseModel):
    user_id: int
    workout_date: date
    exercise_name: str
    muscle_group: str

    sets: int
    reps: int
    weight_kg: float
    rpe: float | None = None

    sets_data: list[WorkoutSet] | None = None


class WorkoutUpdate(BaseModel):
    workout_date: date
    exercise_name: str
    muscle_group: str

    sets: int
    reps: int
    weight_kg: float
    rpe: float | None = None

    sets_data: list[WorkoutSet] | None = None