from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.user.auth import authenticate_user, create_token


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        if user:
            access_token = create_token({"sub": str(user.id)})
            request.session.update({"bearer": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        token = request.session.get("bearer")
        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key="...")
