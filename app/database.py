from datetime import datetime, timezone
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import Column, DateTime, Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings

engine = create_async_engine(str(settings.db.dsn))
AsyncSectionLocal = async_sessionmaker(
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class SQLModelBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default=datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSectionLocal() as session:
        yield session
