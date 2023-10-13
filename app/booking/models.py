from sqlalchemy import Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "booking"

    room_id = mapped_column(ForeignKey("room.id"))
    user_id = mapped_column(ForeignKey("user.id"))
    date_from = mapped_column(Date, nullable=False)
    date_to = mapped_column(Date, nullable=False)
    price = mapped_column(Integer, nullable=False)
    total_cost = mapped_column(Integer, Computed("(date_to - date_from) * price"))
    total_days = mapped_column(Integer, Computed("date_to - date_from"))

    user = relationship("User", back_populates="booking")
    room = relationship("Room", back_populates="booking")
