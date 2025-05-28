import os
from typing import Tuple

import cv2
import numpy as np
from ultralytics import YOLO

from .analysis_method_base import AnalysisMethodBase


class CNNAnalysisMethod(AnalysisMethodBase):
    def __init__(self, weights: str, img_size: Tuple[int, int], device: int | str = 'cpu'):
        self.model = YOLO(weights)
        self.model.img_size = img_size[1]
        self.img_size = img_size
        self.device = device

    async def execute(self, image: np.ndarray) -> np.ndarray:
        dx = self.img_size[1] - image.shape[1]
        dy = self.img_size[0] - image.shape[0]

        input_image = image.copy()

        if dx != 0 or dy != 0:
            input_image = cv2.copyMakeBorder(image, 0, dy, 0, dx, cv2.BORDER_CONSTANT)
        results = self.model(input_image, imgsz=(input_image.shape[:2]), verbose=False, device=self.device)[0]
        if self.device != 'cpu':
            results = results.boxes.data.cpu().detach().numpy()

        else:
            results = results.boxes.data.detach().numpy()

        return results[:, :-2]


weights = os.path.join(os.getcwd(), 'tg_bot', 'routers', 'analysis_methods', 'backend', 'weights', 'best.pt')
cnn_analysis_method = CNNAnalysisMethod(weights, (1408, 1984))