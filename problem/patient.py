
class Patient:
    __name : str
    __survivingChance : int
    __priorities : dict
    __allocated : bool

    def __init__(self):
        pass
    def __init__(self, name : str, chance : int, pUTI : int, pUTSI : int, pUTP : int) -> None:
        self.__name = name
        self.__survivingChance = chance
        self.__priorities = { "UTI" : pUTI, "UTSI" : pUTSI, "UTP" : pUTP }
        self.__allocated = False
    def __init__(self, idx: int, chance : int, pUTI : int, pUTSI : int, pUTP : int) -> None:
        self.__name = f"patient_{idx}"
        self.__survivingChance = chance
        self.__priorities = { "UTI" : pUTI, "UTSI" : pUTSI, "UTP" : pUTP }
        self.__allocated = False
    
    def getName(self) -> str:
        return self.__name

    def getSurvivingChance(self) -> int:
        return self.__survivingChance
    
    def getPriorities(self) -> dict:
        return self.__priorities
    
    def getAllocated(self) -> bool:
        return self.__allocated
    
    def getPriorUTI(self) -> int:
        return self.__priorities["UTI"]
    
    def getPriorUTSI(self) -> int:
        return self.__priorities["UTSI"]
    
    def getPriorUTP(self) -> int:
        return self.__priorities["UTP"]
    
    def setName(self, name : str) -> None:
        self.__name = name

    def setSurvivingChance(self, chance : int) -> None:
        self.__survivingChance = chance

    def setPriorities(self, priorities : dict) -> None:
        self.__priorities = priorities

    def setAllocated(self, allocated : bool) -> None:
        self.__allocated = allocated
    
    def setPriorUTI(self, priority : int) -> None:
        self.__priorities["UTI"]= priority
    
    def setPriorUTSI(self, priority : int) -> None:
        self.__priorities["UTSI"]= priority
    
    def setPriorUTP(self, priority : int) -> None:
        self.__priorities["UTP"]= priority