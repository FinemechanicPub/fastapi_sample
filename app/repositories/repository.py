from typing import Generic, Sequence, Type, TypeVar

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import SQLModelBase

ModelType = TypeVar("ModelType", bound=SQLModelBase)


class Repository(Generic[ModelType]):

    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        self._session = session
        self._model = model

    async def get_by_id(self, object_id: int) -> ModelType | None:
        items = await self._session.exec(
            select(self._model).where(self._model.id == object_id)
        )
        return items.first()

    async def get_list(self, **filters) -> Sequence[ModelType]:
        stmt = select(self._model)
        clauses = self._get_clauses(**filters)
        if not clauses:
            items = await self._session.exec(stmt)
        elif len(clauses) == 1:
            items = await self._session.exec(stmt.where(clauses[0]))
        else:
            items = await self._session.exec(stmt.where(and_(*clauses)))
        return items.all()

    async def create_item(self, data: dict, commit=True) -> ModelType:
        instance = self._model(**data)
        self._session.add(instance)
        if commit:
            await self._session.commit()
            await self._session.refresh(instance)
        return instance

    async def update_item(
        self, instance: ModelType, data: dict, commit: bool = True
    ):
        for field, value in data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        self._session.add(instance)
        if commit:
            await self._session.commit()
            await self._session.refresh(instance)
        return instance

    def _get_clauses(self, **filters) -> list:
        return [
            (
                getattr(self._model, filter).in_(value)
                if isinstance(value, list)
                else getattr(self._model, filter) == value
            )
            for filter, value in filters.items()
            if value is not None and hasattr(self._model, filter)
        ]
