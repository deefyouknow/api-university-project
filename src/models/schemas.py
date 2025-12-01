from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    f: str
    l: str

class Add_user_info(BaseModel):
    f: str = Field(..., min_length=3, max_length=100, example="John")
    # l: str = Field(..., min_length=3, max_length=100, example="Doe") ไม่ใช้
    e: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", example="john@example.com")
    #name>@>name>.>name
    p: int = Field(..., ge=12345678, le=9999999999, example="0891234567")
    pw: str = Field(..., min_length=8, max_length=100, example="password")

# min_length=3 → ต้องมีอย่างน้อย 3 ตัวอักษร
# max_length=100 → ไม่เกิน 100 ตัวอักษร
# ... → บังคับว่าต้องส่งค่า (ไม่เป็น None)

# Schema สำหรับรับ Token จากหน้าบ้าน
class GoogleAuthRequest(BaseModel):
    token: str

# Schema สำหรับส่งข้อมูล User กลับไปให้หน้าบ้าน
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None
    class Config:
        from_attributes = True
