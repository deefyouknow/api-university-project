# ---------------------------------------------------------------------
# หนัาล็อกอิน /docs and /redocs
from fastapi import FastAPI, APIRouter , Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi

security = HTTPBasic()
router = APIRouter(tags=["Login"])

from dotenv import load_dotenv
import os
load_dotenv()
import secrets

async def verify(credentials: HTTPBasicCredentials = Depends(security)):
    username = os.getenv("docsredoc_user")
    password = os.getenv("docsredoc_pass")
    username_correct = secrets.compare_digest(credentials.username, username)
    password_correct = secrets.compare_digest(credentials.password, password)

    if not (username_correct and password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

@router.get("/", dependencies=[Depends(verify)])
async def root():
    return {"msg": "secured"}

# ✅ ป้องกันหน้า docs และ redoc
@router.get("/docs", include_in_schema=False)
async def get_docs_auth(ok: bool = Depends(verify)):
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Secure Docs")

@router.get("/redoc", include_in_schema=False)
async def get_redoc_auth(ok: bool = Depends(verify)):
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(openapi_url="/openapi.json", title="Secure Redoc")

# สร้าง Endpoint openapi.json เองแล้วใส่ verify
# @router.get("/openapi.json", include_in_schema=False)
# async def get_open_api_endpoint(username: str = Depends(verify)): # เรียกใช้ verify จาก secure router
#     from fastapi.openapi.utils import get_openapi
#     from fastapi import FastAPI
#     app = FastAPI() # Initializing FastAPI here since app wasn't defined in this scope.  Consider where app is normally defined and how best to access it here.
#     return get_openapi(
#         title="ProjectOne2025",
#         version="1.0.0",
#         description="API for ProjectOne2025",
#         routes=app.routes,
#     )
