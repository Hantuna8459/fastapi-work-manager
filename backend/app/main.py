# app run here
from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.app.core.config import settings
from backend.app.api.routes import router
from backend.app.background_service import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.include_router(router)