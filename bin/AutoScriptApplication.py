import os
import time
from numpy import uint8, fromfile
import cv2

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

    time.sleep(1)
    # 3. 循环截图目标窗口，将截图与模板图片进行匹配（模板图片是截图中的一小部分，预处理时需保证分辨率一致）
    # capture screen
    capture = GetScreenCapture(hwnd[1], 1000, 700)
    screen = capture.window_screen()
    # ImgProcess.show_img(screen)
    # capture phone screen
    # GetScreenCapture.adb_screen("258905d3")

    # 4. 当匹配上模板文件夹（放置在指定目录下）中的其中一个时，读取该模板图片的文件名，
    # 5. 解析一些信息
    processesInfo = GetProcessesInfo.get("egp")
    print(processesInfo)

    # 6. 循环截图，比对processesInfo里的图片信息

    # 7. do click



if __name__ == "__main__":
    main()
