from problem.bed import Bed

class Unity:
    __type : str
    __qtdBeds : int
    __beds : set

    def __init__(self) -> None:
        pass
    def __init__(self, type : str, qtd : int, beds : set) -> None:
        self.__type = type
        self.__qtdBeds = qtd
        self.__beds = beds
    def __init__(self, type : str, qtd : int) -> None:
        self.__type = type
        self.__qtdBeds = qtd
        self.__beds = set( f"{type}_{i}" for i in range(qtd) )

    def getType(self) -> str:
        return self.__type
    
    def getQtdBeds(self) -> int:
        return self.__qtdBeds
    
    def getBeds(self) -> set:
        return self.__beds
    
    def setType(self, type : str) -> None:
        self.__type = type

    def setQtdBeds(self, qtd : int) -> None:
        self.__qtdBeds = qtd
    
    def setBeds(self, beds : set) -> None:
        self.__beds = beds
    
    def addBed(self, bed : Bed) -> None:
        self.__beds.add(bed)
    
    def removeBed(self, bed: Bed) -> None:
        self.__beds.remove(bed)