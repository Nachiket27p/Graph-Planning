"""
###############################################################################
                                    Globals
###############################################################################
"""
# These variables are used when mutexes are added to StateLayer and
# ActionLayer objects. These variables are also used in GraphPlanGenerate.py
# and GraphPlanExtract.py when inserting mutexes.
mNL = 1
mIE = 2
mI = 3
mCN = 4
mIS = 5


"""
###############################################################################
                                    Classes
###############################################################################
"""


class LayerElement:
    """
        This is the base class for the State and Action class. This class
        has three properties; name, preconditions, and effects. The class also
        overloads the __str__, __repr__, and __le__ functions.
    """

    def __init__(self, name, isState=False):
        """
            Constructor for this class, takes one parameter. The name, and
            sets the preconditions and effects to itself so it can be used
            to represent persistance during graph planning.

        Args:
            name (String): Name of the state/action
        """
        self._name = name
        self._preconditions = []
        self._effects = []
        if isState:
            self._preconditions.append(self)
            self._effects.append(self)

    @property
    def name(self):
        """
            Getter for the name of the state.
        Returns:
            String: Name of the state
        """
        return self._name

    @property
    def preconditions(self):
        """
            Getter for the preconditions.
        Returns:
            List: A list containing this state itself
        """
        return self._preconditions

    @property
    def effects(self):
        """
            Getter for the effects.
        Returns:
            List: A list containing this state itself
        """
        return self._effects

    def __str__(self):
        """
            Overrides the str() operator
        Returns:
            String: The name of the action
        """
        return self._name

    def __repr__(self):
        """
            Overrides the repr() operator
        Returns:
            String: The name of the action
        """
        return self._name

    def __le__(self, other):
        """
            Overrides the '<=' operator
        Returns:
            boolean: True if the name (String) is <= to the other,
                        False otherwise
        """
        return (self._name <= other.name)


class State(LayerElement):
    """
        This class represents states/literals in graph planning. This
        class inherits the LayerElement class.
    Args:
        LayerElement (LayerElement): SuperClass of this class
    """

    def __init__(self, name):
        """
            Calls the parent class constructor with extra
            paremeter to indicate this is a state/literal.
        Args:
            name (String): Name of this state
        """
        LayerElement.__init__(self, name, isState=True)


class Action(LayerElement):
    """
        This class represents the actions in graph planning. This 
        class inherits the LayerElement class.
    Args:
        LayerElement (LayerElement): SuperClass of this class
    """

    def __init__(self, name):
        """
            Calls the parent class constructor.
        Args:
            name (String): Name of this action
        """
        LayerElement.__init__(self, name)

    def addPrecondition(self, precondition):
        """
            Adds a precondition to the end list of preconditions,
            this function does not perform any duplicate checking.
        Args:
            precondition (State): The state/literal object which is 
                                    the precondition.
        """
        self._preconditions.append(precondition)

    def addEffect(self, effect):
        """
            Adds n effect to the end of the list of effects,
            this function does not perform any duplicate checking.
        Args:
            effect ([type]): [description]
        """
        self._effects.append(effect)


