from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["start"]))
async def command_start(message: Message, bot: Bot, base_url: str):
    await message.answer("""Hi!\nSend me any type of message to star""")


@router.message(~F.message.via_bot)
async def echo_all(message: Message, base_url: str):
    await message.answer("Test webview")
