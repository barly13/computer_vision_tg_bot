from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def generate_inline_menu_kb():
    main_menu_inline_kb = InlineKeyboardBuilder()

    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.MainMenu} Привет!', callback_data='nothing_now'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.EmployeeEmoji} Привет!', callback_data='nothing_now'))
    main_menu_inline_kb.row(InlineKeyboardButton(text=f'{Emoji.EditText} Привет!', callback_data='nothing_now'))

    return main_menu_inline_kb.as_markup()
