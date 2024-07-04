import numpy as np
from detection import detection, detectionUtils
from ultralytics import YOLO
from motor.motor_control import *


model = YOLO(r"motor_control/runs/detect/train3/weights/best.pt")

target = detectionUtils.find_target_length(model, camera_index=0)
print(f"Target length is: {target} pixels!")

initialize_motor(portHandler, packetHandler)

length, rate = detectionUtils.find_state(model, camera_index=0)
force_given = 0.02
target_rate = 100

give_force(0.03, 50)

# while(length < 0.9 * target):
#     length, rate = detectionUtils.find_state(model, camera_index=0)
#     print(f"Current length is: {length} pixels!")
#     print(f"Current rate is: {rate} pixels/s!")
    
#     # Take action of increasing force
#     give_force_with_initialization()

    
#     # Find force to be given
    
#     # Apply force
    
     
    
    
