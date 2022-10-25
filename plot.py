import matplotlib.pyplot as plt
import csv
import sys

problems = []
fileName = sys.argv[1]

with open(fileName) as file:
    reader = csv.reader(file, delimiter=",")
    for line in reader:
        try:
            dict = {
                "vars": line[1],
                "time": float(line[7]) / 1e6,
                "solve": line[5]
            }
            problems.append(dict)
        except:
            pass


for prob in sorted(problems, key = lambda i: i["time"]):
    if prob["solve"] == "S":
        plt.scatter(prob["vars"], prob["time"], c ="green")
    elif prob["solve"] == "U":
        plt.scatter(prob["vars"], prob["time"], c ="red")

plt.title(fileName[:-11])
plt.xlabel('variables') 
plt.ylabel('time (s)') 
plt.show()
