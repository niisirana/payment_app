from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.user import router as user_router
from app.api.v1.admin import router as admin_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
