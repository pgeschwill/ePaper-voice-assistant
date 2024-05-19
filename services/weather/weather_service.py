from flask import Flask, jsonify
import json
import requests
import weather_utils

app = Flask(__name__)

with open("/config/config.json") as config_file:
   config = json.load(config_file)
API_KEY = config["weather"]["api_key"]
CITY = config["weather"]["city"]
UNITS = config["weather"]["units"]
TIMEFORMAT = config["general"]["timeformat"]
TIMEZONE = config["general"]["timezone"]
NUMBER_OF_VALUES = 8

@app.route("/health", methods=['GET'])
def health():
    return jsonify(success=True)

@app.route("/get_weather_data", methods=['GET'])
def get_weather_data():

    url = "http://api.openweathermap.org/data/2.5/weather"
    response = requests.get('{}?q={}&units={}&appid={}'.format(url, CITY, UNITS, API_KEY))
    response.raise_for_status()

    return weather_utils.parse_weather_data(response.json(), TIMEFORMAT, TIMEZONE)

@app.route("/get_weather_forecast_data", methods=['GET'])
def get_weather_forecast_data():

    url = "https://api.openweathermap.org/data/2.5/forecast"
    response = requests.get('{}?q={}&units={}&appid={}&cnt='.format(url, CITY, UNITS, API_KEY, NUMBER_OF_VALUES))
    response.raise_for_status()

    return weather_utils.parse_weather_forecast_data(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)