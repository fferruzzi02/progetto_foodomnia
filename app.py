#entrypoint file
import streamlit as st
import random

#*inizializzo session state da subito, così non rischio problemi
if "recipe" not in st.session_state:
    st.session_state.recipe = "random"
if "name" not in st.session_state:
    st.session_state.name = str()
if "ingredients" not in st.session_state:
    st.session_state.ingredients = []
if "servings" not in st.session_state:
    st.session_state.servings = 0
if "steps" not in st.session_state:
    st.session_state.steps = 0
if "tags" not in st.session_state:
    st.session_state.tags = str()
if "logged" not in st.session_state:
    st.session_state.logged = False
if "credentials" not in st.session_state:
    st.session_state.credentials = str()


#*pagine
homepage = st.Page(
    "homepage.py", title="FOODOMNIA", icon=":material/local_dining:", default=True)

recipes = st.Page(
     "recipes_list.py", title="Recipes", icon=":material/receipt_long:")

recipe = st.Page(
     "recipe.py", title=f" {st.session_state.recipe} recipe", icon=":material/menu_book:")
#avendo definito nel session state il nome della ricetta rimane nel cambio pagina

ingredients = st.Page(
     "ingredients.py", title="select ingredients", icon=":material/lists:")

cose = st.Page(
    "cose.py", title="prova", icon=":material/login:" )


#* vari bottoni 
if st.sidebar.button("I want a random recipe!"): #ricetta random 
        st.session_state.recipe = "random"
        st.switch_page("recipe.py")

if st.sidebar.button("Holiday recipes", icon = ":material/celebration:"): #ricette festive (un tag a caso)
        st.session_state.tags = random.choice(["birthday","halloween", "new-years", "thanksgiving", "hanukkah", "valentines-day", "christmas", "cinco-de-mayo"])
        st.switch_page("recipes_list.py")
    #!forse selezionando festività più vicina 

if st.sidebar.button("Recipes on a diet", icon = ":material/no_food:"): #ricette dietetiche (un tag a caso)
        st.session_state.tags =  random.choice(["low-cholesterol", "diet", "healthy", "lowfat", "nofat", "nosugar", "low-sugar", "low-calorie", "low-carb", "nocarb"])
        st.switch_page("recipes_list.py")


#*inserisco  nello state la possibilità di essere admin, come controllo per me per il sito
if 'privilege' not in st.session_state:
    st.session_state.privilege = "admin" #se voglio vedere che ci sia tutto cambio qui 
  
if st.session_state.privilege == "admin": 
    pg = st.navigation({"pages":[homepage, recipes, ingredients, recipe, cose]})

if not st.session_state.logged:
    pg = st.navigation({"pages":[homepage, recipes, ingredients, recipe]})




st.sidebar.divider()
#*login

#se l'utente ha fatto l'accesso
if st.session_state.credentials: 
    st.sidebar.write(f"welcome back {st.session_state.credentials}!")
    st.divider()

#altrimenti    
if not st.session_state.logged:
    #popup per inserire dati di login 
    with st.sidebar.popover("login", icon = ":material/login:"):
        with st.form("my_form"):
            st.write("Insert your credentials")
            name = st.text_input("NAME")
            pssw = st.text_input("PASSWORD", type = "password")
            if st.form_submit_button("LOGIN", icon=":material/login:"):
                st.session_state.logged = True
                st.session_state.credentials = name 
                st.rerun()


if st.session_state.logged:
    if st.sidebar.button("logout", icon=":material/logout:"):
        st.session_state.logged = False
        st.session_state.credentials = str() 
        st.rerun()
                   

st.sidebar.divider()
#citations al dataset
st.sidebar.caption("All the data are from https://www.kaggle.com/datasets/shuyangli94/foodcom-recipes-with-search-terms-and-tags/data")
st.sidebar.caption("Author Name: Shuyang Li")

pg.run()

