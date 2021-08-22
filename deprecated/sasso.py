import pandas as pd
import os, json


import pandas as pd
import os


def cap_regione():
    list_cap_regione = list()
    f_cap = open(f"data{os.sep}capoluoghi_regione.json", 'r', encoding='UTF-8')
    df = json.load(f_cap)
    f_cap.close()

    for key in df.keys():
        list_cap_regione.append(df[key]["comune"])

    return list_cap_regione


def nodes():
    list_cap_provincia = cap_regione()
    f_cap = open(f"data{os.sep}capoluoghi_provincia.json", 'r', encoding='UTF-8')
    df = json.load(f_cap)
    f_cap.close()

    for key in df.keys():
        for city in df[key]["capoluoghi_provincia"]:
            if city not in list_cap_provincia:
                list_cap_provincia.append(city)
    list_cap_provincia.sort()
    return list_cap_provincia


def indexed_cities():
    geo_final = pd.read_json(f"data{os.sep}geo_final.json")

    name_cities = geo_final["comune"].tolist()
    indexed = dict()
    ## Creo l'indice di tutti i comuni
    for i in range(len(name_cities)):
        if name_cities[i] not in indexed.keys():
            indexed[name_cities[i]] = i
    return indexed

def cities_subs(newLen: int):
    """
    Data una matrice e un intero resituisce un subset con tutte le città principali (capoluoghi provincia e regione)
    della dimensione dell'intero.
    """
    geo_final = pd.read_json(f"data{os.sep}geo_final.json")

    name_cities = geo_final["comune"].tolist()
    indexed = dict()
    ## Creo l'indice di tutti i comuni
    for i in range(len(name_cities)):
        if name_cities[i] not in indexed.keys():
            indexed[name_cities[i]] = i

    del name_cities

    name_cities = geo_final["comune"][0:newLen].unique().tolist()

    name_cap_provincia = nodes()
    ## Controllo che ci siano tutti i capoluoghi di provincia
    ## Se non ci sono li aggiungo alla lista e la riordino
    for city in name_cap_provincia:
        #if city.lower() not in map(str.lower, name_cities):
        if city not in name_cities:
            name_cities.append(city)
    name_cities = sorted(name_cities, key=str.lower)

    cities2 = pd.Series(name_cities).unique()
    print(f"{len(name_cities) = }, {len(cities2) = }")

    ##  Creo la lista di tuple, (nome_città, indice)
    cities = list()
    for city in name_cities:
        cities.append((city,indexed[city]))
    
    del name_cities

    offset = len(cities) - newLen
    #print(f"{offset = }")
    
    if offset != 0:
        c_deleted = 0
        for i in range(len(cities)-1,0,-1):
            if cities[i][0] not in name_cap_provincia and c_deleted < offset:
                #print(cities[i])
                c_deleted += 1
                cities.remove(cities[i])
        #offset = len(cities) - newLen
        #print(f"{offset = }")

    return cities


def save_json(obj, filename: str):
    js_file = open(filename, 'w', encoding="utf-8")
    json.dump(obj=obj, fp=js_file, indent=2)
    js_file.close()


def matrix_sub(cities):
    f = open(f"data{os.sep}matrix_weights.json", 'r', encoding='utf-8')
    matrix_weights = json.load(f)
    f.close()
    indexes = [int(x[1]) for x in cities]

    print(f"{len(matrix_weights) = }, {len(indexes) = }")
    new_m = list()

    for i in range(len(matrix_weights)):
        if i in indexes:
            row = list()
            for j in range(len(matrix_weights[i])):
                if j in indexes:
                    row.append(matrix_weights[i][j])
            new_m.append(row)
            print(f"{round(100/len(matrix_weights)*(i+1),2)}%")

    return new_m

#nodes()
t = cities_subs(5000)
print(len(t))
save_json(matrix_sub(t),"squared_5000.json")


#print(f"{len(indexed_cities()) = }\n{indexed_cities()['Roma'] = }")
#####################################################
def duplicati():
    df = pd.read_json(f"data{os.sep}geo_final.json")
    unique = df["comune"].unique().tolist()

    list_y = df["comune"].tolist()
    del df
    for y in unique:
        list_y.remove(y)
    del unique
    list_y = sorted(list_y, key=str.lower)
    print(f"{list_y = }")
######################################################