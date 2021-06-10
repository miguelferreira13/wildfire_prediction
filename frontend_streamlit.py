import streamlit as st
from streamlit_folium import folium_static
import folium

st.markdown("""

    # Wildfire prediction for Australia

    ## Data Science group project 
    ## Le-Wagon Amsterdam batch 627
    ## Felix Hermes, Miguel Ferreira & Krystyna Kooi
    """)

"# streamlit-folium"

with st.echo():

    map_australia = folium.Map(location=[133.58514407899872, -27.740477149652342], zoom_start=3)

    folium_static(map_australia)

