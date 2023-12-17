from os import listdir
from os.path import join, exists
from typing import List

import cv2
from numpy import uint8, fromfile

from constants.Constants import MatchingConstants
from model.CapturedScreen import CapturedScreen
from model.TemplateEntity import TemplateEntity, TemplateConditionMethod, TemplateCondition
from utils.ImageUtils import ImageUtils
from utils.OperatorUtils import OperatorUtils
from utils.PositionUtils import PositionUtils, GetPosBySiftMatch

IMAGE_COMPRESS_RADIO = 1

class TemplateExecutor:
    def __init__(self, template: TemplateEntity):
        self.template: TemplateEntity = template
        self.image, self.shape, self.sift = self.init_image()
        self.matchingArea = self.template.area
        self.required = self.template.required
        self.condition: TemplateCondition = self.template.condition


    def execute(self, screen: CapturedScreen):
        print(f"start executing template: {self.template.src}")
        ImageUtils.show_img(screen.screen)
        position = self.match(screen)
        print(f"matched: {position is not None}, position: {position}")

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
                value, position = PositionUtils.template_matching_return_position(screen.screen,
                                                                   self.image,
                                                                   screen.originalWidth,
                                                                   screen.originalHeight,
                                                                   )
                matched = OperatorUtils.operateJudgement(value, matchingMethod.threshold, matchingMethod.operator)

            elif matchingMethod == MatchingConstants.METHOD_SIFT_MATCHING:
                position = GetPosBySiftMatch.sift_matching(self.sift, self.sift,
                                                                   (self.shape[1], self.shape[0]),
                                                                   self.image, screen.screen)
                matched = position is not None

