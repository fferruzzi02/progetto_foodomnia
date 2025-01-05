import streamlit as st
import functions

st.title("list of recipes")
st.divider()

#*widget per cercare ricette con filtri
col1,col2 = st.columns([2,1])
search = col1.toggle("search for something else")

if col2.button("", help = "delete filters", icon = ":material/delete:"): #bottone per eliminare filtri 
    search = False #chiudo search (anche se il toggle non cambia)
    st.session_state.name = None
    st.session_state.ingredients = []
    st.session_state.servings = 0
    st.session_state.steps = 0
    st.session_state.tags = []

filter = [st.session_state.name,st.session_state.ingredients,st.session_state.servings,st.session_state.steps,st.session_state.tags] #creo variabile filter (che poi uso per ricerca ricette)

if search: #se schiacchio research apro research
    functions.research()

st.divider()

#box informativi su filtri attivi 
if st.session_state.name:
        st.info(f"searching recipes containing '{st.session_state.name}' in the name")
if st.session_state.steps:
        st.info(f"searching recipes with {st.session_state.steps} steps")
if st.session_state.servings:
        st.info(f"searching recipes with {st.session_state.servings} servings")
if st.session_state.tags:
            x = ""
            x + (str(item) for item in st.session_state.tags)
            st.info(f"searching recipes with the following tags: {x}")
if st.session_state.ingredients:
            x = ""
            x + (str(item) for item in st.session_state.ingredients)
            st.info(f"searching recipes with the following ingredients: {x}")

if not any(filter):  #se non ci sono filtri 
    st.info("no filter applied! Selecting 25 random recipes")
    #seleziono random 25 ricette 
    st.divider()
    
    lst = functions.recipes_list()
    import random
    for i in range(25):
        index = random.randint(0, 80098)
        st.button(lst[index], key = lst[index], help = f"{lst[index]} recipe")



 #! voglio creare caricamento carino con posate e emoji varie 




    




    


