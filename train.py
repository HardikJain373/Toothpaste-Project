from dynamixel_sdk import *

DEVICENAME              = 'COM4'             # Check which port is being used on your controller
                                             # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0"
# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Protocol version
PROTOCOL_VERSION        = 2.0

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Default setting
DXL_ID                  = 1                  # Dynamixel ID: 1
BAUDRATE                = 57600              # Dynamixel default baudrate : 57600
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()
    
ADDR_HARDWARE_ERROR_STATUS = 70
# Check for hardware errors
dxl_hardware_error, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_HARDWARE_ERROR_STATUS)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    if dxl_hardware_error != 0:
        print("Hardware Error Status: %d" % dxl_hardware_error)


import numpy as np
from detection import detection, detectionUtils
from ultralytics import YOLO
from motor.motor_control import *


model = YOLO(r"motor_control/runs/detect/train3/weights/best.pt")

target = detectionUtils.find_target_length(model, camera_index=0)
print(f"Target length is: {target} pixels!")

initialize_motor(portHandler, packetHandler)

length, rate = detectionUtils.find_state(model, camera_index=0)
target_rate = 100


while(length < 0.9 * target):
    length, rate = detectionUtils.find_state(model, camera_index=0)
    print(f"Current length is: {length} pixels!")
    print(f"Current rate is: {rate} pixels/s!")
    
    # Take action of increasing position
    









# give_force_with_initialization(0.5, 50, 9000, portHandler, packetHandler)
    
    
