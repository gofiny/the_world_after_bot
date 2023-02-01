import logging
from typing import Optional

from sqlalchemy import BigInteger, Column, ForeignKey, String, select, update
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from the_world_after.db.db import Base

logger = logging.getLogger(__name__)


class State(Base):
    __tablename__ = "states"

    id = Column(BigInteger, primary_key=True)
    player_id = Column(
        BigInteger, ForeignKey("players.id"), unique=True, index=True
    )
    state = Column(String, nullable=True, default=None)
    data = Column(JSONB, nullable=True, default=None)

    @classmethod
    async def get_by_player_id(
        cls, player_id: int, session: AsyncSession
    ) -> Optional["State"]:
        result: Result = await session.execute(
            select(cls).where(cls.player_id == player_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def update_by_player_id(
        cls, player_id: int, session: AsyncSession, **kwargs
    ) -> None:
        await session.execute(
            update(cls).where(cls.player_id == player_id).values(**kwargs)
        )

    @classmethod
    async def create_or_update(
        cls, player_id: int, session: AsyncSession, **kwargs
    ) -> None:
        data = dict(player_id=player_id, **kwargs)
        await session.execute(
            insert(cls)
            .values(**data)
            .on_conflict_do_update(index_elements=[cls.player_id], set_=data)
        )
