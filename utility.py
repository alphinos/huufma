def readData(file_name: str):
    file = open(file_name, "r")

    rows = file.readlines()
    values = rows[0].strip().split()
    qtd_Patients = int(values[0])

    del(rows[0])

    unities = rows[0].strip().split()
    for i in range(len(unities)):
        unities[i] = int(unities[i])

    del(rows[0])

    lsPatients = list()
    for row in rows:
        [Pi, Pi0, Pi1, Pi2] = map(int, row.strip().split())
        lsPatients.append( [Pi, Pi0, Pi1, Pi2] )
    
    uti = unities[0]
    utsi = unities[1]
    utp = unities[2]
    
    return lsPatients, uti, utsi, utp, qtd_Patients