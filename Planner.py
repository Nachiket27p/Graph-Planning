
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
        return self.__act

    # def __repr__(self):
    #     return self.__act


class ActionLayer:
    def __init__(self):
        self.__prev = None
        self.__actions = dict()
        self.__inconsistentEffects = dict()
        self.__interference = dict()
        self.__competingNeeds = dict()
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
        if action not in self.__actions:
            self.__actions[action] = action

    def addIE(self, act1, act2):
        if ((act1 not in self.__inconsistentEffects)
                and (act2 not in self.__inconsistentEffects)):
            self.__inconsistentEffects[act1] = act2

    def addI(self, act1, act2):
        if ((act1 not in self.__interference)
                and (act2 not in self.__interference)):
            self.__interference[act1] = act2

    def addCN(self, act1, act2):
        if ((act1 not in self.__competingNeeds)
                and (act2 not in self.__competingNeeds)):
            self.__competingNeeds[act1] = act2

    def areMutex(self, a1, a2):
        a = ((a1 in self.__inconsistentEffects) and (
            a2 == self.__inconsistentEffects[a1]))
        a = ((a2 in self.__inconsistentEffects) and (
            a1 == self.__inconsistentEffects[a2]))
        a = ((a1 in self.__interference) and (a2 == self.__interference[a1]))
        a = ((a2 in self.__interference) and (a1 == self.__interference[a2]))
        a = ((a1 in self.__competingNeeds) and (
            a2 == self.__competingNeeds[a1]))
        a = ((a2 in self.__competingNeeds) and (
            a1 == self.__competingNeeds[a2]))

        if (((a1 in self.__inconsistentEffects) and (a2 == self.__inconsistentEffects[a1]))
                | ((a2 in self.__inconsistentEffects) and (a1 == self.__inconsistentEffects[a2]))
                | ((a1 in self.__interference) and (a2 == self.__interference[a1]))
                | ((a2 in self.__interference) and (a1 == self.__interference[a2]))
                | ((a1 in self.__competingNeeds) and (a2 == self.__competingNeeds[a1]))
                | ((a2 in self.__competingNeeds) and (a1 == self.__competingNeeds[a2]))):
            return True
        return False

    def __str__(self):
        rtnStr = "ActLayer: <" + str(self.__depth) + ">"

        rtnStr += "\n\tActions: "
        for key in self.__actions:
            rtnStr += str(key) + ", "

        rtnStr += "\n\tInconsistent Effects: "
        for key in self.__inconsistentEffects:
            rtnStr += "(" + str(key) + "," + \
                str(self.__inconsistentEffects[key]) + "), "

        rtnStr += "\n\tinterference: "
        for key in self.__interference:
            rtnStr += "(" + str(key) + "," + \
                str(self.__interference[key]) + "), "

        rtnStr += "\n\tCompeting Needs: "
        for key in self.__competingNeeds:
            rtnStr += "(" + str(key) + "," + \
                str(self.__competingNeeds[key]) + "), "

        rtnStr += "\n"
        return rtnStr


class StateLayer:
    def __init__(self):
        self.__prev = None
        self.__literals = dict()
        self.__negatedLiterals = dict()
        self.__inconsistentSupport = dict()
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
        if literal not in self.__literals:
            self.__literals[literal] = literal

    def addNL(self, lit, nlit):
        if ((lit not in self.__negatedLiterals)
                and (nlit not in self.__negatedLiterals)):
            self.__negatedLiterals[lit] = nlit

    def addIS(self, lit1, lit2):
        if ((lit1 not in self.__inconsistentSupport)
                and (lit2 not in self.__inconsistentSupport)):
            self.__inconsistentSupport[lit1] = lit2

    def areMutex(self, l1, l2):
        if (((l1 in self.__negatedLiterals) and (l2 == self.__negatedLiterals[l1]))
                | ((l2 in self.__negatedLiterals) and (l1 == self.__negatedLiterals[l2]))
                | ((l1 in self.__inconsistentSupport) and (l2 == self.__inconsistentSupport[l1]))
                | ((l2 in self.__inconsistentSupport) and (l1 == self.__inconsistentSupport[l2]))):
            return True
        return False

    def __str__(self):
        rtnStr = "StateLayer: <" + str(self.__depth) + ">"

        rtnStr += "\n\tLiterals: "
        for key in self.__literals:
            rtnStr += str(key) + ", "

        rtnStr += "\n\tNegated Literals: "
        for key in self.__negatedLiterals:
            rtnStr += "(" + str(key) + "," + \
                str(self.__negatedLiterals[key]) + "), "

        rtnStr += "\n\tInconsistent Support: "
        for key in self.__inconsistentSupport:
            rtnStr += "(" + str(key) + "," + \
                str(self.__inconsistentSupport[key]) + "), "

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
