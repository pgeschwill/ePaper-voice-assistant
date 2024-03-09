from datetime import datetime
from services.audio import audio_service_wrapper as asw
from time import sleep
import infoscreen_service_wrapper as isw
import json

if __name__ == '__main__':

    with open("/config/config.json") as config_file:
        config = json.load(config_file)
    
    infoscreen_service_wrapper = isw.InfoScreenServiceWrapper(config)
    audio_service_wrapper = asw.AudioServiceWrapper()
    while True:
        now = datetime.now()
        current_hour = int(now.strftime("%H"))
        if current_hour == config["infoscreen"]["screensaver_hour"]:
            print("Running screensaver...")
            infoscreen_service_wrapper.display_screensaver()
        print("Refreshing screen...")
        try:
            infoscreen_service_wrapper.refresh_all_panels(config)
        except Exception as e:
            print(e)
            audio_service_wrapper.generate_response("Beim Aktualisieren der Infos ist ein Fehler aufgetreten.")
        sleep(config["infoscreen"]["refresh_interval"])
