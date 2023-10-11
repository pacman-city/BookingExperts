from fastapi import FastAPI

from app.user.router import router_auth, router_users

app = FastAPI(title='booking')

app.include_router(router_users)
app.include_router(router_auth)
