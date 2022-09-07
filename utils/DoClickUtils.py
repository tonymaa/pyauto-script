# -*- coding: utf-8 -*-
import time
import random
import win32com.client
from win32gui import SetForegroundWindow, GetWindowRect
from win32api import MAKELONG, SendMessage
from win32con import WM_LBUTTONUP, WM_LBUTTONDOWN, WM_ACTIVATE, WA_ACTIVE
from pyautogui import position, click, moveTo, mouseDown, mouseUp
from utils.HandleUtils import HandleUtils

class DoClickUtils:
    def __init__(self): pass

    def doInvoke(invokePath):
        with open(".\\process\\egp\\finishEvent.py", mode="r", encoding="utf-8") as r:
            exec(r.read())


    @staticmethod
    def doWindowsClick(handleNum, process, matchingPosition):
        if process is None: return False

        # load事件调用
        print(f"【debug】 invoke function matchEvent")
        try:
            if process["matchEvent"] != None and process["matchEvent"] != "":
                DoClickUtils.doInvoke(process["matchEvent"])
        except Exception: pass

        # 延时
        sleepTime = (process["delayTime"] / 1000) + (random.random() * process["randomDelayTime"] / 1000)
        print(f"【debug】 sleep {sleepTime} second")
        time.sleep(sleepTime) # sleep

        loopTimes = process["loopLeastCount"] + round(random.random() * process["loopRandomCount"])
        for i in range(loopTimes):
            # 一次点击
            # 鼠标移动到指定位置
            x = 0
            y = 0
            if process["useMatchingPosition"] == 1:
                x = process["relativeClickPosition"][0]
                y = process["relativeClickPosition"][1]
            else:
                x = matchingPosition[0]
                y = matchingPosition[1]

            x += round(random.random() * process["randomRightOffset"])
            y += round(random.random() * process["randomBottomOffset"])
            print(f"【debug】 x, y move to ({x}, {y})")

            # 鼠标按下
            position = MAKELONG(x, y)
            SendMessage(handleNum, WM_ACTIVATE, WA_ACTIVE, 0)
            SendMessage(handleNum, WM_LBUTTONDOWN, 0, position)  # 模拟鼠标按下
            print(f"【debug】 click down at ({x}, {y})")
            # 延时
            sleepTime = (process["delayUpTime"] / 1000) + (random.random() * process["delayRandomUpTime"] / 1000)
            print(f"【debug】 sleep {sleepTime} second")
            time.sleep(sleepTime)

            # 微小偏移
            x += random.random() * process["randomOffsetWhenUp"]
            x -= random.random() * process["randomOffsetWhenUp"]
            y += random.random() * process["randomOffsetWhenUp"]
            y -= random.random() * process["randomOffsetWhenUp"]
            x = round(x)
            y = round(y)
            print(f"【debug】 click up at ({x}, {y})")

            # 鼠标抬起
            position = MAKELONG(x, y)
            SendMessage(handleNum, WM_LBUTTONUP, 0, position)  # 模拟鼠标弹起
            print(f"<br>【第 {i + 1} 次】点击坐标: [ {x} , {y} ] <br>窗口名称: [ {HandleUtils.get_handle_title(handleNum)} ]")

            # 点击一次后的延时
            sleepTime = (process["loopDelayLeastTime"] / 1000) + (random.random() * process["loopDelayRandomTime"] / 1000)
            print(f"【debug】 sleep {sleepTime} second")
            time.sleep(sleepTime)

        # 结束延时
        sleepTime = (process["endDelayLeastTime"] / 1000) + (random.random() * process["endDelayRandomTime"] / 1000)
        print(f"【debug】 sleep {sleepTime} second")
        time.sleep(sleepTime)

        # 结束事件调用
        print(f"【debug】 invoke function finishEvent")
        try:
            if process["finishEvent"] != None and process["finishEvent"] != "":
                DoClickUtils.doInvoke(process["finishEvent"])
        except Exception: pass

    @staticmethod
    def doFrontWindowsClick(handleNum, process, matchingPosition, isKeepActive):
        if process is None: return False

        # load事件调用
        print(f"【debug】 invoke function matchEvent")
        try:
            if process["matchEvent"] != None and process["matchEvent"] != "":
                DoClickUtils.doInvoke(process["matchEvent"])
        except Exception: pass

        # 延时
        sleepTime = (process["delayTime"] / 1000) + (random.random() * process["randomDelayTime"] / 1000)
        print(f"【debug】 sleep {sleepTime} second")
        time.sleep(sleepTime) # sleep

        loopTimes = process["loopLeastCount"] + round(random.random() * process["loopRandomCount"])
        for i in range(loopTimes):
            # 一次点击
            # 窗口置顶
            if isKeepActive:
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                SetForegroundWindow(handleNum)
            # 鼠标移动到指定位置
            x = 0
            y = 0
            if process["useMatchingPosition"] == 1:
                x = process["relativeClickPosition"][0]
                y = process["relativeClickPosition"][1]
            else:
                x = matchingPosition[0]
                y = matchingPosition[1]
            x += round(random.random() * process["randomRightOffset"])
            y += round(random.random() * process["randomBottomOffset"])


            now_pos = position() # 记录当前鼠标位置
            # 鼠标移至目标
            moveTo(x, y)
            print(f"【debug】 x, y move to ({x}, {y})")
            # mouth down
            mouseDown()
            # 延时时间计算
            sleepTime = (process["delayUpTime"] / 1000) + (random.random() * process["delayRandomUpTime"] / 1000)
            print(f"【debug】 sleep {sleepTime} second")
            # 微小偏移
            x += random.random() * process["randomOffsetWhenUp"]
            x -= random.random() * process["randomOffsetWhenUp"]
            y += random.random() * process["randomOffsetWhenUp"]
            y -= random.random() * process["randomOffsetWhenUp"]
            x = round(x)
            y = round(y)
            # move
            moveTo(x, y, duration=sleepTime)
            # mouth up
            mouseUp()
            print(f"【debug】 click up at ({x}, {y})")

            print(f"<br>【第 {i + 1} 次】点击坐标: [ {x} , {y} ] <br>窗口名称: [ {HandleUtils.get_handle_title(handleNum)} ]")

            # 鼠标回去
            moveTo(now_pos[0], now_pos[1])

            # 点击一次后的延时
            sleepTime = (process["loopDelayLeastTime"] / 1000) + (random.random() * process["loopDelayRandomTime"] / 1000)
            print(f"【debug】 sleep {sleepTime} second")
            time.sleep(sleepTime)

        # 结束延时
        sleepTime = (process["endDelayLeastTime"] / 1000) + (random.random() * process["endDelayRandomTime"] / 1000)
        print(f"【debug】 sleep {sleepTime} second")
        time.sleep(sleepTime)

        # 结束事件调用
        print(f"【debug】 invoke function finishEvent")
        try:
            if process["finishEvent"] != None and process["finishEvent"] != "":
                DoClickUtils.doInvoke(process["finishEvent"])
        except Exception: pass

    @staticmethod
    def adb_click(device_id):
        """数据线连手机点击"""
        if process is None: return False

        # load事件调用
        print(f"【debug】 invoke function matchEvent")
        try:
            if process["matchEvent"] != None and process["matchEvent"] != "":
                DoClickUtils.doInvoke(process["matchEvent"])
        except Exception: pass

        # 延时
        sleepTime = (process["delayTime"] / 1000) + (random.random() * process["randomDelayTime"] / 1000)
        print(f"【debug】 sleep {sleepTime} second")
        time.sleep(sleepTime) # sleep

        loopTimes = process["loopLeastCount"] + round(random.random() * process["loopRandomCount"])
        for i in range(loopTimes):
            # 一次点击
            # 鼠标移动到指定位置
            x = 0
            y = 0
            if process["useMatchingPosition"] == 1:
                x = process["relativeClickPosition"][0]
                y = process["relativeClickPosition"][1]
            else:
                x = matchingPosition[0]
                y = matchingPosition[1]

            x += round(random.random() * process["randomRightOffset"])
            y += round(random.random() * process["randomBottomOffset"])

            # 延时
            sleepTime = process["delayUpTime"] + (random.random() * process["delayRandomUpTime"])

            # 微小偏移
            toX = x + random.random() * process["randomOffsetWhenUp"]
            toX -= random.random() * process["randomOffsetWhenUp"]
            toY = y + random.random() * process["randomOffsetWhenUp"]
            toY -= random.random() * process["randomOffsetWhenUp"]
            toX = round(toX)
            toY = round(toY)

            # adb shell input swipe x y sleepTime toX toY
            command = rf'.\utils\adb.exe -s {device_id} shell input swipe {x} {y} {sleepTime} {toX} {toY}'
            HandleUtils.deal_cmd(command)
            print(f"<br>点击设备 [ {device_id} ] 坐标: [ {toX} , {toY} ]")

            # 点击一次后的延时
            sleepTime = (process["loopDelayLeastTime"] / 1000) + (random.random() * process["loopDelayRandomTime"] / 1000)
            print(f"【debug】 sleep {sleepTime} second")
            time.sleep(sleepTime)

        # 结束延时
        sleepTime = (process["endDelayLeastTime"] / 1000) + (random.random() * process["endDelayRandomTime"] / 1000)
        print(f"【debug】 sleep {sleepTime} second")
        time.sleep(sleepTime)

        # 结束事件调用
        print(f"【debug】 invoke function finishEvent")
        try:
            if process["finishEvent"] != None and process["finishEvent"] != "":
                DoClickUtils.doInvoke(process["finishEvent"])
        except Exception: pass
        # if self.pos is not None:
        #     # 使用modules下的adb工具执行adb命令
        #     command = abspath(dirname(__file__)) + rf'\adb.exe -s {device_id} shell input tap {cx} {cy}'
        #     HandleSet.deal_cmd(command)
        #     # system(command)
        #     print(f"<br>点击设备 [ {device_id} ] 坐标: [ {cx} , {cy} ]")
        #     return True


