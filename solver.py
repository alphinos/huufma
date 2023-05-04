import gurobipy as gp
from problem import *

def readData(file_name: str):
    file = open(file_name, "r")

    rows = file.readlines()
    values = rows[0].strip().split()
    qtd_Patients = int(values[0])

    del(rows[0])

    vet_Patients = list()
    unities = rows[0].strip().split()
    for i in range(len(unities)):
        unities[i] = int(unities[i])

    del(rows[0])

    patient : Patient

    dictPatients = dict()
    lsPatients = list()
    for row in rows:
        [Pi, Pi0, Pi1, Pi2] = row.strip().split()
        patient = Patient(int(Pi), int(Pi0), int(Pi1), int(Pi2))
        lsPatients.append( patient )

    for i in range(len(lsPatients)):
        dictPatients.update( { f"Patient_{i}" : lsPatients[i] } )
    
    uti = unities[0]
    utsi = unities[1]
    utp = unities[2]
    
    return lsPatients, uti, utsi, utp, qtd_Patients


def solverHU(file_path: str) -> None:

    lsPatients, uti, utsi, utp, qtd_Patients = readData(file_path)

    qtdBeds = uti + utsi + utp

    patients = list(lsPatients)
    unities = Unities( uti, utsi, utp )

    m = gp.Model()

    x = m.addVars(patients, unities.types, unities.dBeds, vtype = gp.GRB.BINARY)

    # Obective function
    m.setObjective(
        gp.quicksum(
            gp.quicksum(
                gp.quicksum(
                    x[i, j, k] * i.survivingChance for k in unities.dictBeds[j]
                ) for j in unities.types
            ) for i in patients
        ),
        sense = gp.GRB.MAXIMIZE
    )

    #Constraints
    c1 = list()
    for j in unities.types:
        for k in unities.dictBeds[j]:
            c1.append(
                m.addConstr(
                    gp.quicksum( x[i, j, k] for i in patients ) <= 1
                )
            )

    c2 = list()
    for i in patients:
        c2.append(
            m.addConstr(
                gp.quicksum(
                    gp.quicksum( x[i, j, k] for k in unities.dictBeds[j]) \
                        for j in unities.types
                ) <= 1
            )
        )

    c3 = list()
    for j in unities.types:
        c3.append(
            m.addConstrs(
            gp.quicksum( x[i, j, k] for k in unities.dictBeds[j] ) <= unities.qtdTypes[j] \
                for i in patients
            )
        )

    c4 =list()
    for i1 in patients:
        for i2 in patients:
            for j in unities.types:
                for k in unities.dictBeds[j]:
                    if i1.priorities[j] > i2.priorities[j]:
                        c4.append(m.addConstr(
                            x[i1, j, k] >= x[i2, j, k]
                            )
                        )

    # # Adicionar restrição para preencher todos os leitos
    # c5 = m.addConstr(
    #     gp.quicksum( x[i, j, k] for k in unities.dictBeds[j] \
    #                     for j in unities.types \
    #                         for i in patients ) == qtdBeds
    # )

    #Execute
    m.optimize()

    answer = dict()
    qtdAlocated = 0
    totalChance = 0

    qtdUTI = 0
    qtdUTSI = 0
    qtdUTP = 0

    for bedType in unities.types:
        for bed in unities.dictBeds[bedType]:
            for patient in patients:
                if x[patient, bedType, bed].X == 1:
                    answer[patient, bedType, bed] = 1
                    totalChance += patient.survivingChance
                    qtdAlocated += 1
                    patient.allocated = True
                    if bedType == "UTI":
                        qtdUTI += 1
                    elif bedType == "UTSI":
                        qtdUTSI += 1
                    elif bedType == "UTP":
                        qtdUTP += 1
                    print(patient.survivingChance)
                    print(patient.priorities["UTI"], patient.priorities["UTSI"], patient.priorities["UTP"])
                    print(bedType, bed)
                else:
                    answer[patient, bedType, bed] = 0

    countVars = 0
    for patient in patients:
        for bedType in unities.types:
            for bed in unities.dictBeds[bedType]:
                print( x[patient, bedType, bed].X)
                countVars += 1
    print(qtdAlocated, totalChance, countVars)

    # NonAllocPatients = [ p for p in patients if p.allocated == False]
    # print([(p.survivingChance, p.priorities["UTI"], p.priorities["UTSI"], p.priorities["UTP"] )\
    #         for p in NonAllocPatients])
    # best = list()
    # while (qtdAlocated < qtdBeds):
    #     print(qtdAlocated, qtdUTI, qtdUTSI, qtdUTP)
    #     best = [0, 0, 0, 0]
    #     if qtdUTI < unities.qtdTypes["UTI"]:
    #         print("UTI")
    #         for patient in NonAllocPatients:
    #             for bedType in unities.types:
    #                 if patient.survivingChance * patient.priorities["UTI"] > best[0] \
    #                     and patient.allocated == False:
    #                     best[0] = patient.survivingChance * patient.priorities["UTI"]
    #                     best[1] = patient
    #         for bed in unities.dictBeds["UTI"]:
    #             if x[best[1], "UTI", bed].X == 0 and answer[best[1], "UTI", bed] == 0:
    #                 print(best[1].survivingChance)
    #                 answer[best[1], "UTI", bed] = 1
    #                 qtdUTI += 1
    #                 qtdAlocated += 1
    #                 totalChance += best[1].survivingChance
    #                 NonAllocPatients.remove(best[1])
    #                 break
    #         print([(p.survivingChance, p.priorities["UTI"], p.priorities["UTSI"], p.priorities["UTP"] )\
    #             for p in NonAllocPatients])
    #         continue
    #     if qtdUTSI < unities.qtdTypes["UTSI"]:
    #         print("UTSI")
    #         for patient in NonAllocPatients:
    #             for bedType in unities.types:
    #                 if patient.survivingChance * patient.priorities["UTSI"] > best[0] \
    #                     and patient.allocated == False:
    #                     best[0] = patient.survivingChance * patient.priorities["UTSI"]
    #                     best[1] = patient
    #         for bed in unities.dictBeds["UTSI"]:
    #             if x[best[1], "UTSI", bed].X == 0 and answer[best[1], "UTSI", bed] == 0:
    #                 print(best[1].survivingChance)
    #                 answer[best[1], "UTSI", bed] = 1
    #                 qtdUTSI += 1
    #                 qtdAlocated += 1
    #                 totalChance += best[1].survivingChance
    #                 NonAllocPatients.remove(best[1])
    #                 break
    #         print([(p.survivingChance, p.priorities["UTI"], p.priorities["UTSI"], p.priorities["UTP"] )\
    #             for p in NonAllocPatients])
    #         continue
    #     if qtdUTP < unities.qtdTypes["UTP"]:
    #         print("UTP")
    #         for patient in NonAllocPatients:
    #             for bedType in unities.types:
    #                 if patient.survivingChance * patient.priorities["UTP"] > best[0] \
    #                     and patient.allocated == False:
    #                     best[0] = patient.survivingChance * patient.priorities["UTP"]
    #                     best[1] = patient
    #         for bed in unities.dictBeds["UTP"]:
    #             if x[best[1], "UTP", bed].X == 0 and answer[best[1], "UTP", bed] == 0:
    #                 print(best[1].survivingChance)
    #                 answer[best[1], "UTP", bed] = 1
    #                 qtdUTP += 1
    #                 qtdAlocated += 1
    #                 totalChance += best[1].survivingChance
    #                 NonAllocPatients.remove(best[1])
    #                 break
    #         print([(p.survivingChance, p.priorities["UTI"], p.priorities["UTSI"], p.priorities["UTP"] )\
    #             for p in NonAllocPatients])
    #         continue
    # for patient in patients:
    #     for bedType in unities.types:
    #         for bed in unities.dictBeds[bedType]:
    #             if answer[patient, bedType, bed] == 1:
    #                 print(patient.survivingChance)
    #                 print(patient.priorities["UTI"], patient.priorities["UTSI"], patient.priorities["UTP"])
    #                 print(bedType, bed)

    # countVars = 0
    # for bedType in unities.types:
    #     for bed in unities.dictBeds[bedType]:
    #         for patient in patients:
    #             print( answer[patient, bedType, bed], bedType, bed, patient)
    #             countVars += 1
    #         print()
    #     print()
    # print(qtdAlocated, totalChance, countVars)


solverHU("Inst_Patients/Inst_0.txt")