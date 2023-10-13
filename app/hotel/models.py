from sqlalchemy import Integer, JSON, String
from sqlalchemy.orm import mapped_column, relationship

from app.database import Base


class Hotel(Base):
    __tablename__ = "hotel"

    name = mapped_column(String, nullable=False)
    location = mapped_column(String, nullable=False)
    services = mapped_column(JSON)
    rooms_quantity = mapped_column(Integer, nullable=False)
    image_id = mapped_column(Integer)

    rooms = relationship("Room", back_populates="hotel")
