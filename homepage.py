import streamlit as st
import functions
from map import map 

st.title("FOODOMNIA")

lst = functions.recipes_list()
#*barra di ricerca
search_query = st.selectbox(options = lst,label = "recipes", placeholder="Search for a recipe:", label_visibility= "collapsed", index = None)

if search_query:  #per controllare se è stato inserito qualcosa
#evito che entri nell'else e mostri errore appena si apre il sito
    if search_query in lst:
        st.session_state["recipe"] = search_query
        st.switch_page("recipe.py")#vado alla ricetta
    else:
        st.error("We don't have that recipe, try again!")


if st.button("recipes list"):
    st.switch_page("recipes.py")


fig = map()
event = st.plotly_chart(fig, on_select="rerun", selection_mode=["points", "box", "lasso"])

"""points = event["selection"].get("points", [])
    if points:
        first_point = points[0]
        sigla = first_point["properties"].get("sigla", None)
    else:
        sigla = None
    """


