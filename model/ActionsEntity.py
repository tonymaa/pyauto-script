from typing import List
class ActionsEntity:
    def __init__(self, **kwargs):
        self.exit = None
        self.nextStep = None
        self.nextProcess = None
        self.click: ClickAction = ClickAction(**kwargs["click"])

    def printObj(self):
        print(self.__dict__)

class ClickAction:
    def __init__(self, **kwargs):
        self.delay: List[int] = None # ms
        self.position = None # absolute: 绝对坐标 , relative找到的图坐标
        self.xy: List[int] = None # [x, y]
        self.clickArea: List[int] = None # [width, height]
        self.delayUpTime: List[int] = None # ms
        self.randomOffsetWhenUp = None # 向各个方向的偏移量
        self.loopCount: List[int] = None # [count1, count2]点击循环 count1 ~ count2次
        self.loopDelayTime = None # ms
        self.endDelayTime = None
        self.__dict__.update(kwargs)

    def printObj(self):
        print(self.__dict__)