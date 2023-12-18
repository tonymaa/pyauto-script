from model.ActionsEntity import ActionsEntity, ClickAction
from model.WindowEntity import WindowEntity
from win32gui import SetForegroundWindow, GetWindowRect
from typing import List
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
        x1, y1, x2, y2 = GetWindowRect(handleNum)
        # x += x1
        # y += y1
        # now_pos = position()  # 记录当前鼠标位置
        # # 鼠标移至目标
        # moveTo(x, y)
        # print(f"【debug】 x, y move to ({x}, {y})")
        # # mouth down
        # mouseDown()
        # # 延时时间计算
        # sleepTime = (process["delayUpTime"] / 1000) + (random() * process["delayRandomUpTime"] / 1000)
        # print(f"【debug】 sleep {sleepTime} second")
        # # 微小偏移
        # x += random() * process["randomOffsetWhenUp"]
        # x -= random() * process["randomOffsetWhenUp"]
        # y += random() * process["randomOffsetWhenUp"]
        # y -= random() * process["randomOffsetWhenUp"]
        # x = round(x)
        # y = round(y)
        # # move
        # moveTo(x, y, duration=sleepTime)
        # # mouth up
        # mouseUp()
        # # 鼠标回去
        # moveTo(now_pos[0], now_pos[1])
        # print(f"<br>【第 {i + 1} 次】点击坐标: [ {x} , {y} ] <br>窗口名称: [ {HandleUtils.get_handle_title(handleNum)} ]")



