import streamlit as st
from streamlit_folium import folium_static
import folium
import pydeck as pdk

st.markdown("""

    # Wildfire prediction for Australia

    ## Data Science group project 
    ## Le-Wagon Amsterdam batch 627
    ## Felix Hermes, Miguel Ferreira & Krystyna Kooi
    """)

st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/satellite-streets-v11",
        initial_view_state={
            "latitude": -25.2744,
            "longitude": 133.7751,
            "zoom": 3.2,
            "pitch": 50,
        },

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

