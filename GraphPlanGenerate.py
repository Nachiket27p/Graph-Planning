
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
    initStateLayer = StateLayer()
    for s in iStates:
        initStateLayer.addLiteral(s)
    return Graph(initStateLayer)


def mutexNL(sl):
    sLen = len(sl.literals)
    for i in range(sLen):
        s1 = sl.literals[i].name
        for j in range(i+1, sLen):
            s2 = sl.literals[j].name
            if (s1[1:] == s2[1:]) and (neg[s1[0]] == s2[0]):
                sl.addNL((s1, s2))


def mutexIE(al, ne):
    aLen = len(al.actions)
    for i in range(aLen-1):
        if ne in al.actions[i].effects:
            al.addIE((al.actions[-1], al.actions[i]))


def applyActions(gp):
    actionLayer = ActionLayer()
    stateLayer = StateLayer()

    deleted = []

    prevNLCount = len(stateLayer.negatedLiterals)
    for a in actions:
        if all(s in gp.current.literals for s in a.preconditions):
            actionLayer.addAction(a)
            for e in a.effects:
                if (e not in stateLayer.literals):
                    stateLayer.addLiteral(e)
                    # check for inconsistent effect
                    if len(stateLayer.negatedLiterals) > prevNLCount:
                        mutexIE(actionLayer, stateLayer.negatedLiterals[-1][1])
                        prevNLCount = len(stateLayer.negatedLiterals)
                else:
                    for nlPair in stateLayer.negatedLiterals:
                        if nlPair[0] == e:
                            mutexIE(actionLayer,
                                    stateLayer.negatedLiterals[-1][1])
                        elif nlPair[1] == e:
                            mutexIE(actionLayer,
                                    stateLayer.negatedLiterals[-1][0])

            deleted.extend(a.preconditions)

    gp.addLayer(actionLayer)

    for s in gp.current.prev.literals:
        if (s not in deleted):
            stateLayer.addLiteral(s)

    gp.addLayer(stateLayer)


def plan():
    gp = initializePlan()

    # apply action and produce the next state layer
    applyActions(gp)

    print(gp)


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
