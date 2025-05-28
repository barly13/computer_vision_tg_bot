from ultralytics import YOLO
import cv2

#weights = '/yololib/yolov8/runs/detect/yolov8_first_pass8/weights/best.pt'
weights = '/yololib/yolov8/runs/detect/yolov8_second_pass4/weights/best.pt'

def visualize_detection(image, detections, class_names, colors=None):
    if colors is None:
        colors = [(0, 255, 0)] * len(class_names)
    
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    for det in detections:
        x1, y1, x2, y2, conf, cls_id = det
        cls_id = int(cls_id) - 1
        
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        
        color = colors[cls_id % len(colors)]
        label = f"{class_names[cls_id+1]}: {conf:.2f}"
        
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        
        (label_width, label_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        
        cv2.rectangle(image, 
                     (x1, y1 - label_height - 10),
                     (x1 + label_width, y1),
                     color, -1)
        
        cv2.putText(image, label, 
                   (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    return image

if __name__ == '__main__':
    model = YOLO(weights)
    #model.conf = 0.1
    model.img_size = 1984
    #model.iou = 0.45
    model.classes = model.names

    #image_test_path = 'datasets/generated_datasets/test/images/1748377492195_mod_1748377648174.jpg'
    image_test_path = 'gen/images/1748450490701.jpg'
    #image_test_path = 'datasets/BCCD_Dataset_with_mask/test/images/f2574be3-81c6-4fc3-8a40-0230d1264f52.jpg'
    image = cv2.imread(image_test_path)

    results = model(image, imgsz=(image.shape[:2]), verbose=False)[0]
    results = results.boxes.data.cpu().detach().numpy()
    output_image = visualize_detection(image, results, list(model.names.values()))
    cv2.imwrite('test5.jpg', output_image)
