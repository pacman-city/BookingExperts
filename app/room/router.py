from datetime import date, datetime, timedelta
from typing import List

from fastapi import Query

from app.hotel.router import router
from app.room.schemas import RoomResponse
from app.room.service import RoomService


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=1)).date()}")
) -> List[RoomResponse]:
    rooms = await RoomService.find_all(hotel_id, date_from, date_to)
    return rooms
