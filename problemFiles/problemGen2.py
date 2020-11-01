rows = 4
cols = 4

positions = [[2, 3], [6, 7], [8, 9], [11, 15]]

grid = [0]*(rows*cols)

x = 1
for p in positions:
    for i in p:
        grid[i] = x
    x += 1

for i in range(0, rows*cols, cols):
    print(grid[i:i+cols])


def inRow(p):
    m = p[0]//cols
    for i in p:
        if (i//cols) != m:
            return -1
    return m


def inCol(p):
    if len(p) == 1:
        return p[0] % cols

    p.sort()
    for i in range(len(p)-1):
        if (p[i] % cols) != (p[i+1] % cols):
            return -1
    return p[0] % cols


print("\n")
for p in positions:
    rc = inRow(p)
    if rc != -1:
        print(str(p) + " in row " + str(rc) + "\n")
    cl = inCol(p)
    if cl != -1:
        print(str(p) + " in col " + str(cl) + "\n")


# TODO


initStates = []
goalState = []
actions = []


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

print(isstring)
print(goalstring)
print(actionString)

# fname = str(rows) + "x" + str(cols) + "Escape.txt"
# f = open(fname, 'w')
# f.write(isstring)
# f.write(goalstring)
# f.write(actionString)
# f.close()
