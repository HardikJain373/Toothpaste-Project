import numpy as np
from detection import detection, detectionUtils
from ultralytics import YOLO


model = YOLO(r"motor_control/runs/detect/train3/weights/best.pt")

target = detectionUtils.find_target_length(model, camera_index=0)
print(f"Target length is: {target} pixels!")


length, rate = detectionUtils.find_state(model, camera_index=0)

while(length < 0.9 * target):
    length, rate = detectionUtils.find_state(model, camera_index=0)
    print(f"Current length is: {length} pixels!")
    print(f"Current rate is: {rate} pixels/s!")
    
    # Take action
    
    # Find force to be given
    
    # Apply force
    
     
    
    
