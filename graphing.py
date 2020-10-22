import networkx as nx
import matplotlib.pyplot as plt

g = nx.Graph()

g.add_node("Hungry")
g.add_node("CleanTable")

g.add_edge("Hungry", "Hungry")
g.add_edge("CleanTable", "Cook")

nx.draw(g, with_labels=True)
plt.show()
