import os
import datetime
import time
import urllib.request
import urllib.error
import numpy as np
import pandas as pd
import folium
import math
import json
import googlemaps
from rich.console import Console
from folium import plugins

#######################################################
GOOGLE_API = "AIzaSyCne109pBSAhpB2rg6SlsdqIP6q5bsbp18"
comuni = f"data{os.sep}comuni.json"
gmaps = googlemaps.Client(key=GOOGLE_API, retry_over_query_limit=False)


#######################################################


def download_needed_file():
    urls = ["https://raw.githubusercontent.com/MatteoFasulo/Algos/main/data/comuni.json",
            "https://raw.githubusercontent.com/MatteoFasulo/Algos/main/data/capoluoghi_regione.json",
            "https://raw.githubusercontent.com/MatteoFasulo/Algos/main/data/capoluoghi_provincia.json",
            "https://raw.githubusercontent.com/MatteoFasulo/Algos/main/data/final.json",
            "https://raw.githubusercontent.com/MatteoFasulo/Algos/main/weights/weights.json"]

    for url in urls:
        filename = url[(url.rfind('/') + 1):]
        connection = True
        os.chdir("data")
        if not os.path.isfile(filename):
            while connection:
                try:
                    print(f"[i] {filename} file not found... creating it")
                    urllib.request.urlretrieve(url, filename)
                    print(f"[i] {filename} downloaded")
                    connection = False
                except urllib.error.URLError:
                    print("[i] No connection with Host... retry in 5 seconds")
                    connection = True
                    time.sleep(5)
        os.chdir("..")
    return


def list_comuni():
    if not os.path.isfile(comuni):
        download_needed_file()
    df = pd.read_json(comuni)
    cities = df["comune"].unique().tolist()
    for i in range(len(cities)):
        print(cities[i])
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


def best_source(graph_type: bool):
    new_df = pd.read_json("weights.json")
    cities = new_df["city"].tolist()
    maximums = []
    best_city = None

    print(graph_type)
    if graph_type is True:
        print("KM")
        parameter = new_df["Distance"].tolist()
    else:
        print("MIN")
        parameter = new_df["Minutes"].tolist()

    # print((new_df["Minutes"].tolist()[43]),(new_df["Distance"].tolist()[43]), sep='\n')

    for i in range(len(cities)):
        maximums.append(max(parameter[i]))

    best_value = min(maximums)
    index = 0

    for value in maximums:
        if value == best_value:
            best_city = (index, value)
            break
        index += 1
    print(cities[best_city[0]])
    return best_city


def choose_city(city_list: list):
    city_list = {k: v for k, v in enumerate(city_list)}

    correct = False
    while not correct:
        graph_type = input("Would you like to analyze distances (Km) or duration (min)? ").strip().lower()
        if graph_type == "distances" or graph_type == "km":
            graph_type = True
            correct = True
        elif graph_type == "duration" or graph_type == "min":
            graph_type = False
            correct = True
    print("choose city type path: ", graph_type)

    correct = False
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
    return (index, city_name, graph_type)


