import networkx as nx
import matplotlib.pyplot as plt

"""
Manual connected graph generation, based on sketch codes from @khakhalin

Generate the graph recursively, by including or skipping each edge (lexicographical order by construction)
Issue with this method is that this brute force approach takes exponential time,
which increases by 2 to the power of n-1 with each vertex increase
"""


def make_graphs(n=2, i=None, j=None):
    graph = []
    if i is None:
        graph = [[(0, 1)] + r for r in make_graphs(n=n, i=0, j=1)]
    elif j < n - 1:
        graph += [[(i, j + 1)] + r for r in make_graphs(n=n, i=i, j=j + 1)]
        graph += [r for r in make_graphs(n=n, i=i, j=j + 1)]
    elif i < n - 1:
        graph = make_graphs(n=n, i=i + 1, j=i + 1)
    else:
        graph = [[]]

    return graph


# This lists all possible isomorphic codes for a graph as tuples (edges are i<j, sorted lexicographically)
def permute(g, n):
    ps = all_perm(n)
    out = set([])
    for p in ps:
        out.add(tuple(sorted([(p[i], p[j]) if p[i] < p[j]
                              else (p[j], p[i]) for i, j in g])))
    return list(out)


def all_perm(n, s=None):
    if s is None:
        return all_perm(n, tuple(range(n)))
    if not s:
        return [[]]
    return [[i] + p for i in s for p in all_perm(n, tuple([k for k in s if k != i]))]


def is_connected(g):
    nodes = set([i for e in g for i in e])
    roots = {node: node for node in nodes}

    # Union finding
    def _root(node, depth=0):
        if node == roots[node]:
            return node, depth
        else:
            return _root(roots[node], depth + 1)

    for i, j in g:
        ri, di = _root(i)
        rj, dj = _root(j)
        if ri == rj:
            continue
        if di <= dj:
            roots[ri] = rj
        else:
            roots[rj] = ri

    return len(set([_root(node)[0] for node in nodes])) == 1


# Select solely the proper graphs, i.e., connected, non-isomorphic and with the right # of vertices
def select(gs, target_nr_vertices):
    mem = set({})
    gs2 = []
    for g in gs:
        nv = len(set([i for e in g for i in e]))
        if nv != target_nr_vertices:
            continue
        if not is_connected(g):
            continue
        if tuple(g) not in mem:
            gs2.append(g)
            mem |= set(permute(g, target_nr_vertices))
    return gs2


def draw_graphs(graphs):
    for graph in graphs:
        print(graph)

        # Convert a graph with edge information into a NetworkX object - in order to be drawn
        n_graph = nx.Graph()
        n_graph.add_edges_from(graph)

        pos = nx.spring_layout(n_graph)
        nx.draw(n_graph, pos, with_labels=True)
        plt.show()


# Converts graph sets (generated with the 'nauty' C package), under the .g6 format, into a Python array (not working)
def convert_g6_to_array(file_name):
    # 'read' mode, indicated by "r"
    file_contents = open(file_name, "r")

    lines = file_contents.readlines()

    for line in lines:

        n = ord(line.split()[0][0]) - 63
        h = ''

        l = n - 1
        for i in range(1, l):
            temp = bin(ord(line.split()[0][i]) - 63)[2:]
            if len(temp) < 6:
                for k in range(6 - len(temp)):
                    h = h + '0'
            h = h + temp

        A = [[0] * n for j in range(n)]
        k = 0
        for i in range(1, n):
            for j in range(0, i):
                A[i][j] = int(h[k])
                A[j][i] = A[i][j]
                k = k + 1

    return A


# connected_10 = convert_g6_to_array("graphs/graph10c.g6")


"""
# Random creation
G = nx.erdos_renyi_graph(20, 0.4)

# Define the forbidden minor K3
H = nx.complete_graph(3)

# Check if the graph contains the forbidden minor
if nx.subgraph(G, list(H.nodes())).number_of_edges() == H.number_of_edges():
    print("Found a forbidden minor!")

    # Adjacency matrix (or whatever format I end up using) to a string format
    a_m = np.array([[0, 0, 1], [1, 1, 0], [1, 0, 0]])
    insert_fm(a_m, 'fm_in_f4', 'forbidden_minors', 'local_host', 'admin', 'admin')
else:
    print("No forbidden minor found.")
"""
