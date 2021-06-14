import streamlit as st
import pandas as pd
import pydeck as pdk
import csv
import json
# from streamlit_folium import folium_static
# import geopandas as gpd
# import folium
# from folium.plugins import TimeSliderChoropleth
# import seaborn as sns
# import plotly.express as px

# with open('../wildfire_prediction/Australian_cities.json') as f:
#     data = json.load(f)
Cities = pd.read_csv("../wildfire_prediction/Australian_cities.csv")
df = pd.DataFrame(data=Cities, columns=['city', 'lat', 'lng', 'admin_name'])

st.markdown("""
    # Wildfire prediction for Australia
    ## Data Science group project, Le-Wagon Amsterdam batch 627
    ### Felix Hermes, Miguel Ferreira & Krystyna Kooi
    """)

title = st.text_input('Forecast', 'Type in an Australian city name')

if title == 'Type in an Australian city name':
    st.write('Waiting for Forecast')
elif  title in list(df['city']):
    st.write(f'The forecast for {title} is')
else:
    st.write('This is not a city in Australia')


st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/satellite-streets-v11",
        initial_view_state={
            "latitude": -25.2744,
            "longitude": 133.7751,
            "zoom": 3.2,
            "pitch": 50,
        }))

# direction = st.radio('Select map', ('Fire', 'right', 'bottom', 'left'))

# st.write(direction)

# if direction == 'top':
#     st.write('🔼')
# elif direction == 'right':
#     st.write('▶️')
# elif direction == 'bottom':
#     st.write('🔽')
# else:
#     st.write('◀️')

# coordinates_states = {'NSW':[-32.0948, 147.0100], 'NT': [-19.2300, 133.2128] ,'SA': [-30.0330, 135.4548],\
#          'QL': [-22.2913, 144.2554], 'VI': [36.5115, 144.1652], 'TA': [-42.0117, 146.3536], 'WA': [-25.1941, 122.1754]}
#         # layers=[
        #     pdk.Layer(
        #         "HexagonLayer",
        #         data=data,
        #         get_position=["lon", "lat"],
        #         radius=100,
        #         elevation_scale=4,
        #         elevation_range=[0, 1000],
        #         pickable=True,
        #         extruded=True,
        #     ),
        # ]
    # ))

# "# streamlit-folium"

# with st.echo():

#     map_australia = folium.Map(location=[-25.2744, 133.7751], 
#     tiles= 'https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia3J5c2NhZ2UiLCJhIjoiY2twcWwzajE3MDh1YzJ2czhvdnI1bDBubCJ9.nAG4P8C2gctaVIhBhH3Z6w', 
#     attr = "blabla",
#     zoom_start=3.2)
    
#     folium_static(map_australia)
