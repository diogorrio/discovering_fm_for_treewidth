from fm_finding.fm_finding import FMFinding, password
from graph_data.db_structure import create_db, create_table


def main():
    # Load database
    create_db('forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f1', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f2', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f3', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f4', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f5', 'forbidden_minors', 'localhost', 'root', password)

    # TODO: Load graph data (if using generated graphs from 'nauty', specifically geng)

    # Find forbidden minors through various techniques; create object and use different methods
    # Testing, for F(1), F(2) or F(3)
    fm_f3 = FMFinding("F(3)")
    fm_f3.combinatorial_enumeration(5)
    fm_f3.random_sampling(10, 0.7)

    # For F(4)
    fm_f4 = FMFinding("F(4)")
    # For 8 (or more) vertices, it takes too long at the moment
    # fm_f4.combinatorial_enumeration(7)
    # fm_f4.random_sampling(10, 0.6)

    # For F(5)
    # fm_f5 = FMFinding("F(5)")
    # fm_f5.tree_decompose()

    # TODO: Check for exhaustiveness


main()
