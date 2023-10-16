from fastapi import APIRouter, Depends

from app.booking.schemas import BookingBody, BookingResponse
from app.booking.service import BookingService
from app.exceptions import BookingUnknownException
from app.user.dependencies import get_current_user
from app.user.models import User
from app.utils import validate_date

router = APIRouter(prefix="/api/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(user: User = Depends(get_current_user)) -> list[BookingResponse]:
    return await BookingService.find_all_with_images(user_id=user.id)


@router.post("", status_code=201)
async def add_booking(
        booking: BookingBody,
        user: User = Depends(get_current_user)):
    validate_date(booking.date_from, booking.date_to)
    booking = await BookingService.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise BookingUnknownException
    return booking


@router.delete("", status_code=204)
async def remove_booking(
        booking_id: int,
        current_user: User = Depends(get_current_user)):
    await BookingService.delete(id=booking_id, user_id=current_user.id)
