from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.static import Emoji


def generate_settings_inline_kb():
    settings_inline_kb = InlineKeyboardBuilder()

    settings_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.ImageSize} Размер изображения',
                                                callback_data='set_image_size'))
    settings_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Photo} Количество изображений',
                                                callback_data='set_num_images'))
    settings_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.ElementPerImage} Элементов на изображении',
                                                callback_data='set_num_elements'))
    settings_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Seed} Seed (число или список)',
                                                callback_data='set_seed'))
    settings_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Success} Сохранить настройки',
                                                callback_data='save_settings'))
    settings_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Delete} Сбросить',
                                                callback_data='reset_settings'))
    settings_inline_kb.row(InlineKeyboardButton(text=f'{str(Emoji.MainMenu)} Главное меню',
                                                callback_data='main_menu'))

    return settings_inline_kb.as_markup()


def generate_button_and_main_menu_inline_kb():
    generate_button_and_main_menu_kb = InlineKeyboardBuilder()

    generate_button_and_main_menu_kb.row(InlineKeyboardButton(text=f'{Emoji.Refresh} Сгенерировать данные',
                                                              callback_data='generate_data'))

    generate_button_and_main_menu_kb.row(InlineKeyboardButton(text=f'{Emoji.MainMenu} Главное меню',
                                                              callback_data='main_menu'))

    return generate_button_and_main_menu_kb.as_markup()