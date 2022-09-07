from service.AutoScriptService import AutoScriptService

if __name__ == '__main__':
    AutoScriptService.startMatching(intervalSelectWindow=3, processName="egp", windowWidth=800, windowHeight=700,
         isBackgroungRunning=True, isKeepActive=False, intervalScreenShot=800, matchingMethod=2,
         compressionRatio=1, allowAbs=False, selectedDeviceIndex=0, debugMode=False)