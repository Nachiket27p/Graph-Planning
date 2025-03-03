rows = 4
cols = 4
# position of the car
carPos = 4

positions = [2, 3, 4, 5, 6, 7, 9, 11]

grid = [0]*(rows*cols)

for p in positions:
    grid[p] = 1

for i in range(0, rows*cols, cols):
    print(grid[i:i+cols])

initStates = []
goalState = ['-5', '-6', '-7']
actions = []

for i in range(len(grid)):
    if i != carPos:
        p = grid[i]
        if p:
            initStates.append("+" + str(i))
        else:
            initStates.append("-" + str(i))

        # generate actions
        if p:
            action = "Act [Move("+str(i)+"-->"
            precond = "Preconditions ["
            if ((i-1)//cols) == (i//cols):
                a = action + str(i-1) + ")]\n"
                a += "Preconditions [-" + str(i-1) + "]\n"
                a += "Effects [+" + str(i-1) + ",-" + str(i) + "]\n"
                actions.append(a)

            if ((i+1)//cols) == (i//cols):
                a = action + str(i+1) + ")]\n"
                a += "Preconditions [-" + str(i+1) + "]\n"
                a += "Effects [+" + str(i+1) + ",-" + str(i) + "]\n"
                actions.append(a)

            if i-cols >= 0:
                a = action + str(i-cols) + ")]\n"
                a += "Preconditions [-" + str(i-cols) + "]\n"
                a += "Effects [+" + str(i-cols) + ",-" + str(i) + "]\n"
                actions.append(a)

            if i+cols < (rows*cols):
                a = action + str(i+cols) + ")]\n"
                a += "Preconditions [-" + str(i+cols) + "]\n"
                a += "Effects [+" + str(i+cols) + ",-" + str(i) + "]\n"
                actions.append(a)

isstring = "InitialState ["
for i in range(len(initStates)):
    isstring += initStates[i]
    if i < len(initStates)-1:
        isstring += ","
isstring += "]\n\n"


goalstring = "GoalState ["
for i in range(len(goalState)):
    goalstring += goalState[i]
    if i < len(goalState)-1:
        goalstring += ","
goalstring += "]\n\n"

actionString = ""
for a in actions:
    actionString += a + "\n"

# print(isstring)
# print(goalstring)
# print(actionString)

fname = str(rows) + "x" + str(cols) + "Escape.txt"
f = open(fname, 'w')
f.write(isstring)
f.write(goalstring)
f.write(actionString)
f.close()
