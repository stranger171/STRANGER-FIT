from pydantic import BaseModel


class UserProfile(BaseModel):
    name: str
    age: int
    height_cm: float
    weight_kg: float
    fitness_goal: str
    experience_level: str