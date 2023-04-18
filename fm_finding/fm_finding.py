import numpy as np


class FMFinding:

    def __init__(self, fm_type):
        self.fm_type = fm_type
        if self.fm_type == "f4":
            self.min_nr_minors = 90
            self.max_nr_minors = 100
        # TODO: TBD: nr_minors
        elif self.fm_type == "f5":
            self.min_nr_minors = 0
            self.max_nr_minors = 0

    # All these methods might justify their own class, if I decide to have different ones to compare
    def tree_decompose(self):
        print("Format working as", self.min_nr_minors)
        return self

    def recursive_construction(self):
        return self

    def combinatorial_enumeration(self):
        return self

    # See if an ML approach is worth it, since training would take time
