from io import BytesIO

import cv2
import numpy as np
from aiogram import Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from ..backend import get_image_to_analise, get_cnn_analysis_result, get_cv_analysis_result, get_ml_analysis_result
from ..keyboard import generate_analysis_methods_inline_kb, generate_is_image_generated_inline_kb
from ....static import Emoji

analysis_methods_router = Router()


class AnaliseImageState(StatesGroup):
    waiting_for_image = State()
    waiting_for_image_type = State()


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

    await state.update_data(image=result.value)
    await message.answer(
        f'{Emoji.Question} Укажите тип изображения:',
        reply_markup=generate_is_image_generated_inline_kb()
    )
    await state.set_state(AnaliseImageState.waiting_for_image_type)


@analysis_methods_router.callback_query(F.data.in_({'real_image', 'generated_image'}))
async def image_type_chosen_handler(callback: CallbackQuery, state: FSMContext):
    is_generated = callback.data == 'generated_image'
    data = await state.get_data()
    image = data.get('image')

    if image is None:
        await callback.message.answer(f'{Emoji.Warning} Сначала загрузите изображение.')
        return

    # Анализ
    cnn_result = await get_cnn_analysis_result(image=image)
    if cnn_result.error:
        await callback.message.answer(f'{Emoji.Cancel} {cnn_result.message}')
        return

    cnn_count = cnn_result.value.get('cnn_result')

    cv_result = await get_cv_analysis_result(image=image, cnn_result=cnn_count)
    if cv_result.error:
        await callback.message.answer(f'{Emoji.Cancel} {cv_result.message}')
        return

    cv_count = cv_result.value.get('cv_result')

    image_size = data.get('image_size', (1984, 1408))
    num_elements = data.get('num_elements', 100)
    seeds = data.get('seeds', [])

    generated_parameters = (
        f'Размер изображения = {image_size[0]}x{image_size[1]}; '
        f'Количество элементов на изображении = {num_elements}; '
        f'Seeds = {','.join(map(str, seeds))}'
    )

    ml_result = await get_ml_analysis_result(image=image, cnn_result=cnn_count, cv_result=cv_count,
                                             is_generated=is_generated, generated_parameters=generated_parameters)
    if ml_result.error:
        await callback.message.answer(f'{Emoji.Cancel} {ml_result.message}')
        return

    results = {
        'opencv_method': cv_result.value,
        'ml_method': ml_result.value,
        'cnn_method': cnn_result.value,
    }

    await state.update_data(results=results)
    await callback.message.answer(f'{Emoji.Success} Изображение проанализировано. '
                                  f'Выберите метод анализа для просмотра:',
                                  reply_markup=generate_analysis_methods_inline_kb())


@analysis_methods_router.callback_query(F.data.split('_')[-1] == 'method')
async def methods_handler(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    results = state_data.get('results')

    if not results:
        await callback.message.answer(f'{Emoji.Warning} Сначала загрузите изображение')
        return

    method = results.get(callback.data)
    image_bytes = method.get('image')

    if not image_bytes:
        await callback.message.answer(f'{Emoji.Warning} Обработка не удалась.')
        return

    if callback.data.split('_')[0] == 'opencv':
        count = method.get('cv_result')

    elif callback.data.split('_')[0] == 'ml':
        count = method.get('ml_result')

    elif callback.data.split('_')[0] == 'cnn':
        count = method.get('cnn_result')

    else:
        await callback.message.answer(f'{Emoji.Warning} Обработка не удалась.')
        return

    await callback.message.answer_photo(
        BufferedInputFile(image_bytes, filename=f'{callback.data}.png'),
        caption=f'Результат обработки: {callback.data.replace('_', ' ').upper()}, количество клеток: {count}.',
        reply_markup=generate_analysis_methods_inline_kb()
    )