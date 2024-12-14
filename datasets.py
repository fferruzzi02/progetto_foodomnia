import polars as pl
import streamlit as st
#import kagglehub #? perché ??? Ha senso usare questo o è un problema se i dati vengono cambiati???

#todo: funzione per ottenere il dataset con info valori nutrizionali ingredienti
#@st.cache_data
def get_nutri():
    #*i dataset sono 5 con le stesse colonne ma righe diverse
    #per primo leggo i 5 datasets 
    nutri1 = pl.read_csv("nutri/FOOD-DATA-GROUP1.csv")
    nutri2 = pl.read_csv("nutri/FOOD-DATA-GROUP2.csv")
    nutri3 = pl.read_csv("nutri/FOOD-DATA-GROUP3.csv")
    nutri4 = pl.read_csv("nutri/FOOD-DATA-GROUP4.csv")
    nutri5 = pl.read_csv("nutri/FOOD-DATA-GROUP5.csv")
    #poi li concateno, per semplificare
    nutri = pl.concat([nutri1,nutri2,nutri3,nutri4,nutri5])
    #ed elimino le colonne inutili 
    nutri = nutri.select(pl.col("*").exclude(nutri.columns[0], nutri.columns[1]))
    return nutri


#!Igore: analisi dataset nutri #*i dataset sono 5 con le stesse colonne ma righe diverse
"""#per primo leggo i 5 datasets  
nutri1 = pl.read_csv("nutri/FOOD-DATA-GROUP1.csv")
nutri2 = pl.read_csv("nutri/FOOD-DATA-GROUP2.csv")
nutri3 = pl.read_csv("nutri/FOOD-DATA-GROUP3.csv")
nutri4 = pl.read_csv("nutri/FOOD-DATA-GROUP4.csv")
nutri5 = pl.read_csv("nutri/FOOD-DATA-GROUP5.csv")
#poi li concateno in uno unico, così ho una sola tabella, tanto la divisione non mi serve 
nutri = pl.concat([nutri1,nutri2,nutri3,nutri4,nutri5])
nutri = nutri.select(pl.col("*").exclude(nutri.columns[0], nutri.columns[1]))
#studiamo un po' il dataset unico
print(nutri.glimpse(return_as_string=True)) 
print(nutri.describe()) #controllo, non ci sono valori null, le colonne sono numeriche tranne il nome del cibo (ovviamente)
#l'unica cosa di troppo (avendo concatenato i dataset) sono le prime due colonne di indici, le rimuovo
nutri = nutri.select(pl.col("*").exclude(nutri.columns[0], nutri.columns[1]))
print(nutri.head()) #ora ho solo le colonne necessarie
"""

#todo: funzione per ottenere file ricette
#@st.cache_data
def get_rec():
    rec = pl.read_csv("recipes.csv") #prendo il dataset 
    #ho il problema che il type delle colonne con liste è String 
    #rimuovo gli elementi superflui per farlo diventare list(String)
    rec = rec.with_columns(pl.col("ingredients",  "ingredients_raw_str", "steps", "tags", "search_terms").str.replace_all(r"[\[\]'{}()]", "").str.split(","))
    #serving size è sempre 1 (...g), elimino il numero e la g, così mi rimane solo l'Int dei grammi di una porzione
    rec = rec.with_columns(pl.col("serving_size").str.replace_all("g1()", "").str.split(","))
    return rec



if __name__ == '__main__':
    nutri = get_nutri()
    print("nutri")
    rec = get_rec()
    print("rec")
    
"""
rec = pl.read_csv("recipes.csv") #prendo il dataset 

print(rec.head())
print(rec.dtypes) 
print(rec.columns) #perfetto 


rec = pl.read_csv("recipes.csv")
print(rec.head())
print(rec.dtypes) 
print(rec.columns)
#!devo trasformare ingredients,  ingredients_raw_str, 'steps', 'tags'
rec.select("serving_size") #ho un altro problema, qui dati doppi, ma posso eliminare 1 e le parentesi
rec.select("search_terms") #qui usa pure graffe, posso tenere lista 

print(rec.select(pl.col("ingredients").cast(pl.List,strict=False))) #se provo a trasformare mi crea valori null

rec = rec.with_columns(pl.col("ingredients",  "ingredients_raw_str", "steps", "tags", "search_terms").str.replace_all(r"[\[\]'{}()]", "").str.split(","))
rec = rec.with_columns(pl.col("serving_size").str.replace_all("g1()", "").str.split(","))


print(rec.head())
print(rec.dtypes) 
print(rec.columns) #perfetto



#todo: confronto due datasets 
rec.with_columns(contains=pl.col("ingredients").list.contains("eggs")).filter(pl.col("contains") == "true")
#check

#*voglio controllare che tutti gli ingredienti di una ricetta siano dentro la lista con i valori nutrizionali 

ingredients = rec.select(pl.col("ingredients").list.explode()).unique() #salvo la lista di tutti gli ingredienti 
ingr = ingredients["ingredients"].to_list()

nutri = get_nutri()
cont = ingredients.with_columns(contains = pl.col("ingredients").is_in(nutri["food"])) #salvo il dataset con lista e se è contenuto o no

cont.filter(pl.col("contains")=="true") #molti pochi ingredienti sono contenuti 
cont.filter(pl.col("contains")=="false")


pattern = "|".join(nutri["food"].to_list())
pattern1 = pattern.replace(" ", "|")


matches = ingredients.with_columns(contains=pl.col("ingredients").is_in(nutri["food"])).filter(pl.col("contains") == "true")


#ma è la lista di ingredienti che lascerò selezionare 
ma = matches["ingredients"].to_list()


#todo: file ricette: analisi esplorativa 
rec = pl.read_csv("RAW_recipes.csv")
print(rec.describe())

print(rec.glimpse(return_as_string=True))
print(rec.dtypes)
print(rec.columns)

rec = rec.select(pl.col("*").exclude("id","contributor_id", "submitted"))
#elimino colonne che non mi servono 

print(rec.glimpse(return_as_string=True))
#! i tag, i valori nutritivi, gli step e gli ingredienti sono str, quando vorrei li leggesse come liste
#studiamo un po' i dati 

print(rec.select(pl.col("ingredients"))[1].glimpse()) #sono liste di stringhe

print(rec.select(pl.col("nutrition").cast(pl.List,strict=False))) #se provo a trasformare mi crea valori null

print(rec.select(pl.col("ingredients").cast(pl.List,strict=False))) #se provo a trasformare mi crea valori null

str.split("")
#provo a scomporre e ricomporre le liste
rec = rec.with_columns(pl.col("ingredients","tags","steps", "nutrition").str.replace_all(r"[\[\]']", "").str.split(","))
print(rec.select(pl.col("tags")))

# ora sono corrette 
#*ho il problema che mi ha preso le virgolette singole '' come caratteri, rimuovo anche quelle (aggiunto sopra)
#devo rendere i valori nutritivi degli int 
print(rec.head())
print(rec.select("nutrition"))



"""