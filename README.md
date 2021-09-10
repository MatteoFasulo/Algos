# Algoritmi e Strutture Dati
## University Project
Progetto di Algoritmi e Strutture Dati

### Description
L'implementazione prevede due differenti modelli. Il primo modello assume che tutti i comuni (nodi) siano fortemente connessi tra loro con distanza (peso) pari al numero di Km che li separa considerando la formula dell'emisenoverso [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula). Il secondo modello prevede che solo i capoluoghi regionali (nodi) siano fortemente connessi tra loro; a partire da ogni capoluogo regionale è possibile arrivare ai capoluoghi di provincia e successivamente ai comuni (se esistenti) ma la connessione tra province e capoluoghi di altre regioni non è diretta; il peso è calcolato mediante la [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula).

### Features
Rappresentazione tramite formato .html di una cartina geografica dell'Italia di tutti i nodi compreso il sorgente e il più distante in Km o minuti. Il raggio di ogni nodo è proporzionale alla distanza in Km. Nel 1° e 2° modello viene inoltre computato il miglior comune sorgente che minimizza le distanze da qualunque altro nodo.
> **Tip:** Nei modelli è possibile tramite un **menù** scegliere se visualizzare tutti i **comuni**, solo **capoluoghi** di provincia o di regione.

### Map Example
[Modello 1](https://matteofasulo.github.io/Algos/result/first_model.html)
[Modello 2](https://matteofasulo.github.io/Algos/result/second_model.html)

### Datasets
- Il dataset contenente le informazioni sulle ASL ed i comuni di riferimento è disponibile all'[indirizzo](https://www.salute.gov.it/portale/documentazione/p6_2_8_1_1.jsp?lingua=italiano&id=16)
- Le coordinate geografiche di ogni comune sono reperite tramite Open Street Map API

### Errori noti
I dataset riportati sono stati in parte modificati manualmente per permettere all'API di Open Street Map di identificare, a partire dal nome del comune, le coordinate di latitudine e longitudine. I dataset ottimizzati sono reperibili nella cartella "data".


### Libraries

| Name | Description |
| ------------- | ------------------------------ |
| [Numpy] | package for scientific computing with Python.
| [Pandas]| fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.
| [Folium]| folium builds on the data wrangling strengths of the Python ecosystem and the mapping strengths of the Leaflet.js library.
| [Webbrowser]| provides a high-level interface to allow displaying Web-based documents to users..
| [Os]| this module provides a portable way of using operating system dependent functionality.
| [Json]| the json library can parse JSON from strings or files.
| [Time]| this module provides various time-related functions.
| [Datetime]| the datetime module supplies classes for manipulating dates and times.
|[Googlemaps]| the Python Client for Google Maps Services is a Python Client library for the following Google Maps APIs.


---
### Dependencies
- [Python 3.9.X]
---
### Installation:
```
$ pip install -r requirements.txt
```
----
### Execution:

```
$ python main.py
```
----
Le possibili scelte dal menù riguardano la visualizzazione (compreso anche il calcolo) del 1° modello e la sola visualizzazione del 2° modello (per motivi strettamente legati alla realizzazione del secondo modello).

### Functions:                
         
| Function                   | Description                    |
| -------------------------- | ------------------------------ |
| `def main()`                       |Gestione del menù con relative scelte e riassunto delle performance|
| `def mk_title()`              |Funzione di utilità per interfaccia CLI|
| `def handle_int(numberOfChoiches)`             |Gestione delle scelte da raw_input dell'utente|
| `def clear()`                 |CLI clearer in base all'OS|
| `def download_comuni()`                     |Retrieve dei dataset da github|
| `def list_comuni()`               |Util per lista delle città nei dataset|
| `def search_comune(comune)`             |Retrieve di latitudine e longitudine a partire dal nome del comune|
| `def cap_regione()`             |lista cap. di regione|
| `def cap_provincia()`             |lista cap. di provincia|
| `def give_comuni()`             |lista dei comuni senza capoluoghi di provincia e regione|
| `def graph_italy()`             |Mappa di Folium con visualizzazione di capoluoghi e comuni compresa la possibilità di deselezionare o selezionare cosa visualizzare. E' possibile inoltre notare il comune rosso (sorgente scelta) e il miglior comune (quello che minimizza le distanze in KM da ogni altro comune sulla mappa (in blu))|
| `def best_source(list_cities, weights)`             |Calcola il miglior comune (in blu) sulla mappa (quello che minimizza le distanze in KM da ogni altro comune)|
| `def matrix*`             |Insieme delle funzioni che gestiscono la matrice di distanze calcolata attraverso la formula dell'emisenoverso|
| `def shortest_path(algorithm: str, matrix, one_way: bool = False, index: int = 0) -> np.ndarray`             |Funzione che attraverso Scipy calcola il tempo di esecuzione in CPython di più noti algoritmi come Dijkstra, Bellman-Ford e Johnson|
| `def subs()`             |La funzione di subsetting della matrice è stata omessa in quanto ritenuta secondaria rispetto ai modelli presentati|
| `def execution_time()`             |Calcolo del tempo di esecuzione e generazione del file CSV con il tempo necessario. Sono stati eseguiti 3 test per ogni Algoritmo e per ogni subset della matrice originaria|
| `def calculate_distance(lon1, lat1, lon2, lat2, R=6373.0)`                     |Date le posizioni di lat e long di due comuni, la funzione calcola la loro distanza attraverso la Haversine Formula|
----
### Considerazioni:

Essendo un modello basato su una distanza "aerea" è chiaro che il miglior comune sarà quello più "centrale" tra tutti i comuni. Ciononostante vista la grande quantità di comuni con ASL al Sud, il "miglior" comune si trova nel Centro-Sud.

[Python 3.9.X]: <https://www.python.org/downloads/>
[time]: <http://robyp.x10host.com/3/time.html#loaded>
[datetime]: <https://docs.python.org/3/library/datetime.html> 
[os]: <https://docs.python.org/3.8/library/os.html>
[json]: <https://docs.python.org/3.8/library/json.html>
[Numpy]: <https://numpy.org/install/>
[Pandas]: <https://pandas.pydata.org/>
[Folium]: <https://python-visualization.github.io/folium/>
[Webbrowser]: <https://docs.python.org/3/library/webbrowser.html>
[googlemaps]: <https://pypi.org/project/googlemaps/>
