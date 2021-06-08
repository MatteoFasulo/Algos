def main():
    pass


import os
import time
import datetime
import json
import numpy as np
import pandas as pd
import folium
from folium import plugins
from distance import calculate_distance
import googlemaps

GOOGLE_API = "AIzaSyCne109pBSAhpB2rg6SlsdqIP6q5bsbp18"
gmaps = googlemaps.Client(key=GOOGLE_API)
ASL = f"data{os.sep}C_17_bancheDati_16_0_0_file.xlsx"
province = f"data{os.sep}cities.json"


def unique_cities():
    df = pd.read_excel(ASL)
    lista_comuni = df["COMUNE"].unique().tolist()
    for i in range(0, len(lista_comuni)):
        lista_comuni[i] = lista_comuni[i].strip().capitalize()
    lista_comuni.sort()
    return lista_comuni


def list_province():
    cities = pd.read_json(province)
    cities = cities["nome"].unique().tolist()
    for i in range(0, len(cities)):
        cities[i] = cities[i].strip().capitalize()
    cities.sort()
    return cities


def make_italy_geo(cities: list):
    # TODO json city, long, lat
    js = list()
    for i in range(len(cities)):
        js_dict = dict()
        print(f"{i}<-->{cities[i]}")
        geocode_result = gmaps.geocode(cities[i], region="IT")
        try:
            geocode_result = geocode_result[0]
        except IndexError:
            print(geocode_result)
        if len(geocode_result) == 0:
            lat, long = None, None
            js_dict["comune"] = cities[i].capitalize()
            js_dict["lng"] = long
            js_dict["lat"] = lat
            js.append(js_dict)
        else:
            geocode_result = geocode_result["geometry"]["location"]
            lat, long = geocode_result["lat"], geocode_result["lng"]
            js_dict["comune"] = cities[i].capitalize()
            js_dict["lng"] = long
            js_dict["lat"] = lat
            js.append(js_dict)
        js_file = open(f"data{os.sep}italy_geo.json", 'w', encoding="utf-8")
        json.dump(obj=js, fp=js_file, indent=2)
        js_file.close()


def search_comune(comune: str):
    geo = pd.read_json("data/italy_geo.json")
    comune = comune.lower().strip()
    try:
        geo["comune"] = geo["comune"].str.lower()
        lat = geo[geo["comune"] == comune]["lat"].values[0]
        long = geo[geo["comune"] == comune]["lng"].values[0]
        return np.float64(long).item(), np.float64(lat).item()
    except IndexError:
        print(comune, geo[geo["comune"] == comune]["lat"], geo[geo["comune"] == comune]["lng"])


def fill_coords(cities: list, filename: str, traffic_model="best_guess"):
    """
    Crea un dataset con i pesi per raggiungere ogni nodo delle città nella lista
    :return: json file
    """
    night_time = datetime.datetime(2022, 1, 1, 4, 0, 0, 0)

    if datetime.datetime.now() >= night_time:
        night_time = datetime.datetime.now() + datetime.timedelta(days=2)

    latitudes = []
    longitudes = []
    origins = []
    destination = []
    distances = []
    time_needed = []

    for i in range(len(cities)):
        long, lat = search_comune(cities[i])
        latitudes.append(lat)
        longitudes.append(long)

    weights_df = pd.DataFrame(data={"city": cities, "lat": latitudes, "long": longitudes})
    weights_df['Distance'] = list
    weights_df['Minutes'] = list

    for i in range(len(cities)):
        LatOrigin = weights_df['lat'][i]
        LongOrigin = weights_df['long'][i]
        origins.append((LatOrigin, LongOrigin))

    for j in range(len(cities)):
        LatDest = weights_df['lat'][j]
        LongDest = weights_df['long'][j]
        destination.append((LatDest, LongDest))
    print(origins)
    print(destination)

    result = gmaps.distance_matrix(origins, destination, mode='driving', departure_time=night_time,
                                   traffic_model=traffic_model)

    print(result)

    """for i in range(len(cities)):
        distances.clear()
        time_needed.clear()
        for j in range(len(cities)):
            LatOrigin = weights_df['lat'][i]
            LongOrigin = weights_df['long'][i]
            origins.append((LatOrigin, LongOrigin))
            LatDest = weights_df['lat'][j]  # Save value as lat
            LongDest = weights_df['long'][j]  # Save value as lat
            destination.append((LatDest, LongDest))
            result = gmaps.distance_matrix(origins, destination, mode='driving', departure_time=night_time,
                                           traffic_model=traffic_model)
            print(result)
            #time = round((result["duration"]["value"]) / 60)
            #result = round((result["distance"]["value"]) / 1000)
            #result = round(result / 1000)
            #distances.append(result)
            #time = gmaps.distance_matrix(origins, destination, mode='driving', departure_time=night_time, traffic_model=traffic_model)["rows"][0]["elements"][0]["duration"]["value"]
            #time = round(time / 60)
            #time_needed.append(time)
            origins.clear()
            destination.clear()
            # print(result)
        weights_df['Distance'][i] = distances[::]
        weights_df['Minutes'][i] = time_needed[::]"""

    # with open(f"{filename}.json", 'w', encoding='utf-8') as file:
    # weights_df.to_json(file, force_ascii=False, indent=2)

    return weights_df


