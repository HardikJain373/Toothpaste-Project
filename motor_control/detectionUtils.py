import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
from torch import where, round
from time import time

TOOTHPASTE_INDEX = 1
TOOTHBRUSH_INDEX = 0  

def find_state(model, camera_index=0, flip=True):
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        return Exception("Camera not found")
    
    fig, ax = plt.subplots()
    
    while(True):
        # height = get_state_from_camera(model, capture, flip, show_raw_video=True, show_processed_video=True, verbose=verbose)
        # length_toothpaste, length_toothbrush = find_length(model, capture, flip=True, show_raw_video=False, verbose=True)
        a=time()
        length_toothpaste, length_toothbrush, rate_toothpaste = find_rate_and_length(model, capture, flip=True, show_raw_video=False,  show_processed_video=True, verbose=True)
        b=time()
        print(f"FPS: {1/(b-a)}")
        print(f"Length of toothbrush is: {length_toothbrush} pixels!")
        print(f"Length of toothpaste is: {length_toothpaste} pixels!")
        print(f"Rate of toothpaste is: {rate_toothpaste} pixels/s!")
        if cv2.waitKey(10) & 0xFF == ord("q"):
            capture.release()
            break

    # return length_toothbrush, length_toothpaste, rate_toothpaste


# def find_length(model, capture, flip=True, show_raw_video=False, verbose=True):
#     # Capturing the frame
#     ret, frame = capture.read()
#     if not ret:
#         return Exception("Error, frame could not be read!")
    
#     # Flipping the frame if required
#     if(flip):
#         frame = cv2.flip(frame, 1)

#     # Converting the frame to RGB and processing it
#     frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     processed_frame = model(frame_RGB)
    
#     # Showing the frame as an image if required
#     if(show_raw_video):
#         cv2.imshow("Raw Video", frame)
    
#     if(TOOTHPASTE_INDEX in processed_frame[0].boxes.cls): # If x  the object even exists in the frame, we will proceed to find id for where the box is and obtain the height for it
#         idx = where(processed_frame[0].boxes.cls == TOOTHPASTE_INDEX)[0][0]
#         bounding_box = processed_frame[0].boxes.xyxy[idx]
#         length1 = round(bounding_box[2] - bounding_box[0], decimals=2)
#         if(verbose):
#             print(f"Toothpaste detected!, Length is: {length1} pixels!")
#     else: # Object not found in the frame
#         if(verbose):
#             print("Toothpaste NOT detected!")
#         length1 = 0

#     if(TOOTHBRUSH_INDEX in processed_frame[0].boxes.cls): # If x  the object even exists in the frame, we will proceed to find id for where the box is and obtain the height for it
#         idx = where(processed_frame[0].boxes.cls == TOOTHBRUSH_INDEX)[0][0]
#         bounding_box = processed_frame[0].boxes.xyxy[idx]
#         length2 = round(bounding_box[2] - bounding_box[0], decimals=2)
#         if(verbose):
#             print(f"Toothbrush detected!, Length is: {length2} pixels!")
#     else: # Object not found in the frame
#         if(verbose):
#             print("Toothbrush NOT detected!")
#         length2 = 0

#     return length1, length2


