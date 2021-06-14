import requests

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
        '02': '',
        '03': 'NT',
        '04': '',
        '05': 'SA',
        '06': '',
        '07': '',
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
    
    return info
    