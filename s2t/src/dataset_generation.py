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
            sign_dict_data[i] = "0"

    for i in string.ascii_uppercase:
        if not os.path.exists("data/" + i):
            os.makedirs("data/" + i)
            sign_dict_data[i] = "0"
else:
    with open("data/isl_dict_data.json") as f:
        sign_dict_data = json.load(f)




# print(sign_dict_data)
# sign_dict_info_json = json.dumps(sign_dict_info)
# print(sign_dict_info_json)
# # reading and displaying image
# img = cv.imread("test-img/hand.jpg")
# if img is None:
#     sys.exit("could not display image")
# cv.imshow("Display window", img)

# cv.waitKey(0)
# # to write/save image
# cv.imwrite("starry_night.png", img)

# start capturing the video stream
cap = cv.VideoCapture(0)
if not cap.isOpened():
    cprint("[Error] Cannot open camera", 'red')
    exit()
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

    interrupt = cv.waitKey(1)
    # if interrupt & 0xFF == ord('c'):
    #     cv.imwrite("data/0/a.jpg", roi)
    # Display the resulting frame
    cv.imshow('frame', frame)
    if interrupt & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

with open("data/isl_dict_data.json", 'w') as f:
    json.dump(sign_dict_data, f, indent=4)