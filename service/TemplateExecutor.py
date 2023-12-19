from os import listdir
from os.path import join, exists
from typing import List

import cv2
from numpy import uint8, fromfile

from constants.Constants import MatchingConstants
from model.Configurations import Configurations
from model.WindowEntity import WindowEntity
from model.CapturedScreen import CapturedScreen
from model.TemplateEntity import TemplateEntity, TemplateConditionMethod, TemplateCondition
from service.ActionsExecutor import ActionsExecutor
from utils.ImageUtils import ImageUtils
from utils.OperatorUtils import OperatorUtils
from utils.PositionUtils import PositionUtils, GetPosBySiftMatch

IMAGE_COMPRESS_RADIO = 1

class TemplateExecutor:
    def __init__(self, window: WindowEntity, template: TemplateEntity):
        self.window = window
        self.template: TemplateEntity = template
        self.image, self.shape, self.sift = self.init_image()
        self.matchingArea = self.template.area
        self.required = self.template.required
        self.condition: TemplateCondition = self.template.condition
        self.onConditionCorrect = self.template.onConditionCorrect


    def execute(self, screen: CapturedScreen):
        print(f"start executing template: {self.template.src}")
        position = self.match(screen)
        print(f"matched: {position is not None}, position: {position}")
        if position is None: return False
        actionsExecutor = ActionsExecutor(self.window, self.onConditionCorrect, position)
        actionsExecutor.execute()

    def init_image(self):
        image = cv2.imdecode(fromfile(self.template.src, dtype=uint8), -1)  # 修复中文路径下opencv报错问题
        shape = image.shape[:2]  # 获取目标图片宽高
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sift = ImageUtils.get_sift(image)
        return image, shape, sift

    def match(self, screen: CapturedScreen):
        matched = False
        position = None
        for matchingMethod in self.condition.matchingMethods:
            if matched: return position
            print(f"matchingMethod: {matchingMethod.__dict__}")
            if matchingMethod.method == MatchingConstants.METHOD_TEMPLATE_MATCHING:
                print("start template matching.....")
                value, position = PositionUtils.template_matching_return_position(screen.screen,
                                                                   self.image,
                                                                   screen.originalWidth,
                                                                   screen.originalHeight,
                                                                   )
                matched = OperatorUtils.operateJudgement(value, matchingMethod.threshold, matchingMethod.operator)

            elif matchingMethod.method == MatchingConstants.METHOD_SIFT_MATCHING:
                print("start sift matching.....")
                position = GetPosBySiftMatch.sift_matching(self.sift, self.sift,
                                                                   (self.shape[1], self.shape[0]),
                                                                   self.image, screen.screen)
                matched = position is not None

