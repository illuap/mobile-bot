import time

import cv2
import numpy as np
import pyautogui
from pytesseract import pytesseract

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

def HighlightEachItem(items):
    # Get item stats
    for i, item in enumerate(items):
        pyautogui.mouseDown(item.x, item.y, button='left')
        time.sleep(0.4)
        inventoryImg = applicationGrabber.get_image()
        items[i].stats_img = GetInventoryOptionTextImg(inventoryImg) #optimize the image to store?
        pyautogui.mouseUp(item.x, item.y, button='left')

def CheckEachItemStatsUsingCompVision(items):
    # Find and Send Text
    for i, item in enumerate(items):
        img = item.stats_img

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, threshold1 = cv2.threshold(img, 130, 130, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 10))
        closed = cv2.morphologyEx(threshold1, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, kernel, iterations=1)  # remove any noise
        closed = cv2.dilate(closed, kernel, iterations=2)  # thickens

        ctrs, hier = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        txt = []
        for cnt in ctrs:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = img[y - 5:y + h, x:x + w]
            #cv2.imshow("asdasdasd2", roi)
            #cv2.waitKey(0)
            txt.append(pytesseract.image_to_string(roi))
        items[i].stats_text_arr = txt
def ClickUselessItems(items):
    # Highlight all the useless ones
    counter = 0
    for item in items:
        if(not item.IsItemUseful()):
            time.sleep(0.25)
            counter = counter + 1
            pyautogui.click(item.x, item.y)
            Logger.log("clicked item")

    return counter

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
    time.sleep(0.2)

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
            #cv2.rectangle(inventoryImg, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            # sanity check. (see if the previous is very close to the current one)
            exists = False
            if(len(items) > 0):
                for item in items:
                    if (abs(item.x - pt[0]) < 10 and abs(item.y - pt[1]) < 10):
                        exists = True
                        break
            if (not exists):
                items.append(Item(pt[0], pt[1]))

    return items
    # cv2.imshow("asdasdasd", inventoryImg)
    # cv2.waitKey(0)
def SetItemsInfo(items):
    HighlightEachItem(items)
    CheckEachItemStatsUsingCompVision(items)
def GrindUselessItems(items):
    ClickByImageMatch_grind()

    # Highlight all the useless ones
    usefulItemCount = ClickUselessItems(items)

    if(usefulItemCount > 0):
        # find and click 'start to grind'
        ClickByImageMatch_start_to_grind()



# HighlightEachItem + CheckEachItemStats combined for more optimization
# NOT USED FOR SIMPLICITY
def GetOptionsFromItemCords(items):
    # Find and Send Text
    for i, item in enumerate(items):
        pyautogui.mouseDown(item.x, item.y, button='left')
        time.sleep(0.4)
        inventoryImg = applicationGrabber.get_image()
        img = GetInventoryOptionTextImg(inventoryImg)
        pyautogui.mouseUp(item.x, item.y, button='left')
        #img = item.stats_img

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, threshold1 = cv2.threshold(img, 130, 130, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 10))
        closed = cv2.morphologyEx(threshold1, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, kernel, iterations=1)  # remove any noise
        closed = cv2.dilate(closed, kernel, iterations=2)  # thickens

        ctrs, hier = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        txt = []
        for cnt in ctrs:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = img[y - 5:y + h, x:x + w]
            #cv2.imshow("asdasdasd2", roi)
            #cv2.waitKey(0)
            txt.append(pytesseract.image_to_string(roi))
        item.stats_text_arr = txt