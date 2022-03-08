from random import randint
from time import sleep
from buildhat import Motor
from requests import get
import json
from pprint import pprint
import requests
import time 
import datetime


time.sleep(10)

timestamp = int(time.time())


weather = Motor('A')
amVpm = Motor('B')
weather.run_to_position(0,10)
amVpm.run_to_position(90,10)


api_key = '9514244124e33dadb217243cd5b2195b'
city = 'Medford'

weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}")

def printer(check,check2):
    city = 'Medford'
    print(f"The weather in {city} is: {check}, and period is: {check2}")

check = ''
sunrise,sunset = 0,0
isWindy = False
isTornado = False
if weather_data.json()['cod'] == '404':
    print("No City Found")
else:
    print(weather_data.json())
    temp = round(weather_data.json()['main']['temp'])

    # print(f"The weather in {city} is: {weather_data.json()['weather'][0]['main']}")
    check = weather_data.json()['weather'][0]['main']

    sunrise = weather_data.json()['sys']['sunrise']
    sunset = weather_data.json()['sys']['sunrise']
    windspeed = weather_data.json()['wind']['speed']
    if windspeed > 20 and windspeed < 70: 
        isWindy = True
        check = ''
    elif windspeed > 70: 
        isTornado = True
        check = ''



## control loop for the clock
state = {"Clear" : 0, "Clouds": 45 , "Atmosphere" : 45* 2 , "Rain" : 45*3,  "Thunder":45*4, "Snow": -(45*3), "Windy": -(45*2), "Tornado":-45 }
Timestate = {"am":0, "pm":180}
check2 = ''
while True:
    

    if timestamp > sunrise or  timestamp < sunset:
        # print("AM TRUE")
            amVpm.run_to_position(Timestate['am'],10)
            check2 = 'day'
        
        
    else:
        # print("PM TRUE")
        amVpm.run_to_position(Timestate['pm'],10)
        check2 = 'night'

    if check == 'Clear':
        weather.run_to_position(state['Clear'],10)  
        printer(check,check2)
    elif check == 'Clouds':
       weather.run_to_position(state['Clouds'],10)
       printer(check,check2) 
    elif check == 'Atmosphere':
        weather.run_to_position(state['Atmosphere'],10)
        printer(check,check2)
    elif check == 'Rain':
        weather.run_to_position(state['Rain'],10)
        printer(check,check2)
    elif check == 'Snow':
        weather.run_to_position(state['Snow'],10)
        printer(check,check2)
    elif check == 'Thunderstorm':
        weather.run_to_position(state['Thunder'],10)
        printer(check,check2) 
    if isWindy:
       weather.run_to_position(state['Windy'],10) 
       printer('Windy',check2)
    if isTornado:
        weather.run_to_position(state['Tornado'],10) 
        printer('Tornado',check2)

    break


