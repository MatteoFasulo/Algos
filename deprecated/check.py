import datetime
import json
import math
import os
import profile

import cProfile
from shutil import copyfile

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


def check(lis: list):
    for i in range(len(lis)):
        if lis[i] is None:
            return False
    return True


def correction1(save: bool = False):
    with open(f"Q:\\removed\\linear_weights_name_0-1960.json") as file:
        name = json.load(file)

    with open(f"Q:\\removed\\linear_weights_name_1960-3920.json") as fin:
        f1 = json.load(fin)

    m = list()
    for i in range(len(name)):
        row = list()
        for j in range(len(name[i])):
            if name[i][j] != inf:
                # print(f"{name[i][j]} type is {type(name[i][j])}")
                row.append(name[i][j])
            elif f1[i][j] != inf:
                row.append(f1[i][j])
            else:
                row.append(None)
        m.append(row)

    NAME = [None for x in range(len(m[0]))]
    for i in range(len(m)):
        for j in range(len(m[i])):
            if (NAME[j] is None) and (m[i][j] != inf):
                NAME[j] = m[i][j]
            elif NAME[j] != m[i][j] and (m[i][j] is not None):
                print(f"{NAME[j]} != {m[i][j]}")

    if check(NAME):
        if save:
            fout = open("data\\REAL CITIES (of matrix).json", 'w', encoding="UTF-8")
            json.dump(obj=NAME, fp=fout, indent=2)
            fout.close()
        else:
            return NAME
    return None


def merge(start: int, stop: int):
    try:
        f_m = open(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}matrix_weights.json", 'r', encoding='UTF-8')
        m = json.load(f_m)
        f_m.close()
    except FileNotFoundError:
        copyfile(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}linear_weights_{start}-{stop}.json",
                 f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}matrix_weights.json")
        os.remove(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}linear_weights_{start}-{stop}.json")
        return

    print(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}linear_weights_{start}-{stop}.json")
    f_temp_m = open(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}linear_weights_{start}-{stop}.json", 'r',
                    encoding='UTF-8')
    temp_m = json.load(f_temp_m)
    f_temp_m.close()
    for row in temp_m:
        m.append(row)
    f_m = open(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}matrix_weights.json", 'w', encoding='UTF-8')
    json.dump(obj=m, fp=f_m, indent=4)
    f_m.close()
    os.remove(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}linear_weights_{start}-{stop}.json")
    return


def correction2(filename, offset):
    """merging"""
    cor = len(correction1())
    print(cor)
    with open(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu)\\{filename}") as file:
        G = json.load(file)

    wrong_rows = list()
    for i in range(len(G)):

        if cor != len(G[i]) or len(G[i]) != 7838:
            print(f"row: {i}\t{len(G[i])}\n")
            wrong_rows.append(i + offset)
    print(f"wrong of {filename}: {wrong_rows}")


def correction2b(filename, offset):
    """merging for 7906 len"""
    cor = 7906
    with open(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu)\\{filename}") as file:
        G = json.load(file)

    wrong_rows = list()
    for i in range(len(G)):

        if cor != len(G[i]):
            print(f"row: {i}\t{len(G[i])}\n")
            wrong_rows.append(i + offset)
    print(f"wrong of {filename}: {wrong_rows}")


def merge_all():
    merge(0, 1318)
    merge(1318, 2636)
    merge(2636, 2800)
    merge(2800, 3954)
    merge(3954, 5272)
    merge(5272, 5712)
    merge(5712, 6152)
    merge(6152, 6262)
    merge(6262, 6372)
    merge(6372, 6482)
    merge(6482, 6488)
    merge(6488, 6509)
    merge(6509, 6536)
    merge(6536, 6563)
    merge(6563, 6590)
    merge(6590, 7906)


def final_check():
    f_m = open(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu){os.sep}matrix_weights.json", 'r', encoding='UTF-8')
    m = json.load(f_m)
    f_m.close()
    if len(m) == len(m[(len(m) - 1)]):
        print("CORRETTO")
        return True
    print("ERRATO")
    return False


""" EXAMPLE
    G = [[0, 5, INF, 10],
         [INF, 0, 3, INF],
         [INF, INF, 0,   1],
         [INF, INF, INF, 0]]"""

with open(f"Q:\\download-2021.6.29_21.45.22-ubuntu-(ubuntu)\\matrix_weights.json") as file:
    G = json.load(file)
global G1
#print(len(G[0]))


def main():
    G1 = floyd_warshall(G, len(G))
    with open("complete.json", "w") as f1:
        json.dump(G1, f1, indent=4)
    #print_solution(G1, len(G))


cProfile.run("main()")

if __name__ == "__main__":
    correction2("linear_weights_0-1960.json", 0)
    # correction2b(f"linear_weights_{offset}-6152.json", offset)
    # merge_all()
    # final_check()
