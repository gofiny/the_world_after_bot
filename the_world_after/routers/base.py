from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State as AState
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message

from the_world_after.db.models import Player

router = Router()


@router.message(Command(commands=["start"]))
async def command_start(message: Message, bot: Bot, base_url: str):
    await message.answer("""Hi!\nSend me any type of message to star""")


@router.message(~F.message.via_bot)
async def echo_all(message: Message, player: Player, state: FSMContext):
    print(await state.get_data())
    await state.set_data({"test": "one"})
    await message.answer("test")
