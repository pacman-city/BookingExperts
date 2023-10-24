import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("user-1@example.com", "string", 201),
    ("user-1@example.com", "string", 409),
    ("user-2@example.com", "string", 201),
    ("invalid", "string", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/api/users/register",
        json={"email": email, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.com", "string", 200),
    ("user@example.com", "string", 200),
    ("not-exist@example.com", "string", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/api/auth/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == status_code
