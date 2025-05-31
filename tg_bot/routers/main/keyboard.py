from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.static import Emoji


def generate_inline_menu_kb():
    main_menu_inline_kb = InlineKeyboardBuilder()

    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Brain} Проанализировать изображение',
                                                 callback_data='analise_image'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Folder} Скачать результаты',
                                                 callback_data='download_results'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Settings} Настройки генерации',
                                                 callback_data='generation_settings'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Refresh} Сгенерировать данные',
                                                 callback_data='generate_data'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Question} Помощь',
                                                 callback_data='help'))

    return main_menu_inline_kb.as_markup()


def generate_main_menu_button_inline_kb():
    main_menu_button_inline_kb = InlineKeyboardBuilder()

    main_menu_button_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.MainMenu} Главное меню',
                                                        callback_data='main_menu'))

    return main_menu_button_inline_kb.as_markup()