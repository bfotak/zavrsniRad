import cv2
import numpy as np
import mjerenjeObjekta
def empty(a):
    pass

def sliderKonture():
    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 640, 240)#problematicno(nezz jel samo prikaz)
    cv2.createTrackbar("Threshold1", "Parameters", 23, 255, empty)
    cv2.createTrackbar("Threshold2", "Parameters", 20, 255, empty)
    cv2.createTrackbar("Area", "Parameters", 1000, 30000, empty)

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        numberOfPixels = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if numberOfPixels > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
            area = mjerenjeObjekta.površina(numberOfPixels)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area))+ "cm^2", (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

def mainContours(img):

    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img, (5, 5), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil, imgContour)

    cv2.imshow("Canny", imgCanny)
    cv2.imshow("Dil", imgDil)
    cv2.imshow("Contour", imgContour)
    return imgContour
