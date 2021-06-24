from googlemaps import client
import numpy as np
from numpy.matrixlib.defmatrix import matrix
import pandas as pd
import googlemaps
import json
import os
from time import sleep
import math, datetime
from random import randint

GOOGLE_API = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
gmaps = googlemaps.Client(key=GOOGLE_API)


def make_italy_geo(cities: list, filename: str=f"data{os.sep}comuni.json"):
    """
    Crea un database in un file json a partire da una lista di città italiane.
    Il database ha i seguenti campi:
    - comune
    - sigla_provincia
    - provincia
    - regione
    - lng
    - lat
    """
    print("[i] Making geo!")
    cities.sort()
    notFoundl = list()
    js = list()
    for i in range(len(cities)):
        sleep(randint(50,450)/150)
        if i%200 == 0:
            print(i,cities[i], end=" ")
        js_dict = dict()
        esiste = False
        try:
            geocode_result = gmaps.geocode(cities[i]+', italy', region="IT", language="IT")[0]
            esiste = True
        except IndexError:
            print("Non esiste", end="")
            notFoundl.append((i,cities[i]))

        print()
        if esiste:
            #print(geocode_result)
            for i in range(len(geocode_result["address_components"])):
                if geocode_result["address_components"][i]["types"][0] == "administrative_area_level_1":
                    js_dict["regione"] = geocode_result["address_components"][i]["long_name"]

                elif geocode_result["address_components"][i]["types"][0] == "locality" or geocode_result["address_components"][i]["types"][0] == "administrative_area_level_3":
                    js_dict["comune"] = geocode_result["address_components"][i]["short_name"]

                elif geocode_result["address_components"][i]["types"][0] == "administrative_area_level_2":
                    js_dict["sigla_provincia"] = geocode_result["address_components"][i]["short_name"]
                    js_dict["provincia"] = geocode_result["address_components"][i]["long_name"]
                    if js_dict["provincia"][:13].lower() == "Provincia di ".lower():
                        js_dict["provincia"] = js_dict["provincia"][13:]
                    elif js_dict["provincia"][:23].lower() == 'Città Metropolitana di '.lower():
                        js_dict["provincia"] = js_dict["provincia"][23:]
                    elif js_dict["provincia"][:14].lower() == "Provincia del ".lower():
                        js_dict["provincia"] = js_dict["provincia"][14:]

            lat, lng = geocode_result["geometry"]["location"]["lat"], geocode_result["geometry"]["location"]["lng"]
            js_dict["lng"] = lng
            js_dict["lat"] = lat
            js.append(js_dict)
    js_file = open(filename, 'w', encoding="utf-8")
    json.dump(obj=js, fp=js_file, indent=2)
    js_file.close()
    print(notFoundl)
    print("[i] Done!")


def make_capoluoghi_regionali(db_input: str=f"data{os.sep}comuni_geo final.json", filename: str=f"data{os.sep}capoluoghi_regione.json"):
    """
    Funzione che preso in ingresso il database generato con make_italy_geo restituisce il database dei soli comuni che sono anche capoluoghi regionali.
    Il database ha i seguenti campi per ogni regione:
    - comune
    - sigla_provincia
    - lng
    - lat
    """
    my_df = pd.read_json(db_input)
    regioni = my_df["regione"].unique().tolist()
    regioni.sort()
    comuni = my_df["comune"].unique().tolist()
    capoluoghi_regionali = dict()

    for regione in regioni:
        capoluogo_regionale = input(f"Inserisci il capoluogo della regione {regione}: ").strip()
        while capoluogo_regionale not in comuni:
            capoluogo_regionale = input(f"Inserisci il capoluogo della regione {regione}: ").strip()
        comuni.remove(capoluogo_regionale)
        capoluoghi_regionali[regione] = dict()
        capoluoghi_regionali[regione]["comune"] = capoluogo_regionale
        capoluoghi_regionali[regione]["sigla_provincia"] = my_df[my_df["comune"] == capoluogo_regionale]["sigla_provincia"].values[0]
        capoluoghi_regionali[regione]["lng"] = np.float64(my_df[my_df["comune"] == capoluogo_regionale]["lng"].values[0]).item()
        capoluoghi_regionali[regione]["lat"] = np.float64(my_df[my_df["comune"] == capoluogo_regionale]["lat"].values[0]).item()

    js_file = open(filename, 'w', encoding="utf-8")
    json.dump(obj=capoluoghi_regionali, fp=js_file, indent=2)
    js_file.close()


