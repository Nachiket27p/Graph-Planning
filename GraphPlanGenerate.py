
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


def areNegated(s1, s2):
    if (s1.name[1:] == s2.name[1:]) and (neg[s1.name[0]] == s2.name[0]):
        return True
    return False


def mutexNL(sl):
    sLen = len(sl.literals)
    for i in range(sLen):
        s1 = sl.literals[i].name
        for j in range(i+1, sLen):
            s2 = sl.literals[j].name
            if (s1[1:] == s2[1:]) and (neg[s1[0]] == s2[0]):
                sl.addNL((s1, s2))


def mutexISHelper(sl, mutexes):
    for amp in mutexes:
        for e1 in amp[0].effects:
            for e2 in amp[1].effects:
                if e1 != e2:
                    p1 = (e1, e2)
                    p2 = (e2, e1)
                    if ((p1 not in sl.inconsistentSupport)
                            and (p2 not in sl.inconsistentSupport)):
                        sl.addIS(p1)


def mutexIS(sl, al):
    mutexISHelper(sl, al.inconsistentEffects)
    mutexISHelper(sl, al.inference)
    mutexISHelper(sl, al.competingNeeds)


def mutexIE(al, ne):
    aLen = len(al.actions)
    for i in range(aLen-1):
        if ne in al.actions[i].effects:
            al.addIE((al.actions[-1], al.actions[i]))


def mutexI(al):
    aLen = len(al.actions)
    for i in range(aLen):
        a1 = al.actions[i]
        for j in range(i+1, aLen):
            a2 = al.actions[j]
            if any(item in a1.effects for item in a2.preconditions):
                al.addI((a1, a2))


def mutexCN(al):
    # TODO
    return


def applyActions(gp):
    actionLayer = ActionLayer()

    stateLayer = StateLayer()

    # all the literal carry over into the next state layer
    # also takes care of 'Negated Literals mutexes'
    for s in gp.current.literals:
        stateLayer.addLiteral(s)

    for a in actions:
        if all(s in gp.current.literals for s in a.preconditions):
            actionLayer.addAction(a)
            for e in a.effects:
                # adds new literal and takes care of 'Negated Literals mutexes'
                if (e not in stateLayer.literals):
                    stateLayer.addLiteral(e)

                # Inconsistent Effect mutexes
                for l in stateLayer.literals:
                    if areNegated(e, l):
                        mutexIE(actionLayer, l)

    gp.addLayer(actionLayer)

    gp.addLayer(stateLayer)

    # Inference mutexes
    mutexI(actionLayer)

    # Competing Needs mutexes
    mutexCN(actionLayer)

    # Inconsistent Support mutexes
    mutexIS(stateLayer, actionLayer)


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
