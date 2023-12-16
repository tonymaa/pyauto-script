import time

from model.StepEntity import StepEntity
from model.WindowEntity import WindowEntity
from utils.ImageUtils import ImageUtils
from utils.ScreenCaptureUtils import ScreenCaptureUtils

IMAGE_COMPRESS_RADIO = 1
class StepService:
    def __init__(self, window: WindowEntity, step: StepEntity):
        self.step = step
        self.window = window
        self.currentCapturedScreen = {
            "screen": None, "originalHeight": None, "originalWidth": None
        }

    def start(self):
        print(f"start step: {self.step.name}")
        self.intervalScreenCapture()

    def onCaptured(self):
        if self.currentCapturedScreen["screen"] is None: return False
        ImageUtils.show_img(self.currentCapturedScreen["screen"])


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
            self.currentCapturedScreen = {
                "screen": screen, "originalHeight": originalHeight, "originalWidth": originalWidth
            }
            self.onCaptured()
            time.sleep(1)