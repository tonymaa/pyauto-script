# -*- coding: utf-8 -*-
# @Link    : https://github.com/aicezam/SmartOnmyoji
# @Version : Python3.7.6
# @MIT License Copyright (c) 2022 ACE
import time
from os.path import abspath, dirname
from time import sleep
import random
import win32com.client
from win32gui import SetForegroundWindow, GetWindowRect
from win32api import MAKELONG, SendMessage
from win32con import WM_LBUTTONUP, WM_LBUTTONDOWN, WM_ACTIVATE, WA_ACTIVE
import math
from pyautogui import position, click, moveTo
from utils.HandleSetUtils import HandleSet

class DoClickUtils:
    def __init__(self): pass

    def doInvoke(invokePath):
        with open(".\\process\\egp\\finishEvent.py", mode="r", encoding="utf-8") as r:
            exec(r.read())

    @staticmethod
    def doWindowsClick(handleNum, process):
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
            x = process["relativeClickPosition"][0]
            y = process["relativeClickPosition"][1]
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
            print(f"<br>【第 {i + 1} 次】点击坐标: [ {x} , {y} ] <br>窗口名称: [ {HandleSet.get_handle_title(handleNum)} ]")

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

    # def adb_click(self, device_id):
    #     """数据线连手机点击"""
    #     if self.pos is not None:
    #         pos = self.pos
    #         click_deviation = int(self.click_deviation)
    #         px = random.randint(-click_deviation - 5, click_deviation + 5)  # 设置随机偏移范围，避免封号
    #         py = random.randint(-click_deviation - 5, click_deviation + 5)
    #         cx = int(px + pos[0])
    #         cy = int(py + pos[1])
    #         # 使用modules下的adb工具执行adb命令
    #         command = abspath(dirname(__file__)) + rf'\adb.exe -s {device_id} shell input tap {cx} {cy}'
    #         HandleSet.deal_cmd(command)
    #         # system(command)
    #         print(f"<br>点击设备 [ {device_id} ] 坐标: [ {cx} , {cy} ]")
    #
    #         roll_num = random.randint(0, 99)
    #         if roll_num < 10:
    #             mx = random.randint(-50, 300) + cx
    #             my = random.randint(-50, 300) + cy
    #             sleep((random.randint(5, 15)) / 100)
    #             command = abspath(dirname(__file__)) + rf'\adb.exe -s {device_id} shell input tap {mx} {my}'
    #             HandleSet.deal_cmd(command)
    #             print(f"<br>点击设备 [ {device_id} ] 坐标: [ {mx} , {my} ]")
    #         elif 47 < roll_num < 50 or roll_num > 97:
    #             mx = random.randint(200, 1000)
    #             my = random.randint(200, 1000)
    #             sleep((random.randint(5, 15)) / 100)
    #             command = abspath(dirname(__file__)) + rf'\adb.exe -s {device_id} shell input tap {mx} {my}'
    #             HandleSet.deal_cmd(command)
    #             print(f"<br>点击设备 [ {device_id} ] 坐标: [ {mx} , {my} ]")
    #
    #         return True
    #
    # def windows_click_bk(self):
    #     """
    #     点击目标位置,只能前台点击（兼容所有窗体程序）
    #     """
    #     # 前台点击，窗口必须置顶，兼容所有窗口（模拟器、云游戏等）点击
    #     pos = self.pos
    #     handle_num = self.handle_num
    #     click_deviation = int(self.click_deviation)
    #     x1, y1, x2, y2 = GetWindowRect(handle_num)
    #
    #     # 设置随机偏移范围，避免封号
    #     px = random.randint(-click_deviation - 5, click_deviation + 5)
    #     py = random.randint(-click_deviation - 5, click_deviation + 5)
    #     cx = int(px + pos[0])
    #     cy = int(py + pos[1])
    #
    #     # 计算绝对坐标位置
    #     jx = cx + x1
    #     jy = cy + y1
    #
    #     # 把窗口置顶，并进行点击
    #     shell = win32com.client.Dispatch("WScript.Shell")
    #     shell.SendKeys('%')
    #     SetForegroundWindow(handle_num)
    #     sleep(0.2)  # 置顶后等0.2秒再点击
    #     now_pos = position()
    #     moveTo(jx, jy)  # 鼠标移至目标
    #     click(jx, jy)
    #
    #     moveTo(now_pos[0], now_pos[1])
    #
    #     print(f"<br>点击坐标: [ {cx} , {cy} ] 窗口名称: [ {HandleSet.get_handle_title(handle_num)} ]")
    #
    #     return True

# if __name__ == '__main__':
#     handle = HandleSet.get_active_window(3)
#     DoClickUtils.doWindowsClick(handle[1], [{'shape': (54, 227), 'filePath': '.\\process\\egp\\1000_200_508x517_175_38_20_5_3_1_1_1000_100_matchEvent_finishEvent.png', 'fileName': '1000_200_508x517_175_38_20_5_3_1_1_1000_100_matchEvent_finishEvent.png', 'sift': None, 'image': None, 'delayTime': 1000, 'randomDelayTime': 200, 'relativeClickPosition': [508, 517], 'randomRightOffset': 175, 'randomBottomOffset': 38, 'delayUpTime': 20, 'delayRandomUpTime': 5, 'randomOffsetWhenUp': 3, 'loopLeastCount': 1, 'loopRandomCount': 1, 'endDelayLeastTime': 1000, 'endDelayRandomTime': 100, 'matchEvent': '.\\process\\egp\\matchEvent.py', 'finishEvent': '.\\process\\egp\\finishEvent.py'}])

