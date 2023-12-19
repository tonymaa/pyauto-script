from model.ActionsEntity import ActionsEntity, ClickAction
from model.WindowEntity import WindowEntity
from win32gui import SetForegroundWindow, GetWindowRect
from typing import List
from pyautogui import position, moveTo, mouseDown, mouseUp
from utils.HandleUtils import HandleUtils
from constants.Constants import PositionTypeConstants
from random import random, randint
import time

class ActionsExecutor:
    def __init__(self, window: WindowEntity, actions: ActionsEntity, matchedPosition: List[int]):
        self.window = window
        self.actions = actions
        self.matchedPosition = matchedPosition

    def execute(self):
        # TODO: execute actions based on self.actions
        print(f"start execute actions: {self.actions.__dict__}")

        if self.actions.click is not None:
            click_action_executor = ClickActionExecutor(self.actions.click, self.window, self.matchedPosition)
            click_action_executor.execute()


class ClickActionExecutor:
    def __init__(self, clickAction: ClickAction, window: WindowEntity, matchedPosition: List[int]):
        self.window = window
        self.clickAction = clickAction
        self.matchedPosition = matchedPosition

    def execute(self):
        now_pos = position()  # 记录当前鼠标位置
        x, y = [0, 0]
        if self.clickAction.position == PositionTypeConstants.POSITION_ABSOLUTE:
            x, y = self.clickAction.xy
        else:
            x += self.matchedPosition[0] + self.clickAction.xy[0]
            y += self.matchedPosition[1] + self.clickAction.xy[1]
        x1, y1, x2, y2 = GetWindowRect(self.window.handleNum)
        x += x1
        y += y1
        for count in range(0, randint(self.clickAction.loopCount[0], self.clickAction.loopCount[1])):
            print(f"<br>【匹配坐标】: [ {x} , {y} ] <br>窗口名称: [ {self.window.title} ]， 第{count + 1}次循环")
            self.clickOnce(x + self.clickAction.clickArea[0] * random(), y + self.clickAction.clickArea[1] * random())
            time.sleep((self.clickAction.loopDelayTime[0] / 1000) + (random() * self.clickAction.loopDelayTime[1] / 1000))
        # # 鼠标回去
        moveTo(now_pos[0], now_pos[1])
        time.sleep((self.clickAction.endDelayTime[0] / 1000) + (random() * self.clickAction.endDelayTime[1] / 1000))

    def clickOnce(self, x, y):
        x = round(x)
        y = round(y)
        # # 鼠标移至目标
        moveTo(x, y)
        print(f"【debug】 x, y move to ({x}, {y})")
        # delay
        delay = (self.clickAction.delay[0] / 1000) + (random() * self.clickAction.delay[1] / 1000)
        time.sleep(delay)
        # # mouth down
        print(f"【debug】 mouse down")
        mouseDown()
        # # 延时时间计算
        delayUpTime = (self.clickAction.delayUpTime[0] / 1000) + (random() * self.clickAction.delayUpTime[1] / 1000)
        # 微小偏移 [-randomOffsetWhenUp[1], -randomOffsetWhenUp[0]] && [randomOffsetWhenUp[0], randomOffsetWhenUp[1]]
        randomOffset = lambda: (self.clickAction.randomOffsetWhenUp[0] +
                                (random() * (self.clickAction.randomOffsetWhenUp[1] -
                                             self.clickAction.randomOffsetWhenUp[
                                                 0]))
                                ) * (random() > 0.5 if 1 else -1)
        x += randomOffset()
        y += randomOffset()
        x = round(x)
        y = round(y)
        # move
        print(f"【debug】 sleep {delayUpTime} second")
        print(f"【debug】 x, y move to ({x}, {y})")
        moveTo(x, y, duration=delayUpTime)
        # # mouth up
        print(f"【debug】 mouse up")
        mouseUp()
