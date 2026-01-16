from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database import create_tables
from app.routers.videos import router as videos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(videos_router, prefix="/videos")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
