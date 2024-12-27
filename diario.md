# Diario di bordo del progetto "Foodomnia"

## idea progetto

L'obiettivo

## informazioni generali

**Macchina**: Il progetto è stato fatto interamente su un MacBook Air M1 del 2020

**software**: L'applicazione usata per scrivere codice è Visual Studio Code
(Version: 1.95.3 (Universal), Commit: f1a4fb101478ce6ec82fe9627c43efbf9e98c813 )

Le estensioni di VSCode usate attivamente in questo progetto sono le seguenti:

- Pylance (v2024.11.3)
- Python (v2024.20.0)
- Python Debugger (v2024.12.0)
- Better Comments (v3.0.2)
- Bracket Pair Color DLW (v0.0.6)
- Snippet Creator (v1.1.3)
- Git Graph (v1.30.0)
- Window Colors (v1.0.51)
- markdownlint (v0.57.0)

**playlist di accompagnamento**: <https://open.spotify.com/playlist/4lFMHfo4EC2yAk30Rwz5U7?si=BaUrgNEZR5q2iM9xI-Wpjg&pi=e-lkwJgPk8Qg2d>

## 19 Novembre 2024

**Obiettivi**: Creare il progetto, inizializzare uv e git, collegare il progetto
a github. Iniziare a guardare i dataset e fare le prime analisi

### Cosa ho fatto davvero

