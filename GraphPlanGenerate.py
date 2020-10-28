
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
# # expected number of arguments
# nArgExpected = 2 + 1  # +1 is for the filename itself
# iStates = []
# gStates = []
# actions = []
# sDict = dict()
# negate = dict()
"""
###############################################################################
                                    Functions
###############################################################################
"""


def loadFile(inFile, iStates, gStates, actions, sDict, negate):
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
                pc = psplit[i]
                if not(pc in sDict):
                    sDict[pc] = State(pc)
                a.addPrecondition(sDict[pc])

            effects = f.readline()
            esplit = re.split('\[|,|]', effects)
            for i in range(1, len(esplit)-1):
                ef = esplit[i]
                if not(ef in sDict):
                    sDict[ef] = State(ef)
                a.addEffect(sDict[ef])

            actions.append(a)

        line = f.readline()

    # create a dictionary for negated literals
    for key in sDict:
        s = sDict[key]
        nkey = "" + neg[key[0]] + key[1:]
        if nkey in sDict:
            negate[s] = sDict[nkey]
        else:
            ns = State(nkey)
            negate[s] = ns
            negate[ns] = s

    f.close()


def displayFile(inFile):
    print("\nThe problem in the file " + inFile +
          " will be solved with graph planning:\n")
    f = open(inFile, 'r')

    print("################################################################################")
    print("\t\t\t\t" + inFile)
    print("################################################################################")

    print(f.read())

    f.close()


def mutexNL(sl, negate):
    sLen = len(sl.literals)
    for i in range(sLen):
        l1 = sl.literals[i]
        for j in range(i+1, sLen):
            l2 = sl.literals[j]
            if negate[l1] == l2:
                sl.addNL(l1, l2)


def mutexISHelper(l1, l2, al, eDict):
    for a1 in eDict[l1]:
        for a2 in eDict[l2]:
            # if any one of pairs are no mutex than l1 and l2
            # cannot be mutexes so return
            if not al.areMutex(a1, a2):
                return False
    return True


def mutexIS(sl, eDict):
    sLen = len(sl.literals)
    for i in range(sLen):
        l1 = sl.literals[i]
        for j in range(i+1, sLen):
            l2 = sl.literals[j]
            if mutexISHelper(l1, l2, sl.prev, eDict):
                # if all action that cause l1 are mutex with all
                # the action that cause l2 are mutex then l1 and l2 are mutex
                sl.addIS(l1, l2)


def mutexIE(al, eDict, negate):
    effects = list(eDict)
    eLen = len(effects)
    for i in range(eLen):
        for j in range(i+1, eLen):
            if negate[effects[i]] == effects[j]:
                for a1 in eDict[effects[i]]:
                    for a2 in eDict[effects[j]]:
                        al.addIE(a1, a2)


def mutexIHelper(a1, a2, al, negate):
    for e in a1.effects:
        for p in a2.preconditions:
            if negate[e] == p:
                al.addI(a1, a2)
                return


def mutexI(al, negate):
    aLen = len(al.actions)
    for i in range(aLen):
        a1 = al.actions[i]
        for j in range(aLen):
            if i != j:
                a2 = al.actions[j]
                mutexIHelper(a1, a2, al, negate)


def mutexCNHelper(a1, a2, al, pl):
    for p1 in a1.preconditions:
        for p2 in a2.preconditions:
            if pl.areMutex(p1, p2):
                al.addCN(a1, a2)
                return


def mutexCN(al):
    pl = al.prev
    aLen = len(al.actions)
    for i in range(aLen):
        a1 = al.actions[i]
        for j in range(i+1, aLen):
            a2 = al.actions[j]
            mutexCNHelper(a1, a2, al, pl)


def initializePlan(iStates):
    initStateLayer = StateLayer()
    for s in iStates:
        initStateLayer.addLiteral(s)
    return Graph(initStateLayer)


def applyActions(gp, actions, negate):
    eDict = dict()

    actionLayer = ActionLayer()

    # add all the persistant literals from the previous layer
    for l in gp.current.literals:
        actionLayer.addAction(l)

    stateLayer = StateLayer()

    # all the literal carry over into the next state layer
    # also takes care of 'Negated Literals mutexes'
    for s in gp.current.literals:
        stateLayer.addLiteral(s)
        # make a mapping for effect to what action caused it
        eDict[s] = [s]

    for a in actions:
        if all(s in gp.current.literals for s in a.preconditions):
            actionLayer.addAction(a)
            for e in a.effects:
                # adds new literal and takes care of 'Negated Literals mutexes'
                if (e not in stateLayer.literals):
                    stateLayer.addLiteral(e)

                # make a mapping for effect to what action caused it
                if e in eDict:
                    eDict[e].append(a)
                else:
                    eDict[e] = [a]

    # add the action and the preceding state layer to the graph
    gp.addLayer(actionLayer)
    gp.addLayer(stateLayer)

    # compute the negated literal mutexes
    mutexNL(stateLayer, negate)

    # compute the inconsistent effects mutexes
    mutexIE(actionLayer, eDict, negate)

    # interference mutexes
    mutexI(actionLayer, negate)

    # Competing Needs mutexes
    mutexCN(actionLayer)

    # Inconsistent Support mutexes
    mutexIS(stateLayer, eDict)


def checkCompletion(gp):
    currStateLayer = gp.current
    lastStateLayer = currStateLayer.prev.prev
    return (currStateLayer == lastStateLayer)


def writeOutGP(gp, outFile):
    gp.writeOut(outFile)


def plan(gp, actions, negate):
    complete = False
    while(not complete):
        # apply action and produce the next state layer
        applyActions(gp, actions, negate)
        complete = checkCompletion(gp)


def graphPlanGenerate():
    # expected number of arguments
    nArgExpected = 2 + 1  # +1 is for the filename itself
    iStates = []
    gStates = []
    actions = []
    sDict = dict()
    negate = dict()

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

    # display the file to the user
    displayFile(inFile)

    loadFile(inFile, iStates, gStates, actions, sDict, negate)
    gp = initializePlan(iStates)
    plan(gp, actions, negate)
    gp.writeOut(outFile)

    return 0


if __name__ == "__main__":
    graphPlanGenerate()
