import cv2
import numpy as np
from pathlib import Path
import os

WIDTH = 1984
HEIGHT = 1408

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

    for in_dir in input_dirs:
        os.makedirs(Path(in_dir) / 'labels', exist_ok=True)
        os.makedirs(Path(in_dir) / 'images', exist_ok=True)
        images_folder = Path(in_dir) / 'images'
        orig_folder = Path(in_dir) / 'original'
        in_folder = Path(in_dir) / 'mask'
        out_folder = Path(in_dir) / 'labels'

        for file in in_folder.iterdir():
            bboxes = find_bounding_boxes(str(file))
            with open(str(out_folder / f'{file.stem}.txt'), 'w') as f:
                for bbox in bboxes:
                    f.write(' '.join(map(str, bbox)) + '\n')

        for file in orig_folder.iterdir():
            image = cv2.imread(str(file))
            dx = WIDTH - image.shape[1]
            dy = HEIGHT - image.shape[0]
            image = cv2.copyMakeBorder(image, 0, dy, 0, dx, cv2.BORDER_CONSTANT)
            cv2.imwrite(str(images_folder / f'{file.stem}.jpg'), image)

