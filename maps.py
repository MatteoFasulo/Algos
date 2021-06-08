import datetime
from itertools import tee

import googlemaps
import numpy as np
import pandas as pd

GOOGLE_API = "AIzaSyCne109pBSAhpB2rg6SlsdqIP6q5bsbp18"
capoluoghi = ["L'Aquila", "Potenza", "Catanzaro", "Napoli", "Bologna", "Trieste", "Roma", "Genova", "Milano", "Ancona",
              "Campobasso", "Torino", "Bari", "Cagliari", "Palermo", "Firenze", "Trento", "Perugia", "Aosta",
              "Venezia", "Bolzano"]
latitudes = []
longitudes = []

gmaps = googlemaps.Client(key=GOOGLE_API)


def search_city(comune: str):
    geo = pd.read_json("data/italy_geo.json")
    try:
        comune = comune.lower().strip()
        geo["comune"] = geo["comune"].str.lower()
        lat = geo[geo["comune"] == comune]["lat"].values[0]
        long = geo[geo["comune"] == comune]["lng"].values[0]
        return np.float64(lat).item(), np.float64(long).item()
    except IndexError:
        print(comune, geo[geo["comune"] == comune]["lat"], geo[geo["comune"] == comune]["lng"])


for i in range(len(capoluoghi)):
    lat, long = search_city(capoluoghi[i])
    latitudes.append(lat)
    longitudes.append(long)

new_df = pd.DataFrame(data={"city": capoluoghi, "lat": latitudes, "long": longitudes})
# print(new_df)

origins = []
destination = []
distances = []
time_needed = []

night_time = datetime.datetime(2022, 1, 1, 5, 0, 0, 0)

new_df['Distance'] = list
new_df['Minutes'] = list

for i in range(len(capoluoghi)):
    distances.clear()
    time_needed.clear()
    for j in range(len(capoluoghi)):
        LatOrigin = new_df['lat'][i]
        LongOrigin = new_df['long'][i]
        origins.append((LatOrigin, LongOrigin))
        LatDest = new_df['lat'][j]  # Save value as lat
        LongDest = new_df['long'][j]  # Save value as lat
        destination.append((LatDest, LongDest))
        result = gmaps.distance_matrix(origins, destination, mode='driving', departure_time=night_time, traffic_model="best_guess")["rows"][0]["elements"][0]["distance"]["value"]
        result = round(result/1000)
        distances.append(result)
        time = gmaps.distance_matrix(origins, destination, mode='driving', departure_time=night_time, traffic_model="best_guess")["rows"][0]["elements"][0]["duration"]["value"]
        time = round(time/60)
        time_needed.append(time)
        origins.clear()
        destination.clear()
        print(result)
    new_df['Distance'][i] = distances[::]
    new_df['Minutes'][i] = time_needed[::]

with open('percorsi.json', 'w', encoding='utf-8') as file:
    new_df.to_json(file, force_ascii=False)
