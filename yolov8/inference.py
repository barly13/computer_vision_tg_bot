from ultralytics import YOLO
import time
from pathlib import Path
import os
import cv2

input_dir = 'datasets/BCCD_Dataset_with_mask/test/images'
output_dir = 'datasets/inference_results'

weights = '/yololib/yolov8/runs/detect/yolov8_second_pass4/weights/best.pt'

WIDTH = 1984
HEIGHT = 1408

if __name__ == '__main__':
    model = YOLO(weights)
    model.imgsz = WIDTH

    output_dir = Path(output_dir) / f'{time.time()}'
    os.makedirs(output_dir, exist_ok=True)

    for file in Path(input_dir).iterdir():
        image = cv2.imread(str(file))
        dx = WIDTH - image.shape[1]
        dy = HEIGHT - image.shape[0]
        if dx != 0 or dy != 0:
            image = cv2.copyMakeBorder(image, 0, dy, 0, dx, cv2.BORDER_CONSTANT)
        
        results = model(image, imgsz=(image.shape[:2]), verbose=False, device='cpu')[0]
        results = results.boxes.data.cpu().detach().numpy()

        with open(str(output_dir / f'{file.stem}.txt'), 'w') as f:
            for res in results:
                f.write(' '.join(map(str, res)) + '\n')

