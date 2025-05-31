import functools
from datetime import datetime
from io import BytesIO

import cv2
import numpy as np
from aiogram.types import Message

from database import ExperimentReport
from tg_bot.dtos import Response
from .cnn_analysis_method import cnn_analysis_method
from .cv_analysis_method import CVAnalysisMethod
from .visual_functions import visualise_detection
from ....settings import  SAVE_PATH


def save_report_to_db(
    image_path: str | None,
    is_generated: bool,
    generation_params: str | None,
    opencv_result: int,
    ml_result: int,
    cnn_result: int,
):
    ExperimentReport.create(
        image_path=None if is_generated else image_path,
        generation_params=generation_params if is_generated else None,
        is_generated=is_generated,
        date=datetime.now(),
        opencv_result=opencv_result,
        ml_result=ml_result,
        cnn_result=cnn_result
    )


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
        cnn_image = image.copy()

        detections = cnn_analysis_method.execute(cnn_image)
        cnn_count = len(detections)
        output_image = visualise_detection(cnn_image, detections)
        _, buffer = cv2.imencode('.png', output_image)

        return Response(value={'image': buffer.tobytes(), 'cnn_result': cnn_count})

    except Exception as exp:
        return Response(message=f'Ошибка при CNN-анализе: {exp}', error=True)


async def get_cv_analysis_result(image, cnn_result: int) -> Response:
    try:
        cv_image = image.copy()

        cv_method = CVAnalysisMethod()
        detections = cv_method.execute(cv_image)
        cv_count = len(detections)
        output_image = visualise_detection(cv_image, detections)
        _, buffer = cv2.imencode('.png', output_image)

        return Response(value={'image': buffer.tobytes(), 'cnn_result': cnn_result, 'cv_result': cv_count})

    except Exception as exp:
        return Response(message=f'Ошибка при OpenCV-анализе: {exp}', error=True)


async def get_ml_analysis_result(
    image,
    cnn_result: int,
    cv_result: int,
    is_generated: bool,
    generated_parameters: str = None
) -> Response:
    try:
        ml_image = image.copy()
        ml_result = 0

        if is_generated:
            save_report_to_db(
                is_generated=True,
                generation_params=generated_parameters,
                image_path=None,
                opencv_result=cv_result,
                ml_result=ml_result,
                cnn_result=cnn_result
            )

        else:
            last_id = ExperimentReport.get_all()[-1].id if ExperimentReport.get_all() else 0
            image_path = SAVE_PATH / f'real_image_{last_id + 1}.png'

            cv2.imwrite(str(image_path), image)

            save_report_to_db(
                is_generated=False,
                generation_params=None,
                image_path=str(image_path),
                opencv_result=cv_result,
                ml_result=ml_result,
                cnn_result=cnn_result
            )

        return Response(
            value={
                'image': ml_image,
                'cnn_result': cnn_result,
                'cv_result': cv_result,
                'ml_result': ml_result
            }
        )

    except Exception as exp:
        return Response(message=f'Ошибка при ML-анализе: {exp}', error=True)