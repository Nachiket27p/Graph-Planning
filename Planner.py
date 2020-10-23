
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

    # def __repr__(self):
    #     return self.__name


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
        return ("Action: " + self.__act +
                "\n\tPreconditions:\t" +
                str(self.__preconditions) +
                "\n\tEffects:\t" +
                str(self.__effects))


class Vertex:
    def __init__(self, value):
        self.__value = value
        self.__prev = []

    @property
    def value(self):
        return self.__value

    @property
    def prev(self):
        return self.__prev


# class Edge:
#     def __inti__(self, v1, v2):
#         self.__v1 = v1
#         self.__v2 = v2


class Layer:
    def __init__(self, vertices, prev):
        self.__vertices = vertices
        self.__prev = prev
        self.__negatedLiterals = []
        self.__inconsistentEffects = []
        self.__inference = []
        self.__competingNeeds = []
        self.__inconsistentSupport = []

    @property
    def vertices(self):
        return self.__vertices

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
    def setter(self, value):
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

    @property
    def root(self):
        return self.__root

    @property
    def current(self):
        return self.__current

    def addActionLayer(self, actionLayer):
        actionLayer.prev = self.__current
        self.__current = actionLayer

    def addStateLayer(self, stateLayer):
        stateLayer.prev = self.__current
        self.__current = stateLayer
