from random import randint

<<<<<<< HEAD
from problem import Patient

=======
>>>>>>> b3e40f6 (Simplificando o solver e reorganizando as pastas do projeto)
def generateUnities():
    unities = list()
    for i in range(3):
        amt = randint(1, 3)
        unities.append(amt)
    return unities

def generateProblem():
    unities = generateUnities()
    min = unities[0] + unities[1] + unities[2]
    qtd_Patients = randint(min + 1, 2*min)
    return qtd_Patients, unities

def generatePatient():
    chance = randint(1, 5)
    uti = chance
    if uti == 4:
        utsi = randint(4, 5)
        utp = randint(1, 3)
    if uti == 2:
        utsi = 5
        utp = randint(2, 4)
    elif uti == 1:
        utsi = randint(2, 4)
        utp = randint(4, 5)
    else:
        utsi = randint(2, 4)
        utp = randint(uti, 5)
    chance *= randint(1, 20) 
    if chance == 100:
        chance = 99
<<<<<<< HEAD
    patient = Patient(chance, uti, utsi, utp)
=======
    patient = [chance, uti, utsi, utp]
>>>>>>> b3e40f6 (Simplificando o solver e reorganizando as pastas do projeto)
    return patient

def generatePatientList(qtd_items: int):
    return [generatePatient() for i in range(qtd_items)]

def createFile(id: int, path: str):
    file = open(f"{path}/Inst_{id}.txt", "w")
    return file

def appendToFile(file, content: str):
    file.write(f"{content}\n")
    return file

def closeAllFiles(instances: list):
    closedFiles = [f.close() for f in instances]
    return closedFiles

def generateInstances(total: int, path: str):
    instances = [createFile(i, path) for i in range(total)]
    return instances

def populateInstances(instances: list):
    for instance in instances:
        problem = generateProblem()
        appendToFile(instance, f"{problem[0]}")
        unities = ""
        for p in problem[1]:
            unities += f"{p} "
        appendToFile(instance, unities)
        patientList = generatePatientList(problem[0])
        for i in patientList:
<<<<<<< HEAD
            appendToFile(instance, f"{i.survivingChance} {i.priorities['UTI']} {i.priorities['UTSI']} {i.priorities['UTP']}")
=======
            appendToFile(instance, f"{i[0]} {i[1]} {i[2]} {i[3]}")
>>>>>>> b3e40f6 (Simplificando o solver e reorganizando as pastas do projeto)
    
    closeAllFiles(instances)

if __name__ == "__main__":
    instances = generateInstances(3, "Inst_Patients")
    populateInstances(instances)