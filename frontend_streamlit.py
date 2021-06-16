import streamlit as st
import pandas as pd
import pydeck as pdk
import csv
import json
import matplotlib.pyplot as plt
import os
import folium
from streamlit_folium import folium_static
from google.cloud import storage
from api.fast import predict_fire, predict_city

coordinates = [{'state': 'NSW', 'coordinates': [-31.840233, 145.612793]},
               {'state': 'NT', 'coordinates': [-19.491411, 132.550964]},
               {'state': 'QL', 'coordinates': [-20.917574, 142.702789]},
               {'state': 'SA', 'coordinates': [-30.000233, 136.209152]},
               {'state': 'TA', 'coordinates': [-41.640079, 146.315918]},
               {'state': 'VI', 'coordinates': [-37.020100, 144.964600]},
               {'state': 'WA', 'coordinates': [-25.042261, 117.793221]}]
#storage_client = storage.Client.from_service_account_json("/home/kryscage/code/kryscage/fine-citadel-311213.json")
#bucket = storage_client.get_bucket('wildfires_le_wagon')
#data = bucket.get_blob('Australian_cities')
# STORAGE_LOCATION3 = ‘merged_data/Australian_cities.csv’
# Cities = pd.read_csv(f”gs://{STORAGE_LOCATION3}“)
df = pd.DataFrame(data=coordinates, columns=['state', 'coordinates'])
root_path = os.path.dirname(os.path.abspath(os.path.curdir))
data_folder_path = os.path.join(root_path, 'wildfire_prediction')
data_file_path = os.path.join(data_folder_path, 'Australian_cities.csv')

data = pd.read_csv(data_file_path)

st.markdown("""
    # Wildfire prediction for Australia
    ## Data Science group project, Le-Wagon Amsterdam batch 627
    ### Felix Hermes, Miguel Ferreira & Krystyna Kooi
    """)

CITY = st.text_input('Forecast', 'Type in an Australian city name')
HORIZON = st.text_input('Horizon', 'Type in the amount of days')

if CITY == 'Type in an Australian city name':
    st.write('Waiting for Forecast')
elif  CITY in list(data['city']):
    st.write(f'The forecast for {CITY} is')
    #Weather API
else:
    st.write('This is not a city in Australia')

button_pressed = False
if st.button('click me'):
    button_pressed = True


#layer = pdk.Layer(
           # "ScatterplotLayer",
            #data = df,
        #    pickable=True,
         #   opacity=0.8, #input here for probability
          #  stroked=True,
           # filled=True,
            #radius_min_pixels=1,
        #    radius_max_pixels=100000,
         #   line_width_min_pixels=1,
          #  get_position=coordinates,
           # get_radius='normValue', #input will be the firesize
            #get_fill_color=[255, 140, 0],
            #get_line_color=[0, 0, 0]
       # )
#Key = 'pk.eyJ1Ijoia3J5c2NhZ2UiLCJhIjoiY2twcWwzajE3MDh1YzJ2czhvdnI1bDBubCJ9.nAG4P8C2gctaVIhBhH3Z6w'

#st.pydeck_chart(pdk.Deck(
    #    map_style='mapbox://styles/mapbox/satellite-streets-v11',
     #   layers = [layer],
      #  initial_view_state=pdk.ViewState(
       #     mapboxApiAccessToken= Key,
        #    latitude = -25.2744,
         #   longitude =  133.7751,
          #  zoom =  3.2,
           # pitch =  50,
     #   )
   # ))

# "# streamlit-folium"

# with st.echo():

#     map_australia = folium.Map(location=[-25.2744, 133.7751], 
#     tiles= 'https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia3J5c2NhZ2UiLCJhIjoiY2twcWwzajE3MDh1YzJ2czhvdnI1bDBubCJ9.nAG4P8C2gctaVIhBhH3Z6w', 
#     attr = "blabla",
#     zoom_start=3.2)
    
#     folium_static(map_australia)

# coordinates_states = {'NSW':[-32.0948, 147.0100], 'NT': [-19.2300, 133.2128] ,'SA': [-30.0330, 135.4548],\
#          'QL': [-22.2913, 144.2554], 'VI': [36.5115, 144.1652], 'TA': [-42.0117, 146.3536], 'WA': [-25.1941, 122.1754]}


horizon = 1 if HORIZON == None or HORIZON == 'Type in the amount of days' else int(HORIZON)
data_api = predict_fire(horizon)
sizes = data_api['size']
probabilities = data_api['probability']




with st.map():
    coordinates_aus = [-25.2744, 133.7751]

    m = folium.Map(tiles='Stamen Terrain',location=coordinates_aus, zoom_start=3.5)
    for i in range(7):
        folium.Circle(coordinates[i]['coordinates'],
                      fill=True,
                      fill_color='crimson',
                      color='red',
                      radius=sizes[i]*500,
                      popup=f'The probability of a fire is {probabilities[i][1]:.1%}\
                          and an estimated size of {sizes[i]:.1f} km_2').add_to(m)
    
    if button_pressed:
        city_api = predict_city(horizon, CITY)
        sizes_city = city_api['size'][0]
        probabilities_city = city_api['probability'][0][1]
        city_coordinates = list(data[data.city == CITY.title()][['lat', 'lng']].values)[0]
        folium.Circle(list(city_coordinates),
                      fill=True,
                      fill_color='crimson',
                      color='red',
                      radius=sizes_city*500,
                      popup=f'The probability of a fire is {probabilities_city:.1%}\
                          and an estimated size of {sizes_city:.1f} km_2').add_to(m)
    
    folium_static(m)


# print(predict_fire(horizon)['size'])