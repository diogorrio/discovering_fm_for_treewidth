import networkx as nx
import matplotlib.pyplot as plt

# Class for handling own graphs, using the NetworkX package
# TODO Ask if this is allowed or if I have to create my own graph class

G = nx.Graph()

# Manual creation
G.add_node('A')
G.add_node('B')
G.add_node('C')
G.add_node('D')

G.add_edge('A', 'B')
G.add_edge('B', 'C')

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
plt.show()

# -----------------------------------------
# Random creation
G = nx.erdos_renyi_graph(20, 0.4)

# Define the forbidden minor
H = nx.complete_graph(3)

# Check if the graph contains the forbidden minor
if nx.subgraph(G, list(H.nodes())).number_of_edges() == H.number_of_edges():
    print("Found a forbidden minor!")

    # TODO: Take this away from here, but an e.g. on how to add an adjacency matrix to the db
    # Adjacency matrix (or whatever format I end up using) to a string format
    # a_m = np.array([[0, 0, 1], [1, 1, 0], [1, 0, 0]])
    # insert_fm(a_m, 'fm_in_f4', 'forbidden_minors', 'local_host', 'admin', 'admin')
else:
    print("No forbidden minor found.")
