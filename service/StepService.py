from model.StepEntity import StepEntity


class StepService:
    def __init__(self, step: StepEntity):
        self.step = step

    def start(self):
        print(f"start step: {self.step.name}")

