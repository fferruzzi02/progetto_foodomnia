#checklist degli ingredienti che si hanno

import streamlit as st
import functions 
import datasets
import polars as pl

st.title("ingredients checklist")
st.divider()


st.info("select what you have in the fridge, we'll find a recipe")

lst = functions.col_list("ingredients")
ingr = st.multiselect("select the ingredients", lst, default=[])

if st.button("search for recipes!"):
    st.session_state.ingredients = ingr

if st.session_state.ingredients:
    x = ""
    x + (item for item in st.session_state.ingredients)
    st.write("you are searching for recipes with the following ingredients:", x)
    
#todo: rimandare a lista ricette e poi andare 

else: 
    st.write("no ingredients selected!")