import asyncio
import json
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.booking.models import Booking
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotel.models import Hotel
from app.main import app as fastapi_app
from app.room.models import Room
from app.user.models import User


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        # SQLAlchemy не принимает дату в текстовом формате -> datetime
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Hotel, hotels),
            (Room, rooms),
            (User, users),
            (Booking, bookings),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    """Асинхронный клиент для тестирования эндпоинтов"""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    """Асинхронный аутентифицированный клиент для тестирования эндпоинтов"""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/api/auth/login", json={
            "email": "test@test.com",
            "password": "string",
        })
        assert ac.cookies["Bearer"]
        yield ac
