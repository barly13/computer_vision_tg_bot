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


@main_router.callback_query(F.data == 'main_menu')
async def main_menu_second_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'{Emoji.MainMenu} Главное меню', reply_markup=generate_inline_menu_kb())


@main_router.callback_query(F.data == 'help')
async def help_handler(callback: CallbackQuery, state: FSMContext):
    text = (
        "<b>🤖 Computer Vision Bot</b>\n\n"
        "Бот позволяет подсчитать количество клеток крови на изображении. \n"
        "📈 Доступны три метода: \n"
        "   1️⃣ обработка классическими методами компьютерного зрения \n"
        "   2️⃣ обработка при помощи классических МЛ методов \n"
        "   3️⃣ обработка при помощи CNN \n"
        "Доступные действия: \n"
        "   ➡️ «Проанализировать изображение» - загрузите изображение (реальное или сгенерированное в этой сессии), после чего можете посмотреть результаты каждого метода\n"
        "   ➡️ «Скачать результаты» - сформировать эксель файл с результатыми анализа изображений\n"
        "   ➡️ «Настройки генерации» - настроить генератор изображений с клетками крови\n"
        "   ➡️ «Сгенерировать данные» - создать изображения, исходя из заданных настроек генерации\n"
        "<b>❗ Важно:</b>\n"
        "🗑️ Настройки генерации хранятся только в течение сессии \n"
        "🖼 Лучше всего бот обрабатывает изображения с разрешением 1984x1408\n"
        "Надеемся это поможет! 😊"
    )

    await callback.message.edit_text(text=text,
                                     reply_markup=generate_main_menu_button_inline_kb())
