from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import UserAdmin, HotelAdmin, RoomAdmin, BookingAdmin
from app.booking.router import router as router_booking
from app.database import engine
from app.hotel.router import router as router_hotel
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.user.router import router_auth, router_users

app = FastAPI(title='booking')

# Подключение API:
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotel)
app.include_router(router_booking)

# Загрузка картинок:
app.include_router(router_images)

# Подключение Страниц:
app.include_router(router_pages)

# Подключение Статики(images, css, js):
app.mount("/static", StaticFiles(directory="app/static"), "static")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["https://127.0.0.1:9000"],
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Set-Cookie",
                   "Content-Type",
                   "Authorization",
                   "Access-Control-Allow-Origin",
                   "Access-Control-Allow-Headers"]
)


# Подключение redis:
@app.on_event("startup")
def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


# Подключение админки:
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
admin.add_view(BookingAdmin)
