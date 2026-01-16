from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.videos import VideoStatus


class VideoQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: list[VideoStatus] | None = Field(None)
    camera_number: list[int] | None = Field(None)
    location: list[str] | None = Field(None)
    start_time_from: datetime | None = Field(None)
    start_time_to: datetime | None = Field(None)
