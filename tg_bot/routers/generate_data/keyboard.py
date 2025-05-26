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

    return settings_inline_kb.as_markup()