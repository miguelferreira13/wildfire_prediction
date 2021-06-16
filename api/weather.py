from math import ceil
import requests
import pandas as pd
import datetime
import numpy as np
import os

from requests.api import get


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def get_weather(i, location):
    
    url = 'https://api.weatherbit.io/v2.0/forecast/daily'
    params = {
        'key': '84b60447ea064fd89d7365f1940bc0eb',
        'units': 'M',
        'days': i,
        'city': location,
        'country': 'AU'
    }
    response = requests.get(url, params=params).json()
    
    states = {
        '01': '',
        '02': 'NSW',
        '03': 'NT',
        '04': 'QL',
        '05': 'SA',
        '06': 'TA',
        '07': 'VI',
        '08': 'WA'
    }
    
    info = {
        'min() Temperature' : response['data'][i-1]['min_temp'],
        'max() Temperature' : response['data'][i-1]['max_temp'],
        'mean() Temperature' : response['data'][i-1]['temp'],
        'mean() Precipitation' : response['data'][i-1]['precip'],
        'mean() SolarRadiation' : response['data'][i-1]['uv'],
        'mean() WindSpeed' : response['data'][i-1]['wind_spd'],
        'mean() RelativeHumidity' : response['data'][i-1]['rh'],
        'NSW' : 1 if states[response['state_code']] == 'NSW' else 0,
        'NT' : 1 if states[response['state_code']] == 'NT' else 0,
        'QL' : 1 if states[response['state_code']] == 'QL' else 0, 
        'SA' : 1 if states[response['state_code']] == 'SA' else 0, 
        'TA' : 1 if states[response['state_code']] == 'TA' else 0, 
        'VI' : 1 if states[response['state_code']] == 'VI' else 0, 
        'WA' : 1 if states[response['state_code']] == 'WA' else 0
    }
    
    # print(info)
    
    root_path = os.path.dirname(os.path.abspath(os.path.curdir))
    data_folder_path = os.path.join(root_path, 'wildfire_prediction')
    data_file_path = os.path.join(data_folder_path, 'wfz_data.csv')

    data = pd.read_csv(data_file_path, index_col=0)
    month = datetime.datetime.today().month
    state = states[response['state_code']]
    
    filtered_data = data[(data.index == month) & (data.Region == state)]
    values = {f'{col}': filtered_data[col].values[0] for col in filtered_data.columns}
    
    # print(values)
    
    return merge_two_dicts(info, values)

def size(i, location):
    
    columns_size = ['count()[unit: km^2]', 'max() Temperature', 'mean() Precipitation',
        'mean() RelativeHumidity', 'mean() SolarRadiation',
        'mean() Temperature', 'mean() WindSpeed', 'min() Temperature',
        'Vegetation_index_mean', 'Shrubs', 'Herbaceous vegetation',
        'Cultivated and managed vegetation/agriculture (cropland)',
        'Urban / built up', 'Bare / sparse vegetation',
        'Permanent water bodies', 'Herbaceous wetland', 'Open sea', 'Forest',
        'NSW', 'NT', 'QL', 'SA', 'TA', 'VI', 'WA']
    
    data = get_weather(i, location)
    
    fire_size = np.array([data[col] for col in columns_size])
    
    columns_binary = ['count()[unit: km^2]', 'mean() Temperature', 'max() Temperature',
        'min() Temperature', 'mean() WindSpeed',
        'mean() RelativeHumidity', 'mean() Precipitation', 'mean() SolarRadiation',
        'Vegetation_index_mean', 'Shrubs', 'Herbaceous vegetation',
        'Cultivated and managed vegetation/agriculture (cropland)',
        'Urban / built up', 'Bare / sparse vegetation',
        'Permanent water bodies', 'Herbaceous wetland', 'Open sea',
        'NSW', 'NT', 'QL', 'SA', 'TA', 'VI', 'WA', 'Forest']
    
    fire_binary = np.array([data[col] for col in columns_binary])
    
    return pd.DataFrame(fire_size.reshape(-1, len(fire_size)), columns=columns_size), \
        pd.DataFrame(fire_binary.reshape(-1, len(fire_size)), columns=columns_binary)
        
        
        