class Layer:
    """
        This class represents an action layer which can be inserted into
        the Graph class, and used for planning. It overrides the __eq__ and
        __str__ operator functions. The layer has two pointers for the next
        and previous layers. It uses dictionaries to keep track of actions
        and mutexes which exist within this layer.
    """

    def __init__(self):
        """
            Constructor for the ActionLayer, no parameters are required. It
            initializes the prev, next and depth as None. The actions and mutexes
            are initialized as empty dictionary objects.
        """
        self._prev = None
        self._next = None
        self._depth = None
        self._elements = dict()
        self._mutexes = dict()

    @property
    def prev(self):
        """
            Getter for the prev layer.
        Returns:
            StateLayer/ActionLayer: The previous layer
        """
        return self._prev

    @ property
    def next(self):
        """
            Getter for the next layer.
        Returns:
            StateLayer/ActionLayer: The next layer
        """
        return self._next

    @property
    def elements(self):
        """
            Getter for the list of actons.
        Returns:
            List: Returns a list of elements in the layer
        """
        return list(self._elements)

    @property
    def depth(self):
        """
            Getter for the depth of the layer.
        Returns:
            int: Depth of the layer
        """
        return self._depth

    @property
    def mutexes(self):
        """
            Getter for the mutexes in this layer.
        Returns:
            Dict: Returns a Dict of mutexes
        """
        return self._mutexes

    @prev.setter
    def prev(self, value):
        """
            Setter for the prev property of the layer.
        Args:
            value (StateLayer/ActionLayer): The layer which will be
                                                previous to this one.
        """
        self._prev = value

    @ next.setter
    def next(self, value):
        """
            Setter for the next property of the layer.
        Args:
            value (StateLayer/ActionLayer): The layer which will be
                                                next to this one.
        """
        self._next = value

    @depth.setter
    def depth(self, value):
        """
            Setter for the depth property of the layer.
        Args:
            value (int): The depth of this layer in graph planning.
        """
        self._depth = value

    def addAction(self, action):
        """
            This funtion adds the action to the list of elements
            in this layer.
        Args:
            action (LayerElement): Action/State to add to this layer.
        """
        if action not in self._elements:
            self._elements[action] = action

    def _addMutex(self, a1, a2, mType):
        """
        This function adds a mutex between the two LayerElements
        provided. It checks which elements is saller and sets that
        as the first elements in the tuple which is used as the key
        for the dictionary of mutexes, the mutex type is appended
        to the value associated with this key.

        Args:
            a1 (LayerElement): [description]
            a2 (LayerElement): [description]
            mType (int): Represents the type of mutex

        Returns:
            [type]: [description]
        """
        # make sure both are not the same
        if a1 != a2:
            # ensure a1 is the smaller of the two mutexes
            # this helps when searching for mutexes mutexes
            # are always in a systematic order.
            if a2 <= a1:
                a1, a2 = a2, a1

            if (a1, a2) not in self._mutexes:
                self._mutexes[(a1, a2)] = [mType]
            else:
                if mType not in self._mutexes[(a1, a2)]:
                    self._mutexes[(a1, a2)].append(mType)

    def areMutex(self, a1, a2):
        """
            Checks if the two actions/states are mutexes.
            As in the addMutex function the smaller of the two
            is set as a1 and the other is set to a2.
        Args:
            a1 (LayerElement): [description]
            a2 (LayerElement): [description]
        Returns:
            boolean: True if a1 and a2 are mutexes, False otherwise.
        """
        if a2 <= a1:
            a1, a2 = a2, a1

        if (a1, a2) in self._mutexes:
            return True

        return False

    def __validMutex(self, mType):
        """
            Private function to check if the mutex type is valid for
            action layer.
        Args:
            mType (int): int representing mutex type
        Returns:
            boolean: True if the mutex type is valid, False otherwise.
        """
        if mType == mIE | mType == mI | mType == mCN:
            return True
        return False

    def __eq__(self, other):
        """
            Checks if two Action layers are the same, it checks the actions
            and mutexes in this layer.
        Args:
            other (ActionLayer): The other action layer being compared.
        Returns:
            boolean: True if both layers contain the same elements and mutexes.
        """
        if (self.elements == other.elements) and (self._mutexes == other.mutexes):
            return True
        return False


class ActionLayer(Layer):
    """
        This class represents an action layer which can be inserted into
        the Graph class, and used for planning. It overrides the __eq__ and
        __str__ operator functions. The layer has two pointers for the next
        and previous layers. It uses dictionaries to keep track of actions
        and mutexes which exist within this layer.
    """

    def __init__(self):
        """
            Calls the parent class Layer to construct this ActionLayer.
        """
        Layer.__init__(self)

    @property
    def actions(self):
        """
            Getter for the list of actons.
        Returns:
            List: Returns a list of actions in the layer
        """
        return list(self._elements)

    def addAction(self, action):
        """
            This funtion adds the action to the list of actions
            in this layer.
        Args:
            action (LayerElement): Action/State to add to this layer.
        """
        if action not in self._elements:
            self._elements[action] = action

    def addMutex(self, a1, a2, mType):
        """
        This function adds a mutex between the two LayerElements
        provided. It checks which elements is smaller and sets that
        as the first elements in the tuple which is used as the key
        for the dictionary of mutexes, the mutex type is appended
        to the value associated with this key.

        Args:
            a1 (LayerElement): [description]
            a2 (LayerElement): [description]
            mType (int): Represents the type of mutex

        Returns:
            [type]: [description]
        """
        # check the mutex type is valid for action layer
        if not self.__validMutex:
            return False
        self._addMutex(a1, a2, mType)

    def __validMutex(self, mType):
        """
            Private function to check if the mutex type is valid for
            action layer.
        Args:
            mType (int): int representing mutex type
        Returns:
            boolean: True if the mutex type is valid, False otherwise.
        """
        if mType == mIE | mType == mI | mType == mCN:
            return True
        return False

    def __str__(self):
        """
            Returns the string representation of this layer by concatinating
            all the action into one line, and all the types of mutexes
            into their individual lines.
        Returns:
            String: All the actions and mutexes in this layer.
        """
        rtnStr = "ActLayer: <" + str(self._depth) + ">"

        rtnStr += "\n\tActions: "
        for a in self._elements:
            if isinstance(a, Action):
                rtnStr += str(a) + ", "

        if rtnStr[-2] == ',':
            rtnStr = rtnStr[:-2]

        ieString = "\n\tInconsistent Effects: "
        iString = "\n\tinterference: "
        cnString = "\n\tCompeting Needs: "

        for m in self._mutexes:
            val = self._mutexes[m]
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


