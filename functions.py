import polars as pl
import datasets
import streamlit as st

#* funzioni utili per rendere più leggibile il codice nelle pagine


#?così scritta male? 
#todo: funzione per il rendering di una lista di ricette
#filter:list|str|None = None,filter_col: str|None = None)
def recipes_list(filter:list[str|None,list,int|None,int|None,list] =None)-> list:  #*ritorna lista ricette
    #*filter è una lista con i filtri delle colonne in ordine 

    rec = datasets.get_rec()
    if filter: #se non ci sono filtri inserisco tutte le ricette
        if filter[0]: #name -> filtro per lettera
            rec = rec.filter(pl.col("name").str.contains(filter[0]))

        if filter[1]: #ingredients_raw_str -> filtro per ingredienti 
            for i in range(len(filter[1])):
                rec = rec.filter(pl.col("ingredients_raw_str").list.contains(filter[1][i]))

        if filter[2]: #servings -> filtro per numero di porzioni
            rec = rec.filter(pl.col("servings") == filter[2])

        if filter[3]:  # number of steps (col = steps) -> filtro per numero di steps (lunghezza elemento steps)
            rec = rec.filter(pl.col("steps").list.len == filter[3])

        if filter[4]: #tags -> filtro per lista di tag
            for i in range(len(filter[4])):
                rec = rec.filter(pl.col("tags").list.contains(filter[4][i]))
    
    lst = rec["name"].to_list() 
    return lst


#todo: funzione per selezionare i tags/ gli ingredienti
def get_lst(col: str, unique: bool = True) -> list: 
    #*ritorna la lista dei tags o degli ingredienti 
    #specifico se  voglio unique o no 
    rec = datasets.get_rec()
    if unique: 
        lst = rec.select(pl.col(col).list.explode().unique())
    else: 
        lst = rec.select(pl.col(col).list.explode())
    lst = lst[col].to_list() #lista di python, più comoda
    return lst


#todo: funzione per selezionare una ricetta
def select_recipe(name: str) -> dict:   #*ritorna il dizionario con tutti gli elementi di una ricetta 
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
          "tags": r["tags"].to_list()[0]}
    return recipe


#todo: funzione che crea un carosello per visualizzare i tags
#! aggiungere immagini (forse)
@st.fragment(run_every=10)
#*fragment, così non devo rerunnare tutto ma solo un pezzo + cambia ogni 10 secondi 
def carosel():
    if st.session_state.button: #serve per cambiare pagina quando viene cliccato un pulsante tra i tag
        st.switch_page("recipes.py") 
    
    import math         
    tags = [
    ["birthday", "april-fools-day","halloween-cocktails", "rosh-hashanah", "halloween", "new-years", "chinese-new-year", "memorial-day", "passover ", "ramadan", "thanksgiving", "hanukkah", "valentines-day", "christmas", "mothers-day", "cinco-de-mayo", "labor-day", "irish-st-patricks-day"],
    ["low-cholesterol", "diet", "healthy", "lowfat", "nofat", "nosugar", "low-sugar", "low-calorie", "low-carb", "nocarb"],
    ["vegan", "kosher", "nomeat", "non-alcoholic", "gluten-free", "diabetic"],
    ["dinner", "lunch", "dips-lunch-snacks", "snacks", "main-dish-casseroles", "snack", "cakes", "cocktails", "breakfast", "desserts", "main-dish"],
    ["heirloom-historical-recipes", "60-minutes-or-less", "30-minutes-or-less", "15-minutes-or-less", "for-1-or-2", "summer", "romantic", "inexpensive", "beginner-cook", "easy"]
    ]   #tags 
    titles = ["festivities", "dietary", "food restrictions","by-meal", "other"]  #titoli gruppi tags

    if "carosel" not in st.session_state: #per segnare le pagine del carosello
        st.session_state.carosel = int(0)
    
    st.session_state.carosel = (st.session_state.carosel + 1) % len(tags) #così non supera mai 5 

    st.write(f"{titles[st.session_state.carosel]} recipes") 

    #*riempio con i tag su 4 colonne
    lst = tags[st.session_state.carosel]
    nrows = math.ceil(len(lst)/4)  #e calcolo le righe (arrotondo a intero superiore)
    col = st.columns(4) 
    count = 0 
    for nrow in range(nrows): #riempio griglia
        for ncol in range(4):
            if count < len(lst):

                def change_page(): #callback per i pulsanti
                       st.session_state.button = 1 #uso session state 

                st.session_state.tags = [lst[count]]
                col[ncol].button(lst[count], on_click=change_page) #se clicco cambio pagina
                count += 1

    #*pulsante per cambiare pagina del carosello
    col1,col2, col3 = st.columns([2,10,2])
    if col3.button("",icon=":material/arrow_circle_right:", help = "next"): 
        st.rerun(scope="fragment")
    if col1.button("",icon=":material/arrow_circle_left:", help = "last"): 
        st.session_state.carosel = (st.session_state.carosel + 1) % len(tags) #faccio il giro al contrario 
        st.rerun(scope="fragment")


#todo: funzione per gestire ricerca ricette
@st.fragment() 
#*fragment per non dover rerunnare tutto ogni volta (aumentando i tempi)
def research():
    st.info("find the recipe for you!") 
    col1,col2, col3= st.columns(3) #divido in 3 colonne
    
    #ricerca per numero di porzioni 
    servings = col1.slider("number of portions", min_value=0, max_value=10)
    if servings:
        st.session_state.servings = servings

    #ricerca per steps   
    steps = col1.slider("number of steps", min_value=0, max_value=30)
    if steps:
        st.session_state.steps = steps

        #ricerca per nome  
    name = col2.text_input("recipe name", help = "search recipe by words in the name")
    if name:
        st.session_state.name = name
    
    #per fare ricerca per ingredienti o tags prima chiedo per cosa si vuole cercare
    col = ["ingredients", "tags"]
    selection = col2.segmented_control("filter", col, selection_mode="multi")

    #poi apro multiselect 
    if selection:
        for col in selection: #1 se seleziono solo ingredients, 2 solo per tags
            lst = get_lst(col)
            col3.multiselect(f"select {col}", lst)
    
    if st.button("apply filters!"): #se applico i filtri faccio rerun di tutta l'app, così cerco ricette
         st.rerun(scope = "app")



if __name__ == '__main__':
    #*prova di recipes_list
    """lst = recipes_list() 
    for i in range(10):
        print(lst[i])
    lst = recipes_list(filter = "eggs",col = "ingredients") 
    print(lst)"""
    #*prova di select_recipe
    print(select_recipe("random"))
    print(len(recipes_list(None)))
    print(len(recipes_list([None, None, None, None, None])))

    print(len(recipes_list(["and", None, None, None, None])))
    print(len(recipes_list([None, ["onions"], None, None, None])))
    print(len(recipes_list([None, None, 2, None, None])))
    print(len(recipes_list([None, None, 2, 14, None])))
    print(len(recipes_list([None, None, None, None, ["christmas"]])))
    print(len(recipes_list([None, ["flour"], None, None, ["christmas"]])))

recipes_list([None, ["onions"], None, None, None])
    

