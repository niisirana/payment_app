from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import PaymentRead, WebhookPayload
from app.services.payment_service import process_payment_webhook

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/webhook", response_model=PaymentRead)
async def payment_webhook(data: WebhookPayload, db: AsyncSession = Depends(get_db)):
    return await process_payment_webhook(data, db)
