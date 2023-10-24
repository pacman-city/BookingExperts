import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    (4, "2030-05-01", "2030-05-15", 3, 201),
    (4, "2030-05-02", "2030-05-16", 4, 201),
    (4, "2030-05-03", "2030-05-17", 5, 201),
    (4, "2030-05-04", "2030-05-18", 6, 201),
    (4, "2030-05-05", "2030-05-19", 7, 201),
    (4, "2030-05-06", "2030-05-20", 8, 201),
    (4, "2030-05-07", "2030-05-21", 9, 201),
    (4, "2030-05-08", "2030-05-22", 10, 201),
    (4, "2030-05-09", "2030-05-23", 10, 409),
    (4, "2030-05-10", "2030-05-24", 10, 409),
])
async def test_add_and_get_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        booked_rooms,
        authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post("/api/bookings", json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/api/bookings")
    assert len(response.json()) == booked_rooms
