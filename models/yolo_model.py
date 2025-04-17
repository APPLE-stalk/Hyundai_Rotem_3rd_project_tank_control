from ultralytics import YOLO

class objectDetector:
    def __init__(self, model_path = 'yolov8n.pt'):
        self.model = YOLO(model_path)
        
    def detect(self, image_path):
        results = self.model(image_path)
        return results