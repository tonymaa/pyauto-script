from model.CapturedScreen import CapturedScreen
from model.TemplateEntity import TemplateEntity
from utils.ImageUtils import ImageUtils


class TemplateExecutor:
    def __init__(self, template: TemplateEntity):
        self.template: TemplateEntity = template

    def execute(self, screen: CapturedScreen):
        print(f"start executing template: {self.template.src}")
        ImageUtils.show_img(screen.screen)