#!/usr/bin/env python3

from Planner import *
import os
import re
from sys import argv
import itertools

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


def loadFile(inFile, iStates, gStates, allActions, negate):
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
        allActions (list): Empty list which will be populated with the actions
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

            allActions.append(a)

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

    print("--------------------------------------------------------------------------------")
    print("\t\t\t\t" + inFile)
    print("--------------------------------------------------------------------------------")

    print(f.read())

    f.close()


def mutexNL(gp, negate):
    """
        This function is responsible for computing the negated literas in
        the state layer. It uses the negate dictionary to lookup the negation
        of the literals in the state layer to determine if they are mutex.

    Args:
        gp (StateLayer): The Graph object representing the graph plan
        negate (dicionary): Dictionary used to lookup negated literals
    """
    sl = gp.current
    literals = sl.literals
    sLen = len(literals)
    for i in range(sLen):
        l1 = literals[i]
        for j in range(i+1, sLen):
            l2 = literals[j]
            # if the negated literal has a negated literal in the state then
            # add the pair to the list of negated literals of the layer
            if negate[l1] == l2:
                sl.addMutex(l1, l2, mNL)


def mutexISHelper(l1, l2, al, sl):
    """
        This function is a helper function to the mutexIS function, it
        checks if all the pairs of actions which prodice the literals are
        mutex.

    Args:
        l1 (State): The first literal
        l2 (State): The second literal
        al (ActionLayer): The previous action layer
        sl (StateLayer): State layer object

    Returns:
        boolean: True if all pairs of actions which procide the literals
                    are mutexes, else False
    """
    for a1 in sl.causes(l1):
        for a2 in sl.causes(l2):
            # if any one of pairs are no mutex than l1 and l2
            # cannot be mutexes so return
            if not al.areMutex(a1, a2):
                return False
    return True


def mutexIS(gp):
    """
        This function is responsible for computing all the inconsistent
        support mutexes in the state layer. An inconsistent support is one
        where all the pairs of actions which could produce a pair of literals
        are mutex in the previous layer.

    Args:
        gp (StateLayer): The Graph object representing the graph plan

    """
    sl = gp.current
    literals = sl.literals
    sLen = len(literals)
    for i in range(sLen):
        l1 = literals[i]
        for j in range(i+1, sLen):
            l2 = literals[j]
            if mutexISHelper(l1, l2, sl.prev, sl):
                # if all action that cause l1 are mutex with all
                # the action that cause l2 are mutex then l1 and l2 are mutex
                sl.addMutex(l1, l2, mIS)


def mutexIE(gp, negate):
    """
        This function computes all the inconsistent effect mutexes for the
        action layer. An inconsistent effect is one where an effect of one
        action is the negation of the effect of another action. This function
        used the negate dictionary to check negated effects.

    Args:
        gp (StateLayer): The Graph object representing the graph plan
        negate (dictionary): A dictionary containing pairs of negated literals
    """
    sl = gp.current
    al = sl.prev
    effects = sl.literals
    eLen = len(effects)
    for i in range(eLen):
        for j in range(i+1, eLen):
            # check if two effects are negated then find for all
            # actions which produce the effect are negated
            if negate[effects[i]] == effects[j]:
                for a1 in sl.causes(effects[i]):
                    for a2 in sl.causes(effects[j]):
                        al.addMutex(a1, a2, mIE)


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
                al.addMutex(a1, a2, mI)
                # if any pair of effect and action are negations of each other
                # return after addion to the mutex list
                return


def mutexI(gp, negate):
    """
        This function is responsible for computing all the Interference mutexes
        in the action layer. An interference is when two actions have a precondition
        which are negated. It uses the negete dictionary to look up negated preconditions.

    Args:
        gp (StateLayer): The Graph object representing the graph plan
        negate (dictionary): A dictionary with negate literals as key value pairs
    """
    al = gp.current.prev
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
                al.addMutex(a1, a2, mCN)
                return


def mutexCN(gp):
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
    al = gp.current.prev
    actions = al.actions
    aLen = len(actions)
    for i in range(aLen):
        a1 = actions[i]
        for j in range(i+1, aLen):
            a2 = actions[j]
            mutexCNHelper(a1, a2, al, al.prev)


