from fastapi import FastAPI

from app.user.router import router_auth, router_users
from app.hotel.router import router as router_hotel
from app.booking.router import router as router_booking

app = FastAPI(title='booking')

app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_hotel)
app.include_router(router_booking)
