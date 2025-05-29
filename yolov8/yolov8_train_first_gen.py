from ultralytics import YOLO
 
model = YOLO('yolov8/yolov8n.pt')

results = model.train(
   data='yolov8/generated_dataset.yaml',
   imgsz=1952,
   epochs=10,
   batch=8,
   name='yolov8_first_pass',
   device=0)