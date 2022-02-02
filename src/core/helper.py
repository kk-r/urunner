
from fastapi import HTTPException
import json


import requests


def get_weather_condition_data(city_name):
    url = 'https://samples.openweathermap.org/data/2.5/weather'

    params = dict(
        appid='b1b15e88fa797225412429c1c50c122a1',
        q=city_name
    )
    try:
        resp = requests.get(url=url, params=params)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise HTTPException(status_code=500, detail=f'{e}')
    
    data = resp.json() 
    
    return data['weather'][0] if 'weather' in data else {}
    