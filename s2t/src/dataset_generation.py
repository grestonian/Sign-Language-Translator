import os
import cv2 as cv
import json
import sys
import string
from termcolor import colored, cprint
import time
print(cv.__version__)

# creating directory structure for the dataset
if not os.path.exists("data"):
    os.makedirs("data")
    sign_dict_data= dict()
    for i in string.digits:
        if not os.path.exists("data/" + i):
            os.makedirs("data/" + i)
            sign_dict_data[i] = 0

    for i in string.ascii_uppercase:
        if not os.path.exists("data/" + i):
            os.makedirs("data/" + i)
            sign_dict_data[i] = 0
else:
    with open("data/isl_dict_data.json") as f:
        sign_dict_data = json.load(f)

# start capturing the video stream
cap = cv.VideoCapture(0)
if not cap.isOpened():
    cprint("[Error] Cannot open camera", 'red')
    exit()

directory = "data/"
user_name = 'gurpreet'
max_roi_captures = 5
roi_capture_count = 1
key_captured_flag = False
wait_time = 5
delay_time = 2
first_delay = True

while True:
    # Capture frame by frame
    ret, frame = cap.read()
    # Simulating mirror image
    frame = cv.flip(frame, 1)

    # if frame is read correctly, ret is True
    if not ret:
        cprint("[Error] Can't receive frame (stream end?). Exiting ...", 'red')
        break

    # ----------------Our operations on the frame come here----------------
    # defining region of interest(for capturing hand signs)
    x1 = int(0.5 * frame.shape[1]) - 10
    y1 = 10
    x2 = frame.shape[1] - 10
    y2 = int(0.5 * frame.shape[1]) - 10

    # draw the ROI for user reference
    cv.rectangle(frame, (x1-1, y1-1), (x2, y2), (255,0,0), 1)
    # extract the ROI
    roi = frame[y1:y2, x1:x2]

    # ---------------LOGIC TO CAPTURE FRAMES AFTER A WAIT AND THEN DELAY REPEATEDLY -----------------
    # capture user key-press
    interrupt = cv.waitKey(1)
    
    if interrupt & 0xFF == 27:      # if key-pressed == 'ESC', EXIT!
        cprint('------- [EXITING APPLICATION] -------', 'red')
        break
    # if other keypressed (alpha/numeric), capture it and store it
    # once key is captured, no other key is captured once the frames have been captured
    if interrupt != 27 and interrupt != -1 and not key_captured_flag:
        key_captured = chr(interrupt).upper() if interrupt > 96 else chr(interrupt)
        print("CCAPTURED KEY: " + str(key_captured))
        key_captured_flag = True
        initial_time = time.time()
        delay_time_start = time.time()
    
    start_time = time.time()
    # checking if wait_time has passed after the key was pressed by user
    if key_captured_flag and (start_time - initial_time)  > (wait_time):
        if roi_capture_count <= max_roi_captures:   # checking count of captures in a single go
            if time.time() - delay_time_start >= delay_time:
                cprint("[Message] Writing image: "+ str(sign_dict_data[key_captured] + 1), 'green')
                cv.imwrite(directory + key_captured + '/' + user_name + str(sign_dict_data[key_captured] + 1) + ".jpg", roi)
                roi_capture_count += 1
                sign_dict_data[key_captured] += 1
                delay_time_start = time.time()
        else:
            key_captured_flag = False   # once images have been captured and stored, reset the flag
            roi_capture_count = 1
    elif key_captured_flag:             # countdown before image capturing starts
        cv.putText(frame, str(int(wait_time-(start_time - initial_time - 1))), (100, 100), cv.FONT_HERSHEY_PLAIN, 5, (0,255,255), 2)
    cv.imshow('frame', frame)



# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

# writing output file containing data about characters and count of their images
with open("data/isl_dict_data.json", 'w') as f:
    json.dump(sign_dict_data, f, indent=4)