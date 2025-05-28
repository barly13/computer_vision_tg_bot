from abc import ABC, abstractmethod

import numpy as np


class AnalysisMethodBase(ABC):
    @abstractmethod
    async def execute(self, image: np.ndarray):
        pass
