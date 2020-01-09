import math
import os
import random
import time
from enum import Enum

import numpy as np
import pyautogui
from cv2 import cv2

import Logger
from Services.InventoryService import GetImgsInFolderByNumber
from grabber.ApplicationImageGrabber import ApplicationImageGrabber
from models.enum.ProcessEnum import Process

dir = '.\images\\LOH\\template\\'
applicationGrabber = ApplicationImageGrabber("Nox")

templateNames = [""]

RETRY_COUNT = 3
RETRY_TIME = 0.5

class LOHState(Enum):
    FIRST_BAN_FLAG = "first_ban.png"
    FIRST_PICK_ME_FLAG = "first_pick_me.png"
    ENEMY_PICK_FLAG = "enemy_pick.png"
    QUEUING = "lv.png"
    LAST_BAN_FLAG = "last_ban.png"
    BATTLE_LOADING = "battle_loading.png"
    BATTLING = "battling.png"
    READY_TO_DUEL_YES = "yes.png"
    READY_TO_DUEL_PAGE = "ready_to_duel.png"



'''
1) Ready to duel button
2) Confirm 'yes'
3) State lv.
4) 'new' challenger
5) State FirstBan
6) Find first ban char
7) 
'''
threshold = 0.85

class LOHService(object):

    ## Load images into memory
    stateDic = dict()
    heroIconBanList = list()
    heroIconPickList = list()
    select_ban_template = []

    def __init__(self):
        for state in (LOHState):
            fileName = state.value
            self.stateDic[fileName] = cv2.imread(dir + fileName, 0)
        Logger.log("Is the State dictionary: {}".format(self.stateDic.keys()))

        self.heroIconBanList = GetImgsInFolderByNumber(dir + "FirstBans\\")
        self.heroIconPickList = GetImgsInFolderByNumber(dir + "Picks\\")

        self.select_ban_template = cv2.imread(dir + "select_ban.png", 0)

    def PerformPickBanPhase(self):
        i = 0
        while(i <= RETRY_COUNT):
            screenImg = applicationGrabber.get_image()
            screenImg_post = cv2.cvtColor(cv2.cvtColor(screenImg, cv2.COLOR_BGR2RGB), cv2.COLOR_BGR2GRAY)

            state = self.CheckState(screenImg_post)

            if(state != None):
                nextStep = self.PerformStateActions(state, screenImg_post)
                i = 0
                if(nextStep == Process.EXIT):
                    return
            else:
                i += 1
            time.sleep(RETRY_TIME)

        Logger.log("Could not find any states after {} times. Stopping...".format(RETRY_COUNT))
        return

    def CheckState(self, screenImg):
        for state in self.stateDic.keys():
            res = cv2.matchTemplate(screenImg, self.stateDic[state], cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            pos = loc[::-1]

            if (len(pos[0]) > 0):
                Logger.log("Is in State: {}".format(state))
                return state
        Logger.log("Could not find any state.")
        return None


    def PerformStateActions(self, state, screenImg):
        if (state == LOHState.FIRST_BAN_FLAG.value):
            self.FirstBanHero(screenImg)
        elif (state == LOHState.FIRST_PICK_ME_FLAG.value):
            self.PlayerPick(screenImg)
        elif (state == LOHState.ENEMY_PICK_FLAG.value or state == LOHState.QUEUING.value):
            time.sleep(1)
        elif (state == LOHState.LAST_BAN_FLAG.value):
            self.LastBanHero(screenImg)
        elif (state == LOHState.READY_TO_DUEL_PAGE.value):
            ClickScreenImgUsingTemplateImg(screenImg, self.stateDic[LOHState.READY_TO_DUEL_PAGE.value])
            time.sleep(0.5) #wait for animations
        elif(state == LOHState.READY_TO_DUEL_YES.value):
            ClickScreenImgUsingTemplateImg(screenImg, self.stateDic[LOHState.READY_TO_DUEL_YES.value])
            time.sleep(0.5)
        elif (state == LOHState.BATTLE_LOADING.value or state == LOHState.BATTLING.value ):
            Logger.log("Entering Battle Phase.")
            return Process.EXIT
        return Process.CONTINUE

    def FirstBanHero(self, screenImg):
        Logger.log("Starting to ban first hero")
        FindFirstTemplateAndClick(screenImg, self.heroIconBanList)
        time.sleep(0.2)
        ClickScreenImgUsingTemplateImg(screenImg, self.select_ban_template)
        time.sleep(0.2)

    def LastBanHero(self, screenImg):
        Logger.log("Starting to ban last hero")
        # Banning the first hero
        xScale = 0.58125
        yScale = 0.36666
        height = screenImg.shape[0]
        width = screenImg.shape[1]
        pyautogui.click(abs(width * xScale), abs(height * yScale))
        time.sleep(0.2)

        ClickScreenImgUsingTemplateImg(screenImg, self.select_ban_template)
        time.sleep(0.2)

    def PlayerPick(self, screenImg):
        Logger.log("Starting to pick hero")
        FindFirstTemplateAndClick(screenImg, self.heroIconPickList)
        time.sleep(0.2)
        ClickScreenImgUsingTemplateImg(screenImg, self.select_ban_template)
        time.sleep(0.5)
        FindFirstTemplateAndClick(screenImg, self.heroIconBanList)
        time.sleep(0.2)
        ClickScreenImgUsingTemplateImg(screenImg, self.select_ban_template)
        time.sleep(0.2)

def FindFirstTemplateAndClick(screenImg, templateImgList):
    for templateImg in templateImgList:
        results = ClickScreenImgUsingTemplateImg(screenImg, templateImg)

        if(results):
            return

    Logger.log("Failed to find any template imgs.")
    return

def ClickScreenImgUsingTemplateImg(screenImg, templateImg, randomOffset = 10):
    res = cv2.matchTemplate(screenImg, templateImg, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    pos = loc[::-1]

    if (not len(pos[0]) > 0):
        Logger.log("Failed to find template Image")
        return False

    #Select the first point.
    randX = pos[0][0] + random.randint(0,randomOffset)
    randy = pos[1][0] + random.randint(0,randomOffset)
    pyautogui.click(randX, randy)
    Logger.log("Clicked Image around {},{}.".format(randX, randy))
    return True
