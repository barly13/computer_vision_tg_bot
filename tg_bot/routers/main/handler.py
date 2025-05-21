from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from .keyboard import generate_inline_menu_kb

base_main_router = Router()


@base_main_router.message(Command('start'))
async def main_menu_handler(message: Message, state: FSMContext):
    main_menu_inline_kb = generate_inline_menu_kb()
    await message.answer(f'Главное меню', reply_markup=main_menu_inline_kb)
    await state.clear()


@base_main_router.callback_query(F.data == 'main_menu')
async def main_menu_second_handler(callback: CallbackQuery, state: FSMContext):
    main_menu_inline_kb = generate_inline_menu_kb()

    await callback.message.edit_text(f'Главное меню', reply_markup=main_menu_inline_kb)
    await state.clear()