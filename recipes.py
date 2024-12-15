import streamlit as st
import functions


st.title("list of recipes")


lst = functions.recipes_list()

for i in range(10):
    st.button(lst[i], key = lst[i], help = f"{lst[i]} recipe")

    


