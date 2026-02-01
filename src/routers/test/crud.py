from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.models import User, User_info
from src.models.schemas import UserCreate, Add_user_info
from src.database import get_db

routers = APIRouter(prefix="/test", tags=["Test"], responses={404: {"description": "Not found"}})

@routers.post("/post")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(f=user.f, l=user.l)
    # Check if user with same f and l already exists
    existing_user = await db.execute(
        (User.__table__.select()).where(User.f == user.f, User.l == user.l)
    )
    existing_user = existing_user.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with same first and last name already exists")
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@routers.post("/info")
async def add_user_info(u:Add_user_info, db: AsyncSession = Depends(get_db)):
    user_info = User_info(fn=u.f, em=u.e, ph=u.p, pw=u.pw)
    db.add(user_info)
    await db.commit()
    await db.refresh(user_info)
    return user_info

@routers.get("/health")
async def health_check():
    return {"status": "ok"}

@routers.get("/xxxxx")
async def health_check():
    return {"status": "ok"}
