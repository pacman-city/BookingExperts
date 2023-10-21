from fastapi import Depends, Request
from jose import jwt

from app.config import settings
from app.exceptions import TokenException
from app.user.models import User
from app.user.service import UsersService


def get_token_pyload(request: Request) -> dict:
    """Read JWT token from cookies and returns token payload"""
    token = request.cookies.get("Bearer")
    if not token:
        raise TokenException(detail="Токен отсутствует")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise TokenException(detail="Срок действия токена истек")
    except jwt.JWTError:
        raise TokenException

    return payload


async def get_current_user(jwt_payload=Depends(get_token_pyload)) -> User:
    """Return current user or raise error"""
    user_id: str = jwt_payload.get("sub")
    if not user_id:
        raise TokenException

    user = await UsersService.find_one_or_none(id=int(user_id))
    if not user:
        raise TokenException

    return user


async def verify_jwt(request: Request) -> bool:
    """Check if JWT is present and valid"""
    try:
        get_token_pyload(request)
    except TokenException:
        return False
    return True
