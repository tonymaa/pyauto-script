import unittest

from utils.HandleUtils import HandleUtils
from utils.ImageUtils import ImageUtils
from utils.ScreenCaptureUtils import ScreenCaptureUtils


class TestStringMethods(unittest.TestCase):
    def test_backend_windows_screen_capture(self):
        hand_win_title, hand_num = HandleUtils.get_active_window()
        image = ScreenCaptureUtils.window_screen(hand_num)
        ImageUtils.show_img(image)

    def test_frontend_windows_screen_capture(self):
        hand_win_title, hand_num = HandleUtils.get_active_window()
        image = ScreenCaptureUtils.front_window_screen(hand_num)
        ImageUtils.show_img(image)


if __name__ == '__main__':
    unittest.main()