import streamlit as st 
import functions

        
st.title("carosel")
st.divider()

st.session_state.button = 0
functions.carosel()


tab1, tab2 = st.tabs(["1", "2"])

with tab1:
    st.write("tab1")

with tab2:
    st.write("Daje Roma")


