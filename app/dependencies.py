from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.repositories.video_repository import VideoRepository


async def get_video_repository(
    session: AsyncSession = Depends(get_session),
) -> VideoRepository:
    return VideoRepository(session)


VideoRepo = Annotated[VideoRepository, Depends(get_video_repository)]
