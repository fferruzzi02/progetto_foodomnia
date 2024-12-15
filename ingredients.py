#checklist degli ingredienti che si hanno

import streamlit as st
import functions 
st.title("ingredients checklist")
st.write("select what you have in the fridge, we'll find a recipe")

lst = functions.recipes_list()
st.multiselect("select the ingredients", lst)

