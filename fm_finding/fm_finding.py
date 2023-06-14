import sys

import networkx as nx
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import getpass
from networkx.algorithms.approximation import treewidth_min_fill_in
from networkx.algorithms.minors import contracted_edge

from fm_finding.tw_quickbb import quick_bb
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


# Setup script
def wait_for_input():
    yes = {'yes', 'y', 'yeah', ''}
    no = {'no', 'n', 'nah'}

    sys.stdout.write("Do you want to start up the database? (Type 'yes' or 'no')")

    y_n = input().lower()
    if y_n in yes:
        start_db_wfi = True
        password_wfi = getpass.getpass("Please insert the server password: ")
        return password_wfi, start_db_wfi
    elif y_n in no:
        start_db_wfi = False
        password_wfi = ""
        print("Database not initiated.")
        return password_wfi, start_db_wfi
    else:
        print("Input was not valid. Rerun the program.")
        sys.exit(0)


password, start_db = wait_for_input()


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
        return self

    def recursive_construction(self):
        return self

    def combinatorial_enumeration(self, nr_v):
        nr_vertices = nr_v
        # For F(n), the tw has to be n+1
        all_graphs = gen_connected_graphs_with(nr_vertices)
        min_forbidden_minors = find_minimal_forbidden_minors(all_graphs, self.treewidth, self.table_name)

        draw_graphs(min_forbidden_minors)

        print("Combinatorial enumeration process finished for", nr_v, "vertices")
        print("This outputs", len(min_forbidden_minors),
              "minimal forbidden minors, out of the established", self.max_nr_minors, "at most",
              "for the set", self.fm_type)

    def random_sampling(self, nr_v, edge_p, nr_gen):
        edge_prob = edge_p
        nr_vertices = nr_v
        nr_gen_graphs = nr_gen

        all_graphs = rnd_graph_sample(nr_vertices, edge_prob, nr_gen_graphs)

        # Make sure of connectivity (and thus, viability) of analyzing the sampled graphs
        conn_graphs = []
        for graph in all_graphs:
            if nx.is_connected(graph):
                conn_graphs.append(graph)

        print(len(conn_graphs), "out of the initially sampled", len(all_graphs), "graphs are connected.")

        min_forbidden_minors = find_minimal_forbidden_minors_rnd(conn_graphs, self.treewidth, self.table_name)

        draw_graphs_rnd(min_forbidden_minors)

        #  Isomorphism:
        #  An option could be simply generating and adding them all and
        #  only doing the isomorphism check on the entire db later - instead of at every addition of a mfm

        print("Random sampling process finished for", nr_v, "vertices.")
        print("This outputs", len(min_forbidden_minors),
              "minimal forbidden minors, out of the established", self.max_nr_minors, "at most",
              "for the set", self.fm_type)

    def find_best_ratio(self, nr_v, nr_gen, l_bound, u_bound, step_size):
        nr_gen_graphs = nr_gen
        ratios = []
        edge_probs = []

        for edge_p in np.arange(l_bound, u_bound, step_size):
            gen_graphs = rnd_graph_sample(nr_v, edge_p, nr_gen_graphs)

            conn_graphs = []
            for graph in gen_graphs:
                if nx.is_connected(graph):
                    conn_graphs.append(graph)

            print(len(conn_graphs), "out of the initially sampled", len(gen_graphs), "graphs are connected.")

            if len(conn_graphs) != 0:
                crt_ratio = ratio_tw_per_gen(conn_graphs, nr_v, edge_p, self.treewidth)
                ratios.append(crt_ratio)
                edge_probs.append(edge_p)

        best_ratio = np.max(ratios)
        best_ratio_i = np.argmax(ratios)
        best_edge_p = edge_probs[best_ratio_i]
        print("The edge probability that gives the best ratio for treewidth", self.treewidth,
              "and for", nr_v, "vertices is", best_edge_p * 100, "%. The ratio is", best_ratio, "%.")


