import cv2 as cv

img = cv.imread("test-img/hand.jpg")
if img is None:
    sys.exit("could not display image")

imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
blur = cv.GaussianBlur(imgHSV, (11,11), 0)
blur = cv.medianBlur(blur, 15)
gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
thresh = cv.merge((thresh,thresh,thresh))
thresh = cv.cvtColor(thresh, cv.COLOR_BGR2GRAY)
# thresh = thresh[y:y+h, x:x+w]

cv.imshow("Display window", thresh)

interrupt = cv.waitKey(0)
if interrupt & 0xFF == ord('q'):
    exit()
