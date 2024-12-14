import streamlit as st
st.title("FOODOMNIA")

search_query = st.text_input("Search for a food item:")

if st.button("recipes list"):
    st.switch_page("recipes.py")



