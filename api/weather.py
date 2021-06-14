from math import ceil
import requests
import pandas as pd
import datetime
import numpy as np

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
        'NT' : 1 if states[response['state_code']] == 'NR' else 0,
        'QL' : 1 if states[response['state_code']] == 'QL' else 0, 
        'SA' : 1 if states[response['state_code']] == 'SA' else 0, 
        'TA' : 1 if states[response['state_code']] == 'TA' else 0, 
        'VI' : 1 if states[response['state_code']] == 'VI' else 0, 
        'WA' : 1 if states[response['state_code']] == 'WA' else 0
    }
    
    # print(info)
    
    data = pd.read_csv('../wildfire_prediction/data/wfz_data.csv',index_col=0)
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
    
    data = get_weather(i, location)
    
    fire_binary = np.array([data[col] for col in columns_binary])
    
    return pd.DataFrame(fire_size.reshape(-1, len(fire_size)), columns=columns_size), \
        pd.DataFrame(fire_binary.reshape(-1, len(fire_size)), columns=columns_binary)
