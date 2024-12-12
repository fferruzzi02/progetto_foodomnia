#funzioni utili
import streamlit as st
import polars as pl
import datasets
 
#todo: funzione per il rendering di una lista di ricette
def recipes_list(filter = None): 
    rec = datasets.get_rec()
    names = rec["name"].to_list()
    return names



#todo: funzione per il rendering di una ricetta
if __name__ == '__main__':
    recipes_list(filter = None)
    
