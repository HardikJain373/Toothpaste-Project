import motor_control_utils
from motor_control_utils import *
import serial


# Initialize the motor
initialize_motor(portHandler, packetHandler)

write_position(portHandler, packetHandler, 20000) # Increasing goal position lowers the screw

ser = serial.Serial('/dev/ttyUSB1', 9600)  # Arduino connected to COM3


def give_force(target_force):
    
    # read futek sensor
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            futek_reading = float(line)
            force_reading = futek_reading * 111 / 1024
            print(f"Futek Reading: {futek_reading}")
        except ValueError:
            print(f"Received invalid data: {line}")
            futek_reading = 0
            
        
    if(force_reading > target_force):
        curr_motor_pos = read_position(portHandler, packetHandler)
        
        while(True):
            write_position(portHandler, packetHandler, curr_motor_pos - 100)
            curr_motor_pos = read_position(portHandler, packetHandler)
            time.sleep(0.1)
            
            # Reading the futek sensor
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                futek_reading = float(line)
                force_reading = futek_reading * 111 / 1024
                print(f"Futek Reading: {futek_reading}")
            
            if futek_reading < target_force:
                break
    else:
        curr_motor_pos = read_position(portHandler, packetHandler)
        
        while(True):
            write_position(portHandler, packetHandler, curr_motor_pos + 100)
            curr_motor_pos = read_position(portHandler, packetHandler)
            time.sleep(0.1)
            
            # Reading the futek sensor
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                futek_reading = float(line)
                force_reading = futek_reading * 111 / 1024
                print(f"Futek Reading: {futek_reading}")
            
            if futek_reading > target_force:
                break
        
    
    

