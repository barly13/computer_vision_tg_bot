from skimage.feature import graycomatrix, graycoprops
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import cv2
import numpy as np

from ..analysis_method_base import AnalysisMethodBase


class MLAnalysisMethod(AnalysisMethodBase):
    @staticmethod
    def extract_features(patch):
        features = []

        glcm = graycomatrix(patch, distances=[1], angles=[0, np.pi/4, np.pi/2], 
                            levels=256, symmetric=True, normed=True)
        for prop in ['contrast', 'energy', 'homogeneity', 'correlation']:
            features.extend(graycoprops(glcm, prop).ravel())
        
        hist_int = np.histogram(patch, bins=16, range=(0, 256))[0]
        features.extend(hist_int/np.sum(hist_int))
        
        return np.array(features)

    def count_cells_ml(image, patch_size=16, min_area=400):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 51)

        features = []
        positions = []
    
        for y in range(0, gray.shape[0] - patch_size, patch_size):
            for x in range(0, gray.shape[1] - patch_size, patch_size):
                patch = gray[y:y+patch_size, x:x+patch_size]
                features.append(MLAnalysisMethod.extract_features(patch))
                positions.append((x, y))

        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        kmeans = KMeans(n_clusters=2)
        labels = kmeans.fit_predict(features_scaled)
        
        cluster_stats = []
        for i in range(2):
            cluster_features = features_scaled[labels == i]
            cluster_stats.append({
                'mean_contrast': np.mean(cluster_features[:, 0]),
                'mean_energy': np.mean(cluster_features[:, 1]),
                'size': len(cluster_features)
            })
        
        cell_cluster = np.argmax([s['mean_contrast'] * s['mean_energy'] for s in cluster_stats])
        
        result = np.zeros_like(gray)
        for (x, y), label in zip(positions, labels):
            if label == cell_cluster:
                cv2.rectangle(result, (x, y), (x+patch_size, y+patch_size), 255, -1)
        
        kernel = np.ones((15, 15), np.uint8)
        result = cv2.erode(result,kernel,iterations = 1)

        contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        keep_contours = [contour for contour in contours if cv2.contourArea(contour) >= min_area]
        return keep_contours

    def execute(self, image: np.ndarray):
        return self.count_cells_ml(image)