def find_rate_and_length(model, capture, flip=True, show_raw_video=False, show_processed_video=False, verbose=True):
    # Capturing the frame
    ret1, frame1 = capture.read()
    if not ret1:
        return Exception("Error, frame could not be read!")
    
    time1 = time()

    # Flipping the frame if required
    # if(flip):
    #     frame1 = cv2.flip(frame1, 1)

    # Converting the frame to RGB and processing it
    frame_RGB = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    processed_frame1 = model(frame_RGB)

    ret2, frame2 = capture.read()
    if not ret2:
        return Exception("Error, frame could not be read!")

    time2 = time()

    # Flipping the frame if required
    # if(flip):
    #     frame2 = cv2.flip(frame2, 1)

    # Converting the frame to RGB and processing it
    frame_RGB = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    processed_frame2 = model(frame_RGB)

    # Showing the raw video if required
    # if(show_raw_video):
    #     cv2.imshow("Raw Video", frame2)

    time_rate = time2 - time1

    if(TOOTHPASTE_INDEX in processed_frame1[0].boxes.cls): # If x  the object even exists in the frame, we will proceed to find id for where the box is and obtain the height for it
        idx = where(processed_frame1[0].boxes.cls == TOOTHPASTE_INDEX)[0][0]
        bounding_box = processed_frame1[0].boxes.xyxy[idx]
        length1 = round(bounding_box[2] - bounding_box[0], decimals=2)
        if(verbose):
            print(f"Toothpaste detected!, Length is: {length1} pixels!")
    else: # Object not found in the frame
        if(verbose):
            print("Toothpaste NOT detected!")
        length1 = 0

    if(TOOTHPASTE_INDEX in processed_frame2[0].boxes.cls): # If x  the object even exists in the frame, we will proceed to find id for where the box is and obtain the height for it
        idx = where(processed_frame2[0].boxes.cls == TOOTHPASTE_INDEX)[0][0]
        bounding_box = processed_frame2[0].boxes.xyxy[idx]
        length2 = round(bounding_box[2] - bounding_box[0], decimals=2)
        if(verbose):
            print(f"Toothpaste detected!, Length is: {length2} pixels!")
    else: # Object not found in the frame
        if(verbose):
            print("Toothpaste NOT detected!")
        length2 = 0

    if(TOOTHBRUSH_INDEX in processed_frame2[0].boxes.cls): # If x  the object even exists in the frame, we will proceed to find id for where the box is and obtain the height for it
        idx = where(processed_frame2[0].boxes.cls == TOOTHBRUSH_INDEX)[0][0]
        bounding_box = processed_frame2[0].boxes.xyxy[idx]
        length3 = round(bounding_box[2] - bounding_box[0], decimals=2)
        if(verbose):
            print(f"Toothbrush detected!, Length is: {length3} pixels!")
    else: # Object not found in the frame
        if(verbose):
            print("Toothbrush NOT detected!")
        length3 = 0

    rate = (length2 - length1)/time_rate

    # Showing the processed video if required
    if(show_processed_video):
        cv2.imshow("Annotated Video", cv2.cvtColor(processed_frame2[0].plot(), cv2.COLOR_RGB2BGR))

    return length2, length3, rate



# BIRD_INDEX = 67
# UPPER_PIPE_INDEX = 68
# LOWER_PIPE_INDEX = 69
# GROUND_INDEX = 70
# GAME_WINDOW_INDEX = 71


# def display_state_from_camera(model, camera_index=0, flip=True, verbose=True):
#     capture = cv2.VideoCapture(camera_index)
#     if not capture.isOpened():
#         return Exception("Camera not found")
    
#     fig, ax = plt.subplots()
    
#     while(True):
#         height = get_state_from_camera(model, capture, flip, show_raw_video=True, show_processed_video=True, verbose=verbose)
#         print(f"Height is: {height} pixels!")
#         if cv2.waitKey(10) & 0xFF == ord("q"):
#             capture.release()
#             break
        
# def get_state_from_camera(model, capture, flip=True, show_raw_video=False, show_processed_video=False, verbose=True):
#     # Taking the actual photo.
#     ret, frame = capture.read()
#     if not ret:
#         return Exception("Error, frame could not be read!")
        
#     # Flipping the frame if required
#     if(flip):
#         frame = cv2.flip(frame, 1)
        
#     # Converting the frame to RGB and processing it
#     frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     processed_frame = model(frame_RGB)
    
#     # Showing the raw video if required
#     if(show_raw_video):
#         cv2.imshow("Raw Video", frame)
    
        
#     # Figuring out the height of the object if it exists in this frame
#     if(BIRD_INDEX in processed_frame[0].boxes.cls): # If x  the object even exists in the frame, we will proceed to find id for where the box is and obtain the height for it
#         idx = where(processed_frame[0].boxes.cls == BIRD_INDEX)[0][0]
#         bounding_box = processed_frame[0].boxes.xyxy[idx]
#         height = round(bounding_box[3] - bounding_box[1], decimals=2)
#         if(verbose):
#             print(f"Object detected!, Height is: {height} pixels!")
#     else: # Object not found in the frame
#         if(verbose):
#             print("Object NOT detected!")
#         height = 0


#     # Showing the processed video if required
#     if(show_processed_video):
#         cv2.imshow("Annotated Video", cv2.cvtColor(processed_frame[0].plot(), cv2.COLOR_RGB2BGR))
        
#     return height



