import streamlit as st 
import functions

        
st.title("Testing time")
st.divider()

st.session_state.button = 0
functions.carosel()


tab1, tab2 = st.tabs(["forza Roma", "forza Lazio"])

with tab1:
    st.write("Ha perso l'aRoma")

with tab2:
    st.write("Lazio merda")


