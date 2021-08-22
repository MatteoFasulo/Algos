import os
import datetime
import threading
import time
import urllib.request
import urllib.error
from statistics import mean

import numpy as np
import pandas as pd
import folium
import googlemaps
import polyline
from rich.console import Console
from folium import plugins

#######################################################
GOOGLE_API = "AIzaSyCne109pBSAhpB2rg6SlsdqIP6q5bsbp18"
comuni = f"data{os.sep}comuni.json"
gmaps = googlemaps.Client(key=GOOGLE_API, retry_over_query_limit=False)
#######################################################

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


def compute_weights(cities: list, filename: str, traffic_model="best_guess", night_time=datetime.datetime(2022, 1, 1, 4, 0, 0, 0)):

    if datetime.datetime.now() >= night_time:
        night_time = datetime.datetime.now() + datetime.timedelta(days=2)
        compute_weights(cities, filename, traffic_model, night_time)

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
                                           traffic_model=traffic_model)["rows"][0]["elements"][0]
            # print(result)
            time = round((result["duration"]["value"]) / 60)
            result = round((result["distance"]["value"]) / 1000)
            time_needed.append(time)
            distances.append(result)
            origins.clear()
            destination.clear()
            # print(result)
        weights_df['Distance'][i] = distances[::]
        weights_df['Minutes'][i] = time_needed[::]

    with open(f"{filename}.json", 'w', encoding='utf-8') as file:
        weights_df.to_json(file, force_ascii=False, indent=2)

    return


def best_source(graph_type: bool):
    new_df = pd.read_json(f"data{os.sep}weights.json")
    cities = new_df["city"].tolist()
    maximums = []
    best_city = None

    # print(graph_type)
    if graph_type is True:
        # print("KM")
        parameter = new_df["Distance"].tolist()
    else:
        # print("MIN")
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
    # print("choose city type path: ", graph_type)

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


def threaded_tasks(list_cities: list):
    console = Console()
    tasks = [f"{n} ~ " for n in range(len(list_cities))]
    with console.status("[bold green]Calculating directions...") as status:
        i = 0
        while tasks:
            task = tasks.pop(0)
            time.sleep(0.11)
            console.log(f"{task}{list_cities[i]}")
            i += 1


def graph_italy(filename=f"data{os.sep}weights.json"):
    past = datetime.datetime.now()
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

    # print(best_source_index, value)

    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, zoom_start=5.8,
                   zoom_control=True, min_lat=33, max_lat=50, min_lon=9.5, max_lon=15.5, max_bounds=False)

    if graph_type is True:
        parameter = path[index]
    else:
        parameter = minutes[index]

    thread = threading.Thread(target=threaded_tasks, args=(list_cities,))
    thread.start()

    # print(decoded)
    f1 = folium.FeatureGroup(f"{city_name}")

    for i in range(len(cities)):
        directions_result = gmaps.directions(city_name,
                                             cities[i],
                                             mode="driving",
                                             units="metric",
                                             region="IT")
        linea = directions_result[0]
        linea = linea.get("overview_polyline")
        linea = linea.get("points")
        decoded = polyline.decode(linea)  # TODO update README WITH polyline

        folium.vector_layers.PolyLine(decoded, popup=f'<b>{city_name} ~ {cities[i]}</b>',
                                      tooltip=f'{city_name} ~ {cities[i]}',
                                      color='black', weight=1).add_to(f1)
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
                radius=parameter[i] * 10,
                color="purple",
                fill=True,
                fill_color="purple"
            ).add_to(m)
        elif i == best_source_index:
            folium.Circle(
                location=(search_comune(cities[i])[1], search_comune(cities[i])[0]),
                popup=f"{cities[i]}\n{path[index][i]}Km\n{minutes[index][i]}min",
                radius=parameter[i] * 10,
                color="blue",
                fill=True,
                fill_color="blue"
            ).add_to(m)
        else:
            folium.Circle(
                location=(search_comune(cities[i])[1], search_comune(cities[i])[0]),
                popup=f"{cities[i]}\n{path[index][i]}Km\n{minutes[index][i]}min",
                radius=parameter[i] * 10,
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
    f1.add_to(m)
    folium.LayerControl().add_to(m)
    if not os.path.isdir("result"):
        os.mkdir("result")
    m.save(os.path.join("result", "second_model.html"))
    return (os.path.abspath(f"result{os.sep}second_model.html"), datetime.datetime.now() - past)


def main():
    path, time_needed = graph_italy()
    return path, time_needed
