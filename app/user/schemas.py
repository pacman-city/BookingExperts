from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    email: EmailStr
    first_name: Annotated[str | None, MinLen(2), MaxLen(25)] = Field(None, pattern=r'^[\p{L}]+$', examples=["string"])
    last_name: Annotated[str | None, MinLen(2), MaxLen(25)] = Field(None, pattern=r'^[\p{L}]+$', examples=["string"])


class UserBody(BaseUser):
    password: Annotated[str, MinLen(6), MaxLen(25)]


class UserResponse(BaseUser):
    id: int


class LoginBody(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(6), MaxLen(25)]
