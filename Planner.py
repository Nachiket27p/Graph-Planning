
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

    def __le__(self, other):
        return (self.__name <= other.name)


class Action:
    def __init__(self, name):
        self.__name = name
        self.__preconditions = []
        self.__effects = []

    @property
    def name(self):
        return self.__name

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
        return self.__name

    def __repr__(self):
        return self.__name

    def __le__(self, other):
        return (self.__name <= other.name)


class ActionLayer:
    def __init__(self):
        self.__prev = None
        self.__next = None
        self.__actions = []
        self.__inconsistentEffects = []
        self.__interference = []
        self.__competingNeeds = []
        self.__depth = None

    @property
    def prev(self):
        return self.__prev

    @ property
    def next(self):
        return self.__next

    @property
    def actions(self):
        return self.__actions

    @property
    def depth(self):
        return self.__depth

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

    @ next.setter
    def next(self, value):
        self.__next = value

    @depth.setter
    def depth(self, value):
        self.__depth = value

    def addAction(self, action):
        self.__actions.append(action)

    def addIE(self, a1, a2):
        if a1 != a2:
            if a1 <= a2:
                self.__inconsistentEffects.append((a1, a2))
            else:
                self.__inconsistentEffects.append((a2, a1))

    def addI(self, a1, a2):
        if a1 != a2:
            if a1 <= a2:
                self.__interference.append((a1, a2))
            else:
                self.__interference.append((a2, a1))

    def addCN(self, a1, a2):
        if a1 != a2:
            if a1 <= a2:
                self.__competingNeeds.append((a1, a2))
            else:
                self.__competingNeeds.append((a2, a1))

    def areMutex(self, a1, a2):
        if a2 <= a1:
            a1, a2 = a2, a1

        if (((a1, a2) in self.__inconsistentEffects)
                | ((a1, a2) in self.__interference)
                | ((a1, a2) in self.__competingNeeds)):
            return True
        return False

    def __eq__(self, other):
        if ((self.__actions == other.actions)
                and (self.__inconsistentEffects == other.__inconsistentEffects)
                and (self.__interference == other.__interference)
                and (self.__competingNeeds == other.__competingNeeds)):
            return True
        return False

    def __str__(self):
        rtnStr = "ActLayer: <" + str(self.__depth) + ">"

        rtnStr += "\n\tActions: "
        for i in range(len(self.__actions)):
            if isinstance(self.__actions[i], Action):
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
        self.__next = None
        self.__literals = []
        self.__negatedLiterals = []
        self.__inconsistentSupport = []
        self.__depth = None

    @ property
    def prev(self):
        return self.__prev

    @ property
    def next(self):
        return self.__next

    @ property
    def literals(self):
        return self.__literals

    @ property
    def depth(self):
        return self.__depth

    @ property
    def negatedLiterals(self):
        return self.__negatedLiterals

    @ property
    def inconsistentSupport(self):
        return self.__inconsistentSupport

    @ prev.setter
    def prev(self, value):
        self.__prev = value

    @ next.setter
    def next(self, value):
        self.__next = value

    @ depth.setter
    def depth(self, value):
        self.__depth = value

    def addLiteral(self, literal):
        self.__literals.append(literal)

    def addNL(self, l1, l2):
        if l1 != l2:
            if l1 <= l2:
                self.__negatedLiterals.append((l1, l2))
            else:
                self.__negatedLiterals.append((l2, l1))

    def addIS(self, l1, l2):
        if l1 != l2:
            if l1 <= l2:
                self.__inconsistentSupport.append((l1, l2))
            else:
                self.__inconsistentSupport.append((l2, l1))

    def areMutex(self, l1, l2):
        if l2 <= l1:
            l1, l2 = l2, l1

        if (((l1, l2) in self.__negatedLiterals)
                | ((l1, l2) in self.__inconsistentSupport)):
            return True
        return False

    def __eq__(self, other):
        if ((self.__literals == other.literals)
                and (self.__negatedLiterals == other.negatedLiterals)
                and (self.__inconsistentSupport == other.__inconsistentSupport)):
            return True
        return False

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
        self.__current.next = layer
        self.__current = layer

    def writeOut(self, outFile):
        of = open(outFile, "w")
        of.write(str(self))
        of.close()

    def __str__(self):
        curr = self.__root
        gpString = ""
        while curr:
            gpString += str(curr)
            curr = curr.next
        return gpString
