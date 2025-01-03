#entrypoint file
import streamlit as st


#*inizializzo session state da subito, così non rischio problemi
if "recipe" not in st.session_state:
    st.session_state.recipe = "random"
if "tags" not in st.session_state:
    st.session_state.tags = []
if "servings" not in st.session_state:
    st.session_state.servings = 0

#*pagine
homepage = st.Page(
    "homepage.py", title="FOODOMNIA", icon=":material/local_dining:", default=True
)

recipes = st.Page(
     "recipes.py", title="Recipes", icon=":material/receipt_long:"
     )

recipe = st.Page(
     "recipe.py", title=f" {st.session_state.recipe} recipe", icon=":material/menu_book:"
     )
#avendo definito nel session state il nome della ricetta rimane nel cambio pagina

ingredients = st.Page(
     "ingredients.py", title="select ingredients", icon=":material/lists:"
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
    st.session_state.privilege = "guest" #se voglio vedere che ci sia tutto cambio qui
#? potrei fare login solo per member, just to have fun



if st.session_state.privilege == "member":
    pg = st.navigation({"pages":[homepage, recipes, ingredients, recipe]})
if st.session_state.privilege == "guest":
    pg = st.navigation({"pages":[homepage, recipes,ingredients, recipe]})

pg.run()

