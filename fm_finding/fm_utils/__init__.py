import getpass

from fm_finding.fm_finding import FMFinding
from graph_data.db_structure import create_db, create_table


def main():
    # Load database
    password = getpass.getpass("Please insert the server password: ")
    create_db('forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f4', 'forbidden_minors', 'localhost', 'root', password)
    create_table('fm_in_f5', 'forbidden_minors', 'localhost', 'root', password)

    # TODO: Load graph data

    # Find forbidden minors through various techniques; create object and use different methods
    # For f(4)
    fm_f4 = FMFinding("f4")
    fm_f4.tree_decompose()
    # For f(5)
    fm_f5 = FMFinding("f5")
    fm_f5.tree_decompose()

    # Check for "exhaustivity"


main()