Dopo aver deciso il progetto e i dati da utilizzare (<https://www.kaggle.com>),
ho iniziato a preparare l'ambiente di lavoro.
Creazione cartella progetto e inizializzazione di uv. Download di streamlit.
Creazione repository di git e push su github (<https://github.com/fferruzzi02/progetto_foodomnia/activity>)
Download con uv di kugglehub (estensione che dovrebbe servire per aprire i file
da kkaggle ma devo ancora capire se funziona).
Creazione file app.py con ben 2 righe di codice (inserimento titolo per
verificare il funzionamento di streamlit con uv).
Creazione file datasets.py

## 20 Novembre 2024

**Obiettivi**: Organizzare meglio il tutto, analizzare il primo dataset
**Idee**:

### Cosa ho fatto davvero

Download locale dei file sulle informazioni nutrizionali. Unione dei 5 dataset
in un dataset unico.
Continuazione file README, aggiunta sitografia e citations

## 23 Novembre 2024

**Obiettivi**: Continuare analisi

### Cosa ho fatto davvero

Dopo aver controllato il dataset concatenato _nutri_ ho eliminato le colonne
degli indici, non necessarie.
Ho aggiunto a uv icecream, perché mi sono ricordato della sua esistenza solo ora.
Ho poi perso 20 minuti nella scelta della musica e del colore dello sfondo di VSCode.
Ho poi creato il diario (dopo aver pensato che le informazioni sulla macchina et
similia stessero meglio in un file a parte) e creato il file diario (compilato
ex post).
Creazione file con impostazioni di markdown (.markdownlint.json) e del file
.gitignore (che per qualche motivo non c'era già) per togliere impostazioni md.
Ricerca dataset ricette. Il file che avevo trovato pesa 2.3 giga, mi manda in
palla vscode.
Trovato questo:
<https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions/data>
Ma non so come aprire la mappa numeri-ingredienti -->
provo a farli tornare normale (file try.py)
In realtà mi sono impelagato nel nulla, nel file recipes RAW ci sono gli ingredienti
Elimino tutti i file non necessari, rimango solo con RAW_recipes.csv
Non avendo più tempo faccio il push --> il file RAW_recipes è troppo grande
**Commenti e problemi**:

1. Le liste di ingredienti e altre colonne sono prese come str invece che lista
2. Non ci sono le quantità degli ingredienti
   --> se non trovo file migliori tengo questo

## 27 Novembre 2024

**Obiettivi**:Risolvere il problema e fare push su github

### Cosa ho fatto davvero

Per prima cosa sono tornato alla precedente versone con _git reset HEAD@{1}_ e
ho inserito il file incriminato (RAWrecipes.csv) in .gitignore
Poi ho fatto un commit. Ho iniziato a provare a risolvere il problema delle liste

## 28 Novembre 2024

**Obiettivi**:Continuare analisi dataset ricette e spostare i dataset
in un servizio come <https://figshare.com/>

### Cosa ho fatto davvero

Ho risolto il problema delle liste prese come stringhe.
Ora voglio trovare gli ingredienti che hanno i valori nutrizionali
per farlo potrei:

1. usare list.eval() per controllare che ogni elemento della lista sia nel
   secondo dataset (con join)
2. usare list.explode() per creare una colonna con tutti gli ingredienti e
   confrontarla con il dataset nutri
   Scelgo la seconda per cominciare perché posso vedere gli ingredienti che mancano
   e capire se sono scritti in modo diverso (es: hard-cooked eggs è sempre eggs)
   Il problema è che ci sono pochi file in cui si ripete il nome
   Cambiando leggermente metodo ne ho 8.000 su 22.000, buono. Ora voglio capire
   quali ricette non hanno match ma non riesco a capire come fare

Sto provando inoltre a risolvere il problema di come gestire i file:

- potrei usare i siti consigliati ma ho paura ci sia un problema di diritti di autore
- protrei usare le api di kaggle ma si deve fare il login, funziona solo su
  questa macchina credo
- potrei usare git lfs ma non ci ho capito molto

## 9 Dicembre 2024

**Obiettivi**: Provare a creare un po' il sito

### Cosa ho fatto davvero

Schema cartaceo del sito

## 12 Dicembre 2024

**Obiettivi**: Provare a creare un po' il sito e selezionare dataset

### Cosa ho fatto davvero

Selezione dataset (finally) e creazione functions.py per gestire funzioni da riciclare
Creazione funzioni specifiche in datasets per pulire i dataset e selezionari con
una funzione.

**Commenti e problemi**:
Non riesco a far visualizzare una lista di ricette.
errore per dei simboli specifici

## 14 Dicembre 2024

**Obiettivi**: Continuare a creare la struttura del sito

### Cosa ho fatto davvero

Video di 2 ore su streamlit
Creato e ricreato la struttura delle pagine. Sono finalmente venuto a capo dei link
e del fare una multipage app. So come girare tra le pagine
Ho provato ad aggiungere le setting colore ma non le prende per qualche ragione.
Beh ho risolto l'errore che mi dava eliminando la riga dal dataset...magic

## 15 Dicembre 2024

**Obiettivi**: Continuare a creare la struttura del sito

### Cosa ho fatto davvero

Sono andato molto avanti con la struttura del sito, sistemando diverse pagine.
Ho fatto la searchbar dell'homepage, la struttura di una ricetta e sistemato le funzioni

**Commenti e problemi**:
Ora ho il problema che le ricette sono troppe, voglio quindi filtrarle
Stavo iniziando a selezionare per stato (così faccio mappa). Manca mettere
tutto il lowercase nelle liste, sennò fa casino (cerca metodo di polars)
Potrei filtrare in altri modi, tipo tags utili o eliminando ricette corte...
Devo leggermi i tags e i search_terms

## 18 Dicembre 2024

**Obiettivi**: Filtrare e sistemare dataset

### Cosa ho fatto davvero

Sto cercando di filtrare il dataset eliminando righe inutili. Sto studiando i tags
e i search_terms, li unirò per semplicità.
Volevo filtrare tenendo le righe che hanno lo stato del piatto, così da fare
una mappa cliccabile.
Ho filtrato per i tag il dataset, modificandone alcuni

## 27 Dicembre 2024

**Obiettivi**: continuare a filtrare dataset per tags et similia

### Cosa ho fatto davvero

Dopo circa 3 ore sono riuscito a fare la mappa (anche se devo ancora capire come
renderla cliccabile). Ho prima provato a disegnarla con i metodi fatti,
ma ho poi scoperto che plotly.express funziona senza dover importare mappe se
si usa il globo. Molto divertente.
Ho continuato a lavorare sul file dataset.py, devo finire analisi tags
e scrivere funzione che mi permetta di filtrare per tags. Ho in parte sistemato
get_rec()

## todos

- aggiungere settings colore
- guarda percorsi assoluti
- guarda per references (magari in piccolo sul sito)

## domande

- virgole in recipes
- numerosità ricette
- personalizzazione grafica con HTML
- download datasets
