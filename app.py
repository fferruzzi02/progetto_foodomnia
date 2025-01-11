#entrypoint file
import streamlit as st


#*inizializzo session state da subito, così non rischio problemi
if "recipe" not in st.session_state:
    st.session_state.recipe = "random"
if "name" not in st.session_state:
    st.session_state.name = None
if "ingredients" not in st.session_state:
    st.session_state.ingredients = []
if "servings" not in st.session_state:
    st.session_state.servings = 0
if "steps" not in st.session_state:
    st.session_state.steps = 0
if "tags" not in st.session_state:
    st.session_state.tags = []



#*pagine
homepage = st.Page(
    "homepage.py", title="FOODOMNIA", icon=":material/local_dining:", default=True
)

recipes = st.Page(
     "recipes_list.py", title="Recipes", icon=":material/receipt_long:"
     )

recipe = st.Page(
     "recipe.py", title=f" {st.session_state.recipe} recipe", icon=":material/menu_book:"
     )
#avendo definito nel session state il nome della ricetta rimane nel cambio pagina

ingredients = st.Page(
     "ingredients.py", title="select ingredients", icon=":material/lists:"
     )


cose = st.Page(
     "cose.py", title="cose di prova", icon=":material/login:"
     )

st.sidebar.title("Actions")  
if st.sidebar.button("I want a random recipe!"):
        st.session_state.recipe = "random"
        st.switch_page("recipe.py")

if st.sidebar.button("LOGIN"):
     #st.switch_page("login")
     st.error("you thought it was a login, but it was me, Dio!")

#!da fare login (forse)
#*inserisco  nello state la possibilità di essere admin, come controllo per me per il sito
if 'privilege' not in st.session_state:
    st.session_state.privilege = "logged" #se voglio vedere che ci sia tutto cambio qui
#? potrei fare login solo per member, just to have fun
  

if st.session_state.privilege == "guest": 
    if st.sidebar.button("",icon=":material/login:"):
        st.session_state.privilege = "logged"
        st.rerun()


if st.session_state.privilege == "logged": 
    if st.sidebar.button("",icon=":material/logout:"):
        st.session_state.privilege = "guest"
        st.rerun()




if st.session_state.privilege == "guest":
    pg = st.navigation({"pages":[homepage, recipes, ingredients, recipe]})
if st.session_state.privilege == "logged":
    pg = st.navigation({"pages":[homepage, recipes,ingredients, recipe, cose]})

pg.run()

