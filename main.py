import argparse
import math
import time

import cv2
import eel
import numpy as np
import pyautogui
from PIL import Image
from pytesseract import pytesseract

from const.Colour import Colour
from engine import DisplayEngine
from engine.ClickerEngine import ClickerEngine
from engine.DisplayEngine import display_dots_on_img, display_msg
from engine.ImageEngine import scan_image, scan_image2
from engine.PreImageProcessor import *
from grabber.ApplicationImageGrabber import ApplicationImageGrabber
from Services import InventoryService
from Services.InventoryService import InventoryFilterScrollToUnlockedGear
from models.Item import Item
from utility import ImageHelper
from utility.ImageHelper import GetSampleImage
# Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255].

def GetSwiftDarknessTemplateImages():
    dir = '.\images\\template\\'
    template_imgs_filename = [
        '1.png',
        '2.png',
        '3.png',
        '4.png',
        '5.png',
        '6.png',
        '7.png',
        '8.png',
        '9.png',
        '10.png',
        '11.png',
        '12.png',
        '13.png',
        '14.png',
        '15.png',
        '16.png',
        '17.png'
    ]
    template_imgs = [dir + filename for filename in template_imgs_filename]

    imgs = [cv2.imread(filename, 0) for filename in template_imgs]

    return imgs

@eel.expose
def blahblah(param):
    print(param)
    main8()
    print("done")

def main():
    eel.init('web')
    eel.start('main.html', block=False)


    while True:
        eel.sleep(10)


def main8():
    InventoryService.FilterIventoryBySwiftDarkGear()

    imgs = GetSwiftDarknessTemplateImages()

    atEnd = False
    count = 0
    InventoryService.ClickByImageMatch_grind()

    while(not atEnd):
        items = InventoryService.GetItemsOnScreenFromTemplates(imgs)

        # Get item stats
        InventoryService.SetItemsInfo(items)
        count = count + InventoryService.ClickUselessItems(items)

        # Draw Markers!
        applicationGrabber = ApplicationImageGrabber("Nox")
        img = applicationGrabber.get_image()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        nonErrorCords = []
        ErrorCords = []
        for item in items:
            if(not item.IsError()):
                nonErrorCords.append( (item.x,item.y) )
            else:
                ErrorCords.append((item.x, item.y))

        #temp = display_dots_on_img(img,nonErrorCords,(0,255,0))
        #final = display_dots_on_img(temp, ErrorCords, (0, 0, 255))
        temp = display_msg(img,nonErrorCords, "OK",(0,255,0))
        final = display_msg(temp, ErrorCords, "Error")
        #cv2.imshow("final", final)
        #cv2.waitKey(0)

        atEnd = InventoryService.CheckByImageMatch_end_of_inventory()
        if(not atEnd): #Scroll Down
            InventoryService.ScrollToNewRowInInventory()

        #InventoryService.GrindUselessItems(items)

        #InventoryService.ClickByImageMatch_yes_grind()

    InventoryService.ClickByImageMatch_start_to_grind()
    # move

def main4():
    img = cv2.imread('.\images\item_stats.png')

    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret , threshold1 = cv2.threshold(img, 130,130, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(40,10))
    closed = cv2.morphologyEx(threshold1, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, kernel, iterations=1) #remove any noise
    closed = cv2.dilate(closed, kernel, iterations=2) #thickens

    ctrs, hier = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    txt = []
    for cnt in ctrs:
        x, y, w, h = cv2.boundingRect(cnt)
        roi = img[y-5:y + h, x:x + w]
        txt.append(pytesseract.image_to_string(roi))
        print(txt)
    cv2.imshow('img', closed)
    cv2.waitKey(0)


def main3():
    last_time = time.time()
    while(True):
        AppImgGrabber = ApplicationImageGrabber("Nox")
        app_img = AppImgGrabber.get_image()

        hsv = cv2.cvtColor(app_img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, Colour.OPTIONTEXT_LOWER_HSV, Colour.OPTIONTEXT_UPPER_HSV)
        res = cv2.bitwise_and(app_img, app_img, mask=mask)

        print('loop took {} seconds '.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('noxviewer', cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        ##cv2.imshow('nox-viewer', res)
        if(cv2.waitKey(25) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break

def main2():
    #AppImgGrabber = ApplicationImageGrabber("Nox")
    #app_img = AppImgGrabber.get_image()


    app_img = Get_Outlined_Text(GetSampleImage("2"))#Get_Colour_Mask(GetSampleImage("1"),MAIN_SCREEN_LOWER_HSV,MAIN_SCREEN_UPPER_HSV)
    #black out certain areas of the given image
    #app_img[210:230, 350:440] = (0,0,0)


    #scan_image(app_img)


    #win_info = AppImgGrabber.window_info
    wh = tuple(GetSampleImage("1").shape[1::-1])
    scan_image2(cv2.cvtColor(app_img,cv2.COLOR_GRAY2RGB), wh[0], wh[1], "frozen_east_text_detection.pb")




    # doesn't reach here..


    #ClickerEngine(win_info['x'],win_info['y'],win_info['width'],win_info['height']).open_portal_precentage()

    #x = DisplayEngine.display_sample_text(win_info['x'] + math.floor(win_info['width']*0.59),
    #                                      win_info['y'] + math.floor(win_info['height']*0.90))


if __name__ == '__main__':
    main()