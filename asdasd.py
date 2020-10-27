c1 = "-Car"
c2 = "-Car"

x = {'+': '-', '-': '+'}

if c1[1:] == c2[1:] and x[c1[0]] == c2[0]:
    print("Cool")

if '*' in x:
    print("in")
else:
    print("out")

for k in x:
    print((k, x[k]))
