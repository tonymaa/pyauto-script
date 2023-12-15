class StepEntity:
    def __init__(self, **kwargs):
        self.name = None
        self.isAsync = None
        self.conditions = None
        self.onConditionIncorrect = None
        self.__dict__.update(kwargs)

    def printObj(self):
        print(self.__dict__)