from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update

from the_world_after.db.db import get_session
from the_world_after.db.models import Player


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        async with get_session() as session:
            user = event.message.from_user
            player = await Player.get_or_create(user.id, session)
            data.update(player=player)
            await session.commit()

        return await handler(event, data)
