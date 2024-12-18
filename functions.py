#funzioni utili
import polars as pl
import datasets
import streamlit as st
#*funzione per il rendering di una lista di ricette
def recipes_list(filter:list|str|None = None,filter_col: str|None = None)-> list:  
    #funzione che riceve in input il filtro e il nome della colonna in cui filtrare 
    #quindi se metto come filtro lista di tag dovrò specificare che deve cercare nella colonna tag
    #non mi serve inserire vincoli su col perché non è controllato dallo user
    #specifico io ogni volta in cui faccio una call alla funzione
    rec = datasets.get_rec()
    if filter != None: #se non ci sono filtri inserisco tutte le ricette
        #!da modificare, il filtro per lista con cella che è
        rec = rec.filter(pl.col(filter_col).is_in(filter)) #?da errore for some reason
    lst = rec["name"].to_list() 
    return lst

#*funzione che crea pulsante tag che quando viene premuto porta alla pagina recipes con liste filtrate
def tag(tag:str):
    rec = datasets.get_rec()
    if st.button(tag):
        filtered = rec.filter(pl.col("tags").list.contains("tag"))
        lst = filtered["name"].to_list() 
        st.switch_page()


#*funzione che riporta lista di una delle colonne con List(String)
def col_list(col:str, filter:list|str|None = None,filter_col: str|None = None) ->list:
    rec = datasets.get_rec()
    if filter != None: #se non ci sono filtri prendo tutte 
        #!da modificare, il filtro per lista con cella che è
        pass
        #rec = rec.filter(pl.col(filter_col).is_in(filter)) 
    df = rec.select(pl.col(col).list.explode()).unique() #salvo la lista di tutti gli ingredienti/tag/serach_terms 
    lst = df[col].to_list()
    return lst

#*funzione che seleziona una ricetta
def select_recipe(name: str) -> dict:
    #funzione che ritorna il dizionario con tutti gli elementi di una ricetta 
    rec = datasets.get_rec() 
    if name == "random": #se devo prendere una ricetta random 
        r = rec.sample(1, with_replacement=True) #uso funzione sample di polars (senza scomodare random)
    else: 
        r = rec.filter(pl.col("name") == name) #altrimenti trovo la ricetta con quel nome
    #creo il dizionario con tutte le info
    recipe = {"name"  : r["name"].to_list()[0],
          "description": r["description"].to_list()[0], 
          "ingredients": r["ingredients_raw_str"].to_list()[0], 
          "serving_size": r["serving_size"].to_list()[0], 
          "servings": r["servings"].to_list()[0], 
          "steps": r["steps"].to_list()[0], 
          "tags": r["tags"].to_list()[0],
          "search_terms": r["search_terms"].to_list()[0]}
    return recipe

if __name__ == '__main__':
    #*prova di recipes_list
    """lst = recipes_list() 
    for i in range(10):
        print(lst[i])
    lst = recipes_list(filter = "eggs",col = "ingredients") 
    print(lst)"""
    #*prova di select_recipe
    print(select_recipe("random"))

    
