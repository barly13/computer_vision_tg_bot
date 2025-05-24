import os

from aiogram import Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, BufferedInputFile, InputMediaPhoto

from ..backend import ImageGenerator


generate_data_router = Router()


@generate_data_router.callback_query(F.data == 'generate_data')
async def generate_data_handler(callback: CallbackQuery, state: FSMContext):
    image_generator = ImageGenerator(num_images=3)

    patterns_path = os.path.join(os.getcwd(), 'tg_bot', 'static', 'generate_patterns')

    images_bytes, _ = await image_generator.generate(patterns_path)

    media_group = []

    for index, image in enumerate(images_bytes):
        photo = BufferedInputFile(file=image.getvalue(), filename=f'generated_{index}.png')
        media_group.append(InputMediaPhoto(media=photo, caption='Generated images:' if index == 0 else ''))

    await callback.message.answer_media_group(media_group)
