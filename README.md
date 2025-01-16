# Progetto sistemi 2: foodomnia

## descrizione progetto

Il seguente progetto vuole simulare un sito di ricette, con varie funzionalità.
Per utlizzarlo basta digitare il comando "uv run streamlit run app.py"
Per avere più informazioni sul progetto, una volta lanciato il sito, si può accedere
alla sezione _informations_, contenente tutte le informazioni.
Per qualsiasi cosa i contatti de

## informazioni

Le informazioni specifiche sulla macchina usata e sulle scelte fatte sono
contenute nel file diario.md
È stato usato il pacchetto _uv_ per non avere problemi di dipendenze

## file del progetto

### file app

Il file _app.py_ è il file di base dell'app, con l'ordine delle pagine e
le impostazioni della sidebar.

### file datasets

Il file _datasets.py_ raccoglie i dati grezzi e li manipola con Polars,
rendendoli utilizzabili

### file diario

Il file _diario.md_ è un diario del progetto scritto in linguaggio markdown,
diviso per giorno. Contiene le informazioni specifiche su pc e versione di python

### file functions

Il file _functions.py_ raccoglie le funzioni troppo lunghe e complesse per
essere inserite nelle singole pagine. Ogni funzione ha la sua spiegazione
nel codice

### file homepage

Il file _homepage.py_, come si intuisce dal nome, è l'homepage del sito

### file info

Il file _info.py_ renderizza la pagina con le informazioni sul progetto
e sui dati raccolti, con grafici di spiegazione. È in lingua italiana

### file ingredients

Il file _ingredients.py_ renderizza la pagina che permette di cercare
le ricette da degli ingredienti

### file map

Il file _map.py_ contiene il codice per creare la mappa cliccabile presente in homepage

### file recipe

Il file _recipe.py_ renderizza la pagina tipo di una ricetta

### file recipes_list

Il file _recipes_list.py_ renderizza la pagina di ricerca delle ricette,
che permette di filtrare il dataset

### file try.py

Il file _try.py_ contiene il codice aggiuntivo usato per scegliere i colori

### altri file

Sono presenti inoltre 5 file .png, con fotografie usate nella pagina _info_.
C'è poi il file _Demonyms.csv_, con gli stati e i loro demonimi, usato
dalla mappa per collegare i tags agli stati.
La cartella _.streamlit_ contiene il file _config.toml_ con le impostazioni
di colore del sito.
La cartella _.vscode_ contiene il file _settings.json_ con le impostazioni
di colore di vscode, matchate con il sito stesso (essenziale).
Il file _pyproject.toml_ contiene le indicazioni di dipendenze dei pacchetti
per _uv_
Il file _.markdownlint.json_ contiene le impostazioni di markdown per la
compilazione del diario e del file README.md stesso
Il file .gitignore contiene i file locali nel pacchetto da ingnorare

## sitografia

Tutti i dataset sono stati scaricati dal sito <https://www.kaggle.com>

### Citations

Dataset ricette -> nome variabile = rec

Author Name: Shuyang Li
Bio: PhD Researcher @ UC San Diego
link: <https://www.kaggle.com/datasets/shuyangli94/foodcom-recipes-with-search-terms-and-tags/data>
