import os
import numpy as np
import pandas as pd
import folium
import time
from copy import deepcopy
import urllib.request
import urllib.error
from folium import plugins
import json

from distance import calculate_distance

##############################################
comuni = f"data{os.sep}geo_final.json"


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


##############################################


def download_comuni(filename="geo_final.json"):
    url = "https://raw.githubusercontent.com/MatteoFasulo/Algos/main/data/geo_final.json"
    connection = True
    while connection:
        try:
            print(f"[i] {filename} file not found... creating it")
            os.chdir("data")
            urllib.request.urlretrieve(url, filename)
            os.chdir("..")
            print(f"[i] {filename} downloaded")
            connection = False
        except urllib.error.URLError:
            print("[i] No connection with Host... retry in 5 seconds")
            connection = True
            time.sleep(5)
    return


def list_comuni():
    if not os.path.isfile(comuni):
        download_comuni()
    df = pd.read_json(comuni)
    cities = df["comune"].unique().tolist()
    for i in range(len(cities)):
        cities[i] = cities[i].capitalize().strip()
    cities.sort()
    return cities


def search_comune(comune: str):
    geo = pd.read_json(comuni)
    comune = comune.lower().strip()
    try:
        geo["comune"] = geo["comune"].str.lower()
        lat = geo[geo["comune"] == comune]["lat"].values[0]
        long = geo[geo["comune"] == comune]["lng"].values[0]
        return np.float64(long).item(), np.float64(lat).item()
    except IndexError:
        print(comune, geo[geo["comune"] == comune]["lat"], geo[geo["comune"] == comune]["lng"])


def choose_city(city_list: list):
    city_list = {k: v for k, v in enumerate(city_list)}
    correct = False
    clear()
    while not correct:
        city = input("Source node (city name or ID): ").capitalize().strip()
        try:
            city = int(city)
            if city in city_list.keys():
                index = city
                city_name = city_list[city]
                correct = True
        except ValueError:
            if city in city_list.values():
                for i in range(len(city_list)):
                    if city_list[i] == city:
                        index = i
                city_name = city
                correct = True
            else:
                print("\n[!] Not found\n", city_list, sep='')
    return (index, city_name, city_list)


def cap_regione():
    list_cap_regione = []
    f_cap = open(f"data{os.sep}capoluoghi_regione.json", 'r', encoding='UTF-8')
    df = json.load(f_cap)
    f_cap.close()

    for key in df.keys():
        list_cap_regione.append(df[key]["comune"])

    return list_cap_regione


def cap_provincia():
    list_cap_provincia = []
    f_cap = open(f"data{os.sep}capoluoghi_provincia.json", 'r', encoding='UTF-8')
    df = json.load(f_cap)
    f_cap.close()

    cap_reg = cap_regione()

    for key in df.keys():
        for city in df[key]["capoluoghi_provincia"]:
            if city not in cap_reg:
                list_cap_provincia.append(city)

    return list_cap_provincia


def give_comuni():
    list_comuni = list()
    df = pd.read_json(f"data{os.sep}geo_final.json")
    comuni = df["comune"].tolist()
    cap_reg = cap_regione()
    cap_prov = cap_provincia()

    for comune in comuni:
        if (comune not in cap_reg) and (comune not in cap_prov):
            list_comuni.append(comune)

    return list_comuni


