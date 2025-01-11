import streamlit as st
import functions
from map import map 

st.title("FOODOMNIA")
st.divider()

#*barra di ricerca
lst = functions.recipes_list()
search_query = st.selectbox(options = lst,label = "recipes", placeholder="Search recipe by name:", label_visibility= "collapsed", index = None)
st.info('Search for a recipe by name', icon=":material/search:")

if search_query:  #per controllare se è stato inserito qualcosa
#evito che entri nell'else e mostri errore appena si apre il sito
    st.session_state.recipe = search_query
    st.switch_page("recipe.py")#vado alla ricetta

#! inserire tags frequenti in qualche modo 

#*tasti navigazione rapida
st.divider()
col1, col2 = st.columns(2)
if col1.button("recipes list"): #porta alla pagina con lista ricette
    st.switch_page("recipes.py")
if col2.button("recipes by ingredients"):
    st.switch_page("ingredients.py")

#*mappa
st.divider()
fig = map()
event = st.plotly_chart(fig, use_container_width = True, on_select="rerun", 
                        selection_mode="points")
st.info('Search for a recipe by state of origin', icon=":material/travel_explore:")

#interattività (FUNZIONAAAAAAAAA)
if event["selection"]["points"]: #se viene selezionato qualcosa
    t = event["selection"]["points"][0]["customdata"]
    st.write(f"there are {t[3]} recipes from {t[0]}")
    if t[3]: #se ci sono ricette di quello stato 
        st.info(f"you want some {t[1]} recipes?") 
        if st.button("click here!"):#se clicco
            st.session_state.tags = [str(t[1])] 
            st.switch_page("recipes.py") #rimando alla pagina lista di ricette
    else:#se non ci sono 
        st.info(f"sorry we do not have {t[1]} recipes, try another state!")


st.caption("""All the data are from https://www.kaggle.com/datasets/shuyangli94/foodcom-recipes-with-search-terms-and-tags/data
           Author Name: Shuyang Li""")
