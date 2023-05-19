class Patient:
    def __init__(self, chance : int, pUTI : int, pUTSI : int, pUTP : int) -> None:
        self.survivingChance : int = chance
        self.priorities : dict = { "UTI" : pUTI, "UTSI" : pUTSI, "UTP" : pUTP }
        self.allocated : bool = False
    
class Unities:
    def __init__(self, uti : int, utsi : int, utp : int) -> None:
        self.types : list = [ "UTI", "UTSI", "UTP" ]
        self.qtdTypes : dict = { "UTI" : uti, "UTSI" : utsi, "UTP" : utp }

        self.setUTI : list = [ f"Bed_UTI_{i}" for i in range( self.qtdTypes["UTI"] ) ]
        self.setUTSI : list = [ f"Bed_UTSI_{i}" for i in range( self.qtdTypes["UTSI"] ) ]
        self.setUTP : list = [ f"Bed_UTP_{i}" for i in range( self.qtdTypes["UTP"] ) ]
        
        self.setBeds_ : list = [ self.setUTI, self.setUTSI, self.setUTP ]
        self.listBeds : list = self.setBeds()
        self.dictBeds : dict = { "UTI" : self.setUTI, "UTSI" : self.setUTSI, "UTP" : self.setUTP }
        self.dBeds = self.getDictBed()

    def setBeds(self) -> list:
        set = list()
        for i in range( self.qtdTypes["UTI"] ):
            set.append("UTI_")
        for i in range( self.qtdTypes["UTSI"] ):
            set.append("UTSI_")
        for i in range( self.qtdTypes["UTP"] ):
            set.append("UTP_")
        return set

    def getDictBed(self) -> dict:
        d = dict()

        for i in self.setUTI:
            d[i] = i
        for i in self.setUTSI:
            d[i] = i
        for i in self.setUTP:
            d[i] = i
        
        return d