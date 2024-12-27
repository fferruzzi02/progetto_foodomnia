import streamlit as st
import polars as pl
import plotly.express as px
import pycountry
import datasets

#funzione che lavora sui dataset e renderizza mappa con numero di tags 
#@st.cache_data
def map():
    dem = pl.read_csv("Demonyms.csv") 
    rec = datasets.get_rec() 
    search = rec.select(pl.col("tags").list.explode())
    search = search["tags"].to_list()
    type(search)
    demonyms = dem["Demonym"].to_list() #lista demonimi 
    sta = dem["State"].to_list() #lista stati 
    lc_demonyms = [item.lower() for item in demonyms]
    states_dishes = {} 
    for el in search:
        if el in lc_demonyms:
            if el in states_dishes: 
                states_dishes[el] += 1
            else:
                states_dishes[el] = 1
    states_dishes 
    #aggiungiamo quelli mancanti 
    for el in lc_demonyms:
        if el not in states_dishes:
            states_dishes[el] = 0

    #lista con stati, counter e codice per mappare 
    lst = []
    for i in range(len(sta)):
        x = []
        x.append(sta[i])
        x.append(lc_demonyms[i])
        code = pycountry.countries.search_fuzzy(sta[i])[0].alpha_3
        x.append(code)
        num = states_dishes[lc_demonyms[i]]
        x.append(num)
        lst.append(x)

    #ddf con stato demonym, ... 
    df = pl.DataFrame(
        lst,
        schema=["state", "demonym", "code", "counter"]
    )

    fig = px.choropleth(df, locations="code",
                        color="counter",
                        color_continuous_scale="viridis") 
    return fig 

