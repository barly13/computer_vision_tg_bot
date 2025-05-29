import functools
from io import BytesIO

import cv2
import numpy as np
from aiogram.types import Message

from tg_bot.dtos import Response
from .cnn_analysis_method import cnn_analysis_method
from .cv_analysis_method import CVAnalysisMethod
from .visual_functions import visualise_detection


async def get_image_to_analise(message: Message):
    try:
        photo = message.photo[-1]
        file = await message.bot.download(photo.file_id)
        image_data = file.read()

        file_array = np.asarray(bytearray(image_data), dtype=np.uint8)
        image = cv2.imdecode(file_array, cv2.IMREAD_COLOR)

        if image is None:
            return Response(message='Не удалось декодировать изображение', error=True)

        return Response(value=image)

    except Exception as exp:
        return Response(message=f'Ошибка при получении изображения: {exp}', error=True)


async def get_cnn_analysis_result(image) -> Response:
    try:
        detections = cnn_analysis_method.execute(image)
        output_image = visualise_detection(image, detections)
        _, buffer = cv2.imencode('.png', output_image)

        return Response(value=buffer.tobytes())

    except Exception as exp:
        return Response(message=f'Ошибка при CNN-анализе: {exp}', error=True)


async def get_cv_analysis_result(image) -> Response:
    try:
        cv_method = CVAnalysisMethod()
        detections = cv_method.execute(image)
        output_image = visualise_detection(image, detections)
        _, buffer = cv2.imencode('.png', output_image)

        return Response(value=buffer.tobytes())

    except Exception as exp:
        return Response(message=f'Ошибка при OpenCV-анализе: {exp}', error=True)
