
from Planner import *
import os
import re
from sys import argv

__author__ = 'Nachiket Patel'
__email__ = 'nnpatel5@ncsu.edu'


"""
###############################################################################
                                Global Variables
###############################################################################
"""
# expected number of arguments
nArgExpected = 2 + 1  # +1 is for the filename itself
iStates = []
gStates = []
actions = []
sDict = dict()


"""
###############################################################################
                                    Functions
###############################################################################
"""


def loadFile(inFile):
    f = open(inFile, 'r')
    line = f.readline()
    while line:
        split = re.split('\[|,|]', line)
        if split[0] == 'InitialState ':
            for i in range(1, len(split)-1):
                s = State(split[i])
                iStates.append(s)
                sDict[split[i]] = s
        elif split[0] == 'GoalState ':
            for i in range(1, len(split)-1):
                if not(split[i] in sDict):
                    sDict[split[i]] = State(split[i])
                gStates.append(sDict[split[i]])
        elif split[0] == 'Act ':
            a = Action(split[1])
            preconds = f.readline()
            psplit = re.split('\[|,|]', preconds)
            for i in range(1, len(psplit)-1):
                if not(psplit[i] in sDict):
                    sDict[psplit[i]] = State(psplit[i])
                a.addPrecondition(sDict[psplit[i]])

            effects = f.readline()
            esplit = re.split('\[|,|]', effects)
            for i in range(1, len(esplit)-1):
                if not(esplit[i] in sDict):
                    sDict[esplit[i]] = State(esplit[i])
                a.addEffect(sDict[esplit[i]])

            actions.append(a)

        line = f.readline()

    f.close()


def initializePlan():
    ivs = []
    for i in iStates:
        ivs.append(Vertex(i))

    return Graph(Layer(ivs, None))


def precondSatisfied(a, gp):
    for p in a.preconditions:
        s = False
        for v in gp.current.vertices:
            vs = v.value
            if vs == p:
                s = True
                break
        if not s:
            break
    return s


def applyAction(gp):
    for a in actions:
        if precondSatisfied(a, gp):
            print(a.act)


def plan():
    gp = initializePlan()
    applyAction(gp)
    # for a in actions:
    #     for p in gp.current.vertices:


def graphPlanGenerate():
    # number of arguments
    nArgActual = len(argv)

    # check if valid number of args passed
    if nArgActual != nArgExpected:
        print("Usage: \n\tpython BanditAlg.py <Infile> <GraphFile>")
        print("Infile - The input file with problem specification.")
        print("GraphFile - The file which will contain the resultant graph.")
        quit()

    inFile = argv[1]
    outFile = argv[2]

    loadFile(inFile)

    plan()

    # for i in iStates:
    #     print(i)
    # for g in gStates:
    #     print(g)
    # for a in actions:
    #     print((a.act))
    #     print(a.preconditions)
    #     print(a.effects)

    return 0


if __name__ == "__main__":
    graphPlanGenerate()
