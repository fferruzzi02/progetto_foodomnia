#funzioni utili
import polars as pl
import datasets
import icecream as ic

#todo: funzione per il rendering di una lista di ricette
def recipes_list(filter:list|str|None = None,col: str|None = None)-> list:  
    #funzione che riceve in input il filtro e il nome della colonna in cui filtrare 
    #quindi se metto come filtro lista di tag dovrò specificare che deve cercare nella colonna tag
    #non mi serve inserire vincoli su col perché non è controllato dallo user
    #specifico io ogni volta in cui faccio una call alla funzione
    rec = datasets.get_rec()
    if filter != None: #se non ci sono filtri inserisco tutte le ricette
        #!da modificare, il filtro per lista
        rec = rec.filter(pl.col(col) == filter) #?da errore for some reason
    names = rec["name"].to_list() 
    return names



#todo: funzione per il rendering di una ricetta
def select_recipe(name: str):
    rec = datasets.get_rec()
    if name == "random":
        t = rec.sample(1, with_replacement=True)
    else: 
        t = rec.filter(pl.col("name") == name)
        ic(t)
    return t

if __name__ == '__main__':
    #*prova di recipes_list
    """lst = recipes_list() 
    for i in range(10):
        print(lst[i])
    lst = recipes_list(filter = "eggs",col = "ingredients") 
    print(lst)"""
    #*prova di select_recipe
    print(select_recipe("random"))

    
