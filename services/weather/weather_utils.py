from datetime import datetime as dt
import pytz

def degrees_to_geographic_direction(deg):
    if deg > 337.5: return "N"
    if deg > 292.5: return "NW"
    if deg > 247.5: return "W"
    if deg > 202.5: return "SW"
    if deg > 157.5: return "S"
    if deg > 122.5: return "SE"
    if deg >  67.5: return "E"
    if deg >  22.5: return "NE"
    return "N"

def parse_weather_data(data, timeformat, timezone):

    # Sunrise and Sunset
    if timeformat == "12h":
        sunrise = dt.fromtimestamp(data['sys'].get('sunrise'), tz=pytz.timezone(timezone)).strftime('%I:%M %p')
        sunset  = dt.fromtimestamp(data['sys'].get('sunset'), tz=pytz.timezone(timezone)).strftime('%I:%M %p')
    else:
        sunrise = dt.fromtimestamp(data['sys'].get('sunrise'), tz=pytz.timezone(timezone)).strftime('%H:%M')
        sunset  = dt.fromtimestamp(data['sys'].get('sunset'), tz=pytz.timezone(timezone)).strftime('%H:%M')

    # Rain and Snow
    rain = {}
    if "rain" in data:
        rain.update({"1h": data["rain"].get("1h")})
        rain.update({"3h": data["rain"].get("3h")})
    
    snow = {}
    if "snow" in data:
        snow.update({"1h": data["snow"].get("1h")})
        snow.update({"3h": data["snow"].get("3h")})

    # Wind
    wind = {
        "dir": degrees_to_geographic_direction(data['wind'].get('deg')),
        "speed": int(round(data['wind'].get('speed')))
    }

    weather_data = {
        "description": data['weather'][0].get('description'),
        "humidity": data['main'].get('humidity'),
        "temp_cur": int(round(data['main'].get('temp'))),
        "temp_min": int(round(data['main'].get('temp_min'))),
        "temp_max": int(round(data['main'].get('temp_max'))),
        "temp_feels_like": int(round(data['main'].get('feels_like'))),
        "sunrise": sunrise,
        "sunset": sunset,
        "rain": rain,
        "snow": snow,
        "wind": wind,
        "icon": data['weather'][0].get('icon')
    }

    return weather_data

def parse_weather_forecast_data(data):

    data_length = len(data["list"])
    temp_forecast = []
    precip_forecast = []
    icon_forecast = []
    rain_forecast = [0] * data_length

    for i in range(0, data_length):
        temp_forecast.append(round(data["list"][i]["main"]["temp"], 1))
        precip_forecast.append(round(data["list"][i]["pop"] * 100))
        icon_forecast.append(data["list"][i]["weather"][0]["icon"])
        if "rain" in data["list"][i]:
            rain_forecast[i] = round(data["list"][i]["rain"]["3h"], 1)

    forecast_data = {
        "temp": temp_forecast,
        "precip": precip_forecast,
        "rain": rain_forecast,
        "icon": icon_forecast
    }
    
    return forecast_data