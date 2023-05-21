import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import getpass
from networkx.algorithms.approximation import treewidth_min_fill_in
from networkx.algorithms.minors import contracted_edge

from graph_data.db_structure import *
from graph_data.graph_structure import *

"""
- HOW FAR IS A GRAPH FROM A BEING A TREE? -

A graph G has threewidth 4 if there is a tree decomposition of G, denoted (T, X) where:
    T is a tree
    X is a set of subsets of vertices of G (BAGS) that satisfy the conditions:
    1. EACH vertex of G is contained in AT LEAST 1 bag
    2. For EACH edge (u, v) in G, there exists a bag in which both u and v are contained
    3. For ANY vertex u, the bags containing u form a CONNECTED subtree in T
    4. Size of EACH bag is AT MOST 4

"In simpler terms, a treewidth 4 graph can be represented by a tree-like structure where each bag contains
at most 4 vertices, and the bags capture the connectivity and relationships between vertices in the graph"

https://en.wikipedia.org/wiki/Treewidth#/media/File:Tree_decomposition.svg (* width *)
tw is the MIN width over ALL tree-decompositions of a graph G (* threewidth *)

- ON FORBIDDEN MINORS -

"For every finite value of k, the graphs of treewidth at most k
MAY BE characterized by a finite set of forbidden minors.
i.e. ANY graph of treewidth > k includes one of the graphs in the set as a minor.
EACH of these sets of forbidden minors includes AT LEAST one planar graph."
(see Wagner's theorem on planar graphs)

Some random, possibly useful theory notes:
    1. Every complete graph K_n has treewidth n–1
    2. Treewidth is always AT LEAST the clique number minus one (~)
    3. For k >= 4, the # of forbidden minors grows AT LEAST as quickly as the exponential of the square root of k
        However, this is only a LOWER BOUND - upper bounds are MUCH higher
    4. Width is the # of vertices in a bag (after t.d.) 
        (the -1 part has to do with the fact that trees should have tw 1)
    5. If H is a minor of G, then tw(H) <= tw(G)
    6. ...  
    (7. Should the degree of each one of the vertices be larger or equal to the actual tw we're looking for?)
    (8. Do all the vertices have to have the same degree as all the others?)
    (9. ...)
"""


class FMFinding:

    def __init__(self, fm_type):
        self.fm_type = fm_type
        # For F(n), the tw has to be n+1
        if self.fm_type == "F(1)":
            self.treewidth = 2
            self.table_name = 'fm_in_f1'
            self.min_nr_minors = 1
            self.max_nr_minors = 1
        elif self.fm_type == "F(2)":
            self.treewidth = 3
            self.table_name = 'fm_in_f2'
            self.min_nr_minors = 1
            self.max_nr_minors = 1
        elif self.fm_type == "F(3)":
            self.treewidth = 4
            self.table_name = 'fm_in_f3'
            self.min_nr_minors = 1
            self.max_nr_minors = 4
        elif self.fm_type == "F(4)":
            self.treewidth = 5
            self.table_name = 'fm_in_f4'
            self.min_nr_minors = 90
            self.max_nr_minors = 100
        # TODO: TBD: nr_minors in f5
        elif self.fm_type == "F(5)":
            self.treewidth = 6
            self.table_name = 'fm_in_f5'
            self.min_nr_minors = 0
            self.max_nr_minors = 0

    # All these methods might justify their own class, if I decide to have different ones to compare

    def tree_decompose(self):
        print("Format working as", self.min_nr_minors)
        return self

    def recursive_construction(self):
        return self

    def combinatorial_enumeration(self, nr_v):
        nr_vertices = nr_v
        # For F(n), the tw has to be n+1
        all_graphs = gen_connected_graphs_with(nr_vertices)
        min_forbidden_minors = find_minimal_forbidden_minors(all_graphs, self.treewidth, self.table_name)

        draw_graphs(min_forbidden_minors)

        print("Combinatorial enumeration process finished.")
        print("This outputs", len(min_forbidden_minors),
              "minimal forbidden minors, out of the established", self.max_nr_minors, "at most",
              "for the set", self.fm_type)

    def random_sampling(self, nr_v, edge_p):
        edge_prob = edge_p
        nr_vertices = nr_v

        nr_gen_graphs = 150
        all_graphs = rnd_graph_sample(nr_vertices, edge_prob, nr_gen_graphs)

        min_forbidden_minors = find_minimal_forbidden_minors(all_graphs, self.treewidth, self.table_name)

        print("Random sampling process finished.")
        print("This outputs", len(min_forbidden_minors),
              "minimal forbidden minors, out of the established", self.max_nr_minors, "at most",
              "for the set", self.fm_type)


