#checklist degli ingredienti che si hanno

import streamlit as st
import functions 

st.title("ingredients checklist")
st.divider()
st.info("select what you have in the fridge, we'll find a recipe")
st.divider()
st.session_state.ingredients = str()
lst = functions.get_ingr()
ingr = st.multiselect("select the ingredients", lst, default=[])

if st.button("search for recipes!"):
    st.session_state.ingredients = ingr

@st.fragment() #*frammento che trova ricette
def find(): 
    #filtro le ricette per gli ingredienti 
    lst = functions.recipes_list(ingr = st.session_state.ingredients)
    
    if len(lst) == 0:
        st.error("sorry, we don't have recipes with one of those ingredients!")

    if len(lst) < 30:
        txt = f"{len(lst)} recipes with one of the following ingredients" 
        for i in range(len(ingr)):
            txt += f"{ingr[i]}, "
        st.info(txt)
        st.divider()
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

    else: 
        txt = "30 random recipes with one of the following ingredients"
        for i in range(len(ingr)):
            txt += f"{ingr[i]}, "
        st.info(txt)

        st.divider()
        import random
        index = random.randint(0, len(lst))
        col1,a, col2 = st.columns([10,1,10], vertical_alignment="center")
        for i in range(15):
            if col1.button(lst[index], key = index, help = f"{lst[index]} recipe"):
                st.session_state.recipe  = lst[index]
                st.switch_page("recipe.py")
            st.divider()

        for i in range(15):
            if col2.button(lst[index], key = index, help = f"{lst[index]} recipe"):
                st.session_state.recipe  = lst[index]
                st.switch_page("recipe.py")
            st.divider()
    
        if st.button("try again", help = "press to find other random recipes"):
            st.rerun(scope="fragment")

    


if st.session_state.ingredients:
    find()
    
else: 
    st.write("no ingredients selected!")