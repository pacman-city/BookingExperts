from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions import IncorrectCredentialsException
from app.user.service import UsersService
from app.user.models import User

encrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return encrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return encrypt.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> User:
    user = await UsersService.find_one_or_none(email=email)
    if not (user and verify_password(password, user.password)):
        raise IncorrectCredentialsException
    return user
