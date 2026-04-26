from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User, Admin
from app.schemas import LoginRequest, TokenRead
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/user/login", response_model=TokenRead)
async def user_login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": str(user.id), "role": "user"})

    return TokenRead(access_token=token)


@router.post("/admin/login", response_model=TokenRead)
async def admin_login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin).where(Admin.email == data.email))
    admin = result.scalar_one_or_none()

    if admin is None or not verify_password(data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": str(admin.id), "role": "admin"})

    return TokenRead(access_token=token)
