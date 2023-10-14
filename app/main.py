from fastapi import FastAPI

from app.user.router import router_auth, router_users
from app.hotel.router import router as router_hotel

app = FastAPI(title='booking')

app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_hotel)
