import json
from services.weather import weather_utils
from os import path

PATH_TO_THIS_FILE = path.dirname(path.abspath(__file__))

class TestWeatherUtils:

    def test_parse_weather_data(self):
        # ARRANGE
        input = json.loads("""{
                                "coord": {
                                    "lon": 8.6908,
                                    "lat": 49.4077
                                },
                                "weather": [
                                    {
                                    "id": 501,
                                    "main": "Rain",
                                    "description": "moderate rain",
                                    "icon": "10n"
                                    }
                                ],
                                "base": "stations",
                                "main": {
                                    "temp": 11.11,
                                    "feels_like": 10.6,
                                    "temp_min": 9.58,
                                    "temp_max": 12.75,
                                    "pressure": 1023,
                                    "humidity": 89
                                },
                                "visibility": 10000,
                                "wind": {
                                    "speed": 3.09,
                                    "deg": 180
                                },
                                "rain": {
                                    "1h": 2.3
                                },
                                "clouds": {
                                    "all": 75
                                },
                                "dt": 1707940121,
                                "sys": {
                                    "type": 2,
                                    "id": 2072664,
                                    "country": "DE",
                                    "sunrise": 1707892664,
                                    "sunset": 1707928881
                                },
                                "timezone": 3600,
                                "id": 12345678,
                                "name": "Berlin",
                                "cod": 200
                            }""")
        timeformat = "24h"
        timezone = "Europe/Berlin"

        # ACT
        actual_weather_data = weather_utils.parse_weather_data(input, timeformat, timezone)
    
        # ASSERT
        expected_weather_data = {
            "description": "moderate rain",
            "humidity": 89,
            "temp_cur": 11,
            "temp_min": 10,
            "temp_max": 13,
            "temp_feels_like": 11,
            "sunrise": "07:37",
            "sunset": "17:41",
            "rain": {"1h": 2.3, "3h": None},
            "snow": {},
            "wind": {"dir": "S", "speed": 3},
            "icon": "10n"
        }
        assert actual_weather_data == expected_weather_data

    def test_degrees_to_geographic_direction(self):
        # ARRANGE
        deg = 300

        # ACT
        actual_geographic_direction = weather_utils.degrees_to_geographic_direction(deg)
    
        # ASSERT
        assert actual_geographic_direction == "NW"

    def test_parse_weather_forecast_data(self):
        # ARRANGE
        inputFile = path.join(PATH_TO_THIS_FILE, "weather_forecast_data.json")
        with open(inputFile) as f:
            input = json.load(f)

        # ACT
        actual_weather_forecast_data = weather_utils.parse_weather_forecast_data(input)

        # ASSERT
        expected_weather_forecast_data = {
            "temp": [11.2, 10.6, 9.4, 8.2, 10.0, 13.3, 13.4, 11.3],
            "precip": [85, 54, 0, 0, 0, 0, 0, 0],
            "rain": [2.1, 0.3, 0, 0, 0, 0, 0, 0]
        }
        assert expected_weather_forecast_data == actual_weather_forecast_data
    