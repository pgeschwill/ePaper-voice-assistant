from services.google import google_service_wrapper as gsw
from urllib.parse import quote
import requests

class InfoScreenServiceWrapper:
    def __init__(self, config):
        self.infoscreen_service_url = "http://infoscreen-service:7000"
        self.weather_service_url = "http://weather-service:8000/"
        self.shopping_list_doc_id = config["google"]["docs"]["shopping_list_doc_id"]
        self.mental_load_doc_id = config["google"]["docs"]["mental_load_doc_id"]
        self.google_service_wrapper = gsw.GoogleServiceWrapper(config)
    
    def refresh_all_panels(self, config):
        self.update_date_info_panel(config["infoscreen"]["panels"]["date_info"], clear_display_sleep=False)
        self.update_calendar_panel(config["infoscreen"]["panels"]["calendar"], clear_display_sleep=False)
        self.update_shopping_list_panel(config["infoscreen"]["panels"]["shopping_list"], clear_display_sleep=False)
        self.update_mental_load_panel(config["infoscreen"]["panels"]["mental_load"], clear_display_sleep=False)
        self.update_weather_panel(config["infoscreen"]["panels"]["weather"])
        
    def update_weather_panel(self, panel_config, clear_display_sleep=True):
        weather_data = requests.get(self.weather_service_url + "/get_weather_data")
        forecast_data = requests.get(self.weather_service_url + "/get_weather_forecast_data")
        json_params = {
            "weather_data": quote(weather_data.content),
            "forecast_data": quote(forecast_data.content),
            "panel_config": panel_config,
            "clear_display_sleep": clear_display_sleep
        }
        return requests.post(self.infoscreen_service_url + "/update_weather_panel", json=json_params)

    def update_shopping_list_panel(self, panel_config, clear_display_sleep=True):
        shopping_list_content = self.google_service_wrapper.get_document_content(document_id=self.shopping_list_doc_id)
        json_params = {
            "shopping_list_content": quote(shopping_list_content.content),
            "panel_config": panel_config,
            "clear_display_sleep": clear_display_sleep
        }
        return requests.post(self.infoscreen_service_url + "/update_shopping_list_panel", json=json_params)

    def update_mental_load_panel(self, panel_config, clear_display_sleep=True):
        mental_load_content = self.google_service_wrapper.get_document_content(document_id=self.mental_load_doc_id)
        json_params = {
            "mental_load_content": quote(mental_load_content.content),
            "panel_config": panel_config,
            "clear_display_sleep": clear_display_sleep
        }
        return requests.post(self.infoscreen_service_url + "/update_mental_load_panel", json=json_params)

    def update_calendar_panel(self, panel_config, clear_display_sleep=True):
        calendar_items = self.google_service_wrapper.get_calendar_items()
        json_params = {
            "calendar_items": quote(calendar_items.content),
            "panel_config": panel_config,
            "clear_display_sleep": clear_display_sleep
        }
        return requests.post(self.infoscreen_service_url + "/update_calendar_panel", json = json_params)
    
    def update_date_info_panel(self, panel_config, clear_display_sleep=True):
        json_params = {
            "panel_config": panel_config,
            "clear_display_sleep": clear_display_sleep
        }
        return requests.post(self.infoscreen_service_url + "/update_date_info_panel", json = json_params)
    
    def display_screensaver(self):
        return requests.get(self.infoscreen_service_url + "/display_screensaver")