def canPerformAction(gp, a):
    """
    This function is responsible for checking if the action can be
    performed by checking that all the pecondition for this action
    exist in the previous state layer and none of them are mutex in the
    previos state layer.

    Args:
        gp (Graph): The Graph object containing all the action and state layers
        a (Action): The action being checked to see if it can be performed

    Returns:
        boolean: True if the action can be performed, False otherwise
    """
    for p1 in a.preconditions:
        for p2 in a.preconditions:
            if (p1 != p2) and (gp.current.areMutex(p1, p2)):
                return False

    return all(s in gp.current.literals for s in a.preconditions)


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
        initStateLayer.addLiteral(s, s)
    return Graph(initStateLayer)


def applyActions(gp, allActions, negate):
    """
        This function is responsible for computing the the next step in
        the graph planning, each time this function called it generates the
        next action layer and the proceeding state layer for the graph
        provided in the parameters.

    Args:
        gp (Graph): The graph obejct representing the graph plan
        allActions (list): The list of actions which can be performed
        negate (dictionary): A dictionary with negate literals as key value pairs
    """
    actionLayer = ActionLayer()

    # add all the persistant literals from the previous layer
    for l in gp.current.literals:
        actionLayer.addAction(l)

    stateLayer = StateLayer()

    # all the literal carry over into the next state layer
    # also takes care of 'Negated Literals mutexes'
    for s in gp.current.literals:
        stateLayer.addLiteral(s, s)

    for a in allActions:
        if canPerformAction(gp, a):
            actionLayer.addAction(a)
            for e in a.effects:
                # adds new literal and takes care of 'Negated Literals mutexes'
                stateLayer.addLiteral(e, a)

    # add the action and the preceding state layer to the graph
    gp.addLayer(actionLayer)
    gp.addLayer(stateLayer)

    # compute the negated literal mutexes
    mutexNL(gp, negate)

    # compute the inconsistent effects mutexes
    mutexIE(gp, negate)

    # interference mutexes
    mutexI(gp, negate)

    # Competing Needs mutexes
    mutexCN(gp)

    # Inconsistent Support mutexes
    mutexIS(gp)


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


"""
BROKEN
"""


def recExtractSolHelper(c, currState):
    cLen = len(c)
    for i in range(cLen):
        for j in range(i+1, cLen):
            if currState.areMutex(c[i], c[j]):
                return False
    return True


def recExtractSol(currState, gStates, solution, iStates):
    # look all the actions which cause the literals to appera in the
    # current stat layer
    if currState.depth == 0:
        if all(s in iStates for s in gStates):
            return True
        else:
            return False

    if len(gStates) == 0:
        return False

    x = []
    for g in gStates:
        temp = currState.causes(g)
        if temp not in x:
            x.append(temp)

    if None in x:
        return False

    for c in itertools.product(*x):
        # if a combination of actions have no mutex then
        if recExtractSolHelper(c, currState.prev.prev):
            igStates = []
            for a in c:
                for p in a.preconditions:
                    if p not in igStates:
                        igStates.append(p)

            if recExtractSol(currState.prev.prev, igStates, solution, iStates):
                act = []
                for a in c:
                    if isinstance(a, Action):
                        act.append(a)
                solution.append(act)
                return True


def extractSolution(gp, gStates, iStates):
    solution = []
    currState = gp.current
    if not all(g in currState.literals for g in gStates):
        return solution

    recExtractSol(currState, gStates, solution, iStates)
    return solution


"""
BROKEN
"""


def writeOutGP(gp, outFile):
    """
        Writes the graph plan out to the output file provided.

    Args:
        gp (Graph): The graph plan which is being written out to the output file
        outFile (string): The output file path
    """
    gp.writeOut(outFile)


def confirmSolution(iStates, solution, gStates):
    return


def plan(gp, allActions, gStates, iStates, negate):
    """
        This function is responsible for performing the graph plan
        while repeatedly calling the apply Actions function which progesses
        the graph plan along two steps.

    Args:
        gp (Graph): The graph plan object
        allActions (list): The list of action whcih can be performed
        negate (dictionary): A dictionary with negate literals as key value pairs
    """
    complete = False
    while(not complete):
        # apply action and produce the next state layer
        applyActions(gp, allActions, negate)
        solution = extractSolution(gp, gStates, iStates)
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
    allActions = []
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

    loadFile(inFile, iStates, gStates, allActions, negate)
    gp = initializePlan(iStates)
    plan(gp, allActions, gStates, iStates, negate)
    gp.writeOut(outFile)


if __name__ == "__main__":
    graphPlanGenerate()
