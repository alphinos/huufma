from problem import *
from utility import *

def solverHU(file_path: str) -> None:

    lsPatients, qtdUti, qtdUtsi, qtdUtp, qtd_Patients = readData(file_path)

    print(qtdUti, qtdUtsi, qtdUtp)

    qtdBeds = qtdUti + qtdUtsi + qtdUtp

    uti = Unity("UTI", qtdUti)
    utsi = Unity("UTSI", qtdUtsi)
    utp = Unity("UTP", qtdUtp)

    typeSet = { "UTI", "UTSI", "UTP" }

    qtdTypes = { "UTI" : qtdUti, "UTSI" : qtdUtsi, "UTP" : qtdUtp }

    unitiesSet = set() 
    unitiesSet.update(uti.getBeds(), utsi.getBeds(), utp.getBeds())

    patients = set()
    patients2 = set()
    for idx, item in enumerate(lsPatients):
        patient = Patient( idx, item[0], item[1], item[2], item[3] )
        patients.add(patient)
        patients2.add(patient)

    unitiesDict = dict( [ ( "UTI", uti.getBeds() ), ( "UTSI", utsi.getBeds() ), ( "UTP", utp.getBeds() ) ] )

    answer = dict()

    for typeBed in typeSet:
        for bed in unitiesDict[typeBed]:
            for patient in patients:
                answer[ patient, typeBed, bed ] = 0

    qtdAlocated = 0
    totalChance = 0
    qtdUTI = 0
    qtdUTSI = 0
    qtdUTP = 0
    best : Patient
    while (qtdAlocated < qtdBeds):

        best = Patient(0, 0, 0, 0, 0)
        if qtdUTI < qtdTypes["UTI"]:
            for patient in patients:
                if patient.getSurvivingChance() * patient.getPriorities()["UTI"] > best.getPriorities()["UTI"] * best.getSurvivingChance() \
                    and patient.getAllocated() == False:
                    best = patient
            for bed in unitiesDict["UTI"]:
                if answer[(best, "UTI", bed)] == 0:
                    print(best.getSurvivingChance())
                    answer[(best, "UTI", bed)] = 1
                    qtdUTI += 1
                    qtdAlocated += 1
                    totalChance += best.getSurvivingChance()
                    best.setAllocated(True)
                    patients.remove(best)
                    break
        
        best = Patient(0, 0, 0, 0, 0)
        if qtdUTSI < qtdTypes["UTSI"]:
            for patient in patients:
                if patient.getSurvivingChance() * patient.getPriorities()["UTSI"] > best.getPriorities()["UTSI"] * best.getSurvivingChance() \
                    and patient.getAllocated() == False:
                    best = patient
            for bed in unitiesDict["UTSI"]:
                if answer[(best, "UTSI", bed)] == 0:
                    print(best.getSurvivingChance())
                    answer[(best, "UTSI", bed)] = 1
                    qtdUTSI += 1
                    qtdAlocated += 1
                    totalChance += best.getSurvivingChance()
                    best.setAllocated(True)
                    patients.remove(best)
                    break
        
        best = Patient(0, 0, 0, 0, 0)
        if qtdUTP < qtdTypes["UTP"]:
            for patient in patients:
                if patient.getSurvivingChance() * patient.getPriorities()["UTP"] > best.getPriorities()["UTP"] * best.getSurvivingChance() \
                    and patient.getAllocated() == False:
                    best = patient
                    break
            for bed in unitiesDict["UTP"]:
                if answer[(best, "UTP", bed)] == 0:
                    answer[(best, "UTP", bed)] = 1
                    qtdUTP += 1
                    qtdAlocated += 1
                    totalChance += best.getSurvivingChance()
                    best.setAllocated(True)
                    patients.remove(best)
                    break
            
    for patient in patients2:
        for bedType in typeSet:
            for bed in unitiesDict[bedType]:
                if answer[patient, bedType, bed] == 1:
                    print(patient.getSurvivingChance())
                    print(patient.getPriorities()["UTI"], patient.getPriorities()["UTSI"], patient.getPriorities()["UTP"])
                    print(bedType, bed)

    countVars = 0
    for bedType in typeSet:
        for bed in unitiesDict[bedType]:
            for patient in patients2:
                print( answer[(patient, bedType, bed)], bedType, bed, patient.getName())
                countVars += 1
            print()
        print()
    print(qtdAlocated, totalChance, countVars)

solverHU("Inst_Patients/Inst_0.txt")