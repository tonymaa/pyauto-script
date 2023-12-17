
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
        self.delay = None
        self.position = None
        self.xy = None
        self.clickArea = None
        self.delayUpTime = None
        self.randomOffsetWhenUp = None
        self.loopCount = None
        self.loopDelayTime = None
        self.endDelayTime = None
        self.__dict__.update(kwargs)

    def printObj(self):
        print(self.__dict__)