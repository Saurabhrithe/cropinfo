
import requests
import pandas as pd

def load(place, freq):
    df = pd.read_csv( 'Weather.csv', parse_dates=['Time'], index_col=['Time'])
    df_rain = pd.read_csv('Weather_rain.csv')

    place_data1 = df[df['Place'] == place].drop( ['Month'], axis=1 )
    place_data2 = df_rain[df_rain['DISTRICT'] == place.upper()]

    labels_M = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]
    labels_Q = [
        'JAN-MAR', 'APR-JUN', 'JUL-SEP', 'OCT-DEC'
    ]

    l = list( set( df['Place'] ) )
    a, di = range( 1, len( l ) ), {}
    for k, v in zip( a, l ):
        di[v] = k
    df['Place'] = df['Place'].replace( di )

    D1 = place_data1.groupby( ['Time'] )['Humidity', 'Temperature'].mean()

    if freq == "M":

        D1 = round( D1.resample( 'M' ).mean(), 2 )
        place_data2 = [place_data2.iloc[0][m] for m in labels_M]

        labels = labels_M

    else:
        D1 = round( D1.resample( 'QS' ).mean(), 2 )
        place_data2 = [place_data2.iloc[0][m] for m in labels_Q]
        labels = labels_Q


    values1 = list(D1['Humidity'])
    values2 = list(D1['Temperature'] )
    values3 = place_data2

    return [values1, values2, labels], values3

def live_weather(place):
    api_key = "516b385972ffc07a66437095d39ab15d"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + place

    response = requests.get( complete_url )
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temp_mx = round((y["temp_max"] - 273.15), 2)
        temp_mi = round((y["temp_min"] - 273.15), 2)
        feels_like = round( (y["feels_like"] - 273.15), 2)
        humidity = y["humidity"]
        #print(y)
        return temp_mi, temp_mx, feels_like, humidity

    else:
        return None
