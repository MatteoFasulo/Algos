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
province = f"data{os.sep}cities.json"


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


def graph_italy():
    index, city_name, lista_comuni = choose_city(list_province())
    # print(index, city_name, lista_comuni)
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
    filename = f".{os.sep}result{os.sep}italy.html"
    return filename


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


def main():
    graph_italy()
