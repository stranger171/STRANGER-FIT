from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database import get_session
from models.user import User
from schemas.user import UserProfile

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()

    return {
        "users": users
    }


@router.post("/")
def create_user(
    user: UserProfile,
    session: Session = Depends(get_session)
):
    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return {
        "message": "User created successfully",
        "user": db_user
    }