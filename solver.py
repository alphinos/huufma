import gurobipy as grbp
from gurobipy import GRB
from problem import *
from utility import readData


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
    for idx, item in enumerate(lsPatients):
        patient = Patient( idx, item[0], item[1], item[2], item[3] )
        patients.add(patient)

    unitiesDict = dict( [ ( "UTI", uti.getBeds() ), ( "UTSI", utsi.getBeds() ), ( "UTP", utp.getBeds() )] )

    m = grbp.Model()

    for p in patients:
        print(p.getName())
    print(typeSet)
    print(unitiesSet)

    x = m.addVars(patients, typeSet, unitiesSet, vtype = GRB.BINARY)

    # Obective function
    m.setObjective(
        grbp.quicksum(
            grbp.quicksum(
                grbp.quicksum(
                    x[i, j, k] * i.getSurvivingChance() for k in unitiesDict[j]
                ) for j in typeSet
            ) for i in patients
        ),
        sense = grbp.GRB.MAXIMIZE
    )

    #Constraints
    c1 = list()
    for j in typeSet:
        for k in unitiesDict[j]:
            c1.append(
                m.addConstr(
                    grbp.quicksum( x[i, j, k] for i in patients ) <= 1
                )
            )

    c2 = list()
    for i in patients:
        c2.append(
            m.addConstr(
                grbp.quicksum(
                    grbp.quicksum( x[i, j, k] for k in unitiesDict[j]) \
                        for j in typeSet
                ) <= 1
            )
        )

    c3 = list()
    for j in typeSet:
        c3.append(
            m.addConstrs(
            grbp.quicksum( x[i, j, k] for k in unitiesDict[j] ) <= qtdTypes[j] \
                for i in patients
            )
        )

    c4 =list()
    for i1 in patients:
        for i2 in patients:
            for j in typeSet:
                for k in unitiesDict[j]:
                    if i1.getPriorities()[j] > i2.getPriorities()[j]:
                        c4.append(m.addConstr(
                            x[i1, j, k] >= x[i2, j, k]
                            )
                        )

    #Execute
    m.optimize()

    answer = dict()
    qtdAlocated = 0
    totalChance = 0

    qtdUTI = 0
    qtdUTSI = 0
    qtdUTP = 0

    for bedType in typeSet:
        for bed in unitiesDict[bedType]:
            for patient in patients:
                if x[patient, bedType, bed].X == 1:
                    answer[patient, bedType, bed] = 1
                    totalChance += patient.getSurvivingChance()
                    qtdAlocated += 1
                    patient.allocated = True
                    if bedType == "UTI":
                        qtdUTI += 1
                    elif bedType == "UTSI":
                        qtdUTSI += 1
                    elif bedType == "UTP":
                        qtdUTP += 1
                    print(patient.getSurvivingChance())
                    print(patient.getPriorities()["UTI"], patient.getPriorities()["UTSI"], patient.getPriorities()["UTP"])
                    print(bedType, bed)
                else:
                    answer[patient, bedType, bed] = 0

    countVars = 0
    for patient in patients:
        for bedType in typeSet:
            for bed in unitiesDict[bedType]:
                print( x[patient, bedType, bed].X)
                countVars += 1
    print(qtdAlocated, totalChance, countVars)

solverHU("Inst_Patients/Inst_0.txt")