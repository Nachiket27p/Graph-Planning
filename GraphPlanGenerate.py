#!/usr/bin/env python3

from Planner import *
import os
import re
from sys import argv

__author__ = 'Nachiket Patel'
__email__ = 'nnpatel5@ncsu.edu'

"""
This file is the main file from where the grpah planning algorithm starts,
it requires the Planner.py file to be in the same directory to access
the State, Action, StateLayer, ActionLayer, and Graph classes which are
fundamental to performing the graph planning algorith, This program reports
each state and action layer in the graph plan to the output file provided
including all the mutexes for each layer.
As indicated at the beginning of the program this program requires
python3 to function properly. For more details on how to use this program,
please consult the README.md file.
"""

"""
###############################################################################
                                    Functions
###############################################################################
"""


def loadFile(inFile, iStates, gStates, actions, negate):
    """
        This function is responsible for reading the input file
        and lodaing the appropriate literals and actions into the
        appropriate lists provided in the parameters. This function
        also creates a dictionary of negated literals to make it
        easier to check for negated liters during graph planning.

    Args:
        inFile (string): Input file path
        iStates (list): Enpty list which will be populated with the initial states
        gStates (list): Empty list whcih will be populated with the goal states
        actions (list): Empty list which will be populated with the actions
        negate (dictionary): Populated with literal and negated literal key value pairs
    """
    # used to keep track of which states have been already been read in
    sDict = dict()
    # open the file in read mode
    f = open(inFile, 'r')
    line = f.readline()
    # parse each line individually
    while line:
        # split the line using square braces ('[', ']', ',')
        # to extract all the literals
        split = re.split('\[|,|]', line)
        # if the line starts with "InitialState" then place the literals into
        # initial list iStates
        if split[0] == 'InitialState ':
            for i in range(1, len(split)-1):
                s = State(split[i])
                iStates.append(s)
                sDict[split[i]] = s
        # if the line starts with 'GoalState ' then place the literals into
        # the list gStates
        elif split[0] == 'GoalState ':
            for i in range(1, len(split)-1):
                if not(split[i] in sDict):
                    sDict[split[i]] = State(split[i])
                gStates.append(sDict[split[i]])
        # if the line starts with 'Act ' then read the next line to
        # get the preconditions and then read the line after that
        # to get the effects of the action.
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

    # used to determine created negated literals
    neg = {'+': '-', '-': '+'}
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
    # close the file
    f.close()


def displayFile(inFile):
    """
        This function is responsible for printing out the problem file
        for which the graph planning problem will be solved.

    Args:
        inFile (string): File path of the problem
    """
    print("\nThe problem in the file " + inFile +
          " will be solved with graph planning:\n")
    f = open(inFile, 'r')

    print("################################################################################")
    print("\t\t\t\t" + inFile)
    print("################################################################################")

    print(f.read())

    f.close()


def mutexNL(sl, negate):
    """
        This function is responsible for computing the negated literas in
        the state layer. It uses the negate dictionary to lookup the negation
        of the literals in the state layer to determine if they are mutex.

    Args:
        sl (StateLayer): State layer object
        negate (dicionary): Dictionary used to lookup negated literals
    """
    sLen = len(sl.literals)
    for i in range(sLen):
        l1 = sl.literals[i]
        for j in range(i+1, sLen):
            l2 = sl.literals[j]
            # if the negated literal has a negated literal in the state then
            # add the pair to the list of negated literals of the layer
            if negate[l1] == l2:
                sl.addNL(l1, l2)


def mutexISHelper(l1, l2, al, eDict):
    """
    This function is a helper function to the mutexIS function, it
    checks if all the pairs of actions which prodice the literals are
    mutex.

    Args:
        l1 (State): The first literal
        l2 (State): The second literal
        al (ActionLayer): The previous action layer
        eDict (dictionary): A dictionary with effects as keys and list of actions
                            which produce the effect as the value

    Returns:
        boolean: True if all pairs of actions which procide the literals
                    are mutexes, else False
    """
    for a1 in eDict[l1]:
        for a2 in eDict[l2]:
            # if any one of pairs are no mutex than l1 and l2
            # cannot be mutexes so return
            if not al.areMutex(a1, a2):
                return False
    return True


def mutexIS(sl, eDict):
    """
        This function is responsible for computing all the inconsistent
        support mutexes in the state layer. An inconsistent support is one
        where all the pairs of actions which could produce a pair of literals
        are mutex in the previous layer.

    Args:
        sl (StateLayer): State layer object
        eDict (dictionary): A dictionary with effects as keys and list of actions
                            which produce the effect as the value

    """
    sLen = len(sl.literals)
    for i in range(sLen):
        l1 = sl.literals[i]
        for j in range(i+1, sLen):
            l2 = sl.literals[j]
            if mutexISHelper(l1, l2, sl.prev, eDict):
                # if all action that cause l1 are mutex with all
                # the action that cause l2 are mutex then l1 and l2 are mutex
                sl.addIS(l1, l2)


def mutexIE(al, eDict, negate):
    """This function computes all the inconsistent effect mutexes for the
    action layer. An inconsistent effect is one where an effect of one
    action is the negation of the effect of another action. This function
    used the negate dictionary to check negated effects.

    Args:
        al (ActionLayer): Action layer object
        eDict (dictionary): A dictionary with effects as keys and list of actions
                            which produce the effect as the value
        negate (dictionary): A dictionary containing pairs of negated literals
    """
    effects = list(eDict)
    eLen = len(effects)
    for i in range(eLen):
        for j in range(i+1, eLen):
            # check if two effects are negated then find for all
            # actions which produce the effect are negated
            if negate[effects[i]] == effects[j]:
                for a1 in eDict[effects[i]]:
                    for a2 in eDict[effects[j]]:
                        al.addIE(a1, a2)


