mNL = 1
mIE = 2
mI = 3
mCN = 4
mIS = 5


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
        self.__actions = dict()
        self.__mutexes = dict()
        self.__depth = None

    @property
    def prev(self):
        return self.__prev

    @ property
    def next(self):
        return self.__next

    @property
    def actions(self):
        return list(self.__actions)

    @property
    def depth(self):
        return self.__depth

    @property
    def mutexes(self):
        return self.__mutexes

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
        if action not in self.__actions:
            self.__actions[action] = action

    def addMutex(self, a1, a2, mType):
        if not self.__validMutex:
            return False

        if a1 != a2:
            if a2 <= a1:
                a1, a2 = a2, a1

            if (a1, a2) not in self.__mutexes:
                self.__mutexes[(a1, a2)] = [mType]
            else:
                if mType not in self.__mutexes[(a1, a2)]:
                    self.__mutexes[(a1, a2)].append(mType)

    def areMutex(self, a1, a2):
        if a2 <= a1:
            a1, a2 = a2, a1

        if (a1, a2) in self.__mutexes:
            return True

        return False

    def __validMutex(self, mType):
        if mType == mIE | mType == mI | mType == mCN:
            return True
        return False

    def __eq__(self, other):
        if (self.actions == other.actions) and (self.__mutexes == other.mutexes):
            return True
        return False

    def __str__(self):
        rtnStr = "ActLayer: <" + str(self.__depth) + ">"

        rtnStr += "\n\tActions: "
        for a in self.__actions:
            if isinstance(a, Action):
                rtnStr += str(a) + ", "

        if rtnStr[-2] == ',':
            rtnStr = rtnStr[:-2]

        ieString = "\n\tInconsistent Effects: "
        iString = "\n\tinterference: "
        cnString = "\n\tCompeting Needs: "

        for m in self.__mutexes:
            val = self.__mutexes[m]
            for mType in val:
                if mType == mIE:
                    ieString += str(m) + ", "
                elif mType == mI:
                    iString += str(m) + ", "
                elif mType == mCN:
                    cnString += str(m) + ", "

        # remove last comma
        if ieString[-2] == ',':
            ieString = ieString[:-2]
        if iString[-2] == ',':
            iString = iString[:-2]
        if cnString[-2] == ',':
            cnString = cnString[:-2]

        rtnStr += ieString + iString + cnString + "\n"
        return rtnStr


class StateLayer:
    def __init__(self):
        self.__prev = None
        self.__next = None
        self.__literals = dict()
        self.__mutexes = dict()
        self.__depth = None

    @ property
    def prev(self):
        return self.__prev

    @ property
    def next(self):
        return self.__next

    @ property
    def literals(self):
        return list(self.__literals)

    @ property
    def depth(self):
        return self.__depth

    @property
    def mutexes(self):
        return self.__mutexes

    @ prev.setter
    def prev(self, value):
        self.__prev = value

    @ next.setter
    def next(self, value):
        self.__next = value

    @ depth.setter
    def depth(self, value):
        self.__depth = value

    def causes(self, l1):
        if l1 in self.__literals:
            return self.__literals[l1]
        else:
            return None

    def addLiteral(self, literal, cause):
        if literal not in self.__literals:
            self.__literals[literal] = [cause]
        elif cause not in self.__literals[literal]:
            self.__literals[literal].append(cause)

    def addMutex(self, l1, l2, mType):
        if not self.__validMutex:
            return False

        if l1 != l2:
            if l2 <= l1:
                l1, l2 = l2, l1

            if (l1, l2) not in self.__mutexes:
                self.__mutexes[(l1, l2)] = [mType]
            else:
                self.__mutexes[(l1, l2)].append(mType)

    def areMutex(self, l1, l2):
        if l2 <= l1:
            l1, l2 = l2, l1

        if (l1, l2) in self.__mutexes:
            return True
        return False

    def __validMutex(self, mType):
        if mType == mNL | mType == mIS:
            return True
        return False

    def __eq__(self, other):
        if ((self.literals == other.literals) and (self.__mutexes == other.mutexes)):
            return True
        return False

    def __str__(self):
        rtnStr = "StateLayer: <" + str(self.__depth) + ">"

        rtnStr += "\n\tLiterals: "
        for l in self.__literals:
            rtnStr += str(l) + ", "

        if rtnStr[-2] == ',':
            rtnStr = rtnStr[:-2]

        nlString = "\n\tNegated Literals: "
        isString = "\n\tInconsistent Support: "

        for m in self.__mutexes:
            val = self.__mutexes[m]
            for mType in val:
                if mType == mNL:
                    nlString += str(m) + ", "
                elif mType == mIS:
                    isString += str(m) + ", "

        # remove last comma
        if nlString[-2] == ',':
            nlString = nlString[:-2]
        if isString[-2] == ',':
            isString = isString[:-2]

        rtnStr += nlString + isString + "\n"
        return rtnStr


class Graph:
    def __init__(self, rootLayer):
        self.__root = rootLayer
        self.__current = rootLayer
        self.__currentDepth = 0
        self.__solution = "No Plan"
        rootLayer.depth = 0

    @ property
    def root(self):
        return self.__root

    @ property
    def solution(self):
        return self.__solution

    @ property
    def current(self):
        return self.__current

    @solution.setter
    def solution(self, value):
        self.__solution = value

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

    def writeOutSol(self, outFile):
        of = open(outFile, "w")
        sol = "Solution: " + str(self.__solution)
        sol += "\n--------------------------------------------------------------------------------\n"
        of.write(sol)
        of.write(str(self))
        of.close()

    def __str__(self):
        curr = self.__root
        gpString = ""
        while curr:
            gpString += str(curr)
            curr = curr.next
        return gpString
