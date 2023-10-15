from datetime import date, datetime, timedelta

from pydantic import BaseModel
from fastapi import Body


class BookingResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: str | None
    services: list[str]


class BookingBody(BaseModel):
    room_id: int
    date_from: date = Body(examples=[datetime.now().date()])
    date_to: date = Body(examples=[(datetime.now() + timedelta(days=1)).date()])
