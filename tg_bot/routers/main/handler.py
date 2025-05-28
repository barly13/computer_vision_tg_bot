from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from .keyboard import generate_inline_menu_kb, generate_main_menu_button_inline_kb
from ...static import Emoji

main_router = Router()


@main_router.message(Command('start'))
async def main_menu_handler(message: Message, state: FSMContext):
    await message.answer(f'{Emoji.MainMenu} Главное меню', reply_markup=generate_inline_menu_kb())
    await state.clear()


@main_router.callback_query(F.data == 'main_menu')
async def main_menu_second_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'{Emoji.MainMenu} Главное меню', reply_markup=generate_inline_menu_kb())
    await state.clear()


@main_router.callback_query(F.data == 'help')
async def help_handler(callback: CallbackQuery, state: FSMContext):
    text = (
        "<b>📋 Инструкция по заполнению отчёта:</b>\n\n"
        "1️⃣ Перейдите в диалог с ботом, активируйте его (кнопка «Главное меню») и нажмите «Заполнить отчёт».\n"
        "2️⃣ Нажмите «Выбрать сотрудника» и выберите своё ФИО из списка.\n"
        "3️⃣ Если были в отпуске / на больничном / в командировке — выберите даты отсутствия и укажите причину.\n"
        "   ➡️ Если не было отсутствий — нажмите «Пропустить».\n"
        "4️⃣ Укажите выполненные работы за прошедшую неделю.\n"
        "5️⃣ Выберите, что прикрепляете: «Рабочие материалы» или «Документ». "
        "Если выбрали документ — введите его название.\n"
        "6️⃣ Проверьте данные. Если всё верно — сохраните отчёт. При ошибке можно сменить ФИО.\n\n"
        "<b>❗ Важно помнить:</b>\n"
        "🔔 Напоминания приходят каждый вторник в 16:45 и 18:00.\n"
        "🕒 Отчёт необходимо заполнить <b>до 23:58 среды</b>.\n"
        "🗑️ Данные обнуляются каждый четверг в 00:00.\n\n"
        "Спасибо за внимание! 😊"
    )

    await callback.message.edit_text(text=text,
                                     reply_markup=generate_main_menu_button_inline_kb())
