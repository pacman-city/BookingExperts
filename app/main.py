from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.booking.router import router as router_booking
from app.hotel.router import router as router_hotel
from app.pages.router import router as router_pages
from app.user.router import router_auth, router_users

app = FastAPI(title='booking')

app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_hotel)
app.include_router(router_booking)
app.include_router(router_pages)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Set-Cookie",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Headers",
    ]
)
