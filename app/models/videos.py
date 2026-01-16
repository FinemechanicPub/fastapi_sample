from datetime import datetime, timedelta
from enum import Enum

from sqlmodel import Column, DateTime, Field, SQLModel

from app.database import SQLModelBase


class VideoStatus(str, Enum):
    NEW = "new"
    TRANSCODED = "transcoded"
    RECOGNIZED = "recognized"


class VideoBase(SQLModel):
    video_path: str = Field(min_length=1)
    start_time: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    duration: timedelta = Field(gt=0)
    camera_number: int = Field(ge=1)
    location: str = Field(min_length=1)
    status: VideoStatus = Field(default=VideoStatus.NEW)


class Video(SQLModelBase, VideoBase, table=True):
    __tablename__: str = "videos"


class VideoCreate(VideoBase):
    pass


class VideoUpdateStatus(SQLModel):
    status: VideoStatus


class VideoPublic(VideoBase):
    id: int
    created_at: datetime
