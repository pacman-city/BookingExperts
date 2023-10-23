from sqladmin import ModelView

from app.booking.models import Booking
from app.hotel.models import Hotel
from app.room.models import Room
from app.user.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.booking]
    column_details_exclude_list = [User.password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c] + [Hotel.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.hotel, Room.booking]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"


class BookingAdmin(ModelView, model=Booking):
    column_list = [c.name for c in Booking.__table__.c] + [Booking.user, Booking.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
