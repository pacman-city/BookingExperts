from datetime import date

from sqlalchemy import and_, func, or_, select

from app.booking.models import Booking
from app.database import async_session_maker
from app.room.models import Room
from app.service import BaseService


class RoomService(BaseService):
    model = Room

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                  (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            GROUP BY room_id
        )
        SELECT
            -- все столбцы из rooms,
            (quantity - COALESCE(rooms_booked, 0)) AS rooms_left FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE hotel_id = 1
        """
        booked_rooms = (
            select(Booking.room_id, func.count(Booking.room_id).label("rooms_booked"))
            .select_from(Booking)
            .where(
                or_(
                    and_(
                        Booking.date_from >= date_from,
                        Booking.date_from <= date_to,
                    ),
                    and_(
                        Booking.date_from <= date_from,
                        Booking.date_to > date_from,
                    ),
                ),
            )
            .group_by(Booking.room_id)
            .cte("booked_rooms")
        )

        get_rooms = (
            select(
                Room.__table__.columns,
                (Room.price * (date_to - date_from).days).label("total_cost"),
                (Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left"),
            )
            .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
            .where(
                Room.hotel_id == hotel_id
            )
        )
        async with async_session_maker() as session:
            rooms = await session.execute(get_rooms)
            return rooms.mappings().all()