class StateLayer(Layer):
    """
        This class represents a State layer in graph planning.It overrides
        the __eq__ and __str__ operator functions. The layer has two
        pointers for the next and previous layers. It uses dictionaries
        to keep track of actions and mutexes which exist within this layer.
    """

    def __init__(self):
        """
            Calls the parent construc to to create this State layer.
        """
        Layer.__init__(self)

    @ property
    def literals(self):
        """
            Getter for the literals in this state layer.
        Returns:
            List: States in this layer.
        """
        return list(self._elements)

    def causes(self, l1):
        """
            Returns the list of actions/persistant states which cause the
            literal l1 provided in the parameter.
        Args:
            l1 (State): The literal being checked.

        Returns:
            List: The actions/persistant states which caused this literal
        """
        if l1 in self._elements:
            return self._elements[l1]
        else:
            return None

    def addLiteral(self, literal, cause):
        """
            Adds the two literals to the state layer as the key in the
            dictionary and add appends the cause to the value list.
            The cause is the action/persistant literal in the previous
            layer which causes this literal to occur.
        Args:
            literal (State): State object representing the literal
            cause (State/Action): State or action which caused 'literal'
        """
        if literal not in self._elements:
            self._elements[literal] = [cause]
        elif cause not in self._elements[literal]:
            self._elements[literal].append(cause)

    def addMutex(self, l1, l2, mType):
        """
            Adds two mutexes to the dictionary of mutexes by calling
            the parent _addMutex function. It checks which elements is
            smaller and sets that as the first elements in the tuple
            which is used as the key for the dictionary of mutexes.
            The mutex type is checked for validity in the State layer;
            'Negated Literals' and 'Inconsistent Support'.
        Args:
            l1 (State): One of the literals which is a mutex
            l2 (State): Second literal which is a mutex with the first one
            mType (int): int representing the mutex type
        Returns:
            boolean: False if it fails to add the mutex
        """
        if not self.__validMutex:
            return False
        self._addMutex(l1, l2, mType)

    def __validMutex(self, mType):
        """
            Private function to check for validity of mutex for
            state layer.
        Args:
            mType (int): int representing the mutex type
        Returns:
            boolean: True if valis, False otherwise
        """
        if mType == mNL | mType == mIS:
            return True
        return False

    def __str__(self):
        """
            Returns the string representation of the this State layer.
            Lists all the literals in one line, and different type of
            mutexes in this layer printed on individual lines.
        Returns:
            String: String representation of this state layer.
        """
        rtnStr = "StateLayer: <" + str(self._depth) + ">"

        rtnStr += "\n\tLiterals: "
        for l in self._elements:
            rtnStr += str(l) + ", "

        if rtnStr[-2] == ',':
            rtnStr = rtnStr[:-2]

        nlString = "\n\tNegated Literals: "
        isString = "\n\tInconsistent Support: "

        for m in self._mutexes:
            val = self._mutexes[m]
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
    """
        This class represents the graph planning problem, with
        nodes represented by state and action layers. The graph keeps
        track of the root and the current layer in the graph planning
        process. It also keeps a counter to keep track of the current
        depth of the planning process which is used when new layers
        are added.
    """

    def __init__(self, rootLayer):
        """Constructs the Graph object, requires a root layer to be
        given as a parameter to initialize the variables. Current
        depth is initialized to 0, and also has a variable
        which can be used to stor the solution.

        Args:
            rootLayer (Layer): Layer which will be the root layer
                                of this graph plan.
        """
        self.__root = rootLayer
        self.__current = rootLayer
        self.__currentDepth = 0
        self.__solution = "No Plan"
        rootLayer.depth = 0

    @ property
    def root(self):
        """
            Getter for the the root layer.
        Returns:
            Layer : The root layer
        """
        return self.__root

    @ property
    def solution(self):
        """
            Getter for the solution of this graph.
        Returns:
            List: A list representing the solution.
        """
        return self.__solution

    @ property
    def current(self):
        """
            Getter for the current layer in thes graph planning object.
        Returns:
            Layer: A list representing the solution.
        """
        return self.__current

    @solution.setter
    def solution(self, value):
        """
            Setter for the solution parameter for this graph plan.
        Args:
            value (List): A list representing the solution.
        """
        self.__solution = value

    def addLayer(self, layer):
        """
            Adds a layer to this graph plan and progresses the plan
            along lone layer. The depth tracker is incremented, and
            the appropriate next and prev pointer for the layer
            are updated.
        Args:
            layer (Layer): The layer object being added to the graph.
        """
        self.__currentDepth += 1
        layer.depth = self.__currentDepth
        layer.prev = self.__current
        self.__current.next = layer
        self.__current = layer

    def writeOut(self, outFile):
        """
            Writes out the graph plan to the file provided.
        Args:
            outFile (String): File path of output file.
        """
        of = open(outFile, "w")
        of.write(str(self))
        of.close()

    def writeOutSol(self, outFile):
        """
            Writes out the graph plan along with the solution to the
            the plan if one exists.

        Args:
            outFile (String): File path of output file.
        """
        of = open(outFile, "w")
        sol = "Solution: " + str(self.__solution)
        sol += "\n--------------------------------------------------------------------------------\n"
        of.write(sol)
        of.write(str(self))
        of.close()

    def __str__(self):
        """Overrides the string operator function and returns the
        string representation of the graph plan.

        Returns:
            String: The string representation of the graph plan.
        """
        curr = self.__root
        gpString = ""
        while curr:
            gpString += str(curr)
            curr = curr.next
        return gpString
