import polars as pl
#import kagglehub #? perché ??? Ha senso usare questo o è un problema se i dati vengono cambiati???

"""
path = kagglehub.dataset_download("utsavdey1410/food-nutrition-dataset")

print("Path to dataset files:", path)"""

#todo: studio preliminare dataset info nutrizionali cibi
#*i dataset sono 5 con le stesse colonne ma righe diverse
#per primo leggo i 5 datasets  
nutri1 = pl.read_csv("nutri/FOOD-DATA-GROUP1.csv")
nutri2 = pl.read_csv("nutri/FOOD-DATA-GROUP2.csv")
nutri3 = pl.read_csv("nutri/FOOD-DATA-GROUP3.csv")
nutri4 = pl.read_csv("nutri/FOOD-DATA-GROUP4.csv")
nutri5 = pl.read_csv("nutri/FOOD-DATA-GROUP5.csv")
#poi li concateno in uno unico, così ho una sola tabella, tanto la divisione non mi serve 
nutri = pl.concat([nutri1,nutri2,nutri3,nutri4,nutri5])

#*studiamo un po' il dataset unico
print(nutri.glimpse(return_as_string=True)) 
print(nutri.describe()) #controllo, non ci sono valori null, le colonne sono numeriche tranne il nome del cibo (ovviamente)
#l'unica cosa di troppo (avendo concatenato i dataset) sono le prime due colonne di indici, le rimuovo
nutri = nutri.select(pl.col("*").exclude(nutri.columns[0], nutri.columns[1]))

print(nutri.head()) #ora ho solo le colonne necessarie

#todo: file ricette: analisi esplorativa 
rec = pl.read_csv("RAW_recipes.csv")
print(rec.describe())
print(rec.glimpse(return_as_string=True))
rec = rec.select(pl.col("*").exclude("contributor_id", "submitted", "description"))
#elimino colonne che non mi servono 

print(rec.glimpse(return_as_string=True))
#! i tag, i valori nutritivi, gli step e gli ingredienti sono str, quando vorrei li leggesse come liste
#studiamo un po' i dati 

print(rec.select(pl.col("ingredients"))[1].glimpse()) #sono liste di stringhe

print(rec.select(pl.col("ingredients").cast(pl.List,strict=False))) #se provo a trasformare mi crea valori null
str.split("")
#provo a scomporre e ricomporre le liste
rec = rec.with_columns(pl.col("ingredients","tags","steps").str.replace_all(r"[\[\]']", "").str.split(","))
print(rec.select(pl.col("tags")))
# ora sono corrette 
#*ho il problema che mi ha preso le virgolette singole '' come caratteri, rimuovo anche quelle (aggiunto sopra)

#todo: confronto due datasets 
rec.with_columns(contains=pl.col("ingredients").list.contains("eggs")).filter(pl.col("contains") == "true")
#check, 

#*voglio controllare che tutti gli ingredienti di una ricetta siano dentro la lista con i valori nutrizionali 

ingredients = rec.select(pl.col("ingredients").list.explode()).unique() #salvo la lista di tutti gli ingredienti 

cont = ingredients.with_columns(contains = pl.col("ingredients").is_in(nutri["food"])) #salvo il dataset con lista e se è contenuto o no

cont.filter(pl.col("contains")=="true") #molti pochi ingredienti sono contenuti 
cont.filter(pl.col("contains")=="false")


pattern = "|".join(nutri["food"].to_list())
pattern1 = pattern.replace(" ", "|")

# Check for partial matches
matches = ingredients.with_columns(
    contains=pl.col("ingredients").str.contains(pattern)).filter(pl.col("contains") == "true")


ma = matches["ingredients"].to_list()

