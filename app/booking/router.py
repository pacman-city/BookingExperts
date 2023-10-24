from fastapi import APIRouter, Body, Depends
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter

from app.booking.schemas import BookingBody, BookingResponse, BookingAddResponse
from app.booking.service import BookingService
from app.exceptions import BookingUnknownException
from app.tasks.tasks import send_booking_confirmation_email
from app.user.dependencies import get_current_user
from app.user.models import User
from app.utils import validate_date

router = APIRouter(prefix="/api/bookings", tags=["Бронирования"])


@router.get("")
# @cache(expire=60)
async def get_bookings(user: User = Depends(get_current_user)) -> list[BookingResponse]:
    return await BookingService.find_all_with_images(user_id=user.id)


@router.post("", status_code=201)
async def add_booking(
        booking: BookingBody,
        user: User = Depends(get_current_user)):
    validate_date(booking.date_from, booking.date_to, max_days=60)
    booking = await BookingService.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise BookingUnknownException

    validator = TypeAdapter(BookingAddResponse)
    booking_dict = validator.validate_python(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("", status_code=204)
async def remove_booking(
        booking_id: int = Body(embed=True, ge=1, examples=[1]),
        current_user: User = Depends(get_current_user)):
    await BookingService.delete(id=booking_id, user_id=current_user.id)
