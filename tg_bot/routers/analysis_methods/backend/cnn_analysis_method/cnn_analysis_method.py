import os
from typing import Tuple

import cv2
import numpy as np
from ultralytics import YOLO

from tg_bot.settings import WEIGHTS_PATH
from ..analysis_method_base import AnalysisMethodBase


class CNNAnalysisMethod(AnalysisMethodBase):
    def __init__(self, weights_path: str, img_size: Tuple[int, int], device: str | int = 'cpu'):
        self.model = YOLO(weights_path)
        self.model.img_size = img_size[1]
        self.img_size = img_size
        self.device = device

    def execute(self, image: np.ndarray) -> np.ndarray:
        dx = self.img_size[1] - image.shape[1]
        dy = self.img_size[0] - image.shape[0]
        input_image = cv2.copyMakeBorder(image, 0, dy, 0, dx, cv2.BORDER_CONSTANT) if dx or dy else image.copy()

        results = self.model(input_image, imgsz=self.img_size[::-1], verbose=False, device=self.device)[0]
        boxes = results.boxes.data

        if hasattr(boxes, "cpu"):
            boxes = boxes.cpu()
        return boxes.detach().numpy()[:, :-2]


cnn_analysis_method = CNNAnalysisMethod(WEIGHTS_PATH, (1408, 1984))