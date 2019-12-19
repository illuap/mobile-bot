import cv2
import numpy as np

from const.Colour import Colour

DEBUG = True

MAIN_SCREEN_LOWER_HSV = np.array([0,0,180])
#MAIN_SCREEN_LOWER_HSV = cv2.cvtColor(MAIN_SCREEN_LOWER_RGB, cv2.COLOR_RGB2HSV)
MAIN_SCREEN_UPPER_HSV = np.array([30,120,255])
#MAIN_SCREEN_UPPER_HSV = cv2.cvtColor(MAIN_SCREEN_UPPER_RGB, cv2.COLOR_RGB2HSV)

def Get_Colour_Mask(img, lower_hsv, upper_hsv):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    imask = mask > 0
    colourMask = np.zeros_like(img, np.uint8)
    colourMask[imask] = img[imask]

    if(DEBUG):
        cv2.imshow("Text Detection", colourMask)
        cv2.waitKey(0)


    return colourMask

def Get_Outlined_Text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshhold
    ret,bin = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)

    # closing
    kernel = np.ones((3,3),np.uint8)
    closing = cv2.morphologyEx(bin, cv2.MORPH_CLOSE, kernel)

    # invert black/white
    inv = cv2.bitwise_not(closing)

    if(DEBUG):
        cv2.imshow("Text Detection", inv)
        cv2.waitKey(0)


    return inv


def GetInventoryOptionTextImg(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, Colour.OPTIONTEXT_LOWER_HSV, Colour.OPTIONTEXT_UPPER_HSV)
    res = cv2.bitwise_and(img, img, mask=mask)

    return res