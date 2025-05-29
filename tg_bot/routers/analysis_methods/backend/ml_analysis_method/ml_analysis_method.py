import os
from typing import Tuple

from skimage.feature import graycomatrix, graycoprops

from sklearn.cluster import KMeans

import cv2
import numpy as np

from ..analysis_method_base import AnalysisMethodBase


class MLAnalysisMethod(AnalysisMethodBase):
    @staticmethod
    def extract_glcm_features(patch):
        glcm = graycomatrix(patch, [1], [0], levels=256, symmetric=True, normed=True)
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        energy = graycoprops(glcm, 'energy')[0, 0]
        return [contrast, energy]

    def count_cells_glcm_clustering(self, image, patch_size=16):
        features = []
        positions = []

        for y in range(0, image.shape[0] - patch_size, patch_size):
            for x in range(0, image.shape[1] - patch_size, patch_size):
                patch = image[y:y + patch_size, x:x + patch_size]
                feat = self.extract_glcm_features(patch)
                features.append(feat)
                positions.append((x, y))

        features = np.array(features)
        kmeans = KMeans(n_clusters=2, random_state=0).fit(features)
        labels = kmeans.labels_

        # Определим кластер, соответствующий клеткам, как тот, у которого средняя контрастность выше
        cluster_means = [features[labels == i][:, 0].mean() for i in range(2)]
        cell_cluster = int(np.argmax(cluster_means))
        cell_patches = [pos for i, pos in enumerate(positions) if labels[i] == cell_cluster]

        return len(cell_patches), cell_patches

    def execute(self, image: np.ndarray):
        return self.count_cells_glcm_clustering(image)