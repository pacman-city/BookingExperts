from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query

from app.exceptions import NotFoundException
from app.hotel.schemas import HotelAvailableResponse, HotelResponse
from app.hotel.service import HotelService
from app.utils import validate_date

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_available_hotels(
        location: str | None = Query(None, description="Например: алтай"),
        date_from: date = Query(..., description=f"Например: {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например: {(datetime.now() + timedelta(days=5)).date()}"),
) -> list[HotelAvailableResponse]:
    validate_date(date_from, date_to)
    hotels = await HotelService.find_available(location or '', date_from, date_to)
    return hotels


@router.get("/all")
async def get_all_hotels():
    hotels = await HotelService.find_all()
    return hotels


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> HotelResponse:
    hotel = await HotelService.find_one_or_none(id=hotel_id)
    if not hotel:
        raise NotFoundException()
    return hotel
