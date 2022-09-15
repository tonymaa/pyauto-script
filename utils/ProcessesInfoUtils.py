from os import listdir
from os.path import join, exists
from numpy import uint8, fromfile
import cv2
from utils.ImageUtils import ImageUtils

class ProcessesInfoUtils:
    def __init__(self): pass

    @staticmethod
    def get(process, customDir=".\\process"):
        """
            param process: 目标目录
            param customDir: 工作路径
            return: 目标目录的所有图片信息
        """
        targetProcessPath = join(customDir, process)
        if not exists(targetProcessPath):
            print("<br>未找到目标文件夹或图片地址！即将退出！")
            return None
        listdirs = listdir(targetProcessPath)
        if len(listdirs) == 0:
            print("<br>未找到目标文件夹或图片地址！")
            return None  # 脚本结束
        processesInfo = []
        fileTypes = (".png", ".jpg")
        for fileName in listdirs:
            if len(fileName) >= 4 and fileName[-4:].lower() not in fileTypes: continue
            process = {}
            filePath = join(targetProcessPath, fileName)
            # image = cv2.imread(filePath)
            image = cv2.imdecode(fromfile(filePath, dtype=uint8), -1)  # 修复中文路径下opencv报错问题
            process["shape"] = image.shape[:2]  # 获取目标图片宽高
            process["filePath"] = filePath
            process["fileName"] = fileName
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            process["sift"] = ImageUtils.get_sift(image)
            process["image"] = image
            # 解析文件名
            # fileName = fileName.rstrip(".png").rstrip(".jpg").rstrip(".PNG").rstrip(".PNG")
            for type in fileTypes: fileName = fileName.rstrip(type)
            split = fileName.split("_")
            process["delayTime"] = int(split[0])  # 绝对点击时间：匹配上后多久点击（绝对时间ms）
            process["randomDelayTime"] = int(split[1])  # 点击时间随机延迟量：过了绝对点击时间后，随机延迟多久时间（ms）
            process["relativeClickPosition"] = [int(i) for i in split[2].split("x")]  # 要点击的相对与目标窗口的绝对位置坐标 如：Rcp100x200 width x height，python类型(100,200)
            process["randomRightOffset"] = int(split[3])  # 右侧随机偏移量
            process["randomBottomOffset"] = int(split[4])  # 下侧随机偏移量
            process["delayUpTime"] = int(split[5])  # 鼠标单机按下(down)之后，多久ms后抬起(up)
            process["delayRandomUpTime"] = int(split[6])  # 在delay up time 基础上，再随机延迟多久
            process["randomOffsetWhenUp"] = int(split[7])  # 鼠标down 与 up 期间，随机向各个角度的偏移量，一般几个像素点
            process["loopLeastCount"] = int(split[8])  # 至少循环点击几次
            process["loopRandomCount"] = int(split[9])  # 额外随机点击次数
            process["loopDelayLeastTime"] = int(split[10])  # 每次随机点击结束后的延迟时间
            process["loopDelayRandomTime"] = int(split[11])  # 每次随机点击结束后的延迟时间后，额外延迟时间
            process["endDelayLeastTime"] = int(split[12])  # 当所有点击完后，至少多久不再去匹配模板 (ms)
            process["endDelayRandomTime"] = int(split[13])  # 额外等待随机时间ms
            process["threshold"] = int(split[14]) / 100  # 匹配阈值，大于该值时，触发点击事件，范围 0 - 100
            process["useMatchingPosition"] = int(split[15]) # 使用该文件名定义的坐标 #1；还是截图上匹配到的图片坐标 #2
            process["matchEvent"] = join(targetProcessPath, split[16] + ".py")  # 匹配上后的事件：自定义函数，函数须与当前图片同一文件夹，且函数文件名为：函数名.py
            process["finishEvent"] = join(targetProcessPath, split[17] + ".py")  # 所有操作都执行完后的事件：自定义函数，函数须与当前图片同一文件夹，且函数文件名为：函数名.py
            processesInfo.append(process)
        return processesInfo