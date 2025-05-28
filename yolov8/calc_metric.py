from pathlib import Path
import numpy as np

inference_result = 'datasets/inference_results/1748455911.1898527'
labels = 'datasets/BCCD_Dataset_with_mask/test/labels'

if __name__ == '__main__':
    true_numbers = {}
    for file in Path(labels).iterdir():
        with open(file, 'r') as fp:
            true_numbers[file.stem] = sum(1 for line in fp)
        
    predict_numbers = {}
    for file in Path(inference_result).iterdir():
        with open(file, 'r') as fp:
            predict_numbers[file.stem] = sum(1 for line in fp)

    Y_true = []
    Y_pred = []
    for key in true_numbers.keys():
        Y_true.append(true_numbers[key])
        Y_pred.append(predict_numbers[key])
    
    RMSE = np.sqrt(np.square(np.subtract(Y_true, Y_pred)).mean())
    print(RMSE)