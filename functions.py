import polars as pl
import datasets
import streamlit as st

#* funzioni utili e riciclabili per rendere più leggibile il codice nelle pagine


#todo: funzione per filtrare lista di ricette
def recipes_list(filter:list[str|None,int|None,int|None,str|None] = None, ingr:list[str]|None = None)-> list:  #*ritorna lista ricette
    #*filter è una lista con i filtri delle colonne in ordine

    rec = datasets.get_rec()
    if filter: #se non ci sono filtri inserisco tutte le ricette
        if filter[0]: #name -> filtro per lettera
            rec = rec.filter(pl.col("name").str.contains(filter[0]))

        if filter[1]: #servings -> filtro per numero di porzioni
            rec = rec.filter(pl.col("servings") == filter[1])

        if filter[2]:  # number of steps (col = steps) -> filtro per numero di steps (lunghezza elemento steps)
            rec = rec.filter(pl.col("steps").list.len() == filter[2])

        if filter[3]: #tags -> filtro per lista di tag
            rec = rec.filter(pl.col("tags").list.contains(filter[3]))
    

    #inserisco alla fine filtro per ingredienti 
    if ingr: #ingredients -> filtro per ingredienti, ma faccio ricette che abbiano any ingredient
            names = []
            for i in range(len(ingr)): #per ogni ingrediente
                na = rec.filter(pl.col("ingredients").list.contains(ingr[i]))
                names.extend(na["name"].to_list()) #colleziono tutti i nomi delle ricette che hanno quell'ingrediente
            return names #se ci sono filtri per ingredienti ritorna 
    
    else: #se ho filtro ingredienti predilige quello (e ignora gli altri filtri)
        lst = rec["name"].to_list() 
        return lst #altrimenti ritorna lista ricette 


#todo: funzione per selezionare i tags
@st.cache_data 
def get_tags() -> list: 
    #*ritorna la lista dei tags 
    rec = datasets.get_rec()
    tags = rec.select(pl.col("tags").list.explode())
    tags = tags["tags"].to_list() #lista di python, più comoda
    return tags


#todo: funzione per selezionare gli ingredienti
@st.cache_data 
def get_ingr() -> list: 
    #*ritorna la lista degli ingredienti 
    rec = datasets.get_rec()
    ingr = rec.select(pl.col("ingredients").list.explode().unique())
    ingr = ingr["ingredients"].to_list() #lista di python, più comoda
    return ingr


#todo: funzione per selezionare una ricetta
def select_recipe(name: str) -> dict:  
    #*ritorna il dizionario con tutti gli elementi di una ricetta
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
@st.fragment(run_every=10)
#*fragment, così non devo rerunnare tutto ma solo un pezzo + cambia ogni 10 secondi 
def carosel():
    import icecream as ic 
    if st.session_state.button: #serve per cambiare pagina quando viene cliccato un pulsante tra i tag
        #! perché mannaggia la vita se non cambio pagina il session state è giusto mentre se la cambio si annulaaaaaaa
        print(st.session_state.tags)
        st.switch_page("ingredients.py")

    
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
    
    if not st.session_state.button:
        st.session_state.carosel = (st.session_state.carosel + 1) % len(tags)


    st.info(f"{titles[st.session_state.carosel]} recipes") 
    #*riempio con i tag su 4 colonne
    lst = tags[st.session_state.carosel]
    nrows = math.ceil(len(lst)/4)  #e calcolo le righe (arrotondo a intero superiore)
    col = st.columns(4, vertical_alignment= "center") 
    count = 0 
    def change_page(): #callback per i pulsanti
        st.session_state.button = 1 #uso session state 
    
    for nrow in range(nrows): #riempio griglia
        for ncol in range(4):
            if count < len(lst):         
                val = col[ncol].button(lst[count], on_click=change_page) #se clicco cambio pagina
                if val: 
                    st.session_state.tags = lst[count]
                    st.rerun(scope = "fragment")
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
    col1,col2= st.columns([3,2], vertical_alignment="center") #divido in 3 colonne


    #ricerca per steps (col più grande, ho più valori ) 
    steps = col1.slider("number of steps", min_value=0, max_value=50)
    if steps:
        st.session_state.steps = steps

    #ricerca per numero di porzioni 
    servings = col2.slider("number of portions", min_value=0, max_value=10)
    if servings:
        st.session_state.servings = servings

    #ricerca per tags
    tags = list(set(get_tags())) #uso set così elimino i valori ripetuti 
    tg = col1.selectbox(f"select tag", tags)
    if tg:
        st.session_state.tags = tg

    #ricerca per nome  
    name = col2.text_input("recipe name", help = "search recipe by words in the name")
    if name:
        st.session_state.name = name
    





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
    #print(select_recipe("random"))
    #print(len(recipes_list(None)))
    #print(len(recipes_list([None, None, None, None, None])))
    print(len(recipes_list(ingr = ["onions"])))
    #print(len(recipes_list(["and", None, None, None, None])))
    print(len(recipes_list([None, None, None, None])))
    print(len(recipes_list([None, None, None, ["christmas"]])))
    print(len(recipes_list([None, 2, None, None])))
    print(len(recipes_list([None, 2, 14, None])))

    

