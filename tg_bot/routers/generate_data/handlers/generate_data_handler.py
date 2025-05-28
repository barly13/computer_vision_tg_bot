import os

from aiogram import Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, BufferedInputFile, InputMediaPhoto, Message

from tg_bot.static import Emoji
from ..backend import ImageGenerator
from ..keyboard import generate_settings_inline_kb, generate_button_and_main_menu_inline_kb

generate_data_router = Router()


class GenerationSettingsState(StatesGroup):
    waiting_for_size = State()
    waiting_for_num_images = State()
    waiting_for_num_elements = State()
    waiting_for_seed = State()


@generate_data_router.callback_query(F.data == 'generate_data')
async def generate_data_handler(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    image_size = state_data.get('image_size', (1984, 1408))
    num_images = state_data.get('num_images', 3)
    num_elements = state_data.get('num_elements', 100)
    seeds = state_data.get('seeds', [])

    image_generator = ImageGenerator(image_size=image_size, num_images=num_images,
                                     elements_per_image=num_elements, seeds=seeds)

    patterns_path = os.path.join(os.getcwd(), 'tg_bot', 'static', 'generate_patterns')

    images_bytes, _ = await image_generator.generate(patterns_path)

    media_group = []

    for index, image in enumerate(images_bytes):
        photo = BufferedInputFile(file=image.getvalue(), filename=f'generated_{index}.png')
        media_group.append(InputMediaPhoto(media=photo, caption='Generated images:' if index == 0 else ''))

    await callback.message.answer_media_group(media_group)


@generate_data_router.callback_query(F.data == 'generation_settings')
async def generation_settings_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Выберите, что хотите настроить:', reply_markup=generate_settings_inline_kb())


@generate_data_router.callback_query(F.data == 'set_image_size')
async def set_image_size_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите размер изображения в формате: ширина,высота (от 100 до 2000)')
    await state.set_state(GenerationSettingsState.waiting_for_size)


@generate_data_router.message(GenerationSettingsState.waiting_for_size)
async def set_images_size(message: Message, state: FSMContext):
    try:
        width, height = map(int, message.text.strip().split(','))

        if not (100 <= width <= 2000 and 100 <= height <= 2000):
            raise ValueError

        await state.update_data(image_size=(width, height))
        await message.answer(f'{Emoji.Success} Размер установлен: {width}x{height}')

    except:
        await message.answer(f'{Emoji.Cancel} Неверный формат или значения вне допустимого диапазона. Пример: 600, 400')
        return

    await message.answer('Что хотите настроить дальше?', reply_markup=generate_settings_inline_kb())


@generate_data_router.callback_query(F.data == 'set_num_images')
async def set_num_images_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите количество изображений (1–20)')
    await state.set_state(GenerationSettingsState.waiting_for_num_images)


@generate_data_router.message(GenerationSettingsState.waiting_for_num_images)
async def set_num_images(message: Message, state: FSMContext):
    try:
        num_images = int(message.text.strip())

        if not (1 <= num_images <= 20):
            raise ValueError

        await state.update_data(num_images=num_images)
        await message.answer(f'{Emoji.Success} Количество изображений установлено: {num_images}')

    except:
        await message.answer(f'{Emoji.Cancel} Введите целое число от 1 до 20.')
        return

    await message.answer('Что хотите настроить дальше?', reply_markup=generate_settings_inline_kb())


@generate_data_router.callback_query(F.data == 'set_num_elements')
async def set_num_elements_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите количество элементов на изображении (10–500)')
    await state.set_state(GenerationSettingsState.waiting_for_num_elements)


@generate_data_router.message(GenerationSettingsState.waiting_for_num_elements)
async def set_num_elements(message: Message, state: FSMContext):
    try:
        num_elements = int(message.text.strip())

        if not (10 <= num_elements <= 500):
            raise ValueError

        await state.update_data(num_elements=num_elements)
        await message.answer(f'{Emoji.Success} Количество элементов на изображении установлено: {num_elements}')

    except:
        await message.answer(f'{Emoji.Cancel} Введите число от 10 до 500.')
        return

    await message.answer('Что хотите настроить дальше?', reply_markup=generate_settings_inline_kb())


@generate_data_router.callback_query(F.data == 'set_seed')
async def set_seed_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите один или несколько seed через запятую (например: 42 или 1,2,3)')
    await state.set_state(GenerationSettingsState.waiting_for_seed)


@generate_data_router.message(GenerationSettingsState.waiting_for_seed)
async def set_seed(message: Message, state: FSMContext):
    try:
        state_data = await state.get_data()

        if 'num_images' not in state_data:
            await message.answer(f'{Emoji.Cancel} Сначала укажите количество изображений.',
                                 reply_markup=generate_settings_inline_kb())
            return

        try:
            seed_list = list(map(int, message.text.strip().split(',')))
        except ValueError:
            await message.answer(f'{Emoji.Cancel} Введите только целые числа, разделённые запятыми, '
                                 f'например: 42 или 1,2,3')
            return

        if not all(-100000 <= s <= 100000 for s in seed_list):
            await message.answer(f'{Emoji.Cancel} Каждое число должно быть в диапазоне от -100000 до 100000.')
            return

        if len(seed_list) != state_data['num_images']:
            await message.answer(f'{Emoji.Cancel} Вы указали {len(seed_list)} чисел, '
                                 f'а нужно {state_data['num_images']}.')
            return

        await state.update_data(seeds=seed_list)
        await message.answer(f'{Emoji.Success} Seed установлен: {seed_list}')

    except:
        await message.answer(f'{Emoji.Cancel} Произошла непредвиденная ошибка. Попробуйте снова.')
        return

    await message.answer('Что хотите настроить дальше?', reply_markup=generate_settings_inline_kb())


@generate_data_router.callback_query(F.data == 'save_settings')
async def save_settings_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(f'{Emoji.Save} Настройки сохранены:\n\n'
                                  f'Размер: {data.get('image_size', '(600, 400)')}\n'
                                  f'Количество изображений: {data.get('num_images', 3)}\n'
                                  f'Количество элементов на изображении: {data.get('num_elements', 100)}\n'
                                  f'Seed: {data.get('seeds', [])}',
                                  reply_markup=generate_button_and_main_menu_inline_kb())


@generate_data_router.callback_query(F.data == 'reset_settings')
async def reset_settings_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Выберите, что хотите настроить:', reply_markup=generate_settings_inline_kb())
    await state.clear()
