# Algoritmi e Strutture Dati
Progetto di Algoritmi e Strutture Dati

### Description
L'implementazione prevede due differenti modelli. Il primo modello assume che tutti i comuni (nodi) siano direttamente connessi tra loro con distanza (peso) pari al numero di Km che li separa, considerando le loro coordinate geografiche e l'asse terrestre medio pari a 6373Km . Il secondo modello prevede che i capoluoghi regionali (nodi) siano direttamente connessi tra loro con le stesse assunzioni sulla distanza del precedente modello; a partire da ogni capoluogo regionale è possibile arrivare ai capoluoghi di provincia e successivamente ai comuni (se esistenti).

### Features
Rappresentazione tramite formato .html di una cartina geografica dell'Italia di tutti i nodi compreso il sorgente e il più distante (in Km).


### Libraries

| Name | Description |
| ------------- | ------------------------------ |
| [math] | Used for miscellaneous operating system operations.
| [numpy] | Time is a package that implements time in python script.
| [pandas]| Instantly make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable).
| [folium]| Instantly make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable).
| [webbrowser]| Instantly make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable).
| [folium]| Instantly make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable).


---
### Dependencies

[Python 3.9.X]
[FFMPEG]
---
### PyPi

```sh
$ pip install tqdm
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
[time]:<http://robyp.x10host.com/3/time.html#loaded>
[performance]:<https://www.promezio.it/2018/10/02/python-misurazione-delle-performance/>
[pythonds]:<https://elearning.lumsa.it/pluginfile.php/76990/mod_resource/content/1/pythonGraphs.pdf>

