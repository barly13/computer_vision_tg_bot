from typing import Tuple, List

import cv2
import numpy as np


def visualise_detection(image: np.ndarray, detections, method: str,
                        color: Tuple[int, int, int] = None) -> np.ndarray:
    if color is None:
        color = (0, 255, 0)

    output_image = image.copy()

    if len(output_image.shape) == 2 or output_image.shape[2] == 1:
        output_image = cv2.cvtColor(output_image, cv2.COLOR_GRAY2BGR)

    for det in detections:
        if method == 'ml':
            cv2.drawContours(output_image, [det], -1, color, 2)
        elif method == 'cnn':
            x1, y1, x2, y2 = map(int, det)
            cv2.rectangle(output_image, (x1, y1), (x2, y2), color, 2)
        elif method == 'cv':
            x, y, r = map(int, det)
            cv2.circle(output_image, (x, y), r, color, 2)
        else:
            raise ValueError(f"Unknown detection format: {det}")

    return output_image