def graph_italy():
    list_cities = list_comuni()
    index, city_name, list_cities = choose_city(list_cities)

    try:
        f_dist = open(f"data{os.sep}linear_weights.json", 'r', encoding='UTF-8')
        dist = json.load(f_dist)
        f_dist.close()
    except FileNotFoundError:
        dist = matrix_distance()

    longest_path = [max(dist[i]) for i in range(len(list_cities))]

    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, zoom_start=5.8,
                   zoom_control=True, min_lat=36, max_lat=47, min_lon=9.5, max_lon=15.5, max_bounds=False)

    best_source_index, value = best_source(list_cities, dist)

    capoluoghi_regione = cap_regione()
    capoluoghi_provincia = cap_provincia()  # capoluoghi_provincia-capoluoghi_regione
    # comuni = give_comuni()                      #comuni-capoluoghi_provincia

    f1 = folium.FeatureGroup("Capoluoghi di regione")
    f2 = folium.FeatureGroup("Capoluoghi di provincia")
    f3 = folium.FeatureGroup("Comuni")

    for i in range(len(list_cities)):
        distance = dist[index][i]
        ################################################################################################################
        if city_name == list_cities[i]:
            if list_cities[i] in capoluoghi_regione:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=list_cities[i],
                    radius=7500,
                    color="crimson",
                    fill=True,
                    fill_color="crimson"
                ).add_to(f1)
            elif list_cities[i] in capoluoghi_provincia:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=list_cities[i],
                    radius=7500,
                    color="crimson",
                    fill=True,
                    fill_color="crimson"
                ).add_to(f2)
            else:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=list_cities[i],
                    radius=7500,
                    color="crimson",
                    fill=True,
                    fill_color="crimson"
                ).add_to(f3)
        ################################################################################################################
        elif i == best_source_index:
            if list_cities[i] in capoluoghi_regione:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance * 10,
                    color="blue",
                    fill=True,
                    fill_color="blue"
                ).add_to(f1)
            elif list_cities[i] in capoluoghi_provincia:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance * 10,
                    color="blue",
                    fill=True,
                    fill_color="blue"
                ).add_to(f2)
            else:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance * 10,
                    color="blue",
                    fill=True,
                    fill_color="blue"
                ).add_to(f3)
        ################################################################################################################
        elif distance >= longest_path[0]:
            if list_cities[i] in capoluoghi_regione:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance,
                    color="purple",
                    fill=True,
                    fill_color="purple"
                ).add_to(f1)
            elif list_cities[i] in capoluoghi_provincia:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance,
                    color="purple",
                    fill=True,
                    fill_color="purple"
                ).add_to(f2)
            else:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance,
                    color="purple",
                    fill=True,
                    fill_color="purple"
                ).add_to(f3)
        ################################################################################################################
        else:
            if list_cities[i] in capoluoghi_regione:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance,
                    color="green",
                    fill=True,
                    fill_color="green"
                ).add_to(f1)
            elif list_cities[i] in capoluoghi_provincia:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance,
                    color="green",
                    fill=True,
                    fill_color="green"
                ).add_to(f2)
            else:
                folium.Circle(
                    location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                    popup=f"{list_cities[i]}\n{distance}Km",
                    radius=distance,
                    color="green",
                    fill=True,
                    fill_color="green"
                ).add_to(f3)
    plugins.Fullscreen(
        position="topright",
        title="Fullscreen",
        title_cancel="Exit fullscreen",
        force_separate_button=True,
    ).add_to(m)
    minimap = plugins.MiniMap()
    m.add_child(minimap)
    f1.add_to(m)
    f2.add_to(m)
    f3.add_to(m)
    folium.LayerControl().add_to(m)
    if not os.path.isdir("result"):
        os.mkdir("result")
    m.save(os.path.join("result", "first_model.html"))
    return os.path.abspath(f"result{os.sep}first_model.html")


def best_source(list_cities, weights):
    cities = list_cities
    maximums = []
    best_city = None

    for i in range(len(cities)):
        maximums.append(max(weights[i]))

    best_value = min(maximums)
    index = 0

    for value in maximums:
        if value == best_value:
            best_city = (index, value)
        index += 1
    print(f"Best city: {cities[best_city[0]]}")
    return best_city


def make_matrix(leng: int):
    riga = [0 for x in range(leng)]
    matrix = [deepcopy(riga) for x in range(leng)]
    return matrix


def matrix_distance(filename=comuni):
    city = pd.read_json(filename)
    unique = city["comune"].tolist()
    longitudes = city["lng"].tolist()
    latitudes = city["lat"].tolist()

    matrix = make_matrix(len(unique))

    for r in range(len(matrix)):
        for c in range(r, len(matrix[r])):
            dist = calculate_distance(longitudes[r], latitudes[r], longitudes[c], latitudes[c])
            matrix[r][c] = dist
            matrix[c][r] = dist
    js_file = open(f"data{os.sep}linear_weights.json", 'w', encoding="utf-8")
    json.dump(obj=matrix, fp=js_file, indent=4)
    js_file.close()
    return matrix


def print_matrix(matrix):
    print("[", end="")
    for row in range(len(matrix)):
        if row == 0:
            print(matrix[row], sep='')
        elif row == len(matrix) - 1:
            print(' ', matrix[row], sep='', end='')
        else:
            print(' ', matrix[row], sep='')
    print("]\n")


def main():
    path = graph_italy()
    return path
