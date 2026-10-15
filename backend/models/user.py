from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    age: int
    height_cm: float
    weight_kg: float
    fitness_goal: str
    experience_level: str