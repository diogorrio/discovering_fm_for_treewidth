import networkx as nx
from networkx.algorithms.approximation import treewidth_min_fill_in

from fm_finding.fm_finding import FMFinding, password, start_db
from graph_data.db_structure import create_db, create_table, retrieve_entries
from testing.experiments import *


def main():
    # Load database if the user decided to
    if start_db:
        print("Initializing database...")
        load_database()

    # TODO: Load graph data (if using generated graphs from 'nauty', specifically geng)

    # Find forbidden minors through various techniques; create object and use different methods
    # Testing, for F(1), F(2) or F(3)
    fm_f3 = FMFinding("F(3)")
    # combined_approach(fm_f3, 10)
    # fm_f3.random_sampling(10, 0.45, 10000)
    # fm_f3.find_best_ratio(10, 10000, 0, 1, 0.025)

    # For F(4)
    fm_f4 = FMFinding("F(4)")
    # fm_f4.combinatorial_enumeration(7)
    # fm_f4.find_best_ratio(8, 10000, 0, 1, 0.025)
    # fm_f4.random_sampling(9, 0.675, 50000)

    # For F(5)
    fm_f5 = FMFinding("F(5)")
    # fm_f5.combinatorial_enumeration(7)
    # TODO: fm_f5.find_best_ratio(10, 10000, 0, 1, 0.025)
    # fm_f5.random_sampling(8, 0.925, 2000000)

    # Testing
    # cge_testing(fm_f3)
    # erdos_testing(fm_f3)
    # highest_tw_ratio()
    # draw_mfm("fm_in_f4")
    # avg_runs_until_minor()
    # conn_check_pruning()
    # mfm_analysis_aes_vs_abs()


def load_database():
    create_db('forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f1', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f2', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f3', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f4', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f5', 'forbidden_minors', 'localhost', 'root', password)


def combined_approach(fm_fn, max_nr_vertices):
    """
    Combines both the designed approaches (combinatorial enum. and random sampling),
    separated by the number of vertices where it becomes more efficient to change approach
    :param fm_fn: The set of the forbidden minors we want to fill it with
    :param max_nr_vertices: Up until how many vertices do you want the graph search space to go?
    """
    break_point = 7
    for i in range(2, break_point + 1):
        fm_fn.combinatorial_enumeration(i)
    for i in range(break_point + 1, max_nr_vertices + 1):
        fm_fn.random_sampling(i, 0.5)


main()
