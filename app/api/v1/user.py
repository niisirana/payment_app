from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user
from app.schemas import UserRead, AccountRead, PaymentRead
from app.models import User, Account, Payment
from app.database import get_db

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserRead)
async def read_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/accounts", response_model=list[AccountRead])
async def read_user_accounts(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Account).where(Account.user_id == current_user.id))
    accounts = result.scalars().all()

    return accounts


@router.get("/me/payments", response_model=list[PaymentRead])
async def read_user_payments(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Payment).join(Account).where(Account.user_id == current_user.id)
    )
    payments = result.scalars().all()

    return payments
