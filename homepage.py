import streamlit as st
import functions
from map import map 
import datetime

st.divider()
st.markdown("<h1 style='text-align: center;'>FOODOMNIA</h1>", unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.columns([10,3,4], vertical_alignment="center")

#*barra di ricerca 
lst = functions.recipes_list()
search_query = col1.selectbox(options = lst,label = "recipes", placeholder="Search recipe by name:", label_visibility= "collapsed", index = None) 

if search_query:  #per controllare se è stato inserito qualcosa
    #evito che entri nell'else e mostri errore appena si apre il sito
        st.session_state.recipe = search_query
        st.switch_page("recipe.py")#vado alla ricetta


#*tasti navigazione rapida 
if col2.button("recipes list", help = "go to a list of recipies", type = "primary"): #porta alla pagina con lista ricette
        st.switch_page("recipe_list.py")
if col3.button("recipes by ingredients", help = "find a recipe with the ingredients you have!", type = "primary"): #porta alla pagina con ingredienti
        st.switch_page("ingredients.py")


st.divider()
#*carosello
st.session_state.button = 0
functions.carosel()
st.divider()


#creo due sottopagine
tab1, tab2 = st.tabs(["recipes by country", "recipes of the day!"])

#*mappa 
with tab1:
    st.info('Search for a recipe by state of origin', icon=":material/travel_explore:")
    fig = map()
    event = st.plotly_chart(fig, use_container_width = True, on_select="rerun", 
                            selection_mode="points")
    #interattività (FUNZIONAAAAAAAAA)
    if event["selection"]["points"]: #se viene selezionato qualcosa
        t = event["selection"]["points"][0]["customdata"]
        st.write(f"there are {t[3]} recipes from {t[0]}")
        if t[3]: #se ci sono ricette di quello stato 
            col1, col2 = st.columns(2)
            col1.info(f"you want some {t[1]} recipes?", icon = ":material/arrow_forward:")  
            if col2.button("click here!", type = "primary"):#se clicco
                st.session_state.tags = str(t[1]) 
                st.switch_page("recipes_list.py") #rimando alla pagina lista di ricette
        else:#se non ci sono 
            st.info(f"sorry we do not have {t[1]} recipes, try another state!")


with tab2:
    #*un paio di ricette random 
    st.info(f"come and find the recipes of today: {datetime.date.today()}!", icon = ":material/event:")
    num = int(datetime.date.today().strftime("%Y%m%d"))
    lst = functions.recipes_list()
    index = num % 187328
    name = lst[index]
    recipe = functions.select_recipe(name)
    st.subheader(recipe["name"])
    st.write(recipe["description"])
    if st.button("go to the recipe!",type = "primary" ):
         st.session_state.recipe = name
         st.switch_page("recipe.py")
         


st.divider()
with st.expander("Contacts"):
    col1, col2, col3 = st.columns(3)
    if col1.button("+1 248 434-5508", icon = ":material/phone:"): 
        st.balloons()
    col2.link_button("socials",url = "https://www.instagram.com/gordongram?igsh=dmNlZm51OTE1bm9s",  icon = ":material/smartphone:")
    col3.link_button("site", url = "https://www.windows93.net/", icon = ":material/language:")

