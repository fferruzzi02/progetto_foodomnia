#checklist degli ingredienti che si hanno

import streamlit as st
import functions 
import datasets
import polars as pl

st.title("ingredients checklist")
st.divider()


st.info("select what you have in the fridge, we'll find a recipe")

lst = functions.get_ingr()
ingr = st.multiselect("select the ingredients", lst, default=[])

if st.button("search for recipes!"):
    st.session_state.ingredients = ingr

@st.fragment() #*frammento che trova ricette
def find(): 
    #filtro le ricette per gli ingredienti 
    filter = [str(None),st.session_state.ingredients,int(0),int(0),[]]
    lst = functions.recipes_list(filter)

    if len(lst) == 0:
        st.error("sorry, we don't have recipes with those ingredients!")

    if len(lst) < 25:
        txt = f"{len(lst)} recipes with the following ingredients", (f"{item}, " for item in st.session_state.ingredients)
        st.info(txt)
        for i in range(len(lst)):
            st.button(lst[i], key = lst[i], help = f"{lst[i]} recipe")
    else: 
        txt = "25 random recipes with the following ingredients ",(f"{item}, " for item in st.session_state.ingredients)
        st.info(txt)
        import random
        index = random.randint(0, len(lst))
        st.button(lst[index], key = lst[index], help = f"{lst[index]} recipe")
        if st.button("try again", help = "press to find other random recipes"):
            st.rerun(scope="fragment")

    


if st.session_state.ingredients:
    find()
    
else: 
    st.write("no ingredients selected!")