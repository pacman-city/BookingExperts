from app.service import BaseService
from app.user.models import User


class UsersService(BaseService):
    model = User


