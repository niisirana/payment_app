from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class AdminRead(UserRead):
    pass


class AccountBase(BaseModel):
    user_id: int
    balance: Decimal = Decimal("0.00")


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int

    class Config:
        from_attributes = True


class UserWithAccountsRead(UserRead):
    accounts: list[AccountRead] = []

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    transaction_id: str
    account_id: int
    amount: Decimal


class PaymentRead(PaymentBase):
    id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"


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
            raise ValueError("Amount must be greater than zero")
        return v
