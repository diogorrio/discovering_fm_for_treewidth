import networkx as nx
from networkx.algorithms.approximation import treewidth_min_fill_in

from fm_finding.fm_finding import FMFinding, password, start_db
from fm_finding.tw_quickbb import quick_bb
from graph_data.db_structure import create_db, create_table, retrieve_entries


def main():
    # Load database if the user decided to
    if start_db:
        print("Initializing database...")
        load_database()

    # TODO: Load graph data (if using generated graphs from 'nauty', specifically geng)

    # TESTING SECTION: Do comment out residuals if there are any to be found here
    graph = nx.erdos_renyi_graph(10, 0.5)
    print("The result of qbb for", graph, "is", quick_bb(graph))
    print("The result of nx's tw min fill for", graph, "is", treewidth_min_fill_in(graph)[0])

    # Find forbidden minors through various techniques; create object and use different methods
    # Testing, for F(1), F(2) or F(3)
    fm_f3 = FMFinding("F(3)")
    # fm_f3.combinatorial_enumeration(5)
    # TODO: Test how long it takes to find the Wagner graph (8 vertices)
    #  Also note the running time to understand the most effective nr_vertices / edge_prob combination for this problem
    # fm_f3.random_sampling(8, 0.5)

    # For F(4)
    # fm_f4 = FMFinding("F(4)")
    # For 8 (or more) vertices, it takes too long at the moment
    # fm_f4.combinatorial_enumeration(7)
    # fm_f4.random_sampling(10, 0.6)

    # For F(5)
    # fm_f5 = FMFinding("F(5)")
    # fm_f5.tree_decompose()

    # TODO: Check for exhaustiveness


def load_database():
    create_db('forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f1', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f2', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f3', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f4', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f5', 'forbidden_minors', 'localhost', 'root', password)


main()
