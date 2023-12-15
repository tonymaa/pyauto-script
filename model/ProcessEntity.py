from model.StepEntity import StepEntity


class ProcessEntity:
    def __init__(self, **kwargs):
        self.isMainProcess = False
        self.name = None
        self.isAsync = False
        self.mainStep = None
        self.steps = None
        self.__dict__.update(kwargs)

    def printObj(self):
        print(self.__dict__)