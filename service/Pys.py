import cv2
import win32gui
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import QButtonGroup
from PyQt5.QtGui import QImage
from subprocess import Popen, PIPE
from program.pys_ui import Ui_MainWindow
import os
import constant
from numpy import array
from utils.HandleUtils import HandleUtils
from utils.ImageUtils import ImageUtils
from utils.ScreenCaptureUtils import ScreenCaptureUtils
from win32gui import SetForegroundWindow, GetWindowRect
import win32com
from PIL import ImageGrab
import numpy as np
from service.AutoScriptService import AutoScriptService
from service.RunAutoScriptServiceThread import RunAutoScriptServiceThread
constant.WINDOWSMODE = 0
constant.ABSMODE = 1


class Pys(Ui_MainWindow):
    def __init__(self, parent=None):
        Ui_MainWindow.__init__(self)
        self.hwnd = None
        self.curWorkingDir = "./process"
        self.processes = []
        self.curProcess = None
        self.curMode = constant.WINDOWSMODE
        self.deviceIds = None
        self.selectedDeviceIndex = 0
        self.windowHandler = None
        self.windowWidth = 0
        self.windowHeight = 0
        self.phoneWidth = 0
        self.phoneHeight = 0
        self.runThread = None

    def built(self, mainWindow):
        self.initMode(mainWindow)
        self.initEvent()

    def initMode(self, mainWindow):
        selectDeviceRadioGroup = QButtonGroup(mainWindow)
        selectDeviceRadioGroup.addButton(self.radioWindows, 0)
        selectDeviceRadioGroup.addButton(self.radioABD, 1)
        self.radioWindows.setChecked(1)

        runningModeRadioGroup = QButtonGroup(mainWindow)
        runningModeRadioGroup.addButton(self.radioRunFront, 0)
        runningModeRadioGroup.addButton(self.raidoRunBack, 1)
        self.radioRunFront.setChecked(1)

        frontRunningModeActiveWindowRadioGroup = QButtonGroup(mainWindow)
        frontRunningModeActiveWindowRadioGroup.addButton(self.radioActiveYes, 0)
        frontRunningModeActiveWindowRadioGroup.addButton(self.radioActiveNo, 1)
        self.radioActiveNo.setChecked(1)

        matchingMethodRadioGroup = QButtonGroup(mainWindow)
        matchingMethodRadioGroup.addButton(self.radioTemplateMatch, 0)
        matchingMethodRadioGroup.addButton(self.radioSiftMatch, 1)
        self.radioTemplateMatch.setChecked(1)

        self.select_device_id.setDisabled(True)
        self.butRun.setDisabled(True)
        self.butStop.setDisabled(True)

        # slider
        self.compressScreentshots.setMaximum(100)
        self.compressScreentshots.setMinimum(1)
        self.compressScreentshots.setSingleStep(1)
        self.compressScreentshots.setValue(100)

        self.loadProcesses()



    def initEvent(self):
        self.radioWindows.toggled.connect(self.selectWindowsMode) # 切换设备
        self.selectWindow.clicked.connect(self.selectWindowsWindow)
        self.selectWorkingDir.clicked.connect(self.selectDir)
        self.select_mode.currentIndexChanged.connect(self.selectProcess)
        self.butRun.clicked.connect(self.runScript)
        self.butStop.clicked.connect(self.stopScript)
        self.select_device_id.currentIndexChanged.connect(self.selectDevice) # 选择abs设备
    def closing(self):
        pass

    def selectDevice(self, e):
        self.selectedDeviceIndex = e
        # self.screentshot.setDisabled(False)
        # self.save_template.setDisabled(False)
        print(f"【debug】 select device index: {self.selectedDeviceIndex}, and deviceId is {self.deviceIds[e] if e >= 0 and e < len(self.deviceIds) else 'None'}")
        if e >= 0 and e < len(self.deviceIds):
            self.runningLog.setText(f'【选中设备】 {self.deviceIds[e]}')

    def selectWindowsMode(self, e):
        self.curMode = constant.WINDOWSMODE if e else constant.ABSMODE
        self.select_device_id.setDisabled(self.curMode == constant.WINDOWSMODE)
        self.selectWindow.setDisabled(self.curMode == constant.ABSMODE)
        self.inputWindowTitle.setDisabled(self.curMode == constant.ABSMODE)
        self.windowWidthInput.setDisabled(self.curMode == constant.ABSMODE)
        self.windowHeightInput.setDisabled(self.curMode == constant.ABSMODE)

        if self.curMode == constant.ABSMODE:
            self.hwnd = HandleUtils.adb_device_status()
            status, deviceIds = self.hwnd
            self.select_device_id.clear()
            self.deviceIds = deviceIds
            if not status:
                self.select_device_id.addItem("no device detected!")
                self.runningLog.setText(f'【warning】 没找到任何设备！')
                return
            else:
                self.runningLog.setText(f'【info】 已切换到abs模式，请选择设备。')
                for deviceId in deviceIds:
                    self.select_device_id.addItem(deviceId)
        else:
            self.select_device_id.clear()
            self.runningLog.setText(f'【info】 已切换到windows模式，点击截图后，选择窗口。')

        # self.butRun.setDisabled(False)
        # self.butStop.setDisabled(False)

    def selectWindowsWindow(self):
        QtWidgets.QMessageBox.information(None, 'Info', f'请在5秒内选择窗口！')
        self.hwnd = HandleUtils.get_active_window(5)
        hand_win_title, hand_num = self.hwnd
        # print(hand_win_title)
        print(f"【debug】 select window title: {hand_win_title}, and handle is {hand_num}")
        # QtWidgets.QMessageBox.information(None, 'Info', f'【选中窗口】 {hand_win_title}')
        self.runningLog.setText(f'【选中窗口】 {hand_win_title}')
        self.windowHandler = hand_num
        self.butRun.setDisabled(False)
        self.butStop.setDisabled(False)
        self.windowWidthInput.setDisabled(False)
        self.windowHeightInput.setDisabled(False)

        try:
            self.windowHeight = int(self.windowHeightInput.text())
            self.windowWidth = int(self.windowWidthInput.text())
            if self.windowHeight <= 0 or self.windowWidth <= 0:
                QtWidgets.QMessageBox.information(None, 'warnning', f'宽或高输入不合法')
                return
        except Exception:
            QtWidgets.QMessageBox.information(None, 'warnning', f'宽或高输入不合法')
            return
        self.inputWindowTitle.setText("窗口标题：" + hand_win_title)
        win32gui.MoveWindow(self.windowHandler, 0, 0, self.windowWidth, self.windowHeight, True)

    def selectDir(self):
        curWorkingDir = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Working Directory")
        if curWorkingDir is None or curWorkingDir == "": return
        self.curWorkingDir = curWorkingDir
        print(f"【debug】 curWorkingDir: {self.curWorkingDir}")
        self.showWorkingDir.setText(self.curWorkingDir)
        self.loadProcesses()

    def loadProcesses(self):
        # 读取目录下所有文件
        self.select_mode.clear()
        files = os.listdir(self.curWorkingDir)
        self.processes = []
        for process in files:
            if os.path.isdir(os.path.join(self.curWorkingDir, process)):
                self.select_mode.addItem(process)
                self.processes.append(process)
        self.selectProcess(0)

    def selectProcess(self, e):
        if len(self.processes) >= 0 and e < len(self.processes) and e >= 0:
            self.curProcess = self.processes[e]
            print(f"【debug】 current process: {self.curProcess}")
            # 激活运行，停止
            self.butStop.setDisabled(False)
            self.butRun.setDisabled(False)

    def validateInput(self):
        pass

    def stopScript(self):
        if self.runThread is not None and self.runThread.autoScriptService is not None:
            self.runThread.autoScriptService.eventAttribute.terminateProcess()
            self.runningLog.setText("运行结束中...")
            self.runThread = None

    def runScript(self):
        if self.runThread is not None:
            QtWidgets.QMessageBox.information(None, 'Info', f'请先停止脚本!')
            return

        if self.hwnd is None or not self.hwnd[0]:
            QtWidgets.QMessageBox.information(None, 'warning', f'请选择窗口!')
            return
        self.validateInput()
        isBackgroungRunning = self.raidoRunBack.isChecked()
        isKeepActive = self.radioActiveYes.isChecked()
        screenshotsInterval = int(self.screenshotsInterval.text())
        matchingMethod = 1 if self.radioTemplateMatch.isChecked() else 2
        compressionRatio = self.compressScreentshots.value() / 100
        allowAbs = self.curMode == constant.ABSMODE



        self.runThread = RunAutoScriptServiceThread(self.hwnd, self.curProcess, self.curWorkingDir,
                            self.windowWidth, self.windowHeight,
                             isBackgroungRunning, isKeepActive,
                            screenshotsInterval, matchingMethod,
                             compressionRatio, allowAbs,
                                   self.selectedDeviceIndex, self.runningLog)
        self.runThread.setDaemon(True)
        self.runThread.start()
        self.runningLog.setText("脚本运行中...")

        # ass = AutoScriptService()
        # ass.matching(hwnd=self.hwnd, processName=self.curProcess, customDir=self.curWorkingDir,
        #                     windowWidth=self.windowWidth, windowHeight=self.windowHeight,
        #                      isBackgroungRunning=isBackgroungRunning, isKeepActive=isKeepActive,
        #                     intervalScreenShot=screenshotsInterval, matchingMethod=matchingMethod,
        #                      compressionRatio=compressionRatio, allowAbs=allowAbs,
        #                            selectedDeviceIndex=self.selectedDeviceIndex, debugMode=False)