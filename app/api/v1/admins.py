from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_admin
from app.schemas import (
    AdminRead,
    UserWithAccountsRead,
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.models import Admin, User
from app.database import get_db
from app.core.security import get_password_hash

router = APIRouter(prefix="/admins", tags=["admins"])


@router.get("/me", response_model=AdminRead)
async def read_admin(current_admin: Admin = Depends(get_current_admin)):
    return current_admin


@router.get("/users", response_model=list[UserWithAccountsRead])
async def read_users(
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).options(selectinload(User.accounts)))
    users = result.scalars().all()

    return users


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    existing_user_result = await db.execute(
        select(User).where(User.email == data.email)
    )
    existing_user = existing_user_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    hashed_password = get_password_hash(data.password)

    user = User(
        email=data.email, full_name=data.full_name, hashed_password=hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        user.hashed_password = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}", response_model=UserRead)
async def delete_user(
    user_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await db.delete(user)
    await db.commit()

    return user
