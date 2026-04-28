from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.admins import router as admins_router
from app.api.v1.payments import router as payments_router


app = FastAPI()

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(admins_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
