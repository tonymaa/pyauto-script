import json

from service.ProcessService import ProcessService
from utils.ProcessUtils import ProcessUtils
from model.ProcessEntity import ProcessEntity

def main():
    processDict = ProcessUtils.parseProcessFile("./process/NewProcess/newProcess.json")
    processesMap = {}
    mainProcessName = processDict["mainProcess"]
    for process in processDict["processes"]:
        entity = ProcessEntity(**process)
        entity.isMainProcess = entity.name == mainProcessName
        processesMap[entity.name] = entity

    processService = ProcessService(processesMap[mainProcessName])
    processService.start()


if __name__ == '__main__':
    main()
