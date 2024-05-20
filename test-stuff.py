import json
import requests
from datetime import datetime
import numpy as np
from services.audio import audio_service_wrapper as asw
audio_service_wrapper = asw.AudioServiceWrapper()

# URL = "https://api.openweathermap.org/data/2.5/forecast?q=Heidelberg,DE&units=metric&appid=841264421e32d505ae13df46f7337c50&cnt=8&lang=DE"

# response = requests.get(URL)
# response.raise_for_status()

# data = response.json()

# data_length = len(data["list"])
# temp_forecast = []
# precip_forecast = []
# rain_forecast = [0] * data_length

# print(rain_forecast)
# for i in range(0, data_length):
#     temp_forecast.append(round(data["list"][i]["main"]["temp"], 1))
#     precip_forecast.append(round(data["list"][i]["pop"] * 100))
#     if "rain" in data["list"][i]:
#             rain_forecast[i] = round(data["list"][i]["rain"]["3h"], 1)
# forecast_data = {
#     "temp": temp_forecast,
#     "precip": precip_forecast,
#     "rain": rain_forecast
# }
# file = 'forecast_data.json' 
# with open(file, 'w') as f: 
#     json.dump(forecast_data, f, indent=4)

# print(forecast_data)

# x = np.arange(len(forecast_data["temp"]))
# print(x)

# now = datetime.now()
# current_hour = int(now.strftime("%H"))
# num_hours = 24
        
# # Create a time range in hours
# time_range = (np.arange(current_hour, current_hour + num_hours, step=3) % num_hours)
# print(time_range)

# response = requests.get("http://127.0.0.1:5000/play_wav?filename=shit")
# print(response)
# print(response.content)

response = audio_service_wrapper.play_wav("current_weather_info")
print(response.ok)
print(response.content)