import polars as pl
import streamlit as st
import json
#import kagglehub #? perché ??? Ha senso usare questo o è un problema se i dati vengono cambiati???
x =  "['a', 'a']"


json.loads(x.replace("'",'"'))

#todo: funzione per ottenere il dataset info valori nutrizionali ingredienti
#@st.cache_data #essendo le operazioni con polars costose
def get_nutri():
    #i dataset sono 5 con le stesse colonne ma righe diverse
    #per primo leggo i 5 datasets 
    nutri1 = pl.read_csv("nutri/FOOD-DATA-GROUP1.csv")
    nutri2 = pl.read_csv("nutri/FOOD-DATA-GROUP2.csv")
    nutri3 = pl.read_csv("nutri/FOOD-DATA-GROUP3.csv")
    nutri4 = pl.read_csv("nutri/FOOD-DATA-GROUP4.csv")
    nutri5 = pl.read_csv("nutri/FOOD-DATA-GROUP5.csv")
    #poi li concateno, per semplificare
    nutri = pl.concat([nutri1,nutri2,nutri3,nutri4,nutri5])
    #ed elimino le colonne inutili 
    nutri = nutri.select(pl.col("*").exclude(nutri.columns[0], nutri.columns[1]))
    return nutri

#todo: funzione per ottenere il dataset ricette
#! da completare con filtering per tags etc
#@st.cache_data #essendo le operazioni con polars costose
def get_rec():
    rec = pl.read_csv("recipes.csv") #prendo il dataset 
    
    #*pulizia per colonna 
    rec = rec.with_columns(
        (pl.col("search_terms") + "," + pl.col("tags")).alias("tags"))
    #unisco tags e search_terms, sono simili e averli in due colonne non serve
    rec = rec.select(pl.col("*").exclude("search_terms")) #elimino search terms 

    #ho il problema che il type delle colonne con liste è String + i tags hanno spazi e robaccia varia 
    #rimuovo gli elementi superflui per farlo diventare list(String)
    rec = rec.with_columns(pl.col("ingredients", "ingredients_raw_str", "steps").str.replace_all(r"[\[\]'{}()]", "").str.split(","))
    rec = rec.with_columns(pl.col("serving_size").str.replace_all("g1()", "")) #non funziona più porco gesù
    rec = rec.with_columns(pl.col("tags").str.replace_all(r"[\[\]'\{\}\(\)\s]", "").str.split(","))
    
    #*pulizia per riga
    #elimino righe con valori nulli
    rec = rec.filter(pl.col("description").is_not_null()) #descrizioni null

    #elimino ricette che non hanno tra i tags gli stati
    dem = pl.read_csv("Demonyms.csv") #apro dataset 
    search = rec.select(pl.col("tags").list.explode()).unique()
    search = search["tags"].to_list()
    demonyms = dem["Demonym"].to_list() 
    lowercase_list = [item.lower() for item in demonyms] #in demonyms sono uppercase, in tags lowercase
    tags =[] #lista di tags
    for el in search:
        if el in lowercase_list:
            tags.append(el)  
    states_dishes = []
    for i in tags:
        filtered_df = rec.filter(
            pl.col("tags").list.contains(i))
        states_dishes.extend(filtered_df["name"].to_list())
    #tutti i piatti legati a uno stato 
    rec = rec.filter(pl.col("name").is_in(states_dishes)) #mantengo solo i piatti legati a stati
    
    #ora elimino i piatti di tags che non mi interessano 
    tag = ["household-cleansers","homeopathy-remedies","non-food-products"] #non voglio ricette omeopatiche e non ricette 
    remove = []
    for el in tag:
        filtered_df = rec.filter(pl.col("tags").list.contains(el))
        remove.extend(filtered_df["name"].to_list()) #raccolgo tutti i nomi di piatti legati a questi tags 

    names = rec["name"].to_list() #lista completa nomi ricette
    difference = [item for item in names if item not in remove] #tutti i piatti che voglio tenere

    rec = rec.filter(pl.col("name").is_in(difference)) #filtro 

    #*elimino o cambio tags per renderli più utili 
    #sostituzione  
    rep = [("southern-united-states", "american"), ("southwestern-united-states", "american"), ("northeastern-united-states", "american"), ("north-american", "american"), ("curries-indian", "curry"),("iranian-persian", "iranian"), ("jewish-sephardi","jewish"), ("simply-potatoes2","potatoes"), ("gluten-free-appetizers", "gluten-free"), ("meatless", "nomeat"), ("dietary", "diet"), ("healthy2", "healthy"), ("low-saturated-fat", "low-fat"), ("lowfat", "low-fat"), ("fat-free", "nofat"), ("sugarless", "nosugar"), ("sugar-free", "nosugar"), ("flourless", "gluten-free"), ("very-low-carbs", "low-carb"), ("carb-free", "nocarb"), ("noflour", "gluten-free")]
    replace_dict = dict(rep) #creo dizionario con i cambi 

    rec = rec.with_columns(
        pl.col("tags").map_elements(
            lambda tags: [replace_dict.get(tag, tag) for tag in tags] #cambio da tag sbagliato a tag giusto
        ).alias("tags") 
    )

    #rimozione
    delete = ["time-to-make", "high-in-something", "free-of-something", "less_thansql:name_topics_of_recipegreater_than", "time-to-make", "ThrowtheultimatefiestawiththissopaipillasrecipefromFood.com."]
    rec = rec.with_columns(tags=pl.col("tags").list.set_difference(delete))
    print(10)
    return rec 


