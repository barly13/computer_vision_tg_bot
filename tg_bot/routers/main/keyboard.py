from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.static import Emoji


def generate_inline_menu_kb():
    main_menu_inline_kb = InlineKeyboardBuilder()

    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Brain} Выбрать метод анализа',
                                                 callback_data='choose_analysis_method'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.ExperimentHistory} История экспериментов',
                                                 callback_data='experiment_history'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Folder} Скачать результаты',
                                                 callback_data='download_results'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Settings} Настройки генерации',
                                                 callback_data='generation_settings'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Refresh} Сгенерировать данные',
                                                 callback_data='generate_data'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Question} Помощь',
                                                 callback_data='help'))

    return main_menu_inline_kb.as_markup()
