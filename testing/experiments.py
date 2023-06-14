import time
import matplotlib.pyplot as plt


def measure_execution_time(fm_k, nr_vertices):
    start_time = time.time()
    fm_k.combinatorial_enumeration(nr_vertices)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


def cge_testing(fm_k):
    nr_vertices = [1, 2, 3, 4, 5, 6, 7]

    execution_times = []
    for vertex_nr in nr_vertices:
        execution_time = measure_execution_time(fm_k, vertex_nr)
        execution_times.append(execution_time)

    # Plotting the results
    plt.plot(nr_vertices, execution_times, marker='o')
    plt.xlabel('Number of vertices')
    plt.ylabel('Execution Time (s)')
    plt.title('Performance of CGE (Combinatorial Graph Enumeration)')
    plt.grid(True)
    plt.show()
