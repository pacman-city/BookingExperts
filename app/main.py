from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.booking.router import router as router_booking
from app.hotel.router import router as router_hotel
from app.pages.router import router as router_pages
from app.user.router import router_auth, router_users
from app.images.router import router as router_images

app = FastAPI(title='booking')

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotel)
app.include_router(router_booking)
app.include_router(router_images)
app.include_router(router_pages)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://127.0.0.1:8000"],
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Set-Cookie",
                   "Content-Type",
                   "Authorization",
                   "Access-Control-Allow-Origin",
                   "Access-Control-Allow-Headers"]
)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
