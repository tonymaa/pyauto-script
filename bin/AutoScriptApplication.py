import os
import time
from numpy import uint8, fromfile
import cv2

from utils.DoClickUtils import DoClickUtils
from utils.ImageUtils import ImageUtils
from utils.PositionUtils import PositionUtils, GetPosBySiftMatch
from utils.ProcessesInfoUtils import ProcessesInfoUtils
from utils.ScreenCaptureUtils import ScreenCaptureUtils
from utils.HandleUtils import HandleUtils
import win32gui



"""
    intervalSelectWindow: 几秒时间去选择窗口，并定位到此窗口
    processName: 循环遍历该文件夹下的图片模板
    windowWidth: resize窗口后的宽度
    windowHeight: resize窗口后的高度
    isBackgroungRunning: 是否后台运行，某些窗口不兼容后台运行
    isKeepActive: 非后台运行时，是否保持窗口在最顶层
    intervalScreenShot: 每间隔多少毫秒截一次图
    matchingMethod: 匹配算法：#1 模板匹配；#2 sift特征点匹配
    windowName: 可选参数，指定窗口的名字，找不到则选择窗口
    customDir: 所有图片模板的工作路径
    compressionRatio: 截图压缩率，(0, 1] 浮点类型
"""
def main(intervalSelectWindow, processName, windowWidth, windowHeight,
         isBackgroungRunning, isKeepActive, intervalScreenShot,
         matchingMethod = 1, windowName = None, customDir=".\\process", compressionRatio = 0.5):
    # 1. 点击目标窗口/输入目标窗口 获取窗口句柄
    # windows
    hwnd = None
    if windowName is not None:
        hwnd = HandleUtils.find_windows_by_title(windowName)
    if hwnd is None:
        hwnd = HandleUtils.get_active_window(intervalSelectWindow) # ('Service Development Studio - Google Chrome', 67596)
    
    # Android phone
    # print(HandleSet.adb_device_status()) # (True, ['258905d3'])
    # 窗口左上，右下坐标
    # print(GetWindowRect(67596)) # (46, 24, 1234, 1019) left, top, right, bottom

    # 2. 将目标窗口resize成固定大小，如： height: 300, width: 500
    win32gui.MoveWindow(hwnd[1],0,0,windowWidth,windowHeight,True)

    # 4. 当匹配上模板文件夹（放置在指定目录下）中的其中一个时，读取该模板图片的文件名，
    # 5. 解析一些信息
    processesInfo = ProcessesInfoUtils.get(processName, customDir)
    # print(processesInfo)
    # 6. 循环截图目标窗口，将截图与模板图片进行匹配（模板图片是截图中的一小部分，预处理时需保证分辨率一致）
    while True:
        time.sleep(intervalScreenShot / 1000)
        # capture screen
        screen = None
        # 是否后台运行
        if isBackgroungRunning:
            screen = ScreenCaptureUtils.window_screen(hwnd[1]) # 后台截图
        else:
            screen = ScreenCaptureUtils.front_window_screen(hwnd[1], isKeepActive) # 前台截图
        screenSift = None
        # 采用sift算法
        if matchingMethod == 2:
            screenSift = ImageUtils.get_sift(screen)
        # 截图压缩
        originalScreenWidth = screen.shape[1]
        originalScreenHeight = screen.shape[0]
        if compressionRatio != 1:
            screen = ImageUtils.img_compress(screen, compressionRatio)

        # ImageUtils.show_img(screen)
        # ImageUtils.save_img(screen)
        # capture phone screen
        # GetScreenCapture.adb_screen("258905d3")
        # compare template
        for process in processesInfo:
            matchingPosition = None
            try:
                # 模板匹配
                if matchingMethod == 1:
                    # 模板压缩
                    template = process.get("image")
                    if compressionRatio != 1:
                        template = ImageUtils.img_compress(template, compressionRatio)
                    matchingPosition = PositionUtils.template_matching(screen, template, originalScreenWidth, originalScreenHeight, process.get("threshold"))
                    if matchingPosition is None:
                        continue
                # 特征点查找
                elif matchingMethod == 2:
                    matchingPosition = GetPosBySiftMatch.sift_matching(process.get("sift"), screenSift, (screen[0], screen[1]), process.get("image"), screen, True)
                    if matchingPosition is None:
                        continue
            except Exception:
                import traceback
                traceback.print_exc()
                print(f"【error】 matching error... try again")
                break
            print(f"【debug】 matching position: ({matchingPosition[0]}, {matchingPosition[1]})")
            # 7. do click
            if isBackgroungRunning:
                DoClickUtils.doWindowsClick(hwnd[1], process, matchingPosition)
            else:
                DoClickUtils.doFrontWindowsClick(hwnd[1], process, matchingPosition, isKeepActive)

if __name__ == "__main__":
    # main(3, "egp", 800, 700, False, True, 800, matchingMethod=1, compressionRatio=1)

    deviceStatus, deviceIds = HandleUtils.adb_device_status()
    if deviceStatus:
        selectedDevice = 0
        screen = ScreenCaptureUtils.adb_screen(deviceIds[selectedDevice])
    #     ImageUtils.show_img(screen)
        # adb shell input swipe x y sleepTime toX toY
        x = 100
        y = 100
        sleepTime = 1000
        toX = 300
        toY = 300
        device_id = deviceIds[selectedDevice]
        command = rf'.\utils\adb.exe -s {device_id} shell input swipe {x} {y} {sleepTime} {toX} {toY}'
        HandleUtils.deal_cmd(command)
        print(f"<br>点击设备 [ {device_id} ] 坐标: [ {toX} , {toY} ]")