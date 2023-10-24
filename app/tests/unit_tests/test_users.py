import pytest

from app.user.service import UsersService


@pytest.mark.parametrize("email,is_present", [
    ("test@test.com", True),
    ("user@example.com", True),
    ("invalid-email", False)
])
async def test_find_user_by_id(email, is_present):
    user = await UsersService.find_one_or_none(email=email)

    if is_present:
        assert user
        assert user["email"] == email
    else:
        assert not user
