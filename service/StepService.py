import time
from typing import List

from model.CapturedScreen import CapturedScreen
from model.StepEntity import StepEntity
from service.TemplateExecutor import TemplateExecutor
from model.WindowEntity import WindowEntity
from utils.ImageUtils import ImageUtils
from utils.ScreenCaptureUtils import ScreenCaptureUtils

IMAGE_COMPRESS_RADIO = 1
class StepService:
    def __init__(self, window: WindowEntity, step: StepEntity):
        self.step = step
        self.templatesExecutors: List[TemplateExecutor] = []
        self.window = window
        self.currentCapturedScreen: CapturedScreen = CapturedScreen()


    def start(self):
        print(f"start step: {self.step.name}")
        print("start load templates executors")
        self.loadTemplatesExecutor()
        print(f"templates executor loaded: ")
        self.intervalScreenCapture()

    def onCaptured(self):
        if self.currentCapturedScreen.screen is None: return False
        # ImageUtils.show_img(self.currentCapturedScreen["screen"])
        for templateExecutor in self.templatesExecutors:
            templateExecutor.execute(self.currentCapturedScreen)

    def intervalScreenCapture(self):
        while True:
            print("start capture screen...")
            screen = ScreenCaptureUtils.front_window_screen(
                self.window.handleNum, False)  # 前台截图
            print("screen capture finished")
            originalHeight = screen.shape[0]
            originalWidth = screen.shape[1]
            if IMAGE_COMPRESS_RADIO != 1:
                screen = ImageUtils.img_compress(screen, IMAGE_COMPRESS_RADIO)
            self.currentCapturedScreen = CapturedScreen(**{
                "screen": screen, "originalHeight": originalHeight, "originalWidth": originalWidth
            })
            self.onCaptured()
            time.sleep(1)

    def loadTemplatesExecutor(self):
        for template in self.step.templates:
            self.templatesExecutors.append(TemplateExecutor(template))