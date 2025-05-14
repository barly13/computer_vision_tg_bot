from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .keyboard import generate_inline_menu_kb

base_main_router = Router()


@base_main_router.message(Command('start'))
async def main_menu_handler(message: Message, state: FSMContext):
    main_menu_inline_kb = generate_inline_menu_kb()
    await message.answer(f'Главное меню', reply_markup=main_menu_inline_kb)
    await state.clear()
