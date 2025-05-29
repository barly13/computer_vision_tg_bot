from abc import ABC, abstractmethod

import numpy as np


class AnalysisMethodBase(ABC):
    @abstractmethod
    def execute(self, image: np.ndarray):
        pass
