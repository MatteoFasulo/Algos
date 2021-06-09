# Algoritmi e Strutture Dati
Progetto di Algoritmi e Strutture Dati

### Description
L'implementazione prevede tre differenti modelli. Il primo modello assume che tutti i comuni (nodi) siano fortemente connessi tra loro con distanza (peso) pari al numero di Km che li separa considerando la formula dell'emisenoverso [Haversine formula]("https://en.wikipedia.org/wiki/Haversine_formula"). Il secondo modello è una versione migliorata del primo che assume che tutti i comuni (nodi) siano fortemente connessi tra loro con distanza (peso) pari al numero di Km che li separa o pari al tempo impiegato a raggiungerlo; utilizza l'API di Google Maps per calcolare distanza e tempo di percorrenza. Il terzo modello prevede che solo i capoluoghi regionali (nodi) siano fortemente connessi tra loro; a partire da ogni capoluogo regionale è possibile arrivare ai capoluoghi di provincia e successivamente ai comuni (se esistenti) ma la connessione tra province e capoluoghi di altre regioni non è diretta; viene calcolata distanza e tempo di percorrenza tramite API di Google Maps.

### Features
Rappresentazione tramite formato .html di una cartina geografica dell'Italia di tutti i nodi compreso il sorgente (rosso) e il più distante (viola, in Km o minuti). Il raggio di ogni nodo è proporzionale alla distanza in Km (1° modello) o minuti dalla sorgente (2° modello). Nel 1° e 2° modello viene inoltre calcolato il miglior comune sorgente (in blu) che minimizza le distanze o i tempi di percorrenza da qualunque altro nodo. Il 3° modello identifica sia il miglior capoluogo di regione da cui partire che la miglior provincia per ogni capoluogo da cui partire. 

### Datasets
- Il dataset contenente le informazioni sulle ASL ed i comuni di riferimento è disponibile all'[indirizzo](https://www.salute.gov.it/portale/documentazione/p6_2_8_1_1.jsp?id=13)
- Le coordinate geografiche di ogni comune sono state reperite nel [repository](https://github.com/MatteoHenryChinaski/Comuni-Italiani-2018-Sql-Json-excel)

### Errori noti
I dataset riportati sono stati in parte modificati manualmente per permettere all'API di Google Maps di identificare, a partire dal nome del comune, le coordinate di latitudine e longitudine. I dataset ottimizzati sono reperibili nella cartella "data".


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
- [Numpy]
- [Folium]
- [Pandas]
- [Googlemaps]
---
### PIP

```
$ pip install numpy
$ pip install pandas
$ pip install folium
$ pip install googlemaps
$ pip install rich
$ pip install googlemaps
$ pip install polyline

```

----
### Anaconda

Note: 

```
$ conda install pandas
$ conda install numpy
```

----

### Functions:                
         
| Function                   | Description                    |
| -------------------------- | ------------------------------ |
| `def main()`                       | ** **|
| `def ()`              |** **|
| `def ()`             | ** **|
| `def ()`                 | ** **|
| `def ()`                     | ** **|
| `def ()`               | ** **|
| `def()`             | ** **|

----

### *End*

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
