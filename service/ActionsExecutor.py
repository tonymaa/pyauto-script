from model.ActionsEntity import ActionsEntity, ClickAction
from model.WindowEntity import WindowEntity
from win32gui import SetForegroundWindow, GetWindowRect
from typing import List
from pyautogui import position, moveTo, mouseDown, mouseUp
from utils.HandleUtils import HandleUtils

class ActionsExecutor:
    def __init__(self, window: WindowEntity, actions: ActionsEntity, matchedPosition: List[int]):
        self.window = window
        self.actions = actions
        self.matchedPosition = matchedPosition

    def execute(self):
        # TODO: execute actions based on self.actions
        print(f"start execute actions: {self.actions.__dict__}")

        if self.actions.click is not None:
            click_action_executor = ClickActionExecutor(self.actions.click)
            click_action_executor.execute()


class ClickActionExecutor:
    def __init__(self, clickAction: ClickAction):
        self.clickAction = clickAction

    def execute(self):
        x, y = [0, 0]
        if self.clickAction.position == PositionTypeConstants.POSITION_RELATIVE:
            x, y = self.clickAction.xy
        x1, y1, x2, y2 = GetWindowRect(handleNum)
        x += x1
        y += y1
        now_pos = position()  # 记录当前鼠标位置
        # # 鼠标移至目标
        moveTo(x, y)
        print(f"【debug】 x, y move to ({x}, {y})")
        # delay
        delay = (self.clickAction.delay[0] / 1000) + (random() * self.clickAction.delay[1] / 1000)
        time.sleep(delay)
        # # mouth down
        mouseDown()
        # # 延时时间计算
        delayUpTime = (self.clickAction.delayUpTime[0] / 1000) + (random() * self.clickAction.delayUpTime[1] / 1000)
        print(f"【debug】 sleep {delayUpTime} second")
        # 微小偏移 [-randomOffsetWhenDown[1], -randomOffsetWhenDown[0]] && [randomOffsetWhenDown[0], randomOffsetWhenDown[1]]
        randomOffset = lambda: (self.clickAction.randomOffsetWhenUp[0] +
                            (random() * (self.clickAction.randomOffsetWhenDown[1] - self.clickAction.randomOffsetWhenUp[
                                0]))
                                ) * (random() > 0.5 if 1 else -1)
        x += randomOffset()
        y += randomOffset()
        x = round(x)
        y = round(y)
        # move
        moveTo(x, y, duration=sleepTime)
        # # mouth up
        mouseUp()
        # # 鼠标回去
        moveTo(now_pos[0], now_pos[1])
        print(f"<br>【点击坐标: [ {x} , {y} ] <br>窗口名称: [ {HandleUtils.get_handle_title(handleNum)} ]")
