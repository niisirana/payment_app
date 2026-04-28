from sqlalchemy import select
from fastapi import HTTPException, status
from decimal import Decimal

from app.core.security import verify_payment_signature
from app.core.config import settings
from app.models import Payment, User, Account


async def process_payment_webhook(data, db):
    if not verify_payment_signature(data.model_dump(), settings.PAYMENT_SECRET_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature"
        )

    result = await db.execute(
        select(Payment).where(Payment.transaction_id == data.transaction_id)
    )
    existing_payment = result.scalar_one_or_none()

    if existing_payment is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Transaction already processed"
        )

    result = await db.execute(select(User).where(User.id == data.user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    result = await db.execute(
        select(Account).where(
            Account.id == data.account_id, Account.user_id == data.user_id
        )
    )
    account = result.scalar_one_or_none()
    if account is None:
        account = Account(
            id=data.account_id,
            user_id=data.user_id,
            balance=Decimal("0.00"),
        )
        db.add(account)

    account.balance += data.amount

    payment = Payment(
        transaction_id=data.transaction_id,
        account_id=account.id,
        amount=data.amount,
    )

    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    return payment
