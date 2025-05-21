from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.static import Emoji


def generate_analysis_methods_inline_kb():
    analysis_methods_inline_kb = InlineKeyboardBuilder()

    analysis_methods_inline_kb.row(InlineKeyboardButton(text=f'{str(Emoji.Flask)} OpenCV',
                                                        callback_data='open_cv_method'))

    analysis_methods_inline_kb.row(InlineKeyboardButton(text=f'{str(Emoji.Statistics)} ML (облака точек)',
                                                        callback_data='ml_method'))

    analysis_methods_inline_kb.row(InlineKeyboardButton(text=f'{str(Emoji.RobotEmoji)} CNN (нейросетевой анализ)',
                                                        callback_data='cnn_method'))

    analysis_methods_inline_kb.row(InlineKeyboardButton(text=f'{str(Emoji.MainMenu)} Главное меню',
                                                        callback_data='main_menu'))

    return analysis_methods_inline_kb.as_markup()
