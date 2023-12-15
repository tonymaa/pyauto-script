from model.ProcessEntity import ProcessEntity
from typing import List, Tuple, Dict

from model.StepEntity import StepEntity
from service.StepService import StepService


class ProcessService:
    def __init__(self, process: ProcessEntity):
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
        step_service = StepService(step)
        step_service.start()