def get_all_states(i=1):
    
    root_path = os.path.dirname(os.path.abspath(os.path.curdir))
    data_folder_path = os.path.join(root_path, 'wildfire_prediction/wildfire_prediction', 'data')
    data_file_path = os.path.join(data_folder_path, 'wfz_data.csv')

    data = pd.read_csv(data_file_path, index_col=0)
    month = datetime.datetime.today().month
    
    
    coordinates = [{'state': 'NSW', 'coordinates': [-31.840233, 145.612793]},
               {'state': 'NT', 'coordinates': [-19.491411, 132.550964]},
               {'state': 'QL', 'coordinates': [-20.917574, 142.702789]},
               {'state': 'SA', 'coordinates': [-30.000233, 136.209152]},
               {'state': 'TA', 'coordinates': [-41.640079, 146.315918]},
               {'state': 'VI', 'coordinates': [-37.020100, 144.964600]},
               {'state': 'WA', 'coordinates': [-25.042261, 117.793221]}]
    
    all_states = []
    url = 'https://api.weatherbit.io/v2.0/forecast/daily'
    for state in coordinates: 
        lat = state['coordinates'][0]
        lon = state['coordinates'][0]
        params = {
        'key': '84b60447ea064fd89d7365f1940bc0eb',
        'units': 'M',
        'days': i,
        'lat': lat,
        'lon': lon,
        'country': 'AU'
        }
        response = requests.get(url, params=params).json()
        
        info = {
        'min() Temperature' : response['data'][i-1]['min_temp'],
        'max() Temperature' : response['data'][i-1]['max_temp'],
        'mean() Temperature' : response['data'][i-1]['temp'],
        'mean() Precipitation' : response['data'][i-1]['precip'],
        'mean() SolarRadiation' : response['data'][i-1]['uv'],
        'mean() WindSpeed' : response['data'][i-1]['wind_spd'],
        'mean() RelativeHumidity' : response['data'][i-1]['rh'],
        'NSW' : 1 if state['state'] == 'NSW' else 0,
        'NT' : 1 if state['state'] == 'NT' else 0,
        'QL' : 1 if state['state'] == 'QL' else 0, 
        'SA' : 1 if state['state'] == 'SA' else 0, 
        'TA' : 1 if state['state'] == 'TA' else 0, 
        'VI' : 1 if state['state'] == 'VI' else 0, 
        'WA' : 1 if state['state'] == 'WA' else 0
        }
        
        all_states.append(info)
        
    columns_size = ['count()[unit: km^2]', 'max() Temperature', 'mean() Precipitation',
        'mean() RelativeHumidity', 'mean() SolarRadiation',
        'mean() Temperature', 'mean() WindSpeed', 'min() Temperature',
        'Vegetation_index_mean', 'Shrubs', 'Herbaceous vegetation',
        'Cultivated and managed vegetation/agriculture (cropland)',
        'Urban / built up', 'Bare / sparse vegetation',
        'Permanent water bodies', 'Herbaceous wetland', 'Open sea', 'Forest',
        'NSW', 'NT', 'QL', 'SA', 'TA', 'VI', 'WA']
    
    columns_binary = ['count()[unit: km^2]', 'mean() Temperature', 'max() Temperature',
        'min() Temperature', 'mean() WindSpeed',
        'mean() RelativeHumidity', 'mean() Precipitation', 'mean() SolarRadiation',
        'Vegetation_index_mean', 'Shrubs', 'Herbaceous vegetation',
        'Cultivated and managed vegetation/agriculture (cropland)',
        'Urban / built up', 'Bare / sparse vegetation',
        'Permanent water bodies', 'Herbaceous wetland', 'Open sea',
        'NSW', 'NT', 'QL', 'SA', 'TA', 'VI', 'WA', 'Forest']
    
    
    merged_dict = []
    for index, s in enumerate(all_states):
        
        filtered_data = data[(data.index == month) & (data.Region == coordinates[index]['state'])]
        values = {f'{col}': filtered_data[col].values[0] for col in filtered_data.columns}
        merged_dict.append(merge_two_dicts(all_states[index], values))
    
    
    # return pd.DataFrame(fire_size.reshape(-1, len(fire_size)), columns=columns_size), \
    #     pd.DataFrame(fire_binary.reshape(-1, len(fire_size)), columns=columns_binary)
    data_frame = pd.DataFrame(merged_dict)
    
    fire_size = data_frame[columns_size]
    fire_binary = data_frame[columns_binary]
    
    return fire_size, fire_binary


print(size(1, 'sydney'))