#entrypoint file

import streamlit as st

homepage = st.Page(
    "homepage.py", title="FOODOMNIA", icon=":material/local_dining:", default=True
)

recipes = st.Page("recipes.py", title="Recipes", icon=":material/receipt_long:")

if 'recipe' not in st.session_state:
    st.session_state.recipe = "random"

recipe = st.Page("recipe.py", title=f" {st.session_state.recipe} recipe", icon=":material/menu_book:")


pg = st.navigation([homepage, recipes, recipe])
pg.run()
