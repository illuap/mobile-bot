import time

import cv2
import numpy as np
import pyautogui

import Logger
from engine.PreImageProcessor import GetInventoryOptionTextImg
from grabber.ApplicationImageGrabber import ApplicationImageGrabber
from models.Item import Item

dir = '.\images\\template\\'
applicationGrabber = ApplicationImageGrabber("Nox")
threshold = 0.92



#Grabs new SS and Selects the first image it found.
def GetPosByImageMatch(imageName):
    templateImg = cv2.imread(dir + imageName, 0)

    retryCount = 2

    for i in range(0,retryCount):
        appImg = applicationGrabber.get_image()
        appImg = cv2.cvtColor(appImg, cv2.COLOR_BGR2RGB)
        appImg_grey = cv2.cvtColor(appImg, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(appImg_grey, templateImg, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        pos = loc[::-1]

        if(len(pos[0]) > 0):
            break
        else:
            time.sleep(0.03)

    if(pos == None):
        Logger.log("Couldn't find Image {}.".format(imageName))
        return None
    else:
        Logger.log("Found Image {} at:".format(imageName))
        Logger.log(pos)
        return pos


def CheckByImageMatch(imageName):
    pos = GetPosByImageMatch(imageName)

    if(pos == None):
        Logger.log("Couldn't find Image {}.".format(imageName))
        return False
    else:
        Logger.log("Found Image {}.".format(imageName))
        return True

def ClickByImageMatch(imageName):
    pos = GetPosByImageMatch(imageName)

    if(pos == None):
        return

    #Select the first point.
    pyautogui.click(pos[0][0], pos[1][0])
    Logger.log("Clicked Image {}.".format(imageName))



# ==============================================================
#                Micro Helper Functions
# ==============================================================

def InventoryFilterScrollToUnlockedGear():
    Logger.log("Starting scroll.")

    scroll_times = 36
    for i in range(0,scroll_times):
        pyautogui.scroll(-10)
        time.sleep(0.005)

    Logger.log("Finished scrolling.")

# This could be smarter,
# add params to accept middle of screen
def ScrollToTopOfInventory(width = 1600, height = 900):
    Logger.log("Starting scroll.")

    scroll_times = 25
    pyautogui.moveTo(width/2, height/2)
    for i in range(0,scroll_times):
        pyautogui.scroll(10)
        time.sleep(0.005)

    Logger.log("Finished scrolling.")

def ScrollToNewRowInInventory(width = 1600, height = 900):
    scroll_times = 8
    pyautogui.moveTo(width/2, height/2)
    for i in range(0,scroll_times):
        pyautogui.scroll(-10)
        time.sleep(0.005)

def ClickByImageMatch_filter():
    ClickByImageMatch("buttons\\filter.png")

def ClickByImageMatch_swift_darkness_filter():
    ClickByImageMatch("buttons\\swift_darkness_filter.png")

def ClickByImageMatch_unlockedgear_filter():
    ClickByImageMatch("buttons\\unlockedgear_filter.png")

def ClickByImageMatch_ok_filter():
    ClickByImageMatch("buttons\\ok_filter.png")

def ClickByImageMatch_grind():
    ClickByImageMatch("buttons\\grind.png")

def ClickByImageMatch_start_to_grind():
    ClickByImageMatch("buttons\\start_to_grind.png")

def ClickByImageMatch_yes_grind():
    ClickByImageMatch("buttons\\yes_grind.png")

def CheckByImageMatch_end_of_inventory():
    CheckByImageMatch("buttons\\empty_item.png")

# ==============================================================
#                   Business Specific
# ==============================================================
def FilterIventoryBySwiftDarkGear():
    time.sleep(0.01)
    ClickByImageMatch_filter()
    time.sleep(0.01)
    ClickByImageMatch_swift_darkness_filter()
    time.sleep(0.01)
    InventoryFilterScrollToUnlockedGear()
    time.sleep(0.1)
    ClickByImageMatch_unlockedgear_filter()
    time.sleep(0.02)
    ClickByImageMatch_ok_filter()
    time.sleep(0.05)
    ScrollToTopOfInventory()

def GetItemsOnScreenFromTemplates(imgs):
    items = []

    applicationGrabber = ApplicationImageGrabber("Nox")
    inventoryImg = applicationGrabber.get_image()
    inventoryImg = cv2.cvtColor(inventoryImg, cv2.COLOR_BGR2RGB)
    inventoryImg_grey = cv2.cvtColor(inventoryImg, cv2.COLOR_BGR2GRAY)

    w, h = imgs[0].shape[::-1]

    for img in imgs:
        res = cv2.matchTemplate(inventoryImg_grey, img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.92
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(inventoryImg, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            # sanity check. (see if the previous is very close to the current one)
            exists = False
            for item in items:
                if (abs(item.x - pt[0]) < 10 and abs(item.y - pt[1]) < 10):
                    exists = True
                    break
            if (not exists):
                items.append(Item(pt[0], pt[1]))

    # cv2.imshow("asdasdasd", inventoryImg)
    # cv2.waitKey(0)

def HighlightEachItem(items):
    # Get item stats
    for item in items:
        pyautogui.mouseDown(item.x, item.y, button='left')
        time.sleep(0.4)
        inventoryImg = applicationGrabber.get_image()
        item.stats_img = GetInventoryOptionTextImg(inventoryImg)
        pyautogui.mouseUp(item.x, item.y, button='left')
        #cv2.imshow("asdasdasd2", item.stats_img)
        #cv2.waitKey(0)

    #cv2.imshow("asdasdasd2", cv2.cvtColor(items[0].stats_img, cv2.COLOR_BGR2RGB))
    #cv2.imwrite("item_stats.png", cv2.cvtColor(items[0].stats_img, cv2.COLOR_BGR2GRAY))
    #cv2.waitKey(0)