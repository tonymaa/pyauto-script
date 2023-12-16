class WindowEntity:
    def __init__(self, **kwargs):
        self.handleNum = None
        self.selectWindow = True
        self.title = None
        self.width = None
        self.height = None
        self.resize = True
        self.__dict__.update(kwargs)

    def printObj(self):
        print(self.__dict__)