import networkx as nx
import matplotlib.pyplot as plt

__author__ = 'fhca'

G = nx.Graph()

G.add_node("alfa")
G.add_node("beta")
G.add_node("gamma")
G.add_node("delta")

G.add_edge("alfa", "beta")
G.add_edge("alfa", "gamma")
G.add_edge("alfa", "delta")
G.add_edge("beta", "gamma")
G.add_edge("beta", "delta")
# G.add_edge("gamma", "delta")

# print(G.nodes())
# print(G.edges())

plt.figure(figsize=(8, 8))
nx.draw(G, with_labels=True)

plt.show()
