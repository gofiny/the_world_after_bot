import logging
from typing import Any, Optional

from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.base import State as AState
from aiogram.fsm.storage.base import StateType, StorageKey

from the_world_after.db.db import get_session
from the_world_after.db.models import State

logger = logging.getLogger(__name__)


class PostgresStorage(BaseStorage):
    async def set_state(
        self, bot: Bot, key: StorageKey, state: StateType = None
    ) -> None:
        async with get_session() as session:
            await State.create_or_update(
                key.user_id,
                session,
                state=state.state if isinstance(state, AState) else state,
            )
            await session.commit()

    async def get_state(self, bot: Bot, key: StorageKey) -> Optional[str]:
        async with get_session() as session:
            if state := await State.get_by_player_id(key.user_id, session):
                return state.state

    async def set_data(
        self, bot: Bot, key: StorageKey, data: Optional[dict[str, Any]] = None
    ) -> None:
        async with get_session() as session:
            await State.update_by_player_id(key.user_id, session, data=data)
            await session.commit()

    async def get_data(
        self, bot: Bot, key: StorageKey
    ) -> Optional[dict[str, Any]]:
        async with get_session() as session:
            if state := await State.get_by_player_id(key.user_id, session):
                return state.data

    async def close(self) -> None:
        logger.info("Closing postgres storage...")