def choose_city(city_list: list):
    city_list = {k: v for k, v in enumerate(city_list)}
    correct = False
    while not correct:
        city = input("Source node (city name or ID): ").capitalize().strip()
        try:
            city = int(city)
            if city in city_list.keys():
                index = city
                city_name = city_list[city]
                # print(city)
                correct = True
        except ValueError:
            if city in city_list.values():
                for i in range(len(city_list)):
                    if city_list[i] == city:
                        index = i
                city_name = city
                print(f"Values {city}")
                correct = True
            else:
                print("\n[!] Not found\n", city_list, sep='')
    # print(f"{index}, {city_name}")
    return (index, city_name, city_list)


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
                if self.graph[u][v] > 0 and self.vistSet[v] is False and self.distArray[v] > self.distArray[u] + \
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
            if distArray[v] < min and vistSet[v] is False:
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


def graph_dijkstra():
    index, city_name, lista_comuni = choose_city(unique_cities())
    source_lat, source_long = (float(search_comune(city_name)[1]), float(search_comune(city_name)[0]))

    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, max_zoom=7, zoom_start=5.8,
                   zoom_control=True, min_lat=36, max_lat=47, min_lon=9.5, max_lon=15.5, max_bounds=True)

    ourGraph = Graph(len(lista_comuni))
    new_df = pd.read_json("weights.json")
    array = new_df.to_numpy()
    weights = array.tolist()
    ourGraph.graph = weights
    before = time.perf_counter_ns()
    distArray_list = ourGraph.dijkstra(index)  # Calcolo dalla sorgente
    after = time.perf_counter_ns()
    print(after)
    print(f"Execution time: ", ((after - before) / (10 ** 9)))

    for i in range(len(lista_comuni)):
        distance = calculate_distance(source_long, source_lat, float(search_comune(lista_comuni[i])[0]),
                                      float(search_comune(lista_comuni[i])[1]))
        print(f"{distance}<-->{max(distArray_list)}")
        if city_name == lista_comuni[i]:
            folium.Circle(
                location=(search_comune(lista_comuni[i])[1], search_comune(lista_comuni[i])[0]),
                popup=f"{lista_comuni[i]}\nSource",
                radius=7500,
                color="crimson",
                fill=True,
                fill_color="crimson"
            ).add_to(m)
        elif distance >= max(distArray_list):
            folium.Circle(
                location=(search_comune(lista_comuni[i])[1], search_comune(lista_comuni[i])[0]),
                popup=f"{lista_comuni[i]}\n{distance}Km",
                radius=distance * 20,
                color="purple",
                fill=True,
                fill_color="purple"
            ).add_to(m)
        else:
            folium.Circle(
                location=(search_comune(lista_comuni[i])[1], search_comune(lista_comuni[i])[0]),
                popup=f"{lista_comuni[i]}\n{distance}Km",
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
    m.save(os.path.join("result", "italy.html"))


def graph_italy():
    index, city_name, lista_comuni = choose_city(list_province())
    #print(index, city_name, lista_comuni)
    source_lat, source_long = (float(search_comune(city_name)[1]), float(search_comune(city_name)[0]))

    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, max_zoom=7, zoom_start=5.8,
                   zoom_control=True, min_lat=36, max_lat=47, min_lon=9.5, max_lon=15.5, max_bounds=True)

    nodes = []
    for i in range(len(lista_comuni)):
        distance = calculate_distance(source_long, source_lat, float(search_comune(lista_comuni[i])[0]),
                                      float(search_comune(lista_comuni[i])[1]))
        nodes.append(distance)

    for i in range(len(lista_comuni)):
        if city_name == lista_comuni[i]:
            folium.Circle(
                location=(search_comune(lista_comuni[i])[1], search_comune(lista_comuni[i])[0]),
                popup=f"{lista_comuni[i]}\nSource",
                radius=7500,
                color="crimson",
                fill=True,
                fill_color="crimson"
            ).add_to(m)
        elif nodes[i] >= max(nodes):
            folium.Circle(
                location=(search_comune(lista_comuni[i])[1], search_comune(lista_comuni[i])[0]),
                popup=f"{lista_comuni[i]}\n{nodes[i]}Km",
                radius=nodes[i] * 20,
                color="purple",
                fill=True,
                fill_color="purple"
            ).add_to(m)
        else:
            folium.Circle(
                location=(search_comune(lista_comuni[i])[1], search_comune(lista_comuni[i])[0]),
                popup=f"{lista_comuni[i]}\n{nodes[i]}Km",
                radius=nodes[i] * 20,
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
    m.save(os.path.join("result", "italy.html"))


def best_source(lista_comuni):
    ourGraph = Graph(len(lista_comuni))
    new_df = pd.read_json("weights.json")

    array = new_df.to_numpy()
    weights = array.tolist()
    ourGraph.graph = weights
    list_distance = list()  # [(source, max_distance), (source1, max_distance1)]
    best_city = None  # (index, distance)    # Todo memorizzare il minimo fra i massimi
    for city in range(len(lista_comuni)):
        distArray_list = ourGraph.dijkstra(city)  # Calcolo dalla sorgente
        list_distance.append(distArray_list)

    # print(list_distance)
    index = 0
    for lista in list_distance:
        max_dist = max(lista)
        if best_city is None:
            best_city = (index, max_dist)
        elif max_dist < best_city[1]:  # Se la nuova distanza massima è minore (quindi migliore) la memorizzo
            best_city = (index, max_dist)
        index += 1
    print(lista_comuni[best_city[0]])
    return best_city


if __name__ == "__main__":
    # best_source(lista_comuni=unique_cities())
    # fill_coords(unique_cities()[:10], "weights")
    # make_italy_geo(unique_cities())
    # print(len(unique_cities()[::]))
    # make_italy_geo(unique_cities()[::])
    graph_italy()
    # print(search_comune("Roma (Municipi 1,2,3,4,5,6)"))

def main():
    pass