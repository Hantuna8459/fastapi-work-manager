# app run here
from fastapi import FastAPI
from backend.app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME
)