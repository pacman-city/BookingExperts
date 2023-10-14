from datetime import date

from sqlalchemy import and_, func, or_, select

from app.booking.models import Booking
from app.database import async_session_maker
from app.hotel.models import Hotel
from app.room.models import Room
from app.service import BaseService


class HotelService(BaseService):
    model = Hotel

    @classmethod
    async def find_available(cls, location: str, date_from: date, date_to: date):
        """Returns all hotels with anyone room available"""

        """
            WITH booked_rooms AS (
                SELECT room_id, COUNT(room_id) AS rooms_booked
                FROM bookings
                WHERE
                    (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                    (date_from <= '2023-05-15' AND date_to > '2023-05-15')
                GROUP BY room_id
            ),
            booked_hotels AS (
                SELECT hotel_id, SUM(rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left
                FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                GROUP BY hotel_id
            )
            SELECT * FROM hotels
            LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
            WHERE rooms_left > 0 AND location LIKE '%Алтай%';
        """
        booked_rooms = (
            select(Booking.room_id, func.count(Booking.room_id).label("rooms_booked"))
            .select_from(Booking)
            .where(
                or_(
                    and_(
                        Booking.date_from >= date_from,
                        Booking.date_from <= date_to),
                    and_(
                        Booking.date_from <= date_from,
                        Booking.date_to > date_from),
                ),
            )
            .group_by(Booking.room_id)
            .cte("booked_rooms")
        )

        booked_hotels = (
            select(Room.hotel_id, func.sum(
                Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
            ).label("rooms_left"))
            .select_from(Room)
            .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
            .group_by(Room.hotel_id)
            .cte("booked_hotels")
        )

        get_hotels_with_rooms = (
            select(
                Hotel.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotel.id, isouter=True)
            .where(booked_hotels.c.rooms_left > 0, Hotel.location.ilike(f"%{location}%"))
        )
        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
