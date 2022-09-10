
import time

from utils.DoClickUtils import DoClickUtils
from utils.ImageUtils import ImageUtils
from utils.PositionUtils import PositionUtils, GetPosBySiftMatch
from utils.ProcessesInfoUtils import ProcessesInfoUtils
from utils.ScreenCaptureUtils import ScreenCaptureUtils
from utils.HandleUtils import HandleUtils
import win32gui
from model.EventAttribute import EventAttribute
"""
    hwnd: 句柄，windows时参数为[title, handle]; adb时参数为[status, [devicesId...]]
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
    selectedDeviceIndex: adb连接的所有设备，默认选取第一个
    debugMode: debug 
"""
class AutoScriptService:
    def __init__(self): pass
    @staticmethod
    def startMatching(hwnd, intervalSelectWindow, processName, windowWidth, windowHeight,
             isBackgroungRunning, isKeepActive, intervalScreenShot,
             matchingMethod = 1, windowName = None, customDir=".\\process",
             compressionRatio = 0.5, allowAbs = False, selectedDeviceIndex = 0, debugMode = False):
        # 提供一个给匹配事件的自定义函数的作用域，存放一些变量
        eventAttribute = EventAttribute()
        eventAttribute.allowAbs = allowAbs
        eventAttribute.selectedDeviceIndex = selectedDeviceIndex

        # 1. 点击目标窗口/输入目标窗口 获取窗口句柄
        if hwnd is not None:
            if allowAbs: # phone
                hwnd = HandleUtils.adb_device_status()
            else:  # windows
                if windowName is not None:
                    hwnd = HandleUtils.find_windows_by_title(windowName)
                if hwnd is None:
                    hwnd = HandleUtils.get_active_window(intervalSelectWindow) # ('Service Development Studio - Google Chrome', 67596)

        eventAttribute.setHwnd(hwnd)
        # 2. 将目标窗口resize成固定大小，如： height: 300, width: 500
        if not allowAbs: # windows, resize
            win32gui.MoveWindow(hwnd[1],0,0,windowWidth,windowHeight,True)

        # 3. 当匹配上模板文件夹（放置在指定目录下）中的其中一个时，读取该模板图片的文件名，
        # 4. 解析一些信息
        processesInfo = ProcessesInfoUtils.get(processName, customDir)
        # 5. 循环截图目标窗口，将截图与模板图片进行匹配（模板图片是截图中的一小部分，预处理时需保证分辨率一致）
        while eventAttribute.getProcessRunning():
            time.sleep(intervalScreenShot / 1000)
            # capture screen
            screen = None
            # 5.1 截图
            if allowAbs: # phone
                status, deviceIds = hwnd
                if not status:
                    print(f"【error】 no device connected! try again...")
                    break
                screen = ScreenCaptureUtils.adb_screen(deviceIds[selectedDeviceIndex])
            else: # windows
                # 是否后台运行
                if isBackgroungRunning:
                    screen = ScreenCaptureUtils.window_screen(hwnd[1]) # 后台截图
                else:
                    screen = ScreenCaptureUtils.front_window_screen(hwnd[1], isKeepActive) # 前台截图
            screenSift = None
            # 采用sift算法
            if matchingMethod == 2:
                screenSift = ImageUtils.get_sift(screen) # 获取特征点
            # 记录原始截图尺寸
            originalScreenWidth = screen.shape[1]
            originalScreenHeight = screen.shape[0]
            # 5.2 截图压缩
            if compressionRatio != 1:
                screen = ImageUtils.img_compress(screen, compressionRatio)
            if debugMode: ImageUtils.show_img_and_title(screen, "压缩后截图")

            # 5.3 匹配processesInfo里所有图片
            for process in processesInfo:
                if not eventAttribute.getProcessRunning(): return # 结束
                if debugMode: print(processesInfo)
                matchingPosition = None
                # 5.3.1 匹配
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
                        matchingPosition = GetPosBySiftMatch.sift_matching(process.get("sift"), screenSift, (process.get("shape")[1], process.get("shape")[0]), process.get("image"), screen, debugMode)
                        if matchingPosition is None:
                            continue
                except Exception:
                    import traceback
                    traceback.print_exc()
                    print(f"【error】 matching error... try again")
                    break
                print(f"【debug】 matching position: ({matchingPosition[0]}, {matchingPosition[1]})")

                # 5.3.2 点击
                if allowAbs:
                    status, deviceIds = hwnd
                    if not status:
                        print(f"【error】 no device connected! try again...")
                        break
                    DoClickUtils.adb_click(deviceIds[selectedDeviceIndex], process, matchingPosition, eventAttribute)
                else:
                    if isBackgroungRunning:
                        DoClickUtils.doWindowsClick(hwnd[1], process, matchingPosition, eventAttribute)
                    else:
                        DoClickUtils.doFrontWindowsClick(hwnd[1], process, matchingPosition, isKeepActive, eventAttribute)

    @staticmethod
    def matching(hwnd, processName, windowWidth, windowHeight,
             isBackgroungRunning, isKeepActive, intervalScreenShot,
             matchingMethod = 1, windowName = None, customDir=".\\process",
             compressionRatio = 0.5, allowAbs = False, selectedDeviceIndex = 0, debugMode = False):
        # 提供一个给匹配事件的自定义函数的作用域，存放一些变量
        eventAttribute = EventAttribute()
        eventAttribute.allowAbs = allowAbs
        eventAttribute.selectedDeviceIndex = selectedDeviceIndex
        eventAttribute.setHwnd(hwnd)

        # 3. 当匹配上模板文件夹（放置在指定目录下）中的其中一个时，读取该模板图片的文件名，
        # 4. 解析一些信息
        processesInfo = ProcessesInfoUtils.get(processName, customDir)
        # 5. 循环截图目标窗口，将截图与模板图片进行匹配（模板图片是截图中的一小部分，预处理时需保证分辨率一致）
        while eventAttribute.getProcessRunning():
            time.sleep(intervalScreenShot / 1000)
            # capture screen
            screen = None
            # 5.1 截图
            if allowAbs: # phone
                status, deviceIds = hwnd
                if not status:
                    print(f"【error】 no device connected! try again...")
                    break
                screen = ScreenCaptureUtils.adb_screen(deviceIds[selectedDeviceIndex])
            else: # windows
                # 是否后台运行
                if isBackgroungRunning:
                    screen = ScreenCaptureUtils.window_screen(hwnd[1]) # 后台截图
                else:
                    screen = ScreenCaptureUtils.front_window_screen(hwnd[1], isKeepActive) # 前台截图
            screenSift = None
            # 采用sift算法
            if matchingMethod == 2:
                screenSift = ImageUtils.get_sift(screen) # 获取特征点
            # 记录原始截图尺寸
            originalScreenWidth = screen.shape[1]
            originalScreenHeight = screen.shape[0]
            # 5.2 截图压缩
            if compressionRatio != 1:
                screen = ImageUtils.img_compress(screen, compressionRatio)
            if debugMode: ImageUtils.show_img_and_title(screen, "压缩后截图")

            # 5.3 匹配processesInfo里所有图片
            for process in processesInfo:
                if not eventAttribute.getProcessRunning(): return # 结束
                if debugMode: print(processesInfo)
                matchingPosition = None
                # 5.3.1 匹配
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
                        matchingPosition = GetPosBySiftMatch.sift_matching(process.get("sift"), screenSift, (process.get("shape")[1], process.get("shape")[0]), process.get("image"), screen, debugMode)
                        if matchingPosition is None:
                            continue
                except Exception:
                    import traceback
                    traceback.print_exc()
                    print(f"【error】 matching error... try again")
                    break
                print(f"【debug】 matching position: ({matchingPosition[0]}, {matchingPosition[1]})")

                # 5.3.2 点击
                if allowAbs:
                    status, deviceIds = hwnd
                    if not status:
                        print(f"【error】 no device connected! try again...")
                        break
                    DoClickUtils.adb_click(deviceIds[selectedDeviceIndex], process, matchingPosition, eventAttribute)
                else:
                    if isBackgroungRunning:
                        DoClickUtils.doWindowsClick(hwnd[1], process, matchingPosition, eventAttribute)
                    else:
                        DoClickUtils.doFrontWindowsClick(hwnd[1], process, matchingPosition, isKeepActive, eventAttribute)

if __name__ == "__main__":
    AutoScriptService.startMatching(intervalSelectWindow=3, processName="egp", windowWidth=800, windowHeight=700,
         isBackgroungRunning=True, isKeepActive=False, intervalScreenShot=800, matchingMethod=2,
         compressionRatio=1, allowAbs=False, selectedDeviceIndex=0, debugMode=False)
