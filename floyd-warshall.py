import datetime
import math
import profile

from third_model import weights
import cProfile

INF = math.inf
inf = math.inf


def floyd_warshall(G, nV: int):
    distance = list(map(lambda i: list(map(lambda j: j, i)), G))

    for k in range(nV):
        for i in range(nV):
            for j in range(nV):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
    # print_solution(distance, nV)
    return distance  # , nV


def print_solution(distance, nV: int):
    for i in range(nV):
        for j in range(nV):
            if distance[i][j] == INF:
                print("INF", end=" ")
            else:
                print(distance[i][j], end="  ")
        print("\n")


"""EXAMPLE OF MATRIX
    G = [[0, 5, INF, 10],
         [INF, 0, 3, INF],
         [INF, INF, 0,   1],
         [INF, INF, INF, 0]]"""

G = weights()
global G1


def main():
    G1 = floyd_warshall(G, 146)
    print_solution(G1, 146)


cProfile.run("main()")
