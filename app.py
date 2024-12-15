#entrypoint file
import streamlit as st

#*pagine
homepage = st.Page(
    "homepage.py", title="FOODOMNIA", icon=":material/local_dining:", default=True
)

recipes = st.Page("recipes.py", title="Recipes", icon=":material/receipt_long:")

#*inizializzo recipe in session state da subito, così non rischio problemi
if 'recipe' not in st.session_state:
    st.session_state["recipe"] = "random"

#e nel definire il titolo della pagina ricetta aggiungo il session state
recipe = st.Page("recipe.py", title=f" {st.session_state.recipe} recipe", icon=":material/menu_book:")
#così se uno cambia pagina rimane la ricetta

ingredients = st.Page("ingredients.py", title="select ingredients", icon=":material/lists:")


st.sidebar.title("Actions")  
if st.sidebar.button("I want a random recipe!"):
        st.session_state.recipe = "random"
        st.switch_page("recipe.py")


#*iserisco  nello state la possibilità di essere admin, come controllo per me per il sito
if 'privilege' not in st.session_state:
    st.session_state["privilege"] = "guest" #se voglio vedere che ci sia tutto cambio qui
#? potrei fare login solo per member, just to have fun



if st.session_state["privilege"] == "member":
    pg = st.navigation({"pages":[homepage, recipes, ingredients, recipe]})
if st.session_state["privilege"] == "guest":
    pg = st.navigation({"pages":[homepage, recipes,ingredients, recipe]})

pg.run()

