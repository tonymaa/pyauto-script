class EventAttribute:
    def __init__(self):
        self.isProcessRunning = True
        self.curProcess = None
        self.curMatchingPosition = None
        self.allowAbs = False
        self.attribute = {}
        self.hwnd = None
        self.selectedDeviceIndex = 0
        self.runningLog = None

    def getWindowTitle(self):
        if self.hwnd is not None and not self.allowAbs: return self.hwnd[0]
        return None

    def getWindowsHandle(self):
        if not self.allowAbs and self.hwnd is not None: return self.hwnd[1]

    def getAbsDeviceId(self):
        if self.allowAbs and self.hwnd is not None and self.hwnd[0]: return self.hwnd[self.selectedDeviceIndex]

    def setHwnd(self, hwnd):
        self.hwnd = hwnd

    def getHwnd(self):
        return self.hwnd

    def setCurProcess(self, curProcess):
        self.curProcess = curProcess

    def getCurProcess(self):
        return self.curProcess

    def setCurMatchingPosition(self, matchingPosition):
        self.curMatchingPosition = matchingPosition

    def getCurMatchingPosition(self):
        return self.curMatchingPosition

    def getAttribute(self, key):
        return self.attribute.get(key)

    def addAttribute(self, key, value):
        self.attribute[key] = value

    def getProcessRunning(self):
        return self.isProcessRunning

    def terminateProcess(self):
        self.isProcessRunning = False