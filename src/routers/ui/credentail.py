from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select # พระเอกของ Async ORM
from src.database import get_db
from src.models import models, schemas
try:
    from google.oauth2 import id_token
    from google.auth.transport import requests
except ImportError:
    print("Please install google-auth and google-auth-oauthlib.  pip install google-auth google-auth-oauthlib")
import asyncio # ใช้สำหรับแก้ Blocking ของ Google Verify
from dotenv import load_dotenv
import os
load_dotenv()
router = APIRouter(prefix="/auth", tags=["Authentication"])
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID_X")

@router.post("/google", response_model=schemas.UserResponse)
async def google_login(
    payload: schemas.GoogleAuthRequest, 
    db: AsyncSession = Depends(get_db) # ใช้ AsyncSession ของ SQLAlchemy
):
    try:
        # 1. แก้ Blocking I/O: ย้ายงานตรวจสอบ Token ไปทำใน Thread แยก
        loop = asyncio.get_running_loop()
        # verify_oauth2_token เป็น sync function จึงต้องหุ้มด้วย run_in_executor
        idinfo = await loop.run_in_executor(None, lambda: id_token.verify_oauth2_token(
            payload.token, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        ))

        # ข้อมูลจาก Google
        google_sub = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name')
        picture = idinfo.get('picture')

        # 2. Database Query แบบ Async ORM (สะอาดกว่า Raw SQL)
        # แทนที่จะเขียน "SELECT * FROM...", เราใช้ Python Object แทน
        stmt = select(models.User).where(models.User.google_id == google_sub)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            # --- Create (Async) ---
            user = models.User(
                email=email,
                google_id=google_sub,
                name=name,
                picture=picture,
                google_raw_data=idinfo # ถ้า column เป็น JSON/Dict ก็ใส่ได้เลย
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            # --- Update (Async) ---
            user.name = name
            user.picture = picture
            user.google_raw_data = idinfo

            await db.commit()
            await db.refresh(user)

        return user

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google Token")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
