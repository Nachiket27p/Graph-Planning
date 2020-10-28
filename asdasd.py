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

print("\n")
s1 = "+Hungry"
s2 = "Eat"

print(s1 > s2)


x1 = ["a", "b", "c"]
x2 = ["a", "b", "c"]

print("\n")
print(x1 == x2)
