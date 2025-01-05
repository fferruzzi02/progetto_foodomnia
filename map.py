import streamlit as st
import polars as pl
import plotly.express as px
import pycountry
import functions

#todo: funzione che crea una mappa interattiva con plotly.express
@st.cache_data #caching considerato il costo elevato della renderizzazione della mappa 
def map():
    #parto dal dataset con Stati e demonimi
    dem = pl.read_csv("Demonyms.csv") 
    search = functions.get_lst("tags", unique = False) #lista tag 
    demonyms = dem["Demonym"].to_list() #lista demonimi 
    sta = dem["State"].to_list() #lista stati 
    lc_demonyms = [item.lower() for item in demonyms] #in minuscolo perché i tags sono in minuscolo
    states_dishes = {} #creo lista con demonimo e counter 
    for el in search: 
        if el in lc_demonyms:
            if el in states_dishes: 
                states_dishes[el] += 1
            else:
                states_dishes[el] = 1
    states_dishes 
    #aggiungo quelli mancanti 
    for el in lc_demonyms:
        if el not in states_dishes:
            states_dishes[el] = 0

    #lista con stati, counter e codice alpha 2 per mappare 
    lst = []
    for i in range(len(sta)):
        x = []
        x.append(sta[i])
        x.append(lc_demonyms[i])
        code = pycountry.countries.search_fuzzy(sta[i])[0].alpha_3 #API che estrae codice dal nome dello stato
        x.append(code) 
        num = states_dishes[lc_demonyms[i]]
        x.append(num)
        lst.append(x)
    #non differenzia i due congo (nel for i prendo solo il primo)
    lst.append(['Congo', 'congolese', 'COD', 0]) #lo aggiungo a mano per la mia salute mentale
    
    #ddf con stato, demonym, codice e counter del numero di piatti per stato 
    df = pl.DataFrame(
        lst,
        schema=["state", "demonym", "code", "counter"]
    )

    #aggiungo ranghi per avere colore lineare, li calcolo invertiti per avere classifica stati 
    df2 = df.with_columns((pl.col("counter").rank("dense").max() - pl.col("counter").rank("dense")+1).alias("ranking").cast(pl.Float32)) 

    """  import colorspace 
    pal = colorspace.hcl_palettes().get_palette("inferno")  
    viridis_colors = pal(100)
    type(viridis_colors)"""
    #! forse sistemo scala colori, vedo rispetto a palette sito 

    #funzione di plotly express per renderizzare mappa 
    #non servono dataset aggiuntivi, la terra è caricata di default
    fig = px.choropleth(df2, locations="code",
                        color="ranking" , 
                        color_continuous_scale="viridis_r",#scala viridis invertita
                        locationmode="ISO-3", #associo locazione con codice ISO-3
                        hover_name = "state",
                        hover_data = {"state":False, "demonym": True,  "ranking":True, "counter": True, "code":False},
                        labels= {"ranking": "Ranking of countries (by number of recipes) ", "demonym": "recipe origin ", "counter": "number of recipes "}, 
                        projection = 'natural earth') #proiezione ottimizzata per il globo, poca distorsione e effetto "terra" che è carino 
    return fig 

if __name__ == '__main__':
    st.plotly_chart(map())


