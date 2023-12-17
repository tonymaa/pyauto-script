class TemplateEntity:
    def __init__(self, **kwargs):
        self.onConditionCorrect = None
        self.condition = None
        self.area = None
        self.required = None
        self.src = None
        self.__dict__.update(kwargs)

    def printObj(self):
        print(self.__dict__)