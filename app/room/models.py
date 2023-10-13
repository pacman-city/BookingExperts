from sqlalchemy import ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship, mapped_column

from app.database import Base


class Room(Base):
    __tablename__ = "room"

    hotel_id = mapped_column(ForeignKey("hotel.id"), nullable=False)
    name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=True)
    price = mapped_column(Integer, nullable=False)
    services = mapped_column(JSON, nullable=True)
    quantity = mapped_column(Integer, nullable=False)
    image_id = mapped_column(Integer)

    hotel = relationship("Hotel", back_populates="rooms")
    booking = relationship("Booking", back_populates="room")