def mutexIHelper(a1, a2, al, negate):
    """
        This is a helper function for mutexI whcih checks if the two
        action have an effect and a precondition which are negations of
        each other.

    Args:
        a1 (Action): One of the action being compared
        a2 (Action): Another action being compared
        al (ActionLayer): An action layer object
        negate (dictionary): A dictionary containing pairs of negated literals
    """
    for e in a1.effects:
        for p in a2.preconditions:
            if negate[e] == p:
                al.addI(a1, a2)
                # if any pair of effect and action are negations of each other
                # return after addion to the mutex list
                return


def mutexI(al, negate):
    """
        This function is responsible for computing all the Interference mutexes
        in the action layer. An interference is when two actions have a precondition
        which are negated. It uses the negete dictionary to look up negated preconditions.

    Args:
        al (ActionLayer): The action layer for whcih to compute the interference mutexes
        negate (dictionary): A dictionary with negate literals as key value pairs
    """
    aLen = len(al.actions)
    for i in range(aLen):
        a1 = al.actions[i]
        for j in range(aLen):
            if i != j:
                a2 = al.actions[j]
                mutexIHelper(a1, a2, al, negate)


def mutexCNHelper(a1, a2, al, pl):
    """
        This function is a helper function for mutexCN, it check if the two action
        passed in have a pari of precondition which are negation of each other.

    Args:
        a1 (Action): One of the action being compared
        a2 (Action): The second action being compared
        al (ActionLayer): The action layer in which the mutex is being computed
        pl (StateLayer): The previous state layer used to check for mutex
    """
    for p1 in a1.preconditions:
        for p2 in a2.preconditions:
            if pl.areMutex(p1, p2):
                al.addCN(a1, a2)
                return


def mutexCN(al):
    """
        This function is responsible for computing all the competing needs
        mutexes in the action layer provided in the parameter. A competing needs
        mutex is one which ther exists a pair of preconditions which are mutex.
        This function used the mutexCNHelper function to check if a pair of
        preconditions are mutex in the previous layer.

    Args:
        al (ActionLayer): The action layer in which to compute the competing
                            needs mutexes.
    """
    pl = al.prev
    aLen = len(al.actions)
    for i in range(aLen):
        a1 = al.actions[i]
        for j in range(i+1, aLen):
            a2 = al.actions[j]
            mutexCNHelper(a1, a2, al, pl)


def initializePlan(iStates):
    """
        This function is responsible for initializing the graph plan object
        with the initial layer with the intitial stated.

    Args:
        iStates (list): The stated which should be in the initial layer

    Returns:
        Graph: The graph object created with the initial state layer
    """
    initStateLayer = StateLayer()
    for s in iStates:
        initStateLayer.addLiteral(s)
    return Graph(initStateLayer)


def applyActions(gp, actions, negate):
    """
        This function is responsible for computing the the next step in
        the graph planning, each time this function called it generates the
        next action layer and the proceeding state layer for the graph
        provided in the parameters.

    Args:
        gp (Graph): The graph obejct representing the graph plan
        actions (list): The list of actions which can be performed
        negate (dictionary): A dictionary with negate literals as key value pairs
    """
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

    # add the action and the preceding state layer to the graph
    gp.addLayer(actionLayer)
    gp.addLayer(stateLayer)

    # compute the negated literal mutexes
    mutexNL(stateLayer, negate)

    # compute the inconsistent effects mutexes
    mutexIE(actionLayer, eDict, negate)

    # interference mutexes
    mutexI(actionLayer, negate)

    # Competing Needs mutexes
    mutexCN(actionLayer)

    # Inconsistent Support mutexes
    mutexIS(stateLayer, eDict)


def checkCompletion(gp):
    """
        This function is responsible for checking if the graph plan
        algorithm as reached a state where the states not longer evolve.

    Args:
        gp (Graph): The graph plan object which is checked for competing

    Returns:
        boolean: True if the graph is not longer evolving, False otherwise
    """
    currStateLayer = gp.current
    lastStateLayer = currStateLayer.prev.prev
    return (currStateLayer == lastStateLayer)


def writeOutGP(gp, outFile):
    """
        Writes the graph plan out to the output file provided.

    Args:
        gp (Graph): The graph plan which is being written out to the output file
        outFile (string): The output file path
    """
    gp.writeOut(outFile)


def plan(gp, actions, negate):
    """
        This function is responsible for performing the graph plan
        while repeatedly calling the applyActions function which progesses
        the graph plan along two steps.

    Args:
        gp (Graph): The graph plan object
        actions (list): The list of action whcih can be performed
        negate (dictionary): A dictionary with negate literals as key value pairs
    """
    complete = False
    while(not complete):
        # apply action and produce the next state layer
        applyActions(gp, actions, negate)
        complete = checkCompletion(gp)


"""
###############################################################################
                            Main Function/ Start Point
###############################################################################
"""


def graphPlanGenerate():
    """
    This function is the main function where he program starts. It created the
    variable and objects required to perform the graph plan.
    """
    # expected number of arguments
    nArgExpected = 2 + 1  # +1 is for the filename itself
    iStates = []
    gStates = []
    actions = []
    negate = dict()

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

    # display the file to the user
    displayFile(inFile)

    loadFile(inFile, iStates, gStates, actions, negate)
    gp = initializePlan(iStates)
    plan(gp, actions, negate)
    gp.writeOut(outFile)


if __name__ == "__main__":
    graphPlanGenerate()
