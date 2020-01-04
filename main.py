import argparse
import math
import time

import cv2
import eel
import numpy as np
import pyautogui
from PIL import Image
from pytesseract import pytesseract

from Services.LOHService import LOHService
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


def main():
    dog = LOHService()

    eel.init('web')
    eel.start('main.html', block=False)

    while True:
        eel.sleep(10)

@eel.expose
def LOHrun():
    eel.setButtonState(True)
    LOH = LOHService()
    LOH.PerformPickBanPhase()
    eel.setButtonState(False)

@eel.expose
def FilterAndClearInventory():
    InventoryService.FilterIventoryBySwiftDarkGear()

    ClearInventory()

@eel.expose
def ClearInventory():

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


        #InventoryService.ClickByImageMatch_yes_grind()

    InventoryService.ClickByImageMatch_start_to_grind()

if __name__ == '__main__':
    main()
