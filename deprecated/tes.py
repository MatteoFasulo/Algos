import json
import os
import time
import webbrowser

import folium
from folium import plugins
import numpy as np
import pandas as pd
from distance import *

capoluoghi = ["L'Aquila", "Potenza", "Catanzaro", "Napoli", "Bologna", "Trieste", "Roma", "Genova", "Milano", "Ancona",
              "Campobasso", "Torino", "Bari", "Cagliari", "Palermo", "Firenze", "Trento", "Perugia", "Aosta",
              "Venezia", "Bolzano"]


def searh_cap_reg(cap_reg: str):
    geo = pd.read_json("data/italy_geo.json")
    try:
        cap_reg = cap_reg.lower().strip()
        geo["comune"] = geo["comune"].str.lower()
        lat = geo[geo["comune"] == cap_reg]["lat"].values[0]
        long = geo[geo["comune"] == cap_reg]["lng"].values[0]
        return (long, lat)
    except IndexError:
        print(cap_reg, geo[geo["comune"] == cap_reg]["lat"], geo[geo["comune"] == cap_reg]["lng"])


def fill_matrix_cap_reg():
    cap_reg = ["L'Aquila", "Potenza", "Catanzaro", "Napoli", "Bologna", "Trieste", "Roma", "Genova", "Milano", "Ancona",
               "Campobasso", "Torino", "Bari", "Cagliari", "Palermo", "Firenze", "Trento", "Perugia", "Aosta",
               "Venezia", "Bolzano"]
    new_df = pd.DataFrame(np.zeros((len(cap_reg), len(cap_reg))), index=cap_reg, columns=cap_reg)
    for i in range(len(cap_reg)):
        for j in range(len(cap_reg)):
            long1, lat1 = searh_cap_reg(cap_reg[j])
            long2, lat2 = searh_cap_reg(cap_reg[i])
            # print(long1,lat1,long2,lat2)
            new_df[cap_reg[i]][cap_reg[j]] = calculate_distance(float(long1), float(lat1),
                                                                float(long2), float(lat2))
    return new_df


def save_weights_cap_reg():
    with open('cap_reg_weights.json', 'w', encoding='utf-8') as file:
        fill_matrix_cap_reg().to_json(file, force_ascii=False)


def choose_city(city_list: list):
    cap_reg = city_list
    cap_reg = {k: v for k, v in enumerate(cap_reg)}
    correct = False
    while not correct:
        city = input("Source node (city name or ID): ").upper().strip()
        try:
            city = int(city)
            if city in cap_reg.keys():
                index = city
                city_name = cap_reg[city]
                # print(city)
                correct = True
        except ValueError:
            if city in cap_reg.values():

                for i in range(len(cap_reg)):
                    if cap_reg[i] == city:
                        index = i
                city_name = city
                print(f"Values {city}")
                correct = True
            else:
                print("\n[!] Not found\n", cap_reg, sep='')
    # print(f"{index}, {city_name}")
    return (index, city_name, cap_reg)


class Graph():
    # A constructor to iniltialize the values
    def __init__(self, nodes):
        # distance array initialization
        self.distArray = [0 for i in range(nodes)]
        # visited nodes initialization
        self.vistSet = [0 for i in range(nodes)]
        # initializing the number of nodes
        self.V = nodes
        # initializing the infinity value
        self.INF = 1000000
        # initializing the graph matrix
        self.graph = [[0 for column in range(nodes)]
                      for row in range(nodes)]

    def dijkstra(self, srcNode):
        for i in range(self.V):
            # initialise the distances to infinity first
            self.distArray[i] = self.INF
            # set the visited nodes set to false for each node
            self.vistSet[i] = False
        # initialise the first distance to 0
        self.distArray[srcNode] = 0
        for i in range(self.V):

            # Pick the minimum distance node from
            # the set of nodes not yet processed.
            # u is always equal to srcNode in first iteration
            u = self.minDistance(self.distArray, self.vistSet)

            # Put the minimum distance node in the
            # visited nodes set
            self.vistSet[u] = True

            # Update dist[v] only if is not in vistSet, there is an edge from
            # u to v, and total weight of path from src to  v through u is
            # smaller than current value of dist[v]
            for v in range(self.V):
                if self.graph[u][v] > 0 and self.vistSet[v] == False and self.distArray[v] > self.distArray[u] + \
                        self.graph[u][v]:
                    self.distArray[v] = self.distArray[u] + self.graph[u][v]

        lista = self.printSolution(self.distArray)
        return lista

    # A utility function to find the node with minimum distance value, from
    # the set of nodes not yet included in shortest path tree
    def minDistance(self, distArray, vistSet):

        # Initilaize minimum distance for next node
        min = self.INF

        # Search not nearest node not in the
        # unvisited nodes
        for v in range(self.V):
            if distArray[v] < min and vistSet[v] == False:
                min = distArray[v]
                min_index = v
        return min_index

    def printSolution(self, distArray):
        print("Node \tDistance from 0")
        distArray_list = list()
        for i in range(self.V):
            # print(i, "\t", distArray[i])
            distArray_list.append(distArray[i])
        return distArray_list  # ogni elemento è nella stessa posizione del nome comune


