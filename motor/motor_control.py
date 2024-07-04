import motor_control_utils
from motor_control_utils import *
import serial
import time



# write_position(portHandler, packetHandler, 9000) # Increasing goal position lowers the screw

ser = serial.Serial('COM3', 9600)  # Arduino connected to COM3



def read_force():
    force_reading = None
    count = 0
    while force_reading == None:
        try:
            line = ser.readline().decode('utf-8').strip()
            futek_reading = float(line)
            force_reading = futek_reading * 111 / 1024
            print(f"Force Reading: {force_reading}")
        except ValueError:
            count+=1
            futek_reading = 0
            force_reading = None
    print(f"No. of invalid values skipped: {count}")
    return force_reading
        

def give_force_with_initialization(target_force, rate, initial, portHandler, packetHandler):

    # Initialize the motor
    initialize_motor_with_initial_position(portHandler, packetHandler, initial)
    
    # read futek sensor
    while True:

        ser.reset_input_buffer()
        force_reading = read_force()
                
        if(force_reading > target_force):
            curr_motor_pos = read_position(portHandler, packetHandler)
            write_position(portHandler, packetHandler, curr_motor_pos - rate)
        
        else:
            curr_motor_pos = read_position(portHandler, packetHandler)
            write_position(portHandler, packetHandler, curr_motor_pos + rate)




# give_force_with_initialization(0.02, 50, 9000)

# while True:
#     read_force()

def give_force(target_force, rate, portHandler, packetHandler):
    while True:
        
        ser.reset_input_buffer()
        force_reading = read_force()

        if(force_reading > target_force):
            curr_motor_pos = read_position(portHandler, packetHandler)
            write_position(portHandler, packetHandler, curr_motor_pos - rate)

        else:
            curr_motor_pos = read_position(portHandler, packetHandler)
            write_position(portHandler, packetHandler, curr_motor_pos + rate)















# while True:
#     while ser.in_waiting < 32:
#         continue
#     if ser.in_waiting > 0:
#         try:
#             line = ser.readline().decode('utf-8').strip()
#             futek_reading = float(line)
#             force_reading = futek_reading * 111 / 1024
#             print(f"Force Reading: {force_reading}")
#         except ValueError:
#             print(f"Received invalid data: {line}")
#             futek_reading = 0