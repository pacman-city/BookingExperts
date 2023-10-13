from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "user"

    email = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    first_name = mapped_column(String(25))
    last_name = mapped_column(String(25))

    booking = relationship("Booking", back_populates="user")
