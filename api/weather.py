import requests

def get_weather(i, location):
    
    url = 'https://api.weatherbit.io/v2.0/forecast/daily'
    params = {
        'key': '84b60447ea064fd89d7365f1940bc0eb',
        'units': 'M',
        'days': 2,
        'city': location,
        'country': 'AU'
    }
    response = requests.get(url, params=params).json()
    
    temp_min = response['data'][i]['min_temp']
    temp_max = response['data'][i]['max_temp']
    temp_mean = response['data'][i]['temp']
    precipitation = response['data'][i]['precip']
    uv = response['data'][i]['uv']
    wind_speed = response['data'][i]['wind_spd']
    humidity = response['data'][i]['rh']
    
    return temp_min, temp_max, temp_mean, precipitation, uv, wind_speed, humidity
    