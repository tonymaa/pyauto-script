from model.ActionsEntity import ActionsEntity


class ActionsExecutor:
    def __init__(self, actions: ActionsEntity):
        self.actions = actions

    def execute(self):
        # TODO: execute actions based on self.actions
        print(f"start execute actions: {self.actions.__dict__}")