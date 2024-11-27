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

#todo: file ricette
rec = pl.read_csv("recipes/RAW_recipes.csv")
print(rec.describe())
print(rec.glimpse())
#! i tag, i valori nutritivi, gli step e gli ingredienti sono str, quando vorrei li leggesse come liste

a = rec.with_columns(
    pl.col("ingredients","steps").str.replace_all("'", '"'))
