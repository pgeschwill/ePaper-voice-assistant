import os
import requests

class AudioServiceWrapper:

    def __init__(self):
        self.audio_service_url = f"http://{os.environ['audio_service_name']}:{os.environ['audio_service_port']}"

    def play_response(self, response_type):
        params = {
            "response_type": response_type
        }
        return requests.get(self.audio_service_url + "/play_response", params = params)

    def play_wav(self, filename):
        params = {
            "filename": filename
        }
        return requests.get(self.audio_service_url + "/play_wav", params = params)

    def generate_response(self, phrase):
        params = {
            "phrase": phrase
        }
        return requests.get(self.audio_service_url + "/generate_response", params = params)

    def generate_wav(self, phrase, filename):
        params = {
            "phrase": phrase,
            "filename": filename
        }
        return requests.get(self.audio_service_url + "/generate_wav", params = params)

    def set_output_volume(self, volume):
        params = {
            "volume": volume
        }
        return requests.get(self.audio_service_url + "/set_output_volume", params = params)
