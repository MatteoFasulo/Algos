# Algoritmi e Strutture Dati
Progetto di Algoritmi e Strutture Dati

### Description
L'implementazione prevede due differenti modelli. Il primo modello assume che tutti i comuni (nodi) siano direttamente connessi tra loro con distanza (peso) pari al numero di Km che li separa, considerando le loro coordinate geografiche e l'asse terrestre medio pari a 6373Km . Il secondo modello prevede che i capoluoghi regionali (nodi) siano direttamente connessi tra loro con le stesse assunzioni sulla distanza del precedente modello; a partire da ogni capoluogo regionale è possibile arrivare ai capoluoghi di provincia e successivamente ai comuni (se esistenti).

### Features
Rappresentazione tramite formato .html di una cartina geografica dell'Italia di tutti i nodi compreso il sorgente e il più distante (in Km). Il raggio di ogni nodo è proporzionale alla distanza in Km dalla sorgente (considerando solo le loro coordinate geografiche).

### Datasets
- Il dataset contenente le informazioni sulle ASL ed i comuni di riferimento è disponibile all'[indirizzo](https://www.salute.gov.it/portale/documentazione/p6_2_8_1_1.jsp?id=13)
- Le coordinate geografiche di ogni comune sono state reperite nel [repository](https://github.com/MatteoHenryChinaski/Comuni-Italiani-2018-Sql-Json-excel)


### Libraries

| Name | Description |
| ------------- | ------------------------------ |
| [Math] | module that provides access to the mathematical functions defined by the C standard.
| [Numpy] | package for scientific computing with Python.
| [Pandas]| fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.
| [Folium]| folium builds on the data wrangling strengths of the Python ecosystem and the mapping strengths of the Leaflet.js library.
| [Webbrowser]| provides a high-level interface to allow displaying Web-based documents to users..
| [Folium]| Instantly make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable).


---
### Dependencies

- [Python 3.9.X]
- [Numpy]
- [Pandas]
---
### PIP

```sh
$ pip install numpy
$ pip install pandas
```

----
### Anaconda

Note: sostituire <env_name> con il nome dell'enviroment che volete creare...

```sh
$ conda create -n <env_name>
$ conda activate <env_name>
$ conda config --env --add channels conda-forge
$ conda install pandas
$ conda install numpy
```

----

### Functions:                
         
| Function                   | Description                    |
| -------------------------- | ------------------------------ |
| `def main()`                       | **rappresenta la socket TCP principale su cui ogni client si connette prima di essere instradato sulla sua socket personale**|
| `def assign_socket()`              |**crea una nuova socket prendendo una porta disponibile nel nostro sistema a coda, notifica il client e chiude la vecchia connessione**|
| `def release_socket()`             | **chiude la connessione attuale e restituisce la porta al sistema a coda per un nuovo utente**|
| `def tcp_socket()`                 | **instaura una connessione tcp e gestisce tutto il mapping degli argument per eseguire ogni specifica funzione richiesta**|
| `def encode()`                     | **gestisce la compressione video per utenti concorrenti**|
| `def clear_shadow()`               | **rimuove i file nativi dopo che essi sono stati compressi risparmiando spazio sul server**|
| `def compress_video()`             | **comprime il video tramite ffmpeg in un sottoprocesso shell**|

----

### *End*



[time]
[performance]
[pythonds]

[Python 3.9.X]: <https://www.python.org/downloads/release/python-390/>
[time]: <http://robyp.x10host.com/3/time.html#loaded>
[performance]: <https://www.promezio.it/2018/10/02/python-misurazione-delle-performance/>
[pythonds]: <https://elearning.lumsa.it/pluginfile.php/76990/mod_resource/content/1/pythonGraphs.pdf>
[Math]: <https://docs.python.org/3/library/math.html>
[Numpy]: <https://numpy.org/install/>
[Pandas]: <https://pandas.pydata.org/>
[Folium]: <https://python-visualization.github.io/folium/>
[Webbrowser]: <https://docs.python.org/3/library/webbrowser.html>

