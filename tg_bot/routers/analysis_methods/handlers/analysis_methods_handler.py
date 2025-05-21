from aiogram import Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from ..keyboard import generate_analysis_methods_inline_kb

analysis_methods_router = Router()


@analysis_methods_router.callback_query(F.data == 'choose_analysis_method')
async def choose_analysis_method_handler(callback: CallbackQuery, state: FSMContext):
    analysis_methods_inline_kb = generate_analysis_methods_inline_kb()

    await callback.message.edit_text(text='Выберите метод:', reply_markup=analysis_methods_inline_kb)
