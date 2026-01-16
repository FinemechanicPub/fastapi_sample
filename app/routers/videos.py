from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import VideoRepo
from app.models.videos import VideoCreate, VideoPublic, VideoUpdateStatus
from app.schemas.query import VideoQuery

router = APIRouter(tags=["Videos"])


@router.post(
    "/", response_model=VideoPublic, status_code=status.HTTP_201_CREATED
)
async def create_video(video: VideoCreate, repo: VideoRepo):
    return await repo.create_item(video.model_dump())


@router.get("/", response_model=list[VideoPublic])
async def list_videos(query: Annotated[VideoQuery, Query()], repo: VideoRepo):
    return await repo.get_list(**query.model_dump())


@router.get("/{video_id}/", response_model=VideoPublic)
async def get_video(video_id: int, repo: VideoRepo):
    video = await repo.get_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.patch("/{video_id}/", response_model=VideoPublic)
async def update_status(
    video_id: int, new_status: VideoUpdateStatus, repo: VideoRepo
):
    video = await repo.get_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return await repo.update_item(video, {"status": new_status.status.value})
