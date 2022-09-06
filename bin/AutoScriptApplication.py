import os
import time
from numpy import uint8, fromfile
import cv2

from utils.DoClickUtils import DoClickUtils
from utils.GetPositionUtils import GetPosByTemplateMatch
from utils.GetProcessesInfo import GetProcessesInfo
from utils.GetScreenCaptureUtils import GetScreenCapture
from utils.HandleSetUtils import HandleSet
import win32gui

from utils.ImageProcessUtils import ImgProcess




def main():
    # 1. 点击目标窗口/输入目标窗口 获取窗口句柄
    # windows
    hwnd = HandleSet.get_active_window() # ('Service Development Studio - Google Chrome', 67596)
    # Android phone
    print(HandleSet.adb_device_status()) # (True, ['258905d3'])
    # 窗口左上，右下坐标
    # print(GetWindowRect(67596)) # (46, 24, 1234, 1019) left, top, right, bottom

    # 2. 将目标窗口resize成固定大小，如： height: 300, width: 500
    win32gui.MoveWindow(hwnd[1],0,0,1000,700,True)

    time.sleep(4)


    # 4. 当匹配上模板文件夹（放置在指定目录下）中的其中一个时，读取该模板图片的文件名，
    # 5. 解析一些信息
    processesInfo = GetProcessesInfo.get("egp")
    print(processesInfo)

    # 6. 循环截图目标窗口，将截图与模板图片进行匹配（模板图片是截图中的一小部分，预处理时需保证分辨率一致）
    # capture screen
    screen = GetScreenCapture.window_screen(hwnd[1], 1000, 700)
    # ImgProcess.show_img(screen)
    # capture phone screen
    # GetScreenCapture.adb_screen("258905d3")
    # compare template
    for process in processesInfo:
        print(GetPosByTemplateMatch.template_matching(screen, process.get("image"), 1000, 700, 0.7, True, 1))

    # 7. do click
    DoClickUtils.doFrontWindowsClick(hwnd[1], {'shape': (54, 227),
                                            'filePath': '.\\process\\egp\\1000_200_508x517_175_38_20_5_3_1_1_1000_100_matchEvent_finishEvent.png',
                                            'fileName': '1000_200_508x517_175_38_20_5_3_1_1_1000_100_matchEvent_finishEvent.png',
                                            'sift': None, 'image': None, 'delayTime': 1000, 'randomDelayTime': 200,
                                            'relativeClickPosition': [508, 517], 'randomRightOffset': 175,
                                            'randomBottomOffset': 38, 'delayUpTime': 20, 'delayRandomUpTime': 5,
                                            'randomOffsetWhenUp': 3, 'loopLeastCount': 1, 'loopRandomCount': 1,
                                            'endDelayLeastTime': 1000, 'endDelayRandomTime': 100,
                                            'matchEvent': '.\\process\\egp\\matchEvent.py',
                                            'finishEvent': '.\\process\\egp\\finishEvent.py', 'loopDelayLeastTime': 2000, 'loopDelayRandomTime': 100})

if __name__ == "__main__":
    main()

