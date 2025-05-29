from io import BytesIO

import cv2
import numpy as np
from aiogram import Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from ..backend import get_image_to_analise, get_cnn_analysis_result, get_cv_analysis_result
from ..keyboard import generate_analysis_methods_inline_kb
from ....static import Emoji

analysis_methods_router = Router()


class AnaliseImageState(StatesGroup):
    waiting_for_image = State()


@analysis_methods_router.callback_query(F.data == 'analise_image')
async def analise_image_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'{Emoji.Photo} Пожалуйста, загрузите изображение для анализа:')
    await state.set_state(AnaliseImageState.waiting_for_image)


@analysis_methods_router.message(F.photo)
async def upload_photo_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state != AnaliseImageState.waiting_for_image:
        await message.answer(f'{Emoji.Warning} Сначала выберите опцию анализа изображения.')
        return

    result = await get_image_to_analise(message)
    if result.error:
        await message.answer(f'{Emoji.Cancel} {result.message}')
        return

    image = result.value

    cnn_result = await get_cnn_analysis_result(image=image)
    if cnn_result.error:
        await message.answer(f'{Emoji.Cancel} {cnn_result.message}')
        return

    cv_result = await get_cv_analysis_result(image=image)
    if cv_result.error:
        await message.answer(f'{Emoji.Cancel} {cv_result.message}')
        return

    results = {
        'open_cv_method': cv_result.value,
        'ml_method': '',
        'cnn_method': cnn_result.value,
    }

    await state.update_data(results=results)

    await message.answer(f'{Emoji.Success} Изображение проанализировано. '
                         f'Выберите метод анализа, который хотите просмотреть:',
                         reply_markup=generate_analysis_methods_inline_kb())


@analysis_methods_router.callback_query(F.data.split('_')[-1] == 'method')
async def methods_handler(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    results = state_data.get('results')

    if not results:
        await callback.message.answer(f'{Emoji.Warning} Сначала загрузите изображение')
        return

    method = callback.data
    image_bytes = results.get(method)

    if not image_bytes:
        await callback.message.answer(f'{Emoji.Warning} Обработка не удалась.')
        return

    await callback.message.answer_photo(
        BufferedInputFile(image_bytes, filename=f'{method}.png'),
        caption=f'Результат обработки: {method.replace('_', ' ').upper()}',
        reply_markup=generate_analysis_methods_inline_kb()
    )

