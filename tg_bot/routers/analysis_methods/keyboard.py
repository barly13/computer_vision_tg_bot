from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.static import Emoji


def generate_analysis_methods_inline_kb():
    analysis_methods_inline_kb = InlineKeyboardBuilder()

    analysis_methods_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Flask} OpenCV',
                                                        callback_data='opencv_method'))

    analysis_methods_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Statistics} ML (облака точек)',
                                                        callback_data='ml_method'))

    analysis_methods_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.RobotEmoji} CNN (нейросетевой анализ)',
                                                        callback_data='cnn_method'))

    analysis_methods_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.MainMenu} Главное меню',
                                                        callback_data='main_menu'))

    return analysis_methods_inline_kb.as_markup()


def generate_is_image_generated_inline_kb():
    is_generated_inline_kb = InlineKeyboardBuilder()

    is_generated_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.CheckMarkEmoji} Реальное изображение',
                                                    callback_data='real_image'))

    is_generated_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.Brain} Сгенерированное изображение',
                                                    callback_data='generated_image'))

    return is_generated_inline_kb.as_markup()