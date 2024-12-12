import streamlit as st
import functions

st.title("list of recipes")

for i in functions.recipes_list():
    st.write(i)


#names = datasets.get_rec()["name"].to_list()
#st.markdown("### Recipes:")
#st.markdown("\n".join([f"- {item}" for item in names]), infer_schema_length=10000)
