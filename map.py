import streamlit as st
import plotly.express as px
import functions

#todo: funzione che crea una mappa interattiva con plotly.express
@st.cache_data #caching considerato il costo elevato della renderizzazione della mappa 
def map():
    df2 = functions.states()

    #funzione di plotly express per renderizzare mappa 
    #non servono dataset aggiuntivi, la terra è caricata di default
    fig = px.choropleth(df2, locations="code",
                        color="ranking" , 
                        color_continuous_scale="aggrnyl_r",#scala viridis invertita
                        locationmode="ISO-3", #associo locazione con codice ISO-3
                        hover_name = "state",
                        hover_data = {"state":False, "demonym": True,  "ranking":True, "counter": True, "code":False},
                        labels= {"ranking": "Ranking of countries (by number of recipes) ", "demonym": "recipe origin ", "counter": "number of recipes "}, 
                        projection = 'natural earth') #proiezione ottimizzata per il globo, poca distorsione e effetto "terra" che è carino 
    return fig 

if __name__ == '__main__':
    st.plotly_chart(map())


