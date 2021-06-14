import requests
import pandas as pd
import datetime

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
        'temp_min' : response['data'][i-1]['min_temp'],
        'temp_max' : response['data'][i-1]['max_temp'],
        'temp_mean' : response['data'][i-1]['temp'],
        'precipitation' : response['data'][i-1]['precip'],
        'uv' : response['data'][i-1]['uv'],
        'wind_speed' : response['data'][i-1]['wind_spd'],
        'humidity' : response['data'][i-1]['rh'],
        'state' : states[response['state_code']]
    }
    
    # print(info)
    
    data = pd.read_csv('../wildfire_prediction/data/wfz_data.csv',index_col=0)
    month = datetime.datetime.today().month
    
    filtered_data = data[(data.index == month) & (data.Region == 'TA')]
    values = {f'{col}': filtered_data['Region'].values[0] for col in filtered_data.columns}
    
    # print(values)
    
    return merge_two_dicts(info, values)

print(get_weather(1, 'sydney'))

