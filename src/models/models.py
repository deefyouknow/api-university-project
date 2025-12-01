# ตาราง ข้อมูลต้องมี Primary Key 1 ตัว
from sqlalchemy import Column, Integer, String, desc, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSON

# =========================================
from src.database import Base, engine
# =========================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    f = Column(String(100), nullable=False)
    l = Column(String(100), nullable=False)

class User_info(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fn = Column(String(100), nullable=False, comment="ชื่อเต็ม")
    # ln = Column(String(100), nullable=False, comment="นามสกุล") ไม่ใช้แล้ว
    em = Column(String(100), nullable=True, comment="อีเมล")
    ph = Column(Integer, nullable=True, comment="เบอร์โทรศัพท์")
    pw = Column(String(100), nullable=False, comment="รหัสผ่าน")

# ===========================
# google AUTH 2.0
# ===========================
class User(Base):
    __tablename__ = "google_credentials"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # เก็บ Google ID (sub) แยกไว้เพื่อความชัวร์ในการ Query
    google_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    picture = Column(String)
    # *** พระเอกของคุณ: เก็บทุกอย่างที่ Google ส่งมาเป็นก้อน JSON ***
    google_raw_data = Column(JSON) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Base.metadata.create_all(bind=engine)
