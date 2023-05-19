import gurobipy as grbp
from gurobipy import GRB
from utility import readData

def solverHU(file_path: str) -> None:
    patients, qtdUti, qtdUtsi, qtdUtp, qtd_Patients = readData(file_path)
    qtdBeds = qtdUti + qtdUtsi + qtdUtp

    q = [ qtdUti, qtdUtsi, qtdUtp ]

    print(f"uti : {qtdUti}, utsi: {qtdUtsi}, utp: {qtdUtp}, total de pacientes: {qtd_Patients}.")
    print()
    for p in patients:
        print(*p)

    ls_uti = list( range(qtdUti) )
    ls_utsi = list( range( qtdUti, qtdUti + qtdUtsi ) )
    ls_utp = list( range( qtdUti + qtdUtsi, qtdBeds) )

    K_Types = [ ls_uti, ls_utsi, ls_utp ]

    print()
    print("camas de uti:", *ls_uti)
    print("camas de utsi:", *ls_utsi)
    print("camas de utp:", *ls_utp)
    print("conjunto de camas de cada tipo:", *K_Types)
    
    I = list( range(qtd_Patients) )
    J = [0, 1, 2] # 0 = uti | 1 = utsi | 2 = utp
    K = list( range(qtdBeds) )

    print()
    print("pacientes:", *I )
    print("tipos:", *J)
    print("leitos:", *K)

    m = grbp.Model()
    x = m.addVars(qtd_Patients, 3, qtdBeds, vtype = GRB.BINARY)

    #Objective function
    sum_ = 0
    for i in I:
        for j in J:
            for k in K_Types[j]:
                sum_ += x[i, j, k] * patients[i][0]

    m.setObjective( sum_, sense = grbp.GRB.MAXIMIZE )

    #Constraints

    # C1
    for j in J:
        for k in K_Types[j]:
            sum_c1 = 0
            for i in I:
                sum_c1 += x[i, j, k]
            
            m.addConstr( sum_c1 <= 1 )
    
    # C2
    for i in I:
        sum_c2 = 0
        for j in J:
            for k in K_Types[j]:
                sum_c2 += x[i, j, k]
        
        m.addConstr( sum_c2 <= 1 )
    
    # C3
    for j in J:
        sum_c3 = 0
        for i in I:
            for k in K_Types[j]:
                sum_c3 += x[i, j, k]
        m.addConstr( sum_c3 <= q[j] )
    
    # C4
    for i1 in I:
        for i2 in I:
            if i1 == i2:
                continue
            for j in J:
                for k in K_Types[j]:
                    # Cada item de patients é uma lista
                    # Na posição 0, está a chance de sobrevivência
                    # Na posição 1, está uma lista com as prioridades de cada paciente
                    # para cada tipo de leito
                    if patients[i1][1][j] > patients[i2][1][j]:
                        m.addConstr(
                            x[i1, j, k] >= x[i2, j, k]
                        )
    
    #Execute
    m.optimize()

    qtd_Alocated = 0
    total_Chance = 0
    print()
    for j in J:
        for k in K_Types[j]:
            for i in I:
                if x[i, j, k].X == 1:
                    print(f"Paciente_{i}, tipo : {j}, cama_{j}__{k}")
                    print(f"Chance de sobrevivência: {patients[i][0]}, prioridades: {patients[i][1]}\n")
                    qtd_Alocated += 1
                    total_Chance += patients[i][0]
    
    print()
    print("Tipo de uti: 0")
    print("Tipo de utsi: 1")
    print("Tipo de utp: 2")

    print()
    print(f"Quantidade de pacientes alocados: {qtd_Alocated}, Chance total: {total_Chance}")
    print(f"Total de camas: {qtdBeds}")
    print(f"uti : {qtdUti}, utsi: {qtdUtsi}, utp: {qtdUtp}, total de pacientes: {qtd_Patients}.")

solverHU("Inst_Patients/Inst_0.txt")