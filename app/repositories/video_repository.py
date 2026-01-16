from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.videos import Video
from app.repositories.repository import Repository


class VideoRepository(Repository[Video]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Video)

    def _get_clauses(self, **filters) -> list:
        clauses = super()._get_clauses(**filters)
        begin = filters.get("start_time_from")
        end = filters.get("start_time_to")
        if begin is not None:
            print(f"{begin=}")
            clauses.append(self._model.start_time >= begin)
        if end is not None:
            print(f"{end=}")
            clauses.append(self._model.start_time <= end)
        return clauses
