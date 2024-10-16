from fastapi import FastAPI
from app.routers import app_router

app = FastAPI(
    title="CDNVideo",
    description="TZ",
)

app.include_router(router=app_router)
