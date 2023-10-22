from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import NotFoundException
from app.hotel.schemas import HotelAvailableResponse, HotelResponse
from app.hotel.service import HotelService
from app.utils import validate_date

router = APIRouter(prefix="/api/hotels", tags=["Отели"])


@router.get("")
async def get_available_hotels(
        max_days: int = Query(60, include_in_schema=False),
        location: str = Query(None, description="Например: алтай"),
        date_from: date = Query(description=f"Min: {datetime.now().date()}"),
        date_to: date = Query(description=f"Например: {(datetime.now() + timedelta(days=1)).date()}, max: 60 дней")
) -> list[HotelAvailableResponse]:
    validate_date(date_from, date_to, max_days=max_days)
    hotels = await HotelService.find_available(location or '', date_from, date_to)
    return hotels


@router.get("/all")
@cache(expire=60)
async def get_all_hotels():
    hotels = await HotelService.find_all()
    return hotels


@router.get("/{hotel_id}")
@cache(expire=60)
async def get_hotel_by_id(hotel_id: int) -> HotelResponse:
    hotel = await HotelService.find_one_or_none(id=hotel_id)
    if not hotel:
        raise NotFoundException()
    return hotel
