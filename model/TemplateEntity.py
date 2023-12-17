from typing import List


class TemplateEntity:
    def __init__(self, **kwargs):
        self.onConditionCorrect = None
        self.area = None
        self.required = None
        self.src = None
        self.__dict__.update(kwargs)
        self.condition: TemplateCondition = TemplateCondition(**kwargs["condition"])

    def printObj(self):
        print(self.__dict__)


class TemplateCondition(object):
    def __init__(self, **kwargs):
        self.requireAllMethods = False
        self.__dict__.update(kwargs)
        self.matchingMethods: List[TemplateConditionMethod] = []
        for method in kwargs["matchingMethods"]:
            self.matchingMethods.append(TemplateConditionMethod(**method))

    def printObj(self):
        print(self.__dict__)


class TemplateConditionMethod(object):
    def __init__(self, **kwargs):
        self.method = None
        self.required = None
        self.operator = None
        self.threshold = None
        self.__dict__.update(kwargs)

    def printObj(self):
        print(self.__dict__)