def make_capoluoghi_provincia(db_input: str=f"data{os.sep}comuni_geo final.json", db_capoluoghi: str=f"data{os.sep}capoluoghi_regione.json", filename: str=f"data{os.sep}capoluoghi_provincia-t.json"):
    """
    Funzione che preso in ingresso il database generato con make_italy_geo e il database dei capoluoghi,
    restituisce il database dei soli comuni che sono anche capoluoghi regionali.
    Il database ha i seguenti campi per ogni capoluogo di regione:
    - comune
    - sigla_provincia
    """
    f_capoluoghi_regionali = open(db_capoluoghi, 'r', encoding='UTF-8')
    capoluoghi_regionali = json.load(f_capoluoghi_regionali)
    f_capoluoghi_regionali.close()
    my_df = pd.read_json(db_input)
    regioni = my_df["regione"].unique().tolist()
    regioni.sort()
    capoluoghi_provincia = dict()

    for regione in regioni:
        province = my_df[my_df["regione"] == regione]["comune"].unique().tolist()
        province.sort()
        sigla_province = my_df[my_df["regione"] == regione]["sigla_provincia"].unique().tolist()
        sigla_province.sort()
        capoluoghi_provincia[capoluoghi_regionali[regione]["comune"]] = dict()
        if len(province)==len(sigla_province):
            capoluoghi_provincia[capoluoghi_regionali[regione]["comune"]]["capoluoghi_provincia"] = province
        else:
            while len(province)!=len(sigla_province):
                print(province, sigla_province, sep='\n')
                comune = input("Quale comune non è una capoluogo di provincia? ")
                try:
                    province.remove(comune)
                except ValueError:
                    pass
            capoluoghi_provincia[capoluoghi_regionali[regione]["comune"]]["capoluoghi_provincia"] = province
        capoluoghi_provincia[capoluoghi_regionali[regione]["comune"]]["sigla_province"] = sigla_province

    js_file = open(filename, 'w', encoding="utf-8")
    json.dump(obj=capoluoghi_provincia, fp=js_file, indent=2)
    js_file.close()


def make_final():
    """
    Database che ricrea la gerarchia dei livelli del grafo in un file json:
    la struttura è:
    chiave  - chiave            - chiave            - lista valori
    regione - capoluogo regione - sigla provincia   - comuni    (in quella provincia)
    """
    f_capoluoghi_regionali = open(f"data{os.sep}capoluoghi_regione.json", 'r', encoding='UTF-8')
    capoluoghi_regionali = json.load(f_capoluoghi_regionali)
    f_capoluoghi_regionali.close()

    f_capoluoghi_provincia = open(f"data{os.sep}capoluoghi_provincia.json", 'r', encoding='UTF-8')
    capoluoghi_provincia = json.load(f_capoluoghi_provincia)
    f_capoluoghi_provincia.close()

    my_df = pd.read_json(f"data{os.sep}geo_final.json")

    diz = dict()

    for regione in capoluoghi_regionali.keys():
        diz[regione] = dict()
        capol_regione = capoluoghi_regionali[regione]["comune"] 
        diz[regione][capol_regione] = dict()
        sigla_province = capoluoghi_provincia[capol_regione]["sigla_province"]
        for sigla in sigla_province:
            comuni_in_provincia = my_df[my_df["sigla_provincia"]==sigla]["comune"].unique().tolist()
            diz[regione][capol_regione][sigla] = comuni_in_provincia


    js_file = open(f"data{os.sep}final01.json", 'w', encoding="utf-8")
    json.dump(obj=diz, fp=js_file, indent=2)
    js_file.close()


def weights(filename: str ="matrix_weights"):
    my_df = pd.read_json(f"data{os.sep}geo_final.json")
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
    #print(matrix)
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


    cities = pd.read_json(f"data{os.sep}geo_final.json")
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



def search_comune(comune: str):
    geo = pd.read_json(f"data{os.sep}geo_final.json")
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
    print("COMPUTE START!")

    latitudes = []
    longitudes = []
    origins = []
    destination = []
    distances = []
    time_needed = []

    for comune in cities:
        long, lat = search_comune(comune)
        latitudes.append(lat)
        longitudes.append(long)

    weights_df = pd.DataFrame(data={"city": cities, "lat": latitudes, "long": longitudes})
    weights_df['Distance'] = list
    weights_df['Minutes'] = list

    now = datetime.datetime.now()
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

            sleep((randint(50,900)/300))
            result = gmaps.distance_matrix(origins, destination, mode='driving', departure_time=night_time,
                                           traffic_model=traffic_model)["rows"][0]["elements"][0]
            # print(result)
            time = round((result["duration"]["value"]) / 60)
            result = round((result["distance"]["value"]) / 1000)
            time_needed.append(time)
            distances.append(result)
            origins.clear()
            destination.clear()
        print(f"{round(100/len(cities)*(i+1),2)}%")
        weights_df['Distance'][i] = distances[::]
        weights_df['Minutes'][i] = time_needed[::]
    print(f"Tempo: {datetime.datetime.now()-now}\nSalvo...")
    now = datetime.datetime.now()
    with open(f"{filename}.json", 'w', encoding='utf-8') as file:
        weights_df.to_json(file, force_ascii=False, indent=4)
    print(f"Tempo: {datetime.datetime.now()-now}")
    return
    


if __name__ == "__main__":
    #weights()
    #partenza = pd.read_excel(f"data{os.sep}C_17_bancheDati_13_0_0_file.xls")
    #province = pd.read_csv(f"data{os.sep}province.csv")
    
    #df = pd.read_csv("C_17_dataset_3_0_upFile.csv", sep=";", error_bad_lines=False, encoding = "ISO-8859-1")  # todo add download from git
    #df["COMUNE"] = df["COMUNE"].str.strip()
    #comuni = df["COMUNE"].tolist()
    #comuni.sort()
    #make_italy_geo(comuni, f"data{os.sep}geo_final.json")

    my_df = pd.read_json(f"data{os.sep}geo_final.json")
    comuni = my_df["comune"].tolist()
    #comuni = comuni[:11]
    compute_weights(comuni, "weights_2.0")
    #regioni = my_df["regione"].unique().tolist()
    #make_capoluoghi_regionali()
    #make_capoluoghi_provincia()
    #make_comuni_provincia()
    
