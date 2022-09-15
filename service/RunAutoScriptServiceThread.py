
from threading import Thread
from service.AutoScriptService import AutoScriptService

class RunAutoScriptServiceThread (Thread):   #继承父类threading.Thread
    def __init__(self, hwnd, curProcess, customDir, windowWidth, windowHeight, isBackgroungRunning,
            isKeepActive, screenshotsInterval, matchingMethod, compressionRatio, allowAbs, selectedDeviceIndex, runningLog):
        Thread.__init__(self)
        self.hwnd = hwnd
        self.curProcess = curProcess
        self.customDir = customDir
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.isBackgroungRunning = isBackgroungRunning
        self.isKeepActive = isKeepActive
        self.screenshotsInterval = screenshotsInterval
        self.matchingMethod = matchingMethod
        self.compressionRatio = compressionRatio
        self.allowAbs = allowAbs
        self.selectedDeviceIndex = selectedDeviceIndex
        self.runningLog = runningLog

        self.autoScriptService = None

    def run(self):
        try:
            self.autoScriptService = AutoScriptService()
            self.autoScriptService.matching(hwnd=self.hwnd, processName=self.curProcess, customDir=self.customDir,
                            windowWidth=self.windowWidth, windowHeight=self.windowHeight,
                             isBackgroungRunning=self.isBackgroungRunning, isKeepActive=self.isKeepActive,
                            intervalScreenShot=self.screenshotsInterval, matchingMethod=self.matchingMethod,
                             compressionRatio=self.compressionRatio, allowAbs=self.allowAbs,
                                   selectedDeviceIndex=self.selectedDeviceIndex, debugMode=False, runningLog=self.runningLog)
        except Exception:
            import traceback
            traceback.print_exc()
            self.runningLog.append(f"{self.curProcess}文件有误！请检查后重启。")