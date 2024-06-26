# This module takes the image from the camera and processes it using the YOLOv8n model and then shows the detection in live video

import cv2
import sys
import matplotlib.pyplot as plt
import numpy as np
from detectionUtils import *
from ultralytics import YOLO


model = YOLO(r"C:/Personal/Robotics_Project/detection/runs\detect/train2/weights/best.pt")

# height = display_state_from_camera(model, camera_index=0, flip=True, verbose=True)
t = find_state(model, camera_index=0, flip=True)
# print(length_toothbrush, length_toothpaste, rate_toothpaste)