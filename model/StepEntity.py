from typing import List

from model.TemplateEntity import TemplateEntity


class StepEntity:
    def __init__(self, **kwargs):
        self.name = None
        self.isAsync = None
        self.conditions = None
        self.onConditionIncorrect = None
        self.__dict__.update(kwargs)
        self.templates: List[TemplateEntity] = []
        print(kwargs["templates"])
        for template in kwargs["templates"]:
            self.templates.append(TemplateEntity(**template))

    def printObj(self):
        print(self.__dict__)