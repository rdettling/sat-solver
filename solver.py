import time
import sys
import csv

def readFile(fileName): #add all lines in the file to a list
    with open(fileName, "r") as file:
        list = []
        for line in file:
            if line[0] == "c" or line[0] == "p":
                line = line.split(" ")
                line[-1] = line[-1][:-1]
            else:
                line = line.split(",")
                line = line[:-1]

            list.append(line)

    return list 

def getProblems(lines): #create a list called problems where each element is a dictionary which represents a distinct cnf
    problems = []
    i = 0

    while i < len(lines):
        if lines[i][0] == "c":
            dict = { #create a dict for each problem
                "clauseList" : [],
                "num" : lines[i][1],
                "maxLiterals" : lines[i][2],
                "satisfiable" : lines[i][3],
                "vars" : lines[i+1][2],
                "clauses" : lines[i+1][3],
                "totalLiterals" : 0
            }
            
            j = i + 2
            while j < len(lines):
                if lines[j][0] == "c":
                    problems.append(dict)
                    i = j - 1
                    break
                elif j == len(lines)-1:
                    dict["totalLiterals"] += len(lines[j])
                    dict["clauseList"].append(lines[j])
                    problems.append(dict)
                    i = j - 1
                    break
                else:
                    dict["totalLiterals"] += len(lines[j])
                    dict["clauseList"].append(lines[j])
                
                j += 1
        i += 1

    return problems

def varAssignment(vars): #generate all possible var assignments in a list of lists
    combinations = 2**vars
    assignmentList = [[0 for x in range(vars)] for y in range(combinations)] 

    for i in range(vars): 
        max = combinations / 2**(i+1) #max number of trues before switching to false
        countT = 0
        countF = 0
        for j in range(combinations):
            if countT < max:
                assignmentList[j][i] = "T"
                countT += 1
            elif countF < max:
                assignmentList[j][i] = "F"
                countF += 1
            else:
                assignmentList[j][i] = "T"
                countT = 1
                countF = 0
        
    return assignmentList

def verify(expression, assignment): #check if cnf is solvable
    satisfiable = True

    untranslated = [] #copy the expression into a new expression so you can translate it without messing up th original
    for clause in expression:
        untranslated.append(clause[:])

    for clause in untranslated:
        clauseValid = False

        for i in range(len(clause)):
            var = int(clause[i])
            if var > 0:
                clause[i] = assignment[var-1]
            else:
                if assignment[abs(var)-1] == "T":
                    clause[i] = "F"
                else:
                    clause[i] = "T"

        for var in clause: #make sure every clause has at least one true
            if var == "T":
                clauseValid = True
                break

        if not clauseValid: #if any clause is not valid then the whole cnf is not satisfiable
            satisfiable = False
            break

    return satisfiable

def writeOutput(problems, fileName, maxVars): #generate csv
    with open(f"{fileName[:-4]}-output.csv", "w") as output:
        writer = csv.writer(output)

        correct = 0
        solvableCount = 0
        unsolvableCount = 0
        answersProvided = 0

        for problem in problems:
            if int(problem['vars']) > maxVars:
                continue
            solvable = "U"
            
            time1 = time.time()
            for varCombination in varAssignment(int(problem["vars"])):
                if verify(problem["clauseList"], varCombination):
                    solvable = "S"
                    break
            executionTime =  round((time.time() - time1) * 1e6, 1)
            print(f"Finished problem {problem['num']}: Vars: {problem['vars']}, Execution time: {round(executionTime / 1e6, 2)} seconds")

            if solvable == "S":
                solvableCount += 1
            else:
                unsolvableCount += 1

            if problem["satisfiable"] == "?":
                agreed = 0
            elif problem["satisfiable"] == solvable:
                answersProvided += 1 
                agreed = 1
                correct += 1
            else:
                answersProvided += 1 
                agreed = -1

            outputLine = [
                problem["num"],
                problem["vars"],
                problem["clauses"],
                problem["maxLiterals"],
                problem["totalLiterals"],
                solvable,
                agreed,
                executionTime,
            ]

            if solvable == "S":
                for var in varCombination:
                    if var == "T":
                        outputLine.append(1)
                    else:
                        outputLine.append(0)

            writer.writerow(outputLine)
        
        writer.writerow([fileName, len(problems), solvableCount, unsolvableCount, answersProvided, correct])

def main():
    fileName = sys.argv[1]
    if len(sys.argv) > 2: #second command line arg is the max num of vars
        maxVars = int(sys.argv[2])
    else:
        maxVars = 24
    lines = readFile(fileName)
    problems = getProblems(lines)
    writeOutput(problems, fileName, maxVars)


if __name__ == '__main__':
    main()