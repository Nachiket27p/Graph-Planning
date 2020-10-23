import networkx as nx
import matplotlib.pyplot as plt

g = nx.Graph()

g.add_node("Hungry")
g.add_node("CleanTable")

g.add_weighted_edges_from([("Hungry", "Hungry", 1)])
g.add_weighted_edges_from([("CleanTable", "Cook", 2)])

nx.draw(g, with_labels=True)
plt.show()
