import os
from typing import Tuple

import cv2
import numpy as np

from ..analysis_method_base import AnalysisMethodBase


class CVAnalysisMethod(AnalysisMethodBase):
    def execute(self, image: np.ndarray):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        _, threshold = cv2.threshold(opening, 150, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        circles = []

        for cnt in contours:
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [cnt], -1, 255, 1)

            circles_tmp = cv2.HoughCircles(
                mask,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=30,
                param1=150,
                param2=15,
                minRadius=30,
                maxRadius=65
            )

            if circles_tmp is not None:
                circles_tmp = np.round(circles_tmp[0, :]).astype('int')
                for c in circles_tmp:
                    if mask[c[1] - 1, c[0] - 1] == 0:
                        circles.append(c)

        return circles