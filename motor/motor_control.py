import motor_control_utils
from motor_control_utils import *
import serial
import time


# Initialize the motor
initialize_motor(portHandler, packetHandler)

# write_position(portHandler, packetHandler, 9000) # Increasing goal position lowers the screw

ser = serial.Serial('COM3', 9600)  # Arduino connected to COM3


def give_force(target_force, rate):
    
    # read futek sensor
    force_reading = 0
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            futek_reading = float(line)
            force_reading = futek_reading * 111 / 1024
            print(f"Force Reading: {force_reading}")
        except ValueError:
            print(f"Received invalid data: {line}")
            futek_reading = 0
            force_reading = 0
            
        
    if(force_reading > target_force):
        curr_motor_pos = read_position(portHandler, packetHandler)
        
        while(True):
            write_position(portHandler, packetHandler, curr_motor_pos - rate)
            curr_motor_pos = read_position(portHandler, packetHandler)
            
            # Reading the futek sensor
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                futek_reading = float(line)
                force_reading = futek_reading * 111 / 1024
                print(f"Force Reading: {force_reading}")
            
            if force_reading < target_force:
                break
            

    else:
        curr_motor_pos = read_position(portHandler, packetHandler)
        
        while(True):
            write_position(portHandler, packetHandler, curr_motor_pos + rate)
            curr_motor_pos = read_position(portHandler, packetHandler)

            # Reading the futek sensor
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                futek_reading = float(line)
                force_reading = futek_reading * 111 / 1024
                print(f"Force Reading: {force_reading}")
            
            if force_reading > target_force:
                break
            



# while True:
#     if ser.in_waiting > 0:
#         try:
#             line = ser.readline().decode('utf-8').strip()
#             futek_reading = float(line)
#             force_reading = futek_reading * 111 / 1024
#             print(f"Force Reading: {force_reading}")
#         except ValueError:
#             print(f"Received invalid data: {line}")
#             futek_reading = 0

give_force(1, 100)