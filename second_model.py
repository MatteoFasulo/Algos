import math
import os
import time

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra, bellman_ford, johnson

import matplotlib.pyplot as plt

inf = math.inf


# Subsetting
def subs(matrix: list, newLen: int):
    """
    Data una matrice e un intero resituisce un subset con tutte le città principali (capoluoghi provincia e regione)
    della dimensione dell'intero.
    :param matrix:
    :param newLen:
    :return:
    """
    geo_final = pd.read_json(f"data{os.sep}geo_final.json")

    pass


def shortest_path(algorithm: str, matrix, one_way: bool = False, index: int = 0) -> np.ndarray:
    graph = csr_matrix(matrix)
    if algorithm.strip().lower().startswith("d"):
        start = time.time()
        dist_matrix = dijkstra(graph, one_way, index)
        end = time.time()
    elif algorithm.strip().lower().startswith("b"):
        start = time.time()
        dist_matrix = bellman_ford(csgraph=graph, directed=one_way, indices=index)
        end = time.time()
    else:
        start = time.time()
        dist_matrix = johnson(graph, one_way, index)
        end = time.time()

    needed_time = end - start

    return dist_matrix, needed_time


def main(distance_df: str, output_csv: str):
    if os.path.isfile(output_csv):
        df = pd.read_csv(output_csv)
        df = df["0"]
        times = df.values.tolist()
    else:
        times = execution_time(distance_df, output_csv)
    plt.title('Shortest path algorithms')
    plt.ylabel('Time (sec)')
    bars = ['Bellman-Ford', 'Dijkstra (Fib Heap)', 'Johnson']
    plt.bar(bars, times)
    plt.grid()
    plt.show()
    return


def execution_time(input_filename: str, output_csv: str):
    input_data = pd.read_json(input_filename)

    matrix = input_data.values
    times = [shortest_path('b', matrix)[1], shortest_path('d', matrix)[1], shortest_path('j', matrix)[1]]

    print(times)
    df = pd.Series(times, index=['bellman', 'dijkstra', 'johnson'])
    df.to_csv(output_csv)
    return times


if __name__ == "__main__":
    main(distance_df="dati_finali/full_df.json", output_csv="dati_finali/full_df.csv")
