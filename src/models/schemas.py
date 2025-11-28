from pydantic import BaseModel

class UserCreate(BaseModel):
    f: str
    l: str
