import streamlit as st
import polars as pl
import functions

#la ricetta importata è quella che si trova nella session state
recipe = functions.select_recipe(st.session_state["recipe"])
#così controllo che ricetta renderizzare prima di entrare nella pagina stessa

name = recipe["name"] #(se non estraevo la variabile prima non funzionava nel titolo) 
st.session_state["recipe"] = name #cambio lo state di recipe, così rimane nella sidebar

#*titolo
st.title(f"{name} recipe")

#todo: scrivere i tag uno dopo l'altro, cliccabili cos' da avere link ad altre ricette
#col = st.columns(len(recipe["tags"]))
#st.columns
#for i in range(len(col)):
#    with col[i]:
#       st.button(recipe["tags"][i])

#*parte descrizione
st.write(recipe["description"])
st.divider()

#*ingredienti
#!da sistemare, nel dividere gli ingredienti nella lista ci sono virgole anche negli ingredienti
#! vengono ingredienti spezzati
st.write("ingredients")
for i in range(len(recipe["ingredients"])):
    st.write("-",recipe["ingredients"][i])
st.divider()

#*steps
st.write("steps:")
for i in range(len(recipe["steps"])):
    st.write(i+1, recipe["steps"][i])

st.divider()

