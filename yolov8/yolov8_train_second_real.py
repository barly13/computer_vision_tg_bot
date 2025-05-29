from ultralytics import YOLO
 
model = YOLO('/yololib/yolov8/runs/detect/yolov8_first_pass8/weights/best.pt')

results = model.train(
   data='yolov8/real_dataset.yaml',
   imgsz=1984,
   epochs=63,
   batch=8,
   name='yolov8_second_pass',
   device=0)