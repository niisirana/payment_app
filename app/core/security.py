from passlib.context import CryptContext
import hashlib
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.JWT_SECRET, settings.ALGORITHM)
    except JWTError:
        return None


def generate_signature(data: dict, secret_key: str) -> str:
    sorted_keys = sorted([k for k in data.keys() if k != "signature"])
    values_str = "".join(str(data[k]) for k in sorted_keys)
    return hashlib.sha256((values_str + secret_key).encode()).hexdigest()


def verify_payment_signature(data: dict, secret_key: str) -> bool:
    return generate_signature(data, secret_key) == data.get("signature")
