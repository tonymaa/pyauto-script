# -*- coding: utf-8 -*-
import time
import random
import win32com.client
from win32gui import SetForegroundWindow, GetWindowRect
from win32api import MAKELONG, SendMessage
from win32con import WM_LBUTTONUP, WM_LBUTTONDOWN, WM_ACTIVATE, WA_ACTIVE
from pyautogui import position, click, moveTo, mouseDown, mouseUp
from utils.HandleUtils import HandleUtils


def windowsClickOnce(x, y, process, handleNum, i):
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

def frontWindowsClickOnce(x, y, process, handleNum, i, isKeepActive):
    # 窗口置顶
    if isKeepActive:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        SetForegroundWindow(handleNum)
    now_pos = position()  # 记录当前鼠标位置
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
    # 鼠标回去
    moveTo(now_pos[0], now_pos[1])
    print(f"<br>【第 {i + 1} 次】点击坐标: [ {x} , {y} ] <br>窗口名称: [ {HandleUtils.get_handle_title(handleNum)} ]")

def adbClickOnce(x, y, process, device_id, i):
    # 延时
    sleepTime = round(process["delayUpTime"] + (random.random() * process["delayRandomUpTime"]))

    # 微小偏移
    toX = x + random.random() * process["randomOffsetWhenUp"]
    toX -= random.random() * process["randomOffsetWhenUp"]
    toY = y + random.random() * process["randomOffsetWhenUp"]
    toY -= random.random() * process["randomOffsetWhenUp"]
    toX = round(toX)
    toY = round(toY)

    # adb shell input swipe x y sleepTime toX toY
    command = rf'.\utils\adb.exe -s {device_id} shell input swipe {x} {y} {toX} {toY} {sleepTime}'
    # command = rf'.\utils\adb.exe -s {device_id} shell input tap {x} {y}'
    # print(command)
    HandleUtils.deal_cmd(command)
    print(f"<br>【第 {i + 1} 次】点击设备 [ {device_id} ] 坐标: [ {toX} , {toY} ]")

"""
    mode: #1 windows后台点击；#2 windows前台点击；#3 连接安装手机点击
    x: 坐标x
    y: 坐标y
    process: 当前流程
    matchingPosition: 当process的点击坐标模式设置是找图找到的坐标时，使用该坐标
    handleNum: 窗口句柄
    i: 循环变量，打印日志用的
    isKeepActive: 保持窗口active状态，当mode为2是启用
"""
def distributeClick(mode, process, matchingPosition, handleNum, isKeepActive, eventAttribute):
    if process is None: return False
    eventAttribute.setCurProcess(process)
    eventAttribute.setCurMatchingPosition(matchingPosition)
    # load事件调用
    print(f"【debug】 invoke function matchEvent")
    try:
        if process["matchEvent"] != None and process["matchEvent"] != "":
            DoClickUtils.doInvoke(process["matchEvent"], eventAttribute)
    except Exception:
        pass

    # 延时
    sleepTime = (process["delayTime"] / 1000) + (random.random() * process["randomDelayTime"] / 1000)
    print(f"【debug】 sleep {sleepTime} second")
    time.sleep(sleepTime)  # sleep

    loopTimes = process["loopLeastCount"] + round(random.random() * process["loopRandomCount"])
    for i in range(loopTimes):
        # 一次点击

        # 读取process的坐标点击模式（去点击找图匹配的坐标，还是预定义的坐标）
        x = 0
        y = 0
        if process["useMatchingPosition"] == 1: # 预定义的坐标
            x = process["relativeClickPosition"][0]
            y = process["relativeClickPosition"][1]
        else: # 找图找到的坐标
            x = matchingPosition[0]
            y = matchingPosition[1]
        x += round(random.random() * process["randomRightOffset"])
        y += round(random.random() * process["randomBottomOffset"])

        # 点击分发
        if mode == 1:
            windowsClickOnce(x, y, process, handleNum, i)
        elif mode == 2:
            frontWindowsClickOnce(x, y, process, handleNum, i, isKeepActive)
        elif mode == 3:
            adbClickOnce(x, y, process, handleNum, i)

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
            DoClickUtils.doInvoke(process["finishEvent"], eventAttribute)
    except Exception:
        pass


class DoClickUtils:
    def __init__(self): pass

    def doInvoke(invokePath, eventAttribute):
        with open(invokePath, mode="r", encoding="utf-8") as r:
            exec(r.read(), {"eventAttribute": eventAttribute})

    @staticmethod
    def doWindowsClick(handleNum, process, matchingPosition, eventAttribute):
        distributeClick(1, process, matchingPosition, handleNum, None, eventAttribute)

    @staticmethod
    def doFrontWindowsClick(handleNum, process, matchingPosition, isKeepActive, eventAttribute):
        distributeClick(2, process, matchingPosition, handleNum, isKeepActive, eventAttribute)

    @staticmethod
    def adb_click(device_id, process, matchingPosition, eventAttribute):
        distributeClick(3, process, matchingPosition, device_id, None, eventAttribute)



