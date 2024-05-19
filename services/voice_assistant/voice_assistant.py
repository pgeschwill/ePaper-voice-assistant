from datetime import datetime
from services.audio import audio_service_wrapper as asw
from services.audio import speech_recognizer as sr
from services.google import google_service_wrapper as gsw
from services.infoscreen import infoscreen_service_wrapper as isw
import json
import re
import requests

class VoiceAssistant:
    def __init__(self, config):
        self.config = config
        self.wake_word = config["voice-assistant"]["wake_word"]
        self.shopping_list_clear_keyword = config["voice-assistant"]["shopping_list_clear_keyword"]
        self.shopping_list_doc_id = config["google"]["docs"]["shopping_list_doc_id"]
        self.shopping_list_pattern = config["voice-assistant"]["shopping_list_pattern"]
        self.shopping_list_recipe_pattern = config["voice-assistant"]["shopping_list_recipe_pattern"]
        self.mental_load_doc_id = config["google"]["docs"]["mental_load_doc_id"]
        self.mental_load_pattern = config["voice-assistant"]["mental_load_pattern"]
        self.update_panel_pattern = config["voice-assistant"]["update_panel_pattern"]
        self.volume = config["audio"]["initial_volume_percent"]
        self.weather_service_url = "http://weather-service:8000/"
        self.speech_recognizer = sr.SpeechRecognizer(config)
        self.audio_service_wrapper = asw.AudioServiceWrapper()
        self.google_service_wrapper = gsw.GoogleServiceWrapper(config)
        self.infoscreen_service_wrapper = isw.InfoScreenServiceWrapper(config)

    def listen(self):
        print("Listening...")
        self.audio_service_wrapper.set_output_volume(self.volume)

        while True:
            baseline_text = self.speech_recognizer.get_text_from_audio(phrase_time_limit=2)

            if self.wake_word in baseline_text:
                self.audio_service_wrapper.play_response("wake")
                text_after_wake_word = self.speech_recognizer.get_text_from_audio(phrase_time_limit=5)
                print("After Wake-Word: " + text_after_wake_word)

                if self.shopping_list_clear_keyword in text_after_wake_word:
                    kwargs = {"shopping_list_doc_id": self.shopping_list_doc_id}
                    self.try_execute(self.clear_shopping_list, **kwargs)
                elif match := re.search(self.shopping_list_pattern, text_after_wake_word):
                    insert_payload = match.group(1)
                    self.insert_in_document(doc_id=self.shopping_list_doc_id, insert_payload=insert_payload, panel_to_update="einkaufsliste")
                elif match := re.search(self.shopping_list_recipe_pattern, text_after_wake_word):
                    recipe = match.group(1)
                    if recipe in self.config["voice-assistant"]["recipes"]:
                        ingredients = self.config["voice-assistant"]["recipes"][recipe]
                        kwargs = {"document_id": self.shopping_list_doc_id,
                                  "insert_payload": ingredients}
                        self.try_execute(self.google_service_wrapper.insert_in_document_kwargs, **kwargs)
                        self.infoscreen_service_wrapper.update_shopping_list_panel(panel_config=self.config["infoscreen"]["panels"]["shopping_list"])
                    else:
                        self.audio_service_wrapper.play_response("misheard")
                elif match := re.search(self.mental_load_pattern, text_after_wake_word):
                    insert_payload = match.group(1)
                    self.insert_in_document(doc_id=self.mental_load_doc_id, insert_payload=insert_payload, panel_to_update="todo liste")
                elif "uhrzeit" in text_after_wake_word:
                    hour = datetime.now().strftime("%H")
                    minute = datetime.now().strftime("%M")
                    self.audio_service_wrapper.generate_response(f"Es ist {hour} Uhr {minute}.")
                elif match := re.search(self.update_panel_pattern, text_after_wake_word):
                    panel_to_update = match.group(1)
                    self.audio_service_wrapper.play_response("acknowledge")
                    response = self.update_infoscreen_panel(panel_to_update)
                elif "lauter" in text_after_wake_word:
                    self.volume += 10
                    self.audio_service_wrapper.set_output_volume(self.volume)
                    self.audio_service_wrapper.generate_response(f"Die Lautstärke ist jetzt bei {self.volume} Prozent.")
                elif "leiser" in text_after_wake_word:
                    self.volume -= 10
                    self.audio_service_wrapper.set_output_volume(self.volume)
                    self.audio_service_wrapper.generate_response(f"Die Lautstärke ist jetzt bei {self.volume} Prozent.")
                elif "wetter" in text_after_wake_word:
                    try:
                        response = requests.get(self.weather_service_url + "/get_weather_data")
                        weather_data = json.loads(response.content)
                        response = requests.get(self.weather_service_url + "/get_weather_forecast_data")
                        weather_forecast_data = json.loads(response.content)
                        weather_audio_output = (f"Es hat aktuell {weather_data['temp_cur']}, gefühlt {weather_data['temp_feels_like']} Grad. "
                                                f"Die Temperatur bewegt sich heute zwischen {round(min(weather_forecast_data['temp']))} und {round(max(weather_forecast_data['temp']))} Grad. "
                                                f"Die Luftfeuchtigkeit liegt bei {weather_data['humidity']} Prozent.")
                        self.audio_service_wrapper.generate_response(weather_audio_output)
                    except Exception as e:
                        print(e)
                        self.audio_service_wrapper.generate_response("Beim Abrufen der Wetterdaten ist etwas schief gelaufen.")
                else:
                    self.audio_service_wrapper.play_response("misheard")

    def clear_shopping_list(self, **kwargs):
        self.google_service_wrapper.clear_document_content(kwargs["shopping_list_doc_id"])
       
    def insert_in_document(self, doc_id, insert_payload, panel_to_update):
        self.audio_service_wrapper.generate_response(f"Soll ich {insert_payload} aufschreiben?")
        user_response = self.speech_recognizer.get_text_from_audio(phrase_time_limit=3)
        if "ja" in user_response:
            try:
                self.google_service_wrapper.insert_in_document(doc_id, insert_payload)
                self.audio_service_wrapper.play_response("acknowledge")
                self.update_infoscreen_panel(panel_to_update)
            except Exception as e:
                print(e)
                self.audio_service_wrapper.play_response("error")
        elif "nein" in user_response:
            self.audio_service_wrapper.play_wav("acknowledge_alles-klar")
        else:
            self.audio_service_wrapper.play_response("misheard")

    def update_infoscreen_panel(self, panel_to_update):
        try:
            if panel_to_update == "wetter":
                self.infoscreen_service_wrapper.update_weather_panel(panel_config=self.config["infoscreen"]["panels"]["weather"])
            elif panel_to_update == "kalender":
                self.infoscreen_service_wrapper.update_calendar_panel(panel_config=self.config["infoscreen"]["panels"]["calendar"])
            elif panel_to_update == "einkaufsliste":
                self.infoscreen_service_wrapper.update_shopping_list_panel(panel_config=self.config["infoscreen"]["panels"]["shopping_list"])
            elif panel_to_update == "todo liste":
                self.infoscreen_service_wrapper.update_mental_load_panel(panel_config=self.config["infoscreen"]["panels"]["mental_load"])
            elif panel_to_update == "alles":
                self.infoscreen_service_wrapper.refresh_all_panels(config=self.config)
            else:
                self.audio_service_wrapper.play_response("misheard")
        except Exception as e:
            print(e)
            self.audio_service_wrapper.generate_response(f"Beim Aktualisieren des {panel_to_update} Panels ist ein Fehler aufgetreten.")

    def try_execute(self, method, **kwargs):
        try:
            method(**kwargs)
            self.audio_service_wrapper.play_response("acknowledge")
        except Exception as e:
            print(e)
            self.audio_service_wrapper.play_response("error")
