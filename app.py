import streamlit as st 
st.set_page_config(page_title="FOODOMNIA", page_icon=":material/local_dining:")
pg = st.navigation([st.Page("homepage.py", title = "Foodomnia", icon =":material/home:"),
                     st.Page("page_2.py",title = "title", icon =":material/food_bank:")])

pg.run()