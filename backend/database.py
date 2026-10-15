import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine
from models.user import User
from models.workout import Workout


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")


engine = create_engine(
    DATABASE_URL,
    echo=True
)
def get_session():
    with Session(engine) as session:
        yield session


SQLModel.metadata.create_all(engine)