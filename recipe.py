import streamlit as st
import polars as pl
import functions


recipe = functions.select_recipe(st.session_state["recipe"])

st.title(recipe["name"])