import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiohttp.web import run_app
from aiohttp.web_app import Application

from the_world_after.db.db import check_session
from the_world_after.routers import base

from .settings import settings

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    await check_session()

    if settings.IS_WEBHOOK:
        await bot.set_webhook(f"{settings.APP_URL}{settings.APP_EVENTS_PATH}")


async def on_shutdown(bot: Bot):
    if settings.IS_WEBHOOK:
        await bot.delete_webhook()


def prepare_app(bot: Bot, dispatcher: Dispatcher) -> Application:
    app = Application()
    app["bot"] = bot

    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    ).register(app, path=settings.APP_EVENTS_PATH)
    setup_application(app, dispatcher, bot=bot)

    return app


def run_bot():
    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")
    dispatcher = Dispatcher()
    dispatcher["base_url"] = settings.APP_URL
    dispatcher.startup.register(on_startup)

    dispatcher.include_router(base.router)

    if settings.IS_WEBHOOK:
        app = prepare_app(bot, dispatcher)
        run_app(app, host=settings.APP_HOST, port=settings.APP_PORT)
    else:
        dispatcher.run_polling(bot)
