# app run here
from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.api.routes import api_router

app = FastAPI(
    title=settings.PROJECT_NAME
)
app.include_router(api_router)