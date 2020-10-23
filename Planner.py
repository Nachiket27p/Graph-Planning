
"""
###############################################################################
                                Global Variables
###############################################################################
"""

INIT = "Initial"
GOAL = "Goal"
INTER = "Intermediate"

"""
###############################################################################
                                    Classes
###############################################################################
"""


class State:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name


class Action:
    def __init__(self, act):
        self.__act = act
        self.__preconditions = []
        self.__effects = []

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
        return (self.__act +
                "\n  Preconditions: " +
                str(self.__preconditions) +
                "\n        Effects: " +
                str(self.__effects))


class Layer:
    def __init__(self, states, actionLayer=False):
        self.__prev = None
        self.__states = states
        self.__actionLayer = actionLayer
        self.__negatedLiterals = []
        self.__inconsistentEffects = []
        self.__inference = []
        self.__competingNeeds = []
        self.__inconsistentSupport = []
        self.__depth = None

    @property
    def depth(self):
        return self.__depth

    @depth.setter
    def depth(self, value):
        self.__depth = value

    @property
    def actionLayer(self):
        return self.__actionLayer

    @property
    def states(self):
        return self.__states

    @property
    def prev(self):
        return self.__prev

    @property
    def negatedLiterals(self):
        return self.__negatedLiterals

    @property
    def inconsistentEffects(self):
        return self.__inconsistentEffects

    @property
    def inference(self):
        return self.__inference

    @property
    def competingNeeds(self):
        return self.__competingNeeds

    @property
    def inconsistentSupport(self):
        return self.__inconsistentSupport

    @prev.setter
    def prev(self, value):
        self.__prev = value

    def addNL(self, value):
        self.__negatedLiterals.append(value)

    def addIE(self, value):
        self.__inconsistentEffects.append(value)

    def addI(self, value):
        self.__inference.append(value)

    def addCN(self, value):
        self.__competingNeeds.append(value)

    def addIS(self, value):
        self.__inconsistentSupport.append(value)


class Graph:
    def __init__(self, rootLayer):
        self.__root = rootLayer
        self.__current = rootLayer
        self.__currentDepth = 0

    @property
    def root(self):
        return self.__root

    @property
    def current(self):
        return self.__current

    def addLayer(self, layer):
        self.__currentDepth += 1
        layer.depth = self.__currentDepth
        layer.prev = self.__current
        self.__current = layer

    def __str__(self):
        curr = self.__current
        gpString = ""
        while curr:
            for s in curr.states:
                gpString += str(s) + "\n"
            gpString += "--------------------------------------------------------------------------------\n"
            curr = curr.prev
        return gpString
