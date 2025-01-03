#checklist degli ingredienti che si hanno

import streamlit as st
import functions 
import datasets
import polars as pl

datasets.get_rec()
st.title("ingredients checklist")
st.divider()

st.write("select what you have in the fridge, we'll find a recipe")

lst = functions.col_list("ingredients")
ingr = st.multiselect("select the ingredients", lst)

#todo: rimandare a lista ricette e poi andare 