# Bawe
# ตาราง ข้อมูลต้องมี Primary Key 1 ตัว
from sqlalchemy import Column, Integer, String, desc, DateTime, func

# =========================================
from sqlalchemy.orm import declarative_base
Base = declarative_base()
# =========================================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    f = Column(String(100), nullable=False)
    l = Column(String(100), nullable=False)
