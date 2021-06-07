import numpy as np
import pandas as pd
import folium
import webbrowser
import distance


def clear_dataset():
    df = pd.read_excel("./data/C_17_bancheDati_13_0_0_file.xls")
    print("Clear the dataset to last year (2020)")
    df_clean = df[df["ANNO"] == 2020]
    return df_clean


"""regioni = df_clean["DENOMINAZIONE REGIONE"].unique()
regioni"""


def unique_cities():
    lista_comuni = clear_dataset()["COMUNE"].unique().tolist()
    for i in range(0, len(lista_comuni)):
        lista_comuni[i] = lista_comuni[i].strip()

    index = lista_comuni.index("SAN REMO")  # FIX
    lista_comuni[index] = "sanremo".upper()

    index = lista_comuni.index("SAN DONA' DI PIAVE")  # FIX
    lista_comuni[index] = "san donà di piave".upper()
    return lista_comuni


def search_comune(comune: str):
    geo = pd.read_json("./data/italy_geo.json")
    try:
        comune = comune.lower().strip()
        geo["comune"] = geo["comune"].str.lower()
        lat = geo[geo["comune"] == comune]["lat"].values[0]
        long = geo[geo["comune"] == comune]["lng"].values[0]
        return (long, lat)
    except IndexError:
        print(comune, geo[geo["comune"] == comune]["lat"], geo[geo["comune"] == comune]["lng"])


def fill_coords():
    lista_comuni = unique_cities()
    new_df = pd.DataFrame(np.zeros((len(lista_comuni), len(lista_comuni))), index=lista_comuni, columns=lista_comuni)
    for i in range(len(lista_comuni)):
        for j in range(len(lista_comuni)):
            long1, lat1 = search_comune(lista_comuni[j])
            long2, lat2 = search_comune(lista_comuni[i])
            # print(long1,lat1,long2,lat2)
            new_df[lista_comuni[i]][lista_comuni[j]] = distance.calculate_distance(float(long1), float(lat1),
                                                                                   float(long2), float(lat2))
    return new_df


def save_weights():
    with open('weights.json', 'w', encoding='utf-8') as file:
        fill_coords().to_json(file, force_ascii=False)


def graph_italy():
    lista_comuni = unique_cities()
    m = folium.Map(location=[41.87194, 12.56738], tiles="CartoDB positron", min_zoom=5.8, max_zoom=7, zoom_start=5.8,
                   zoom_control=True, min_lat=36, max_lat=47, min_lon=9.5, max_lon=15.5, max_bounds=True)
    for i in range(len(lista_comuni)):
        folium.Circle(
            location=(search_comune(lista_comuni[i])[1], search_comune(lista_comuni[i])[0]),
            popup=lista_comuni[i],
            radius=15000,
            color="green",
            fill=True,
            fill_color="green"
        ).add_to(m)
    m.save("italy.html")
    webbrowser.open_new_tab("italy.html")
