import json
import os

import requests
import weather_utils
from flask import Flask, jsonify, redirect

app = Flask(__name__)

with open("/config/config.json") as config_file:
    config = json.load(config_file)
API_KEY = config["weather"]["api_key"]
CITY = config["weather"]["city"]
UNITS = config["weather"]["units"]
TIMEFORMAT = config["general"]["timeformat"]
TIMEZONE = config["general"]["timezone"]
NUMBER_OF_VALUES = config["weather"]["number_of_values"]


@app.route("/health", methods=["GET"])
def health():
    return jsonify(success=True)


@app.route("/get_weather_data", methods=["GET"])
def get_weather_data():
    url = "http://api.openweathermap.org/data/2.5/weather"
    response = requests.get(
        "{}?q={}&units={}&appid={}".format(url, CITY, UNITS, API_KEY)
    )
    response.raise_for_status()

    return weather_utils.parse_weather_data(response.json(), TIMEFORMAT, TIMEZONE)


@app.route("/get_weather_forecast_data", methods=["GET"])
def get_weather_forecast_data():
    url = "https://api.openweathermap.org/data/2.5/forecast"
    response = requests.get(
        "{}?q={}&units={}&appid={}&cnt={}".format(
            url, CITY, UNITS, API_KEY, NUMBER_OF_VALUES
        )
    )
    response.raise_for_status()

    return weather_utils.parse_weather_forecast_data(response.json())


@app.route("/get_weather_announcement_text", methods=["GET"])
def get_weather_announcement_text():
    weather_data = get_weather_data()
    weather_forecast_data = get_weather_forecast_data()
    announcement_text = (
        f"Es hat aktuell {weather_data['temp_cur']}, gefühlt {weather_data['temp_feels_like']} Grad. "
        f"Die Temperatur liegt heute zwischen {round(min(weather_forecast_data['temp']))} und {round(max(weather_forecast_data['temp']))} Grad. "
        f"Die Luftfeuchtigkeit liegt bei {weather_data['humidity']} Prozent."
    )

    return announcement_text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["weather_service_port"])
