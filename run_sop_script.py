import json

from win32gui import MoveWindow

from model.WindowEntity import WindowEntity
from service.ProcessService import ProcessService
from utils.HandleUtils import HandleUtils
from utils.ProcessUtils import ProcessUtils
from model.ProcessEntity import ProcessEntity
class Main:
    def __init__(self):
        self.window = WindowEntity()
    def init_window(self):
        self.window.title, self.window.handleNum = HandleUtils.get_active_window(3)
        MoveWindow(
            self.window.handleNum,
            0, 0, self.window.width, self.window.height, True)

    def main(self):
        processDict = ProcessUtils.parseProcessFile("./process/NewProcess/newProcess.json")
        processesMap = {}
        mainProcessName = processDict["mainProcess"]
        self.window = WindowEntity(**processDict["window"])
        for process in processDict["processes"]:
            entity = ProcessEntity(**process)
            entity.isMainProcess = entity.name == mainProcessName
            processesMap[entity.name] = entity
        print("start init window")
        self.init_window()
        print("window info:")
        print(self.window.printObj())
        print(f"<br>----------------------")
        processService = ProcessService(self.window, processesMap[mainProcessName])
        processService.start()


if __name__ == '__main__':
    Main().main()
