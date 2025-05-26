from io import BytesIO

import cv2
import numpy as np
from aiogram import Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from ..keyboard import generate_analysis_methods_inline_kb
from ....static import Emoji

analysis_methods_router = Router()


class UploadImageState(StatesGroup):
    waiting_for_image_open_cv = State()
    waiting_for_image_ml = State()
    waiting_for_image_cnn = State()


@analysis_methods_router.callback_query(F.data == 'choose_analysis_method')
async def choose_analysis_method_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Выберите метод:', reply_markup=generate_analysis_methods_inline_kb())


@analysis_methods_router.callback_query(F.data == 'open_cv_method')
async def open_cv_method_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'{Emoji.Photo} Пожалуйста, загрузите фото для OpenCV-анализа:')
    await state.set_state(UploadImageState.waiting_for_image_open_cv)


@analysis_methods_router.callback_query(F.data == 'ml_method')
async def ml_method_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'{Emoji.Photo} Пожалуйста, загрузите фото для ML-анализа:')
    await state.set_state(UploadImageState.waiting_for_image_ml)


@analysis_methods_router.callback_query(F.data == 'cnn_method')
async def cnn_method_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'{Emoji.Photo} Пожалуйста, загрузите фото для CNN-анализа:')
    await state.set_state(UploadImageState.waiting_for_image_cnn)


@analysis_methods_router.message(F.photo)
async def process_uploaded_photo(message: Message, state: FSMContext):
    current_state = await state.get_state()

    photo = message.photo[-1]
    file = await message.bot.download(photo.file_id)

    image_data = file.read()

    file_array = np.asarray(bytearray(image_data), dtype=np.uint8)
    image = cv2.imdecode(file_array, cv2.IMREAD_COLOR)

    if current_state == UploadImageState.waiting_for_image_open_cv:
        await message.answer(f'{Emoji.Success} Идет обработка OpenCV-методом...')

    elif current_state == UploadImageState.waiting_for_image_ml:
        await message.answer(f'{Emoji.Success} Идет обработка ML-методом...')

    elif current_state == UploadImageState.waiting_for_image_cnn:
        await message.answer(f'{Emoji.Success} Идет обработка CNN-методом...')

    else:
        await message.answer(f'{Emoji.Warning} Неизвестное состояние, попробуйте еще раз...')

    await state.clear()
