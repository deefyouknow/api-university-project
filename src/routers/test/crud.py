from fastapi import APIRouter, Depends, HTTPException, status
from src.models.models import User
from src.models.schemas import UserCreate
from src.database import get_db
from sqlalchemy.orm import Session

routers = APIRouter(prefix="/test", tags=["Test"], responses={404: {"description": "Not found"}})

@routers.post("/post")
def create_user(user: UserCreate, db:Session=Depends(get_db)):
    db_user = User(f=user.f, l=user.l)

    # Check if user with same f and l already exists
    existing_user = db.query(User).filter(User.f == user.f, User.l == user.l).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with same first and last name already exists")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
