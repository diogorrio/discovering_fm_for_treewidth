import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import linregress


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
