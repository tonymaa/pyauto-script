from win32gui import MoveWindow

from model.ProcessEntity import ProcessEntity
from typing import List, Tuple, Dict

from model.StepEntity import StepEntity
from model.WindowEntity import WindowEntity
from service.StepService import StepService
from utils.HandleUtils import HandleUtils


class ProcessService:
    def __init__(self, window: WindowEntity, process: ProcessEntity):
        self.window = window
        self.process = process
        self.stepsMap: Dict[str, StepEntity] = {}
        for step in process.steps:
            step_entity = StepEntity(**step)
            self.stepsMap[step_entity.name] = step_entity
            # step_entity.printObj()

    def start(self):
        print(f"start process: {self.process.name}")
        main_step = self.stepsMap[self.process.mainStep]
        self.run_step(main_step)

    def run_step(self, step: StepEntity):
        step_service = StepService(self.window, step)
        step_service.start()

