import streamlit as st
import functions
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




