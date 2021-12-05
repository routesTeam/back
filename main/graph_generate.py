import networkx as nx
from models import *



# import matplotlib 
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt

G = nx.fast_gnp_random_graph(1000, 0.0115, seed=None, directed=False)
city = City.objects.all()
print(city)

# counter = 1
# for x in list(G.edges):
#     print(counter, ' ', x)
#     counter += 1

# f = plt.figure()

# nx.draw(G, width=1, node_size=1, edge_size=1)
# f.savefig("graph.png")