# For n=[0,+oo], n being the # of vertices:
# 1, 1, 1, 2, 6, 21, 112, ... (see https://oeis.org/A001349/list)
def gen_connected_graphs_with(max_nr_vertices):

    gen_graphs = make_graphs(max_nr_vertices)
    gen_graphs = select(gen_graphs, max_nr_vertices)
    #draw_graphs(gen_graphs)

    print("Found", len(gen_graphs), "distinct connected graphs with", max_nr_vertices, "vertices.")

    return gen_graphs


def find_minimal_forbidden_minors(graphs, tw, tn):
    forbidden_minors = []

    for i, graph in enumerate(graphs):
        print("Processing graph", i+1, "out of", len(graphs))

        n_graph = nx.Graph()
        n_graph.add_edges_from(graph)

        if is_mfm(n_graph, tw):
            forbidden_minors.append(graph)
            # Edges representation turned to string to be added to database
            graph_as_str = "[" + ", ".join([str(edge) for edge in graph]) + "]"
            insert_fm(graph_as_str, tn, 'forbidden_minors', 'localhost', 'root', password)

    print("There were", len(forbidden_minors), "minimal forbidden minors found for treewidth", tw)

    return forbidden_minors


def is_mfm(graph, tw):

    if treewidth_min_fill_in(graph)[0] != tw:
        return False

    for node in graph.nodes:
        temp_graph = graph.copy()
        temp_graph.remove_node(node)
        if treewidth_min_fill_in(temp_graph)[0] >= tw:
            return False

    for edge in graph.edges:
        temp_graph = graph.copy()
        temp_graph.remove_edge(*edge)
        if treewidth_min_fill_in(temp_graph)[0] >= tw:
            return False

    for edge in graph.edges:
        temp_graph = graph.copy()
        temp_graph = contracted_edge(temp_graph, edge)
        if treewidth_min_fill_in(temp_graph)[0] >= tw:
            return False

    return True


def rnd_graph_sample(nr_v, edge_p, sample_size):

    gen_graphs = []

    count = 0
    while count < sample_size:
        graph = nx.erdos_renyi_graph(nr_v, edge_p)
        gen_graphs.append(graph)
        count += 1

    return gen_graphs


# Script
password = getpass.getpass("Please insert the server password: ")


"""
- Process to find mfm for treewidth 4 (tw4) -

# TODO: Properly expand each point w/ relevant practical info

    1. Preprocess the tw4 condition, i.e. ID forbidden subgraphs + any properties that are non-existent for tw4
    2. Generate candidate graphs up to a certain number of vertices
    3. Prune to eliminate graphs that are not eligible for tw4 (based on degree constraints, symmetry, ...) - reducing
        the search space - making the algorithm + efficient
    4. Minor check the remaining candidate graphs for tw4, i.e. if a graph can be contracted to tw4 while preserving
        connectivity and vertex order (* graph minor *)
    5. ID the mfms among the remaining graphs that fail the tw4 condition - they are the smallest graphs that are NOT
        contractible to tw4 (* min forbidden minors *)
    6. Store in SQL DB
    7. Iterate this whole process by increasing the nr of max vertices during the generation (or + pruning to narrow
        search space, if still too large)
    8. Analyze the mfms, study properties and evaluate impact on tw4 computations - this may be helpful to understanding
        the constraints and structure of tw4 graphs

# TODO: Check if this is feasible for tw5
"""
