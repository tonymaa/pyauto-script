import sys
from PyQt5 import QtWidgets
from service.Pys import Pys
def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    pys = Pys()
    app.aboutToQuit.connect(pys.closing)
    pys.setupUi(MainWindow)
    pys.built(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    # AutoScriptService.startMatching(intervalSelectWindow=3, processName="egp", windowWidth=800, windowHeight=700,
    #      isBackgroungRunning=True, isKeepActive=False, intervalScreenShot=800, matchingMethod=2,
    #      compressionRatio=1, allowAbs=False, selectedDeviceIndex=0, debugMode=False)