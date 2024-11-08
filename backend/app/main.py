# app run here
from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.app.core.config import settings
from backend.app.core.ws_manager import WSManager
from backend.app.api.routes import router
from backend.app.background_service import scheduler


ws_manager: WSManager = WSManager()


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Lấy dữ liệu từ db và xay dưng instance của WSManager
    print("Start...")
    scheduler.start()
    await ws_manager.add_information()
    
    yield
    print("Close...")
    scheduler.shutdown()


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