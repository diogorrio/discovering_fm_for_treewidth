import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from fm_finding.fm_finding import password
from graph_data.db_structure import retrieve_entries
from graph_data.graph_structure import *


def measure_execution_time(fm_k, nr_vertices, approach, nr_gen):
    start_time = time.time()
    if approach == "cge":
        fm_k.combinatorial_enumeration(nr_vertices)
    elif approach == "rnd":
        fm_k.random_sampling(nr_vertices, 0.5, nr_gen)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


def cge_testing(fm_k):
    nr_vertices = [1, 2, 3, 4, 5, 6, 7]

    execution_times = []
    for vertex_nr in nr_vertices:
        execution_time = measure_execution_time(fm_k, vertex_nr, "cge", 0)
        execution_times.append(execution_time)

    plt.plot(nr_vertices, execution_times, marker='o')
    plt.xlabel('Number of vertices')
    plt.ylabel('Execution Time (s)')
    plt.title('Performance of CGE (Combinatorial Graph Enumeration)')
    plt.grid(True)
    plt.show()


def erdos_testing(fm_k):
    nr_vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    nr_gen = 10000

    execution_times = []
    for vertex_nr in nr_vertices:
        execution_time = measure_execution_time(fm_k, vertex_nr, "rnd", nr_gen)
        execution_times.append(execution_time)

    plt.plot(nr_vertices, execution_times, marker='o')
    plt.xlabel('Number of vertices')
    plt.ylabel('Execution Time (s)')
    plt.title('Performance of E-R Binomial (Random Sampling)')
    plt.grid(True)
    plt.show()


def highest_tw_ratio():
    x = np.array([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    y = np.array([0.800, 0.675, 0.575, 0.500, 0.425, 0.375, 0.350,
                  0.300, 0.275, 0.250, 0.225, 0.200, 0.175])
    z = np.array([64.43, 59.53, 56.08, 53.53, 50.27, 48.35, 46.02,
                  45.76, 43.93, 43.76, 41.76, 42.67, 39.41])

    coeffs_xy = np.polyfit(x, y, 1)
    regression_xy = np.poly1d(coeffs_xy)

    coeffs_xz = np.polyfit(x, z, 1)
    regression_xz = np.poly1d(coeffs_xz)

    # 3D Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)

    x_range_xy = np.linspace(x.min(), x.max(), 100)
    y_range_xy = regression_xy(x_range_xy)
    z_range_xy = np.linspace(z.min(), z.max(), 100)
    ax.plot(x_range_xy, y_range_xy, z_range_xy, color='red')

    x_range_xz = np.linspace(x.min(), x.max(), 100)
    y_range_xz = regression_xz(x_range_xz)
    z_range_xz = regression_xy(x_range_xz)
    ax.plot(x_range_xz, y_range_xz, z_range_xz, color='blue')

    ax.set_xlabel('Number of vertices')
    ax.set_ylabel('Edge creation probability')
    ax.set_zlabel('Accurate treewidth ratio')
    plt.title('Parameter Combination resulting in the Highest Treewidth Ratio (1)')
    plt.show()

    # Two 2D plots
    plt.figure()
    plt.scatter(x, y, color='orange')
    plt.plot(x, regression_xy(x), color='red')
    plt.xlabel('Number of vertices')
    plt.ylabel('Edge creation probability')
    plt.title('Parameter Combination resulting in the Highest Treewidth Ratio (2)')
    plt.legend()
    plt.show()

    plt.figure()
    plt.scatter(x, z, color='orange')
    plt.plot(x, regression_xz(x), color='blue')
    plt.xlabel('Number of vertices')
    plt.ylabel('Accurate treewidth ratio')
    plt.title('Parameter Combination resulting in the Highest Treewidth Ratio (3)')
    plt.legend()
    plt.show()


def draw_mfm(table_name):
    retrieved, n_retrieved = retrieve_entries(table_name, 'forbidden_minors', 'localhost', 'root', password)
    draw_graphs_rnd(n_retrieved)

    print(len(n_retrieved), "minimal forbidden minors from the", table_name, "table were retrieved.")


def avg_runs_until_minor():
    x = [8, 9, 10, 11]
    probs = [16130, 211000, 3320000, 7780000]

    plt.figure()
    ax = sns.heatmap(np.array([probs]), cmap='YlGnBu', annot=True, cbar=True)
    plt.xlabel('Number of Vertices')
    plt.ylabel('A minor is found every N runs (for x vertices)')
    plt.title('Average Number of Runs until an MFM is Found')

    ax.set_xticklabels(x)

    plt.show()


def conn_check_pruning():
    x = [8, 9, 10, 11, 12]
    connected = [999900, 998937, 995427, 989404, 972797]
    total = 1000000
    pruning_achieved = [(total - c / total) * 100 for c in connected]

    plt.figure()
    plt.bar(x, pruning_achieved)
    plt.xlabel('Number of Vertices')
    plt.ylabel('Reduction/Pruning Achieved (%)')
    plt.title('Search Space Reduction when Performing \n Pre-Analysis Connectivity Checking',
              y=1.05)

    plt.ylim(min(pruning_achieved), max(pruning_achieved)+0.05)

    plt.tight_layout()
    plt.show()


def mfm_analysis_aes_vs_abs():
    analysis_times = [724.6, 30.7]
    min_fm_found = [0.35, 0.28]
    method_labels = ['AEC Analysis', 'ABS Analysis']

    fig, ax1 = plt.subplots()

    ax1.bar(method_labels, analysis_times, color='tab:blue')
    ax1.set_ylabel('Analysis Time on Average (sec)')
    ax1.set_ylim(0, max(analysis_times) * 1.2)

    ax2 = ax1.twinx()
    ax2.plot(method_labels, min_fm_found, marker='o', color='tab:red')
    ax2.set_ylabel('MFMs Found on Average')
    ax2.set_ylim(0, max(min_fm_found) * 1.2)

    plt.title('AEC vs. ABS, Performance Comparison')
    ax1.set_xlabel('Approaches')
    ax1.legend(['Analysis Time'], loc='upper left')
    ax2.legend(['MFMs Found'], loc='upper right')

    plt.show()


def sampling_cover():
    sample_size = 2000000
    nr_vertices = list(range(20))
    a001349 = [
        1, 1, 1, 2, 6, 21, 112, 853, 11117, 261080,
        11716571, 1006700565, 164059830476, 50335907869219,
        29003487462848061, 31397381142761241960, 63969560113225176176277,
        245871831682084026519528568, 1787331725248899088890200576580,
        24636021429399867655322650759681644
    ]

    cover = []
    for value in a001349:
        if sample_size >= value:
            cover.append(100)
        else:
            cover.append((sample_size / value) * 100)

    plt.plot(nr_vertices, cover, marker='o')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Coverage (%)')
    plt.title('Feasible Sampling Coverage \n of Existing Connected Non-Isomorphic Graphs')
    plt.xticks(nr_vertices)
    plt.show()

