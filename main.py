from fastapi import FastAPI, APIRouter

import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DB_URL")

app = FastAPI(title="ProjectOne2025", description="API for ProjectOne2025", version="1.0.0", 
    contact={"name": "deef", "email": "thanawat.deef@gmail.com"},
    docs_url=None,
    redoc_url=None
)

router = APIRouter()


from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือระบุเฉพาะ React URL
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------------------
# from src.routers.test.crud import create_user

# router.include_router(create_user.router)
from src.secure import secure
app.include_router(secure.router)


# ======================================
# all import router
# ======================================

from src.routers.test import crud
app.include_router(crud.routers)

@app.get("/test")
def test2():
    return {"message": "Hello World"}
