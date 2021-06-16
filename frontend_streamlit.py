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

BUCKET_NAME= 'wildfires_le_wagon'
STORAGE_LOCATION4 = 'merged_data/Australian_cities.csv'
client = storage.Client()
bucket = client.get_bucket(BUCKET_NAME)
blob = bucket.blob(STORAGE_LOCATION4)
blob.download_to_filename('Australian_cities.csv')

df = pd.DataFrame(data=coordinates, columns=['state', 'coordinates'])
root_path = os.path.dirname(os.path.abspath(os.path.curdir))
data_folder_path = os.path.join(root_path, 'wildfire_prediction')
data_file_path = os.path.join(data_folder_path, 'Australian_cities.csv')

data = pd.read_csv('Australian_cities.csv')
st.set_page_config(page_title="My Wildfire prediction",layout='wide')

st.markdown("""
    # Wildfire prediction for Australia
    ## Data Science group project, Le-Wagon Amsterdam batch 627
    ### Felix Hermes, Miguel Ferreira & Krystyna Kooi
    
    ---
    
    
    """)

col1, col2, col3, col4 = st.beta_columns([1,4,10,1])

col1.markdown("")
col1.markdown("")
col1.markdown(":cityscape:")
col1.markdown("")
col1.markdown("")
col1.markdown("")
col1.markdown("")
col1.markdown(":stopwatch:")
CITY = col2.selectbox('Select a city', tuple(['Showing sates (default)'] + list(data['city'])))
# CITY = col2.text_input('Forecast', 'Type in an Australian city name')

HORIZON = col2.slider('Horizon', 1, 16)

# if CITY == 'Type in an Australian city name':
#     col2.write('Waiting for Forecast')
# elif  CITY.title() in list(data['city']):
#     col2.write(f'The forecast for {CITY.title()} is')
#     #Weather API
# else:
#     col2.write('This is not a city in Australia.')

button_pressed = False
if CITY != 'Showing sates (default)':
    button_pressed = True

horizon = 1 if HORIZON == None or HORIZON == 'Type in the amount of days' else int(HORIZON)
data_api = predict_fire(horizon)
sizes = data_api['size']
probabilities = data_api['probability']

basemaps = {
        'Google Maps': folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Maps',
            overlay = True,
            control = True
        ),
        'Google Satellite': folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Satellite',
            overlay = True,
            control = True
        ),
        'Google Terrain': folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Terrain',
            overlay = True,
            control = True
        ),
        'Google Satellite Hybrid': folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Satellite',
            overlay = True,
            control = True
        ),
        'Esri Satellite': folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = True,
            control = True
        )
    }


with col3:
    
    if not button_pressed:
        
        coordinates_aus = [-25.2744, 133.7751]
        m = folium.Map(location=coordinates_aus, zoom_start=4.3)
    
        for i in range(7):
            folium.Circle(coordinates[i]['coordinates'],
                        fill=True,
                        fill_color='crimson',
                        color='crimson',
                        radius=sizes[i]*800,
                        popup=f"State: {coordinates[i]['state'].upper()}\n\
                            Fire_probability: {probabilities[i][1]*0.8:.1%}\n\
                            Estimated_size: {sizes[i]:.1f} km_2").add_to(m)
        # Add custom basemaps
        basemaps['Google Maps'].add_to(m)
        basemaps['Google Satellite Hybrid'].add_to(m)
        basemaps['Google Terrain'].add_to(m)
        folium_static(m)

    

    
    if button_pressed:
        city_api = predict_city(horizon, CITY)
        sizes_city = city_api['size'][0]
        probabilities_city = city_api['probability'][0][1]
        city_coordinates = list(data[data.city == CITY.title()][['lat', 'lng']].values)[0]
        
        
        m = folium.Map(location=city_coordinates, zoom_start=8.5)
        
        folium.Circle(list(city_coordinates),
                      fill=True,
                      fill_color='crimson',
                      color='crimson',
                      radius=sizes_city*800,
                      popup=f'City: {CITY.title()}\n\
                          Fire_probability: {probabilities_city:.1%}\n\
                          Estimated_size: {sizes_city*0.8:.1f} km_2').add_to(m)
        basemaps['Google Maps'].add_to(m)
        basemaps['Google Satellite Hybrid'].add_to(m)
        basemaps['Google Terrain'].add_to(m)
    
        folium_static(m)


# print(predict_fire(horizon)['size'])