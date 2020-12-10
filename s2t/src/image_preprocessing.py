import cv2 as cv
import sys

# path = "test-img/hand.jpg"
path = './data/A/gurpreet7.jpg'
img = cv.imread(path)
if img is None:
    sys.exit("could not display image")

# imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
blur = cv.GaussianBlur(img, (5,5), 1)
blur = cv.medianBlur(blur, 7)
gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
thresh = cv.merge((thresh,thresh,thresh))
thresh = cv.cvtColor(thresh, cv.COLOR_BGR2GRAY)
# thresh = thresh[y:y+h, x:x+w]

cv.imshow("Display window", gray)

interrupt = cv.waitKey(0)
if interrupt & 0xFF == ord('q'):
    exit()
