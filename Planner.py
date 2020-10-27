
"""
###############################################################################
                                Global Variables
###############################################################################
"""

INIT = "Initial"
GOAL = "Goal"
INTER = "Intermediate"
neg = {'+': '-', '-': '+'}

"""
###############################################################################
                                    Classes
###############################################################################
"""


class State:
    def __init__(self, name):
        self.__name = name
        self.__preconditions = [self]
        self.__effects = [self]

    @property
    def name(self):
        return self.__name

    @property
    def preconditions(self):
        return self.__preconditions

    @property
    def effects(self):
        return self.__effects

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
        return self.__act

    def __repr__(self):
        return self.__act


class ActionLayer:
    def __init__(self):
        self.__prev = None
        self.__actions = []
        self.__inconsistentEffects = []
        self.__interference = []
        self.__competingNeeds = []
        self.__depth = None

    @property
    def actions(self):
        return self.__actions

    @property
    def depth(self):
        return self.__depth

    @property
    def prev(self):
        return self.__prev

    @property
    def inconsistentEffects(self):
        return self.__inconsistentEffects

    @property
    def interference(self):
        return self.__interference

    @property
    def competingNeeds(self):
        return self.__competingNeeds

    @prev.setter
    def prev(self, value):
        self.__prev = value

    @depth.setter
    def depth(self, value):
        self.__depth = value

    def addAction(self, action):
        self.__actions.append(action)

    def addIE(self, value):
        self.__inconsistentEffects.append(value)

    def addI(self, value):
        self.__interference.append(value)

    def addCN(self, value):
        self.__competingNeeds.append(value)

    def areMutex(self, a1, a2):
        if (((a1, a2) in self.__inconsistentEffects)
                | ((a2, a1) in self.__inconsistentEffects)
                | ((a1, a2) in self.__interference)
                | ((a2, a1) in self.__interference)
                | ((a1, a2) in self.__competingNeeds)
                | ((a2, a1) in self.__competingNeeds)):
            return True
        return False

    def __str__(self):
        rtnStr = "ActLayer: <" + str(self.__depth) + ">"

        rtnStr += "\n\tActions: "
        for i in range(len(self.__actions)):
            rtnStr += str(self.__actions[i])
            if i < len(self.__actions)-1:
                rtnStr += ', '

        rtnStr += "\n\tInconsistent Effects: "
        for i in range(len(self.__inconsistentEffects)):
            rtnStr += str(self.__inconsistentEffects[i])
            if i < len(self.__inconsistentEffects)-1:
                rtnStr += ', '

        rtnStr += "\n\tinterference: "
        for i in range(len(self.__interference)):
            rtnStr += str(self.__interference[i])
            if i < len(self.__interference)-1:
                rtnStr += ', '

        rtnStr += "\n\tCompeting Needs: "
        for i in range(len(self.__competingNeeds)):
            rtnStr += str(self.__competingNeeds[i])
            if i < len(self.__competingNeeds)-1:
                rtnStr += ', '

        rtnStr += "\n"
        return rtnStr


class StateLayer:
    def __init__(self):
        self.__prev = None
        self.__literals = []
        self.__negatedLiterals = []
        self.__inconsistentSupport = []
        self.__depth = None

    @ property
    def literals(self):
        return self.__literals

    @ property
    def depth(self):
        return self.__depth

    @ property
    def prev(self):
        return self.__prev

    @ property
    def negatedLiterals(self):
        return self.__negatedLiterals

    @ property
    def inconsistentSupport(self):
        return self.__inconsistentSupport

    @ prev.setter
    def prev(self, value):
        self.__prev = value

    @ depth.setter
    def depth(self, value):
        self.__depth = value

    def addLiteral(self, literal):
        self.__literals.append(literal)
        self.__checkNL(literal)

    def __checkNL(self, nl):
        for l in self.__literals:
            if (nl.name[1:] == l.name[1:]) and (neg[nl.name[0]] == l.name[0]):
                self.addNL((nl, l))

    def addNL(self, value):
        self.__negatedLiterals.append(value)

    def addIS(self, value):
        self.__inconsistentSupport.append(value)

    def __str__(self):
        rtnStr = "StateLayer: <" + str(self.__depth) + ">"

        rtnStr += "\n\tLiterals: "
        for i in range(len(self.__literals)):
            rtnStr += str(self.__literals[i])
            if i < len(self.__literals)-1:
                rtnStr += ', '

        rtnStr += "\n\tNegated Literals: "
        for i in range(len(self.__negatedLiterals)):
            rtnStr += str(self.__negatedLiterals[i])
            if i < len(self.__negatedLiterals)-1:
                rtnStr += ', '

        rtnStr += "\n\tInconsistent Support: "
        for i in range(len(self.__inconsistentSupport)):
            rtnStr += str(self.__inconsistentSupport[i])
            if i < len(self.__inconsistentSupport)-1:
                rtnStr += ', '

        rtnStr += "\n"
        return rtnStr


class Graph:
    def __init__(self, rootLayer):
        self.__root = rootLayer
        self.__current = rootLayer
        self.__currentDepth = 0
        rootLayer.depth = 0

    @ property
    def root(self):
        return self.__root

    @ property
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
            gpString += str(curr)
            curr = curr.prev
        return gpString


"""
if type(curr) == ActionLayer:
                gpString += "ActLayer: <" + str(curr.depth) + ">"
                gpString += "\n\tActions: "

                for i in range(len(curr.actions)):
                    gpString += str(curr.actions[i])
                    if i < len(curr.actions)-1:
                        gpString += ', '

                # for s in curr.actions:
                #     gpString += str(s) + ", "
                gpString += "\n\tInconsistent Effects: "
                for s in curr.inconsistentEffects:
                    gpString += str(s) + ", "
                gpString += "\n\tinterference: "
                for s in curr.interference:
                    gpString += str(s) + ", "
                gpString += "\n\tCompeting Needs: "
                for s in curr.competingNeeds:
                    gpString += str(s) + ", "
                gpString += "\n"

            else:
                gpString += "StateLayer: <" + str(curr.depth) + ">"
                gpString += "\n\tLiterals: "
                for s in curr.literals:
                    gpString += str(s) + ", "
                gpString += "\n\tNegated Literals: "
                for s in curr.negatedLiterals:
                    gpString += str(s) + ", "
                gpString += "\n\tInconsistent Support: "
                for s in curr.inconsistentSupport:
                    gpString += str(s) + ", "
                gpString += "\n"
"""
