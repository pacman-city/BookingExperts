from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError

from app.exceptions import UserExistsException
from app.user.auth import authenticate_user, create_token, hash_password
from app.user.dependencies import get_current_user
from app.user.schemas import LoginBody, UserBody, UserResponse
from app.user.service import UsersService

router_auth = APIRouter(prefix="/api/auth", tags=["Авторизация"])
router_users = APIRouter(prefix="/api/users", tags=["Пользователи"])


@router_users.post("/register", status_code=201)
async def register_user(body: UserBody) -> UserResponse:
    clean_user_data = {
        'email': body.email,
        'password': hash_password(body.password),
        'first_name': body.first_name,
        'last_name': body.last_name,
    }
    try:
        user = await UsersService.add(**clean_user_data)
    except IntegrityError:
        raise UserExistsException
    return user


@router_auth.post("/login")
async def login_user(response: Response, body: LoginBody) -> dict[str, str]:
    user = await authenticate_user(body.email, body.password)
    token = create_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", token, httponly=True)
    return {"access_token": token}


@router_auth.post("/logout")
async def logout_user(response: Response) -> None:
    response.delete_cookie("booking_access_token")


@router_users.get("/me")
async def read_users_me(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return current_user
