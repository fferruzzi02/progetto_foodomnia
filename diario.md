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
ho inserito il file incriminato (RAW\*recipes.csv) in _.gitignore_
Poi ho fatto un commit