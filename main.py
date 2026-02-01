from fastapi import FastAPI, APIRouter, Depends

import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DB_URL")


app = FastAPI(title="ProjectOne2025", description="API for ProjectOne2025", version="1.0.0", 
    contact={"name": "deef", "email": "thanawat.deef@gmail.com"},
    docs_url=None,
    redoc_url=None,
    # openapi_url=None # <--- ปิด JSON default ด้วย
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
@router.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(username: str = Depends(secure.verify)): 
    return get_openapi(
        title="ProjectOne2025",
        version="1.0.0",
        description="API for ProjectOne2025",
        routes=app.routes,
        #test
    )

# ======================================
# all import router
# ======================================

from src.routers.test import crud
app.include_router(crud.routers)

from src.routers.ui import credentail
app.include_router(credentail.router)
