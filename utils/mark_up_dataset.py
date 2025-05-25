import cv2
import numpy as np
from pathlib import Path
import os

def find_bounding_boxes(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f'{image_path} wrong path')

    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bboxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bboxes.append((0, (x + w / 2) / WIDTH, (y + h / 2) / HEIGHT, w / WIDTH, h / HEIGHT)) 
    return bboxes

if __name__ == '__main__':
    input_dirs = ('datasets/BCCD_Dataset_with_mask/train', 
                  'datasets/BCCD_Dataset_with_mask/test')
    WIDTH = 1944
    HEIGHT = 1383
    for in_dir in input_dirs:
        os.makedirs(Path(in_dir) / 'labels', exist_ok=True)

        in_folder = Path(in_dir) / 'mask'
        out_folder = Path(in_dir) / 'labels'

        for file in in_folder.iterdir():
            bboxes = find_bounding_boxes(str(file))
            with open(str(out_folder / f'{file.stem}.txt'), 'w') as f:
                for bbox in bboxes:
                    f.write(' '.join(map(str, bbox)) + '\n')

