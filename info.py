import streamlit as st 
import kagglehub
import polars as pl 
from datasets import get_rec
import altair as alt 
import functions
from collections import Counter
import time
from pathlib import Path

st.title("Informations about the project")
st.subheader("Scritte in italiano per semplicità")
st.divider()

tab1, tab2 = st.tabs(["IL PROGETTO", "I DATI"])

with tab1:
    st.header("IL PROGETTO")

    st.subheader("la progettazione e la scelta dei dati")
    """
    Il progetto è nato come sito che consigliasse ricette rispetto agli ingredienti in frigo e avesse un modellino lineare che prevedesse, rispetto a genere ed età, la probabilità di ordinare cibo invece di cucinare. La ricerca dei dati è stata fatta su kaggle.com. 
    Il primo ostacolo è stato trovare dei dataset decenti con delle ricette. Essendo incappato in un dataset di valori calorici degli ingredienti avevo pensato di aggiungere una pagina con le informazioni nutrizionali... idea deceduta perché i match con gli ingredienti di ben 3 dataset che ho provato a usare erano il 10/15% del totale. 
    """
    col1, col2 = st.columns([4,1])
    col1.write("I dati analizzati sono presi dal sito kaggle (si ringrazia Shuyang Li)")
    col2.link_button("DATI", type = "primary", url="https://www.kaggle.com/datasets/shuyangli94/foodcom-recipes-with-search-terms-and-tags/data", icon = ":material/arrow_back:")

    st.subheader("la costruzione del sito")
    """
    La parte di pulizia dei dati, analizzata nella tab "i dati" (ma vah), è stata più lunga del previsto (ho anche cambiato dataset più volte). Ho quindi eliminato la parte di predittore lineare per concentrarmi a utilizzare al massimo i dati, riciclando il più possibile le funzioni. Ho quindi esteso il numero di pagine puntando a un vero e proprio sito di ricette, incentrato su tags e ingredienti.
    Le parti "salienti" della costruzione delle pagine sono state: 
    - Il carosello (functions.carosel())-> avevo anche trovato il modo di far cambiare pagina utilizzando i fragment di streamlit ma non funzionavano più i tags alle ricette
    - la mappa (map.py)-> non usa altair perchè vuole essere interattiva, ci ho messo i secoli. Anche il filtro dei tag degli Stati è stato lungo, alla fine lo ho inserito in una funzione (functions.states())
    - la funzione per filtrare le ricette (functions.recipes_list())-> usata in più contesti, mi ha fatto penare perchè volevo inserire tutti i filtri contemporaneamente.
    """

    st.subheader("la palette colori")
    """
    Finito (circa) di programmare, ho cercato una palette adeguata per il sito. Ho scelto di partire da una scala colori già validata, per non sbagliare, e da lì selezionare 4 colori. 
    Sono partito guardando vari siti di cucina (anche per farmi venire idee su ulteriori feature) e ho notato che quasi tutti utilizzano colori scuri per far passare un senso di professionalità. Il verde era onnipresente nei siti healthy, perchè associato in psicologia con la natura, il benessere e la tranquillità, ed è usato anche nel marketing per aumentare le vendite (Jonathon P Schuldt, *"Does Green Mean Healthy? Nutrition Label Color Affects Perceptions of Healthfulness"*, February 2013Health Communication 28(8)). 
    Ho quindi cercato una palette che sfruttasse la scala di verdi, trovando la scala **aggrnyl**
    Da qui, ho analizzato quali colori funzionassero meglio, utilizzando il pacchetto **colorspace**, dove la scala ha l'acronimo **ag_GrnYl**
    """
    st.code("pal = colorspace.hcl_palettes().get_palette('ag_GrnYl')")
    col1, col2 = st.columns(2)
    col1.image("pal60.png")
    col2.image("pal60dalt.png")
    col1.code("colorspace.specplot(pal(60))")
    col2.code("colorspace.specplot(colorspace.deutan(pal(60)))")
    st.write("Per prima cosa ho controllato la linearità dei colori per usarli nella mappa, che risulta lineare. In caso di daltonismo meno, ma funziona abbastanza.")
    st.divider()
    st.code("pal(4)")
    st.write("Ho poi estratto 4 colori ")
    c1, c2 = st.columns(2)
    c1.image("contrast1.png")
    c2.image("contrast2.png")
    st.write("Ho poi controllato il contrast ratio, per decidere che colore usare come sfondo. Il migliore è risultato quello con il verde scuro come sfondo")
    st.image("contrast_final.png")
    st.write("Per aumentare ancora di più il contrasto rispetto al testo, ho optato per il bianco come colore al posto del giallo (tra l'altro colore associato meno alla salute)")
    st.info("Il codice usato per l'analisi dei colori è riportato nel file try.py   ")
    
    st.subheader("la pagina info")
    """
    Sezione che rompe la quarta parete visto che parlo della sezione info NELLA sezione info.
    Comunque ho creato prima l'analisi dei dati (per inserire qualche grafico) e poi ho scritto le varie sezioni, in ordine: 
    - la progettazione
    - la costruzione del sito
    - la palette colori 
    - la pagina info.....
    """
    if st.button("...."):
        for i in range(3):
            st.write("......................")
            time.sleep(1)
        st.error("ERRORE: C'è stata una scissione tra l'io narrante e l'io agente")

        with st.popover("per leggere il diario completo del progetto (non lo consiglio)"):
            md = Path("diario.md").read_text()
            st.markdown(md, unsafe_allow_html=True)

