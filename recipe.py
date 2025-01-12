import streamlit as st
import polars as pl
import functions

#la ricetta importata è quella che si trova nella session state
recipe = functions.select_recipe(st.session_state.recipe)
#così controllo che ricetta renderizzare prima di entrare nella pagina stessa

name = recipe["name"] #se non estraevo la variabile prima non funzionava nel titolo) 
st.session_state.recipe = name #cambio lo state di recipe, così rimane nella sidebar

#*titolo
st.title(f"{name} recipe")
st.divider()


#todo: scrivere i tag uno dopo l'altro, cliccabili così da avere link ad altre ricette
#col = st.columns(len(recipe["tags"]))
#st.columns
#for i in range(len(col)):
#    with col[i]:
#       st.button(recipe["tags"][i])


#todo: descrizione
st.write(recipe["description"])
st.divider()

#todo: ingredienti
st.write("ingredients")
for i in range(len(recipe["ingredients"])):
    st.write("-",recipe["ingredients"][i])
st.divider()

#todo: steps
st.write("steps:")
for i in range(len(recipe["steps"])):
    st.write(i+1, recipe["steps"][i])

st.divider()


#todo: feedback sotto le ricette
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

    
