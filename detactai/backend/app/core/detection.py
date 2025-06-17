from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

model = YOLO("app/models/yolov8n.pt")

def detect_objects(image_path: str):
    """Process image and return detection results"""
    results = model(image_path)
    
    # Extract detection data
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                "class": model.names[int(box.cls)],
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist()
            })
    
    # Generate output image with boxes
    output_image = results[0].plot()
    output_path = f"app/temp/{Path(image_path).stem}_output.jpg"
    cv2.imwrite(output_path, output_image)
    
    return {
        "detections": detections,
        "output_path": output_path
    }
