import streamlit as st
import polars as pl
import functions
import math

#*rendering ricetta 

#la ricetta importata è quella che si trova nella session state
recipe = functions.select_recipe(st.session_state.recipe)
#così controllo che ricetta renderizzare prima di entrare nella pagina stessa

name = recipe["name"] #se non estraevo la variabile prima non funzionava nel titolo) 
st.session_state.recipe = name #cambio lo state di recipe, così rimane nella sidebar

#*titolo
st.title(f"{name} recipe")
st.divider()

#*descrizione
st.write(recipe["description"])
st.divider()

#* tags
st.subheader("tags")
lst = recipe["tags"]
nrows = math.ceil(len(lst)/4)  #e calcolo le righe (arrotondo a intero superiore)
col = st.columns(4, vertical_alignment= "center") 
count = 0 
for nrow in range(nrows): #riempio griglia
        for ncol in range(4):
            if count < len(lst):         
                val = col[ncol].button(lst[count]) #se clicco cambio pagina
                if val: 
                    st.session_state.tags = lst[count]
                    st.switch_page("recipes_list.py")
                count += 1
st.divider()




#*porzioni
col1, col2 = st.columns(2)
n = recipe["servings"]
g = recipe["serving_size"]
col1.button(f"servings: {n}", use_container_width=True)
col2.button(f"serving size: {g}", use_container_width=True)
st.divider()

#*ingredienti
st.subheader("ingredients")
for ingr in recipe["ingredients"]:
    if ingr:
        st.write("-",ingr)
st.divider()

#*steps
#nb scritti così in modo da mandare a capo al  momento giusto, altrimenti non funzionava
st.subheader("steps:")
counter = 0
x = ""
for i in recipe["steps"]:
    if i == '\"':
        counter += 1
    else:
        if counter == 2:
            st.write(x)
            x = ""
            counter = 0
        else:
            x += i
        
st.divider()


#*feedback sotto le ricette
st.info('Did you like the recipe? Let us know!', icon=":material/stars:")
stars = st.feedback("stars") 
if stars: #se si lascia stelle si apre il form per lasciare recensione 
    if st.session_state.logged:
        with st.form("leave your review!"):
            st.write("review of the recipe: ",st.session_state.recipe)
            nickname = st.text_input("your name")
            title  = st.text_input("title of your review")
            review = st.text_area("tell us more...")
            if st.form_submit_button("send us your review"):
                st.balloons()
                st.success("Review sent correctly! Thank you for your time", icon=":material/reviews:")
    else:
        st.error("login if you want to write a review!")

    
