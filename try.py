import kagglehub

kagglehub.login() 
path = kagglehub.dataset_download("shuyangli94/food-com-recipes-and-user-interactions")

path1 = path + "/interactions_train.csv"
import polars as pl
albero = pl.read_csv(path1)
