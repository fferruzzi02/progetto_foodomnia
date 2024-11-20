import polars as pl
#import kagglehub #? perché ??? Ha senso usare questo o è un problema se i dati vengono cambiati???

"""
path = kagglehub.dataset_download("utsavdey1410/food-nutrition-dataset")

print("Path to dataset files:", path)"""

#todo: aprire i 5 datasets e unirli insieme in uno unico 
#leggo i 5 datasets 
nutri1 = pl.read_csv("nutri/FOOD-DATA-GROUP1.csv")
nutri2 = pl.read_csv("nutri/FOOD-DATA-GROUP2.csv")
nutri3 = pl.read_csv("nutri/FOOD-DATA-GROUP3.csv")
nutri4 = pl.read_csv("nutri/FOOD-DATA-GROUP4.csv")
nutri5 = pl.read_csv("nutri/FOOD-DATA-GROUP5.csv")

#li concateno in uno unico, così ho una sola tabella
nutri = pl.concat([nutri1,nutri2,nutri3,nutri4,nutri5])

#studiamo un po' il dataset 
print(nutri.glimpse(return_as_string=True)) 
print(nutri.describe())