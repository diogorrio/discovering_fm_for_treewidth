from fm_finding.fm_finding import FMFinding


def main():
    # Load graph data

    # Find forbidden minors through various techniques; create object and use different methods
    # For f(4)
    fm_f4 = FMFinding("f4")
    fm_f4.tree_decompose()
    # For f(5)
    fm_f5 = FMFinding("f5")
    fm_f5.tree_decompose()
    # Check for "exhaustivity"


main()
