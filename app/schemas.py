from pydantic import BaseModel, EmailStr, Field, field_validator
from decimal import Decimal
from typing import List


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class AdminRead(UserRead):
    pass


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccountBase(BaseModel):
    user_id: int
    balance: Decimal = Decimal("0.0")


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    transaction_id: str
    account_id: int
    amount: Decimal

    class Config:
        from_attributes = True


class PaymentRead(PaymentBase):
    id: int


class WebhookPayload(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: Decimal = Field(max_digits=15, decimal_places=2)
    signature: str

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Decimal):
        if v <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        return v
