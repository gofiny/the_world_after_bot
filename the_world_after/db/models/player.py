import logging
from typing import Optional

from sqlalchemy import BigInteger, Column, String, func, select, update
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from the_world_after.db.db import Base
from the_world_after.utils.types import Lang

logger = logging.getLogger(__name__)


class Player(Base):
    __tablename__ = "players"

    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True, default=None, unique=True)
    lang = Column(ENUM(Lang), nullable=False, default=Lang.ru.value)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> "Player":
        logger.info(f"Create user {kwargs=}")
        entry = cls(**kwargs)
        session.add(entry)
        await session.flush()
        return entry

    @classmethod
    async def get(cls, _id: int, session: AsyncSession) -> Optional["Player"]:
        logger.info(f"get user {_id=}")
        result: Result = await session.execute(
            select(cls).where(cls.id == _id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_or_create(
        cls, _id: int, session: AsyncSession, **kwargs
    ) -> "Player":
        if player := await cls.get(_id, session):
            return player
        return await cls.create(session, id=_id, **kwargs)

    @classmethod
    async def update(cls, _id: int, session: AsyncSession, **kwargs) -> None:
        logger.info(f"update user {_id=} {kwargs=}")
        await session.execute(
            update(cls).where(cls.id == _id).values(**kwargs)
        )
