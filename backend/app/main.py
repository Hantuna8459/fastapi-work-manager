# app run here
from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.app.core.config import settings
from backend.app.core.ws_manager import WSManager
from backend.app.api.routes import router


ws_manager: WSManager = WSManager()


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Lấy dữ liệu từ db và xau dưng instance của WSManager
    print("Start...")
    await ws_manager.add_information()

    yield
    print("Close...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)


app.include_router(router)