def graph_italy():
    index, city_name, cap_reg = choose_city(capoluoghi)
    source_lat, source_long = (float(searh_cap_reg(city_name)[1]), float(searh_cap_reg(city_name)[0]))

    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, max_zoom=7, zoom_start=5.8,
                   zoom_control=True, min_lat=36, max_lat=47, min_lon=9.5, max_lon=15.5, max_bounds=True)

    ourGraph = Graph(len(cap_reg))
    new_df = pd.read_json("cap_reg_weights.json")
    array = new_df.to_numpy()
    weights = array.tolist()
    ourGraph.graph = weights
    before = time.perf_counter_ns()
    distArray_list = ourGraph.dijkstra(index)  # Calcolo dalla sorgente
    after = time.perf_counter_ns()
    print(after)
    print(f"Execution time: ", ((after - before) / (10 ** 9)))

    for i in range(len(cap_reg)):
        distance = calculate_distance(source_long, source_lat, float(searh_cap_reg(cap_reg[i])[0]),
                                      float(searh_cap_reg(cap_reg[i])[1]))
        print(f"{distance}<-->{max(distArray_list)}")
        if city_name == cap_reg[i]:
            folium.Circle(
                location=(searh_cap_reg(cap_reg[i])[1], searh_cap_reg(cap_reg[i])[0]),
                popup=f"{cap_reg[i]}\nSource",
                radius=7500,
                color="crimson",
                fill=True,
                fill_color="crimson"
            ).add_to(m)
        elif distance >= max(distArray_list):
            folium.Circle(
                location=(searh_cap_reg(cap_reg[i])[1], searh_cap_reg(cap_reg[i])[0]),
                popup=f"{cap_reg[i]}\n{distance}Km",
                radius=distance * 20,
                color="purple",
                fill=True,
                fill_color="purple"
            ).add_to(m)
        else:
            folium.Circle(
                location=(searh_cap_reg(cap_reg[i])[1], searh_cap_reg(cap_reg[i])[0]),
                popup=f"{cap_reg[i]}\n{distance}Km",
                radius=distance * 20,
                color="green",
                fill=True,
                fill_color="green"
            ).add_to(m)
    plugins.Fullscreen(
        position="topright",
        title="Fullscreen",
        title_cancel="Exit fullscreen",
        force_separate_button=True,
    ).add_to(m)
    minimap = plugins.MiniMap()
    m.add_child(minimap)
    if not os.path.isdir("result"):
        os.mkdir("result")
    m.save(os.path.join("result", "cap_reg.html"))
    webbrowser.open_new_tab("result/cap_reg.html")


def best_source(cap_reg):
    print("\tCalculating best source")
    ourGraph = Graph(len(cap_reg))
    new_df = pd.read_json("cap_reg_weights.json")

    array = new_df.to_numpy()
    weights = array.tolist()
    ourGraph.graph = weights
    list_distance = list()  # [(source, max_distance), (source1, max_distance1)]
    best_city = None  # (index, distance)    # Todo memorizzare il minimo fra i massimi
    for city in range(len(cap_reg)):
        distArray_list = ourGraph.dijkstra(city)  # Calcolo dalla sorgente
        list_distance.append(distArray_list)
        print(f"{round(100 / len(cap_reg) * (city + 1), 2)}%")
    # print(list_distance)
    index = 0
    for lista in list_distance:
        max_dist = max(lista)
        if best_city is None:
            best_city = (index, max_dist)
        elif max_dist < best_city[1]:  # Se la nuova distanza massima è minore (quindi migliore) la memorizzo
            best_city = (index, max_dist)
        index += 1
    print(cap_reg[best_city[0]])
    return best_city


if __name__ == "__main__":
    with open("test.json","r") as f1:
        df = json.load(f1)
        print(len(df))
    for i in range(len(df)):
        print(len(df[i]))
        if len(df) != len(df[i]):
            print("bad")
            break

