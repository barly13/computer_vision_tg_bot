import yaml
import time
from pathlib import Path
import os
import cv2
import numpy as np
import random
import time

def flip(img):
    return cv2.flip(img, 1)

def add_noise(img, mean, std):
    noise = np.random.normal(mean, std, img.shape)
    return img + noise

def add_blur(img, kernel_size):
    return cv2.blur(img, (kernel_size, kernel_size))

if __name__ == '__main__':
    config_path = Path(os.getcwd()) / 'utils' / 'augmentations_config.yml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    random.seed()
    common_rng = np.random.default_rng(seed=config['common']['seed'])
    blur_rng = np.random.default_rng(seed=config['blur']['seed'])
    noise_rng = np.random.default_rng(seed=config['noise']['seed'])

    in_folder = Path(config['common']['input-dir'])
    out_folder = Path(config['common']['output-dir'])
    os.makedirs(out_folder, exist_ok=True)

    files = [f for f in in_folder.iterdir()]
    files_num = int(len(files) * config['common']['augmentation-part'])
    files = common_rng.choice(files, files_num)
    for file in files:
        image = cv2.imread(str(file))
        if config['common']['apply-y-flip']:
            image = flip(image)
        if config['blur']['enable']:
            kernel = blur_rng.integers(config['blur']['kernel-size-min'], 
                                   config['blur']['kernel-size-min'], 
                                   1, endpoint=True)[0]
            image = add_blur(image, kernel)
        if config['noise']['enable']:
            mean = noise_rng.integers(config['noise']['mean-min'], 
                                     config['noise']['mean-max'], 
                                     1, endpoint=True)[0]
            std = noise_rng.integers(config['noise']['std-min'], 
                                     config['noise']['std-max'], 
                                     1, endpoint=True)[0]
            image = add_noise(image, mean, std)

        timestamp_ms = int(time.time() * 1000)
        out_file = out_folder / f'{file.stem}_mod_{timestamp_ms}.png'
        cv2.imwrite(str(out_file), image)
    