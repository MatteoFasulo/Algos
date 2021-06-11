import os
import numpy as np
import pandas as pd
import folium
import time
import urllib.request
import urllib.error
from folium import plugins
from distance import calculate_distance

##############################################
comuni = f"data{os.sep}comuni.json"


##############################################

def download_comuni(filename="comuni.json"):
    url = "https://raw.githubusercontent.com/MatteoFasulo/Algos/main/data/comuni.json"
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
                correct = True
            else:
                print("\n[!] Not found\n", city_list, sep='')
    # print(f"{index}, {city_name}")
    return (index, city_name, city_list)


def graph_italy():
    list_cities = list_comuni()
    index, city_name, list_cities = choose_city(list_cities)
    source_lat, source_long = (float(search_comune(city_name)[1]), float(search_comune(city_name)[0]))

    longest_path = [max(calculate_distance(source_long, source_lat, float(search_comune(list_cities[i])[0]), float(search_comune(list_cities[i])[1])) for i in range(len(list_cities)))]

    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, max_zoom=7, zoom_start=5.8,
                   zoom_control=True, min_lat=36, max_lat=47, min_lon=9.5, max_lon=15.5, max_bounds=True)

    best_source_index, value = best_source()

    """thread = threading.Thread(target=threaded_tasks, args=(list_cities,))
    thread.start()"""

    for i in range(len(list_cities)):
        distance = calculate_distance(source_long, source_lat, float(search_comune(list_cities[i])[0]),
                                      float(search_comune(list_cities[i])[1]))
        if city_name == list_cities[i]:
            folium.Circle(
                location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                popup=list_cities[i],
                radius=7500,
                color="crimson",
                fill=True,
                fill_color="crimson"
            ).add_to(m)
        elif i == best_source_index:
            folium.Circle(
                location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                popup=f"{list_cities[i]}\n{distance}Km",
                radius=distance * 10,
                color="blue",
                fill=True,
                fill_color="blue"
            ).add_to(m)
        elif distance >= longest_path[0]:
            folium.Circle(
                location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                popup=f"{list_cities[i]}\n{distance}Km",
                radius=distance * 10,
                color="purple",
                fill=True,
                fill_color="purple"
            ).add_to(m)
        else:
            folium.Circle(
                location=(search_comune(list_cities[i])[1], search_comune(list_cities[i])[0]),
                popup=f"{list_cities[i]}\n{distance}Km",
                radius=distance * 10,
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
    m.save(os.path.join("result", "first_model.html"))
    return os.path.abspath(f"result{os.sep}first_model.html")


def best_source():
    weights = list()
    comuni = list_comuni()
    for comune_sorgente in comuni:
        temp = list()
        source_lat, source_long = (float(search_comune(comune_sorgente)[1]), float(search_comune(comune_sorgente)[0]))
        for comune_destinazione in comuni:
            dest_lat, dest_long = (
                float(search_comune(comune_destinazione)[1]), float(search_comune(comune_destinazione)[0]))
            distance = calculate_distance(source_long, source_lat, dest_long, dest_lat)
            temp.append(distance)
        weights.append(temp)

    new_df = pd.read_json("weights_1stModel.json")
    cities = new_df["city"].tolist()
    maximums = []
    best_city = None

    # print((new_df["Minutes"].tolist()[43]),(new_df["Distance"].tolist()[43]), sep='\n')

    for i in range(len(cities)):
        maximums.append(max(weights[i]))

    best_value = min(maximums)
    index = 0

    for value in maximums:
        if value == best_value:
            best_city = (index, value)
            break
        index += 1
    print(cities[best_city[0]])
    return best_city


def main():
    path = graph_italy()
    return path
