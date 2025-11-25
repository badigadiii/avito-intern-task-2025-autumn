from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import settings

engine = create_async_engine(
    settings.db_url,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


DbDep = Annotated[AsyncSession, Depends(get_session)]
