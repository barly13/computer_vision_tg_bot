from typing import Tuple

import cv2
import numpy as np


def visualise_detection(image: np.ndarray, detections: np.ndarray, color: Tuple[int, int, int] = None) -> np.ndarray:
    if color is None:
        color = (0, 255, 0)

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    for det in detections:
        x1, y1, x2, y2 = det

        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    return image
