import os
import time
from numpy import uint8, fromfile
import cv2

from utils.DoClickUtils import DoClickUtils
from utils.ImageUtils import ImgProcess
from utils.PositionUtils import GetPosByTemplateMatch, GetPosBySiftMatch
from utils.ProcessesInfo import GetProcessesInfo
from utils.ScreenCaptureUtils import GetScreenCapture
from utils.HandleSetUtils import HandleSet
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
"""
def main(intervalSelectWindow, processName, windowWidth, windowHeight,
         isBackgroungRunning, isKeepActive, intervalScreenShot,
         matchingMethod = 1, windowName = None, customDir=".\\process"):
    # 1. 点击目标窗口/输入目标窗口 获取窗口句柄
    # windows
    hwnd = None
    if windowName is not None:
        hwnd = HandleSet.find_windows_by_title(windowName)
    if hwnd is None:
        hwnd = HandleSet.get_active_window(intervalSelectWindow) # ('Service Development Studio - Google Chrome', 67596)
    
    # Android phone
    # print(HandleSet.adb_device_status()) # (True, ['258905d3'])
    # 窗口左上，右下坐标
    # print(GetWindowRect(67596)) # (46, 24, 1234, 1019) left, top, right, bottom

    # 2. 将目标窗口resize成固定大小，如： height: 300, width: 500
    win32gui.MoveWindow(hwnd[1],0,0,windowWidth,windowHeight,True)

    # 4. 当匹配上模板文件夹（放置在指定目录下）中的其中一个时，读取该模板图片的文件名，
    # 5. 解析一些信息
    processesInfo = GetProcessesInfo.get(processName, customDir)
    # print(processesInfo)
    # 6. 循环截图目标窗口，将截图与模板图片进行匹配（模板图片是截图中的一小部分，预处理时需保证分辨率一致）
    while True:
        time.sleep(intervalScreenShot / 1000)
        # capture screen
        screen = None
        if isBackgroungRunning:
            screen = GetScreenCapture.window_screen(hwnd[1])
        else:
            screen = GetScreenCapture.front_window_screen(hwnd[1], isKeepActive)
        screenSift = None
        if matchingMethod == 2:
            screenSift = ImgProcess.get_sift(screen)
        # ImgProcess.show_img(screen)
        # ImgProcess.save_img(screen)
        # capture phone screen
        # GetScreenCapture.adb_screen("258905d3")
        # compare template
        for process in processesInfo:
            img_src_height = screen.shape[0]
            img_src_width = screen.shape[1]  # 匹配原图的宽高
            matchingPosition = None
            try:
                if matchingMethod == 1:
                    matchingPosition = GetPosByTemplateMatch.template_matching(screen, process.get("image"), img_src_width, img_src_height, process.get("threshold"))
                    if matchingPosition is None:
                        continue
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
    main(3, "egp", 800, 700, False, True, 800, matchingMethod=1)

