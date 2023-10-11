from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import Field


class BaseUser(BaseModel):
    email: EmailStr
    first_name: Annotated[str | None, MinLen(2), MaxLen(25)] = Field(None, pattern=r'^[A-Za-zА-Яа-я]+$', examples=["string"])
    last_name: Annotated[str | None, MinLen(2), MaxLen(25)] = Field(None, pattern=r'^[A-Za-zА-Яа-я]+$', examples=["string"])


class UserBody(BaseUser):
    password: str


class UserResponse(BaseUser):
    id: int


class LoginBody(BaseModel):
    email: EmailStr
    password: str
