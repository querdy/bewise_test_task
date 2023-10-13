import uuid
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.settings import settings


engine = create_async_engine(settings.DB_STRING, echo=False)
sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    __abstract__ = True

    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)


async def get_session() -> AsyncSession:
    async with sessionmaker() as session:
        yield session