if __name__ == '__main__':
    #*controllo
    nutri = get_nutri()
    print("nutri")
    rec = get_rec()
    print(rec)
    
    rec = pl.read_csv("recipes.csv")
    print(rec.head())
    print(rec.dtypes) 
    print(rec.columns)
    #unisco search-terms e tags 
    rec = rec.with_columns(
        (pl.col("search_terms") + "," + pl.col("tags")).alias("tags"))
    
    rec = rec.select(pl.col("*").exclude("search_terms")) 
    #!devo trasformare ingredients,  ingredients_raw_str, 'steps', 'tags'
    rec.select("serving_size") #ho un altro problema, qui dati doppi, ma posso eliminare 1 e le parentesi
    rec.select("tags") #qui usa pure graffe, posso tenere lista 

    print(rec.select(pl.col("ingredients").cast(pl.List,strict=False))) #se provo a trasformare mi crea valori null
    

    rec = rec.with_columns(pl.col("ingredients", "ingredients_raw_str", "steps").str.replace_all("'",'"'))

    reccc = rec.with_columns(
        pl.col("ingredients").apply(
            lambda ingredients: [json.loads(ingr) for ingr in ingredients]
    ))
    reccc = rec.with_columns(
    rec["ingredients"].apply(json.loads)
)

    rec = rec.with_columns(pl.col("serving_size").str.replace_all("g1()", "")) #non funziona più porco gesù
    rec = rec.with_columns(pl.col("tags").str.replace_all(r"[\[\]'\{\}\(\)\s]", "").str.split(","))

    print(rec.head())
    print(rec.dtypes) 
    print(rec.columns) 

    len(rec["tags"].to_list())
    {print(tag) for tag in rec["tags"].to_list()}


    dem = pl.read_csv("Demonyms.csv")

    dem.describe()

    search = rec.select(pl.col("tags").list.explode()).unique()
    search = search["tags"].to_list()
    type(search)
    demonyms = dem["Demonym"].to_list() 

    lowercase_list = [item.lower() for item in demonyms]

    states_dishes =[]

    for el in search:
        if el in lowercase_list:
            states_dishes.append(el)
    states_dishes#DAJEEEEEEE


    states = dem.filter(pl.col("Demonym").str.to_lowercase().is_in(states_dishes))
    states #ho dataframe con stati 

    sta = states["State"].to_list() #lista stati da mettere su mappa, that's nice 


    lst = []

    for i in states_dishes:
        filtered_df = rec.filter(
            pl.col("tags").list.contains(i))
        lst.extend(filtered_df["name"].to_list())

    lst #tutti i piatti legati a uno stato 

    fit = rec.filter(
            pl.col("name").is_in(lst))

    print(fit)
    #già ottima riduzione 
    #quindi fit ora è il mio dataset che voglio usare 

    #todo: analizziamo i tags
    for el in search:
        print(el)


    #todo: rimuovere righe tags 
    tag = ["household-cleansers","homeopathy-remedies","non-food-products"]
    lst = []
    for el in tag:
        filtered_df = fit.filter(pl.col("tags").list.contains(el))
        lst.extend(filtered_df["name"].to_list())

    lst2 = fit["name"].to_list()
    difference = [item for item in lst2 if item not in lst]

    fit2 = fit.filter(
            pl.col("name").is_in(difference))

    for el in tag:
        fit2.filter(pl.col("tags").list.contains(el)) #check
    #done!
    #da 81_780 a #81_765
    fit2

    #todo: cambiare tags
    rep = [("southern-united-states", "american"), ("southwestern-united-states", "american"), ("northeastern-united-states", "american"), ("north-american", "american"), ("curries-indian", "curry"),("iranian-persian", "iranian"), ("jewish-sephardi","jewish"), ("simply-potatoes2","potatoes"), ("gluten-free-appetizers", "gluten-free"), ("meatless", "nomeat"), ("dietary", "diet"), ("healthy2", "healthy"), ("low-saturated-fat", "low-fat"), ("lowfat", "low-fat"), ("fat-free", "nofat"), ("sugarless", "nosugar"), ("sugar-free", "nosugar"), ("flourless", "gluten-free"), ("very-low-carbs", "low-carb"), ("carb-free", "nocarb"), ("noflour", "gluten-free")]

    replace_dict = dict(rep)


    fit3 = fit2.with_columns(
        pl.col("tags").map_elements(
            lambda tags: [replace_dict.get(tag, tag) for tag in tags], return_dtype= pl.List(pl.Utf8)
    ))
    for el in rep:
        fit3.filter(pl.col("tags").list.contains(el[0]))
    #done!


    #todo: rimuovere dai tags 
    tg = ["time-to-make", "high-in-something", "free-of-something", "less_thansql:name_topics_of_recipegreater_than", "time-to-make", "ThrowtheultimatefiestawiththissopaipillasrecipefromFood.com."]

    fit4 = fit3.with_columns(tags=pl.col("tags").list.set_difference(tg))

    fit4.filter(pl.col("tags").list.contains("time-to-make"))
    #done!

    #todo: vediamo i nuovi tags

    search2 = fit4.select(pl.col("tags").list.explode()).unique()
    search2 = search2["tags"].to_list()

    search = rec.select(pl.col("tags").list.explode()).unique()
    search = search["tags"].to_list()
    len(search)
    len(search2)
    #diminuito i tags 

    for i in search2:
        print(i)

    #todo: eliminiamo altre righe
    #che altre rows posso eliminare? es: valori null
    fit4.filter(pl.col("description").is_null()) #ho 1522 ricette senza descrizione, posso eliminarle
    #aspeto di vedere quanto si riduce il dataset 

    fit5 = fit4.filter(pl.col("description").is_not_null())

    print(fit4.columns) 

    #todo: tags specifici
    #!festività 
    festivities = ("birthday", "april-fools-day","halloween-cocktails", "rosh-hashanah", "halloween", "new-years", "chinese-new-year", "memorial-day", "passover ", "ramadan", "thanksgiving", "hanukkah", "valentines-day", "christmas", "mothers-day", "cinco-de-mayo", "labor-day", "irish-st-patricks-day")

    #! dieta 
    diet = ("low-cholesterol", "diet", "healthy", "lowfat", "nofat", "nosugar", "low-sugar", "low-calorie", "low-carb", "nocarb") 
    #!food restrictions 
    restr = ("vegan", "kosher", "nomeat", "non-alcoholic", "gluten-free", "diabetic")
    #! divisione piatti 
    div = ("dinner", "lunch", "breakfast", "dips-lunch-snacks", "snacks", "main-dish-casseroles", "snack", "cakes", "cocktails", "breakfast", "desserts", "main-dish")
    #!altro
    oth = ("heirloom-historical-recipes", "60-minutes-or-less", "30-minutes-or-less", "15-minutes-or-less", "for-1-or-2", "summer", "romantic", "inexpensive", "beginner-cook", "easy")

    #todo: confronto due datasets 
    rec.with_columns(contains=pl.col("ingredients").list.contains("eggs")).filter(pl.col("contains") == "true")
    #check

    #*voglio controllare che tutti gli ingredienti di una ricetta siano dentro la lista con i valori nutrizionali 

    ingredients = fit5.select(pl.col("ingredients").list.explode()).unique() #salvo la lista di tutti gli ingredienti 
    ingr = ingredients["ingredients"].to_list()

    nutri = get_nutri()
    cont = ingredients.with_columns(contains = pl.col("ingredients").is_in(nutri["food"])) #salvo il dataset con lista e se è contenuto o no

    cont.filter(pl.col("contains")=="true") #molti pochi ingredienti sono contenuti 
    x = cont.filter(pl.col("contains")=="false")
    a = x["ingredients"].to_list()
    nut = nutri["food"].to_list()
    count = 0
    ls = []
    for el in a:
        for fo in nut:
            if f"{fo} " in el:
                ls.append((el, fo))
                print(el,"---", fo) 
                count += 1
    len(ls)
    print(ls) #ho 2000 ingredienti contenuti, quindi posso mapparli 


    matches = ingredients.with_columns(contains=pl.col("ingredients").is_in(nutri["food"])).filter(pl.col("contains") == "true")

    #ma è la lista di ingredienti che lascerò selezionare 
    ma = matches["ingredients"].to_list()



    #todo: file ricette: analisi esplorativa 
    rec = pl.read_csv("RAW_recipes.csv")
    print(rec.describe())

    print(rec.glimpse(return_as_string=True))
    print(rec.dtypes)
    print(rec.columns)

    rec = rec.select(pl.col("*").exclude("id","contributor_id", "submitted"))
    #elimino colonne che non mi servono 

    print(rec.glimpse(return_as_string=True))
    #! i tag, i valori nutritivi, gli step e gli ingredienti sono str, quando vorrei li leggesse come liste
    #studiamo un po' i dati 

    print(rec.select(pl.col("ingredients"))[1].glimpse()) #sono liste di stringhe

    print(rec.select(pl.col("nutrition").cast(pl.List,strict=False))) #se provo a trasformare mi crea valori null

    print(rec.select(pl.col("ingredients").cast(pl.List,strict=False))) #se provo a trasformare mi crea valori null

    str.split("")
    #provo a scomporre e ricomporre le liste
    rec = rec.with_columns(pl.col("ingredients","tags","steps", "nutrition").str.replace_all(r"[\[\]']", "").str.split(","))
    print(rec.select(pl.col("tags")))

    # ora sono corrette 
    #*ho il problema che mi ha preso le virgolette singole '' come caratteri, rimuovo anche quelle (aggiunto sopra)
    #devo rendere i valori nutritivi degli int 
    print(rec.head())
    print(rec.select("nutrition"))




