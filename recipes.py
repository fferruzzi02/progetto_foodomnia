import streamlit as st
import functions

st.title("list of recipes")
st.divider()

tab1, tab2 = st.tabs(["current research", "search something else"])

with tab1:
    st.write("fagiolo")
    if st.session_state.tags:
        st.info(f"searching recipes for the following tags: {st.session_state.tags}")
        #! voglio creare caricamento carino con posate e emoji varie 
        st.write("ricetteeee")
        #! completa 
    elif st.session_state.servings:
        st.info(f"searching recipes with {st.session_state.servings} servings")
    st.divider()
    lst = functions.recipes_list()

    for i in range(10):
        st.button(lst[i], key = lst[i], help = f"{lst[i]} recipe")


with tab2:
    st.info("find the recipe for you!")
    col1,col2, col3= st.columns([2,2,1])
    col1.slider("number of portions", min_value=1, max_value=10)
    col = ["name", "ingredients", "tags", "servings"]
    selection = col2.segmented_control("filter", col)
    col3.toggle("bb")
    if selection:
        st.write(selection)




    


