import json
import os
from datetime import datetime
from time import sleep

import requests

from services.audio import audio_service_wrapper as asw
from services.infoscreen import infoscreen_service_wrapper as isw

with open("/config/config.json") as config_file:
    config = json.load(config_file)

INFOSCREEN_SERVICE_WRAPPER = isw.InfoScreenServiceWrapper(config)
AUDIO_SERVICE_WRAPPER = asw.AudioServiceWrapper()
WEATHER_SERVICE_URL = (
    f"http://{os.environ['weather_service_name']}:{os.environ['weather_service_port']}"
)


def generate_weather_announcement_wav():
    print("Generating weather announcement audio file...")
    response = requests.get(WEATHER_SERVICE_URL + "/get_weather_announcement_text")
    AUDIO_SERVICE_WRAPPER.generate_wav(response.content, "current_weather_info.wav")


if __name__ == "__main__":
    while True:
        now = datetime.now()
        current_hour = int(now.strftime("%H"))
        if current_hour == config["infoscreen"]["screensaver_hour"]:
            print("Running screensaver...")
            INFOSCREEN_SERVICE_WRAPPER.display_screensaver()
        try:
            print("Refreshing screen...")
            INFOSCREEN_SERVICE_WRAPPER.refresh_all_panels(config)
            generate_weather_announcement_wav()

        except Exception as e:
            print(e)
            AUDIO_SERVICE_WRAPPER.generate_response(
                "Beim Aktualisieren der Infos ist ein Fehler aufgetreten."
            )
        sleep(config["general"]["refresh_interval"])
