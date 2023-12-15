import json
class ProcessUtils:
    @staticmethod
    def parseProcessFile(path):
        with open(path, encoding='utf-8') as f:
            process = json.load(f)
        return process

    @staticmethod
    def findMainProcessObject(processes, mainProcess):
        for process in processes:
            if process['name'] == mainProcess: return process
        return None