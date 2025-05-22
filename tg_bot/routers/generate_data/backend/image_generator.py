import os
import random

import cv2
import numpy as np

from natsort import natsorted
from io import BytesIO

from typing import Tuple, Dict, List


class ImageGenerator:
    def __init__(self, image_size: Tuple[int, int] = (400, 600), num_images: int = 3, elements_per_image: int = 100):
        self.__image_size = image_size
        self.__num_images = num_images
        self.__elements_per_image = elements_per_image
        self.images = []

    async def generate(self, patterns_path: str) -> List[BytesIO]:
        pattern_files = self.__load_patterns(patterns_path)

        for _ in range(self.__num_images):
            composite = self.__assemble_images(pattern_files)
            self.images.append(composite)

        images_bytes = []

        for image in self.images:
            _, buffer = cv2.imencode('.png', image)
            img_bytes = BytesIO(buffer.tobytes())
            images_bytes.append(img_bytes)

        return images_bytes

    @staticmethod
    def __load_patterns(patterns_path: str) -> Dict[str, List[str]]:
        categorized = {}

        for dirpath, _, filenames in os.walk(patterns_path):
            if filenames:
                label = os.path.normpath(dirpath)
                categorized[label] = natsorted([
                    os.path.join(label, file) for file in filenames
                ])

        return categorized

    def __assemble_images(self, pattern_files: Dict[str, List[str]]) -> np.ndarray:
        positions = self.__random_positions()

        background = cv2.imread(random.choice(list(pattern_files.values())[0]))
        overlay = cv2.imread(random.choice(list(pattern_files.values())[1]), cv2.IMREAD_UNCHANGED)

        background = cv2.resize(background, self.__image_size, interpolation=cv2.INTER_CUBIC)

        for h, w in positions:
            background = self.__blend_element(background, overlay, (h, w))

        return background

    def __random_positions(self) -> List[Tuple[int, int]]:
        h_max, w_max = self.__image_size
        margin_h = int(h_max * 0.01)
        margin_w = int(w_max * 0.01)

        return [
            (random.randint(0, h_max - margin_h), random.randint(0, w_max - margin_w))
            for _ in range(self.__elements_per_image)
        ]

    def __blend_element(self, base: np.ndarray, element: np.ndarray, top_left: Tuple[int, int]) -> np.ndarray:
        scale = round(random.uniform(0.05, 0.20), 2)
        min_dim = min(self.__image_size)
        new_dim = int(min_dim * scale)

        element = cv2.resize(element, (new_dim, new_dim), interpolation=cv2.INTER_CUBIC)
        element, h, w = self.__apply_rotation(element, new_dim, new_dim)

        h_end = min(top_left[0] + h, base.shape[0])
        w_end = min(top_left[1] + w, base.shape[1])

        crop_h = h_end - top_left[0]
        crop_w = w_end - top_left[1]

        if crop_h <= 0 or crop_w <= 0:
            return base

        element = element[:crop_h, :crop_w]
        base_slice = base[top_left[0]:h_end, top_left[1]:w_end]

        rgb = element[:, :, :3]
        if element.shape[2] < 4:
            alpha = np.ones((crop_h, crop_w), dtype=np.float32)
        else:
            alpha = element[:, :, 3] / 255.0

        for c in range(3):
            base_slice[:, :, c] = (1 - alpha) * base_slice[:, :, c] + alpha * rgb[:, :, c]

        base[top_left[0]:h_end, top_left[1]:w_end] = base_slice
        return base

    @staticmethod
    def __apply_rotation(img: np.ndarray, h: int, w: int) -> Tuple[np.ndarray, int, int]:
        angle = random.randint(0, 90)
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        cos, sin = abs(matrix[0, 0]), abs(matrix[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        matrix[0, 2] += (new_w / 2) - center[0]
        matrix[1, 2] += (new_h / 2) - center[1]

        rotated = cv2.warpAffine(img, matrix, (new_w, new_h))
        return rotated, new_h, new_w
