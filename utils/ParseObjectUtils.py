class ParseObjectUtils:
    @staticmethod
    def parseDictToObject(dict, objClass):
        result = objClass()
        result.__dict__.update(dict)
        return result