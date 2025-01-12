import streamlit as st
import functions
import random

st.title("list of recipes")
st.divider()

#*widget per cercare ricette con filtri
col1,col2 = st.columns([10,1])
search = col1.toggle("search for something else")

if col2.button("", help = "remove filters", icon = ":material/delete:"): #bottone per eliminare filtri
    search = False #chiudo search (anche se il toggle non cambia)
    st.session_state.name = str()
    st.session_state.servings = int(0)
    st.session_state.steps = int(0)
    st.session_state.tags = str()
      
filter = [st.session_state.name,st.session_state.servings,st.session_state.steps,st.session_state.tags]
 #creo variabile filter (che poi uso per ricerca ricette)

if search: #se schiacchio research apro research
    functions.research()

st.divider()

#box informativi su filtri attivi 
col1, col2 = st.columns(2)
if st.session_state.name:
        col1.info(f"searching recipes containing '{st.session_state.name}' in the name")
if st.session_state.steps:
        col2.info(f"searching recipes with {st.session_state.steps} steps")
if st.session_state.servings:
        col1.info(f"searching recipes with {st.session_state.servings} servings")
if st.session_state.tags:
            col1.info(f"searching recipes with the following tag: {st.session_state.tags}")


if not any(filter):  #se non ci sono filtri 
    st.info("no filter applied. Selecting 30 random recipes!")
    #seleziono random 20 ricette 
    st.divider()
    col1,a, col2 = st.columns([10,1,10], vertical_alignment="center")
    lst = functions.recipes_list()
    for i in range(15):
        index = random.randint(0, 80098)
        col1.button(lst[index], key = i, help = f"{lst[index]} recipe")
        col1.divider()
    for i in range(15,30):
        index = random.randint(0, 80098)
        col2.button(lst[index], key = i, help = f"{lst[index]} recipe")
        col2.divider()

else:
    lst = functions.recipes_list(filter)
    if len(lst) == 0:
          st.error("we don't have recipes with those filters, sorry!")
    
    st.divider()
    if len(lst) >0 and len(lst)<= 30:
        st.info("recipes with the selected filters!")
        col1,a, col2 = st.columns([10,1,10], vertical_alignment="center")
        for i in range(len(lst)//2):
            col1.button(lst[i], key = i, help = f"{lst[i]} recipe")
            col1.divider()
        
        for i in range(len(lst)//2, len(lst)):
            col2.button(lst[i], key = i, help = f"{lst[i]} recipe")
            col2.divider()

    if len(lst) > 30:
        st.info("30 random recipes with the filters you selected!")
        col1,a, col2 = st.columns([10,1,10], vertical_alignment="center")
        for i in range(15):
            col1.button(lst[i], key = i, help = f"{lst[i]} recipe")
            col1.divider()
        for i in range(15,30):
            col2.button(lst[i], key = i, help = f"{lst[i]} recipe")
            col2.divider()


