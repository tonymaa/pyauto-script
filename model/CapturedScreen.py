class CapturedScreen(object):
    def __init__(self, **kwargs):
        self.originalWidth = None
        self.originalHeight = None
        self.screen = None
        self.sift = None
        self.__dict__.update(kwargs)

    def printObj(self):
        print(self.__dict__)