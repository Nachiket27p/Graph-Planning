
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
negate = dict()
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


# def areNegated(s1, s2):
#     if (s1.name[1:] == s2.name[1:]) and (neg[s1.name[0]] == s2.name[0]):
#         return True
#     return False


def mutexNL(sl):
    for key in sl.literals:
        if negate[key] in sl.literals:
            sl.addNL(key, negate[key])


def mutexISHelper(l1, l2, al, eDict):
    for a1 in eDict[l1]:
        for a2 in eDict[l2]:
            # if any one of pairs are no mutex than l1 and l2
            # cannot be mutexes so return
            if not al.areMutex(a1, a2):
                return False
    return True


def mutexIS(sl, eDict):
    lit = list(sl.literals)
    sLen = len(lit)

    for i in range(sLen):
        l1 = lit[i]
        for j in range(i+1, sLen):
            l2 = lit[j]
            # if all action that cause l1 are mutex with all
            # the action that cause l2 are mutex then l1 and l2 are mutex
            if mutexISHelper(l1, l2, sl.prev, eDict):
                sl.addIS(l1, l2)


def mutexIE(al, sl):
    for act in al.actions:
        for e in act.effects:
            ne = negate[e]
            if ne in sl.literals:
                for otherAct in al.actions:
                    if (act != otherAct) and (ne in otherAct.effects):
                        al.addIE(act, otherAct)


def mutexI(al, sl):
    for act in al.actions:
        for p in act.preconditions:
            ne = negate[p]
            if ne in sl.literals:
                for otherAct in al.actions:
                    if (act != otherAct) and (ne in otherAct.effects):
                        al.addI(act, otherAct)


def mutexCN(al):
    pl = al.prev
    actionList = list(al.actions)
    aLen = len(actionList)
    for i in range(aLen):
        act = actionList[i]
        for j in range(i+1, aLen):
            otherAct = actionList[j]
            for p1 in act.preconditions:
                for p2 in otherAct.preconditions:
                    if pl.areMutex(p1, p2):
                        al.addCN(act, otherAct)


def initializePlan():
    initStateLayer = StateLayer()
    for s in iStates:
        initStateLayer.addLiteral(s)
    return Graph(initStateLayer)


def applyActions(gp):
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

    gp.addLayer(actionLayer)

    gp.addLayer(stateLayer)

    # inconsistent effect
    mutexIE(actionLayer, stateLayer)
    # interference mutexes
    mutexI(actionLayer, stateLayer)
    # Competing Needs mutexes
    mutexCN(actionLayer)

    # negated literal
    mutexNL(stateLayer)
    # Inconsistent Support mutexes
    mutexIS(stateLayer, eDict)


def plan():
    gp = initializePlan()

    # apply action and produce the next state layer
    applyActions(gp)
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
