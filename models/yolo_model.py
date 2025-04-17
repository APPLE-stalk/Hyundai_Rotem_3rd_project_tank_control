from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.target_classes = {
            0: "person",
            2: "car",
            7: "truck",
            15: "rock"
        }

    def detect(self, image_path):
        results = self.model(image_path)
        detections = results[0].boxes.data.cpu().numpy()

        filtered_results = []
        for box in detections:
            class_id = int(box[5])
            if class_id in self.target_classes:
                filtered_results.append({
                    'className': self.target_classes[class_id],
                    'bbox': [float(coord) for coord in box[:4]],
                    'confidence': float(box[4])
                })
        return filtered_results