with tab2:
    st.subheader("I DATI")

    st.info("Si riporta di seguito una superficiale analisi dei dati, evidenziandone i punti salienti")
    st.divider()
    path = kagglehub.dataset_download("shuyangli94/foodcom-recipes-with-search-terms-and-tags")
    path += "/recipes_w_search_terms.csv"
    raw_rec = pl.read_csv(path)
    st.write("I dati iniziali presentavano diverse problematiche")

    with st.expander("dati grezzi (10 righe)"):
        st.write("questi sono i dati appena raccolti (non dai campi)")
        st.dataframe(raw_rec.head(10))
    
    st.write("Terribili, no? Ho quindi provveduto a ripulire il dataset per poterlo utilizzare")
    rec = get_rec()
    with st.expander("dati ripuliti (sempre 10 righe)"):
        st.write("ecco come invece appaiono i dati dopo anni e anni di lavoro")
        st.dataframe(rec.head(10))
    
    st.write("Dopo aver ripulito i dati, vediamo un po' le loro caratteristiche")
    with st.expander("le colonne sono divise in"):
        st.write("- 'name' -> nome del piatto")
        st.write("- 'description' -> descrizione del piatto")
        st.write("- 'ingredients' -> ingredienti, senza unità di misura, marche et similia")
        st.write("- 'ingredients_raw_str' -> ingredienti con unità di misura, marche et similia")
        st.write("- 'serving_size' -> grammi di una porzione")
        st.write("- 'servings' -> numero di porzioni")
        st.write("- 'steps' -> i passaggi della ricetta")
        st.write("- 'tags' -> tag per riconoscere il piatto")

    st.write("E ora, un po' di statistiche (ah ma statistica sarebbe il mio corso di laurea? Non sapevo)")

    st.write("LE TOP 10")
    top10 = ["top 10 ingredienti", "top 10 tags", "top 10 paesi"] 
    top = st.selectbox("", top10)

    if top == top10[0]:
        x = []
        lst = rec["ingredients"].to_list()
        for el in lst:
            x.extend(el)
        ig = Counter(x).most_common(10)
        df = pl.DataFrame(ig, schema=["ingredient", "frequency"])
        ch1 = (alt.Chart(df)
        .mark_bar()
        .configure_mark(color="#9DDE8B")
        .encode(alt.Y("ingredient", sort = "-x"),alt.X("frequency")))

    elif top == top10[1]:
        x = []
        lst = rec["tags"].to_list()
        for el in lst:
            x.extend(el)
        tg = Counter(x).most_common(10)
        df = pl.DataFrame(tg, schema=["tag", "frequency"])
        ch1 = (alt.Chart(df)
        .mark_bar()
        .configure_mark(color="#9DDE8B")
        .encode(alt.Y("tag", sort = "-x"),alt.X("frequency")))
    
    elif top == top10[2]:
        df = functions.states()
        df = df.filter(pl.col("ranking")< 11) 
        ch1 = (alt.Chart(df)
        .mark_bar()
        .configure_mark(color="#9DDE8B")
        .encode(alt.Y("state", sort = "-x"),alt.X("counter")))

    st.altair_chart(ch1, use_container_width=True)

    st.subheader("THE BIGGEST")
    big = ["il piatto con più ingredienti", "il piatto con più porzioni", "il piatto con la porzione più abbondande"]
    bg = st.selectbox("", big, index=None)
    
    if bg == big[0]:
        st.write("il piatto con più ingredienti è...")
        st.balloons()
        df = rec.with_columns(pl.col("ingredients").list.len().alias("count"))
        df = df.filter(pl.col("count")== pl.col("count").max())

        n = df["count"].to_list()[0]; ingr = df["ingredients"].to_list()[0]; name= df["name"].to_list()[0]
        time.sleep(1)
        if st.button(name):
            st.session_state.recipe = name
            st.switch_page("recipe.py")
        st.write(f"con {n} ingredienti:")
        for i in ingr:
            if i:
                st.write("-",i)
        
    if bg == big[1]:
        st.write("il piatto con più porzioni è...")
        st.balloons()
        df =  rec.filter(pl.col("servings")== pl.col("servings").max())
        n = df["servings"].to_list()[0]; name= df["name"].to_list()[0]
        time.sleep(1)
        if st.button(name):
            st.session_state.recipe = name
            st.switch_page("recipe.py")
        st.write(f"con {n} porzioni")

            
    if bg == big[2]:
        st.write("il piatto con la porzione più grande è...")
        st.balloons()
        df =  rec.filter(pl.col("serving_size")== pl.col("serving_size").max())
        n = df["serving_size"].to_list()[0]; name= df["name"].to_list()[0]
        time.sleep(1)
        if st.button(name):
            st.session_state.recipe = name
            st.switch_page("recipe.py")
        st.write(f"con una porzione di {n} grammi")

        

    st.caption("THE SMALLEST")
    small = ["il piatto con meno ingredienti", "il piatto con meno porzioni", "il piatto con la porzione più piccola"]
    sm = st.selectbox("", small, index=None)
    
    if sm == small[0]:
        st.write("il piatto con meno ingredienti è...")
        st.balloons()
        df = rec.with_columns(pl.col("ingredients").list.len().alias("count"))
        df = df.filter(pl.col("count")== pl.col("count").min())        
        n = df["count"].to_list()[0]; ingr = df["ingredients"].to_list()[0]; name= df["name"].to_list()[0]
        time.sleep(1)
        if st.button(name):
            st.session_state.recipe = name
            st.switch_page("recipe.py")
        st.write(f"con {n} ingredienti:")
        for i in ingr:
            if i:
                st.write("-",i)
        
    if sm == small[1]:
        st.write("il piatto con meno porzioni è...")
        st.balloons()
        df =  rec.filter(pl.col("servings") != 0).filter(pl.col("servings")== pl.col("servings").min())
        n = df["servings"].to_list()[0]; name= df["name"].to_list()[0]
        time.sleep(1)
        if st.button(name):
            st.session_state.recipe = name
            st.switch_page("recipe.py")
        st.write(f"con {n} porzioni")

            
    if sm == small[2]:
        st.write("il piatto con la porzione più piccola è...")
        st.balloons()
        df =  rec.filter(pl.col("serving_size") != 0).filter(pl.col("serving_size")== pl.col("serving_size").min())
        n = df["serving_size"].to_list()[0]; name= df["name"].to_list()[0]
        time.sleep(1)
        if st.button(name):
            st.session_state.recipe = name
            st.switch_page("recipe.py")
        st.write(f"con una porzione di {n} grammi")



st.divider()
with st.expander("I contatti della pagina iniziale sono fittizi, quindi per i contatti veri..."):
    st.write("Francesco Ferruzzi, Dipartimento di scienze statistiche, UNIPD")
    st.write("email: francesco.ferruzzi@studenti.unipd.it")