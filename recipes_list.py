import streamlit as st
import functions

st.markdown("<h1 style='text-align: center;'>List of recipes</h1>", unsafe_allow_html=True)
st.divider()

#*widget per cercare ricette con filtri
col1,col2 = st.columns([10,1])
search = col1.toggle("search for something else")

if col2.button("", help = "remove filters", icon = ":material/delete:"): #bottone per eliminare filtri
    search = False #chiudo search (anche se il toggle non cambia)
    st.session_state.name = str()
    st.session_state.servings = int(0)
    st.session_state.portion = int(0)
    st.session_state.tags = str()
      
filter = [st.session_state.name,st.session_state.servings,st.session_state.portion,st.session_state.tags]
 #creo variabile filter (che poi uso per ricerca ricette)

if search: #se schiacchio research apro research
    functions.research()

st.divider()

#box informativi su filtri attivi 
col1, col2 = st.columns(2)
if st.session_state.name:
        col1.info(f"searching recipes containing '{st.session_state.name}' in the name")
if st.session_state.portion:
        col2.info(f"searching recipes with a portion of {st.session_state.portion} grams")
if st.session_state.servings:
        col1.info(f"searching recipes with {st.session_state.servings} servings")
if st.session_state.tags:
            col1.info(f"searching recipes with the following tag: {st.session_state.tags}")


if not any(filter):  #se non ci sono filtri 
    st.info("no filter applied! Search for something!")
    if st.button("random recipe", help = "get to a random recipe", use_container_width=True, type = "primary"):
        st.session_state.recipe = "random"
        st.switch_page("recipe.py") 
else:
    lst = functions.recipes_list(filter)
    if len(lst) == 0:
          st.error("we don't have recipes with those filters, sorry!")
    
    st.divider()
    if len(lst) >0 and len(lst)<= 30:
        st.info("recipes with the selected filters!")
        col1,a, col2 = st.columns([10,1,10], vertical_alignment="center")
        for i in range(len(lst)//2):
            if col1.button(lst[i], key = i, help = f"{lst[i]} recipe"):
                st.session_state.recipe = lst[i]
                st.switch_page("recipe.py")                 
            col1.divider()
        
        for i in range(len(lst)//2, len(lst)):
            if col2.button(lst[i], key = i, help = f"{lst[i]} recipe"):
                st.session_state.recipe = lst[i]
                st.switch_page("recipe.py")
            col2.divider()

    if len(lst) > 30:
        st.info("30 random recipes with the filters you selected!")
        col1,a, col2 = st.columns([10,1,10], vertical_alignment="center")
        for i in range(15):
            if col1.button(lst[i], key = i, help = f"{lst[i]} recipe"):
                st.session_state.recipe = lst[i]
                st.switch_page("recipe.py")
            col1.divider()
        for i in range(15,30):
            if col2.button(lst[i], key = i, help = f"{lst[i]} recipe"):
                st.session_state.recipe = lst[i]
                st.switch_page("recipe.py")
            col2.divider()


