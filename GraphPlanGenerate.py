
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
INIT = "Initial"
GOAL = "Goal"
INTER = "Intermediate"
iStates = []
gStates = []
actions = []

"""
###############################################################################
                                    Classes
###############################################################################
"""


class State:
    def __init__(self, name, sType):
        self.__name = name
        self.__sType = sType

    @property
    def name(self):
        return self.__name

    @property
    def sType(self):
        return self.__sType

    def __str__(self):
        rtn = ""
        if self.__sType == "Goal":
            rtn += "GoalState: "
        elif self.__sType == "Initial":
            rtn += "InitialState: "
        else:
            rtn += "IntermediateState: "

        rtn += self.__name
        return rtn


class Action:
    def __init__(self, act, preconditions=[], effects=[]):
        self.__act = act
        self.__preconditions = preconditions
        self.__effects = effects

    @property
    def act(self):
        return self.__act

    @property
    def preconditions(self):
        return self.__preconditions

    @property
    def effects(self):
        return self.__effects

    def addPrecondition(self, precondition):
        self.__preconditions.append(precondition)

    def addEffect(self, effect):
        self.__effects.append(effect)

    def __str__(self):
        return ("Action: " + self.__act +
                "\n\tPreconditions:\t" +
                str(self.__preconditions) +
                "\n\tEffects:\t" +
                str(self.__effects))


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
                iStates.append(State(split[i], INIT))
        elif split[0] == 'GoalState ':
            for i in range(1, len(split)-1):
                gStates.append(State(split[i], GOAL))
        elif split[0] == 'Act ':
            a = Action(split[1])

            preconds = f.readline()
            psplit = re.split('\[|,|]', preconds)
            for i in range(1, len(psplit)-1):
                a.addPrecondition(psplit[i])

            effects = f.readline()
            esplit = re.split('\[|,|]', effects)
            for i in range(1, len(esplit)-1):
                a.addEffect(esplit[i])

            actions.append(a)

        line = f.readline()

    f.close()


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

    for i in iStates:
        print(i)
    for g in gStates:
        print(g)
    for a in actions:
        print(a)

    return 0


if __name__ == "__main__":
    graphPlanGenerate()