def graph_italy(filename="weights.json"):
    list_cities = list_comuni()
    if not os.path.isfile(filename):
        now = datetime.datetime.now()
        print("Starting now...")
        compute_weights(cities=list_cities, filename="weights")
        print(f"Ho impiegato {datetime.datetime.now() - now} per eseguire {len(list_cities)} confronti")

    new_df = pd.read_json(filename)
    cities = new_df["city"].tolist()
    minutes = new_df["Minutes"].tolist()
    path = new_df["Distance"].tolist()

    index, city_name, graph_type = choose_city(cities)
    best_source_index, value = best_source(graph_type)

    print(best_source_index, value)

    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, max_zoom=7, zoom_start=5.8,
                   zoom_control=True, min_lat=36, max_lat=47, min_lon=9.5, max_lon=15.5, max_bounds=True)

    if graph_type is True:
        parameter = path[index]
    else:
        parameter = minutes[index]

    console = Console()
    tasks = [f"Circle {n}" for n in range(len(cities))]

    with console.status("[bold green]Working on tasks...") as status:
        while tasks:
            task = tasks.pop(0)
            time.sleep(.05)
            console.log(f"{task} inserted")

    for i in range(len(cities)):
        if city_name == cities[i]:
            folium.Circle(
                location=(search_comune(cities[i])[1], search_comune(cities[i])[0]),
                popup=f"{cities[i]}\nSource",
                radius=7500,
                color="crimson",
                fill=True,
                fill_color="crimson"
            ).add_to(m)
        elif parameter[i] >= max(parameter):
            folium.Circle(
                location=(search_comune(cities[i])[1], search_comune(cities[i])[0]),
                popup=f"{cities[i]}\n{path[index][i]}Km\n{minutes[index][i]}min",
                radius=parameter[i] * 20,
                color="purple",
                fill=True,
                fill_color="purple"
            ).add_to(m)
        elif i == best_source_index:
            folium.Circle(
                location=(search_comune(cities[i])[1], search_comune(cities[i])[0]),
                popup=f"{cities[i]}\n{path[index][i]}Km\n{minutes[index][i]}min",
                radius=parameter[i] * 20,
                color="blue",
                fill=True,
                fill_color="blue"
            ).add_to(m)
        else:
            folium.Circle(
                location=(search_comune(cities[i])[1], search_comune(cities[i])[0]),
                popup=f"{cities[i]}\n{path[index][i]}Km\n{minutes[index][i]}min",
                radius=parameter[i] * 20,
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
    return os.path.abspath(f"result{os.sep}italy.html")


########################################################################################################################
def weights(filename: str = "matrix_weights"):
    my_df = pd.read_json(f"data{os.sep}comuni.json")
    my_df["comune"] = my_df["comune"].str.lower()
    comuni = my_df["comune"].unique().tolist()
    matrix = list()
    matrix_name = list()
    # creazione matrice
    for row in range(len(comuni)):
        weights = list()
        weights_name = list()
        known, city_w = conneceted(comuni[row])
        for cols in range(len(comuni)):
            if comuni[cols].lower() in map(str.lower, known):
                weights.append(city_w[cols])
                weights_name.append(comuni[cols])

            else:
                weights.append(math.inf)
                weights_name.append(math.inf)
        matrix.append(weights)
        matrix_name.append(weights_name)
    # print(matrix)
    file = open(f"data{os.sep}{filename}.txt", 'w', encoding="utf-8")
    file.write(str(matrix))
    file.close()
    file = open(f"data{os.sep}{filename}_name.txt", 'w', encoding="utf-8")
    file.write(str(matrix_name))
    file.close()
    return matrix


def conneceted(comune: str):
    comune = comune.lower()
    known = list()
    check1 = check2 = False

    weights = pd.read_json(f"data{os.sep}weights.json")
    weights["city"] = weights["city"].str.lower()
    city_weight = weights[weights["city"]==comune]["Minutes"].values[0]


    cities = pd.read_json(f"data{os.sep}comuni.json")
    cities["comune"] = cities["comune"].str.lower()

    f_final= open(f"data{os.sep}final.json", 'r', encoding='UTF-8')
    final = json.load(f_final)
    f_final.close()

    livels = pd.read_json(f"data{os.sep}capoluoghi_provincia.json")
    first_liv = list(livels)
    if comune in map(str.lower, first_liv):
        known += first_liv
        check1 = True

    #if comune in livels["Firenze"]["capoluoghi_provincia"]
    for cap_reg in first_liv:
        if comune in map(str.lower, livels[cap_reg]["capoluoghi_provincia"]):
            known += livels[cap_reg]["capoluoghi_provincia"]
            check2 = True
            if check1:
                l = [item.lower() for item in known]
                i = l.index(comune)
                known.pop(i)


    siglaProvincia = cities[cities["comune"] == comune]["sigla_provincia"].values[0]
    regione = cities[cities["comune"] == comune]["regione"].values[0]
    cap_reg = list(final[regione].keys())[0]
    known += final[regione][cap_reg][siglaProvincia] #Città all'interno di quella provincia
    if cap_reg not in known:
        known.append(cap_reg)
    if check2:
        l = [item.lower() for item in known]
        i = l.index(comune)
        known.pop(i)

    return known, city_weight

"""def conneceted(comune: str):
    comune = comune.lower()
    known = list()
    check1 = check2 = False

    weights = pd.read_json(f"data{os.sep}weights.json")
    weights["city"] = weights["city"].str.lower()
    city_weight = weights[weights["city"] == comune]["Minutes"].values[0]

    cities = pd.read_json(f"data{os.sep}comuni.json")
    cities["comune"] = cities["comune"].str.lower()

    f_final = open(f"data{os.sep}final.json", 'r', encoding='UTF-8')
    final = json.load(f_final)
    f_final.close()

    livels = pd.read_json(f"data{os.sep}capoluoghi_provincia.json")
    first_liv = list(livels)
    if comune in map(str.lower, first_liv):
        known += first_liv
        check1 = True

    # if comune in livels["Firenze"]["capoluoghi_provincia"]
    for cap_reg in first_liv:
        if comune in map(str.lower, livels[cap_reg]["capoluoghi_provincia"]):
            known += livels[cap_reg]["capoluoghi_provincia"]
            check2 = True
            # if check1:
            #    l = [item.lower() for item in known]
            #    i = l.index(comune)
            #    known.pop(i)

    if not check1 and not check2:
        siglaProvincia = cities[cities["comune"] == comune]["sigla_provincia"].values[0]
        regione = cities[cities["comune"] == comune]["regione"].values[0]
        cap_reg = list(final[regione].keys())[0]
        known += final[regione][cap_reg][siglaProvincia]
        if cap_reg not in known:
            known.append(cap_reg)

    return known, city_weight"""


def main():
    download_needed_file()
    #weights()

if __name__ == "__main__":
    main()