# For n=[0,+oo], n being the # of vertices:
# 1, 1, 1, 2, 6, 21, 112, ... (see https://oeis.org/A001349/list)
def gen_connected_graphs_with(max_nr_vertices):
    gen_graphs = make_graphs(max_nr_vertices)
    gen_graphs = select(gen_graphs, max_nr_vertices)
    # draw_graphs(gen_graphs)

    print("Found", len(gen_graphs), "distinct connected graphs with", max_nr_vertices, "vertices.")

    return gen_graphs


def find_minimal_forbidden_minors(graphs, tw, tn):
    forbidden_minors = []

    for i, graph in enumerate(graphs):
        # print("Processing graph", i+1, "out of", len(graphs))

        n_graph = nx.Graph()
        n_graph.add_edges_from(graph)

        if is_mfm(n_graph, tw):
            forbidden_minors.append(graph)

            if start_db:
                if not is_isomorphic(n_graph, tn):
                    # Edges representation turned to string to be added to database
                    graph_as_str = "[" + ", ".join([str(edge) for edge in graph]) + "]"
                    insert_fm(graph_as_str, tn, 'forbidden_minors', 'localhost', 'root', password)
                else:
                    edge_list_graph = list(n_graph.edges())
                    print("This found minimal forbidden minor was isomorphic to one already on the database:")
                    print(edge_list_graph)
                    print("Skipping...")

    print("> There were", len(forbidden_minors), "minimal forbidden minors found for treewidth", tw)

    return forbidden_minors


def find_minimal_forbidden_minors_rnd(graphs, tw, tn):
    forbidden_minors = []

    for i, graph in enumerate(graphs):
        # print("Processing graph", i+1, "out of", len(graphs))

        if is_mfm(graph, tw):
            forbidden_minors.append(graph)

            edge_list_graph = list(graph.edges())

            if start_db:
                if not is_isomorphic(graph, tn):
                    # Edges representation turned to string to be added to database
                    graph_as_str = "[" + ", ".join([str(edge) for edge in edge_list_graph]) + "]"
                    insert_fm(graph_as_str, tn, 'forbidden_minors', 'localhost', 'root', password)
                else:
                    print("This found minimal forbidden minor was isomorphic to one already on the database:")
                    print(edge_list_graph)
                    print("Skipping...")

    print("> There were", len(forbidden_minors), "minimal forbidden minors found for treewidth", tw)

    return forbidden_minors


def is_mfm(graph, tw):
    if max(1, max(len(u) - 1 for u in quick_bb(graph))) != tw:
        return False

    for node in graph.nodes:
        temp_graph = graph.copy()
        temp_graph.remove_node(node)
        if max(1, max(len(u) - 1 for u in quick_bb(temp_graph))) >= tw:
            return False

    for edge in graph.edges:
        temp_graph = graph.copy()
        temp_graph.remove_edge(*edge)
        if max(1, max(len(u) - 1 for u in quick_bb(temp_graph))) >= tw:
            return False

    for edge in graph.edges:
        temp_graph = graph.copy()
        temp_graph = contracted_edge(temp_graph, edge)
        if max(1, max(len(u) - 1 for u in quick_bb(temp_graph))) >= tw:
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


def is_isomorphic(graph_to_compare, tn):
    # Check isomorphism with any other already previously generated graph
    retrieved, n_retrieved = retrieve_entries(tn, 'forbidden_minors', 'localhost', 'root', password)
    for r_graph in n_retrieved:
        if nx.is_isomorphic(graph_to_compare, r_graph):
            return True

    return False


# For experimenting - trying to determine the combination that has the highest correct tw per # of generations
def ratio_tw_per_gen(graphs, nr_v, edge_p, tw):
    correct_tw_right_away = 0
    for graph in graphs:
        if (max(1, max(len(u) - 1 for u in quick_bb(graph)))) == tw:
            correct_tw_right_away += 1

    ratio = round((correct_tw_right_away / len(graphs)) * 100, 2)

    print("The ratio of the desired treewidth", tw, "for the combination of", nr_v,
          "vertices and an edge probability of", edge_p, "is", ratio)

    return ratio

