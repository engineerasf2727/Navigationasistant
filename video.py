import cv2
import numpy as np
import math
import time
from ultralytics import YOLO  # YOLOv8 module

def estimate_distance(bbox_width, bbox_height):
    # For simplicity, assume the distance is inversely proportional to the box size
    # This is a basic estimation, you may use camera calibration for more accuracy
    focal_length = 1000  # Example focal length, modify based on camera setup
    known_width = 2.0  # Approximate width of the car (in meters)
    distance = (known_width * focal_length) / bbox_width  # Basic distance estimation
    return distance

def process_video():
    model = YOLO('weights/yolov8n.pt')
    cap = cv2.VideoCapture('video/video.mp4')
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return
    target_fps = 30
    frame_time = 1.0 / target_fps
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (1280, 720))
        results = model(resized_frame)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                conf = box.conf[0]  # Confidence score
                cls = int(box.cls[0])  # Class ID

                if model.names[cls] == 'car' and conf >= 0.5: #only draw bounding threshold >0.5
                    label = f'{model.names[cls]} {conf:.2f}'
                    