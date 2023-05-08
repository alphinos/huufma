
class Bed:
    __name : str
    __type : str
    __used : bool

    def __init__(self) -> None:
        pass
    def __init__(self, name : str, type : str) -> None:
        self.__name = name
        self.__type = type
        self.__used = False
    
    def getName(self) -> str:
        return self.__name
    
    def getType(self) -> str:
        return self.__type
    
    def getUsed(self) -> bool:
        return self.__used
    
    def setName(self, name : str) -> None:
        self.__name = name
    
    def setType(self, type : str) -> None:
        self.__type = type
    
    def setUsed(self, used : bool) -> None:
        self.__used = used