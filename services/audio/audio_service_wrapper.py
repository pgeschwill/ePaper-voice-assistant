import requests

class AudioServiceWrapper:

    def __init__(self):
        self.audio_service_url = "http://audio-service:5000"

    def play_response(self, response_type):
        params = {
            "response_type": response_type
        }
        requests.get(self.audio_service_url + "/play_response", params = params)

    def play_wav(self, filename):
        params = {
            "filename": filename
        }
        requests.get(self.audio_service_url + "/play_wav", params = params)

    def generate_response(self, phrase):
        params = {
            "phrase": phrase
        }
        requests.get(self.audio_service_url + "/generate_response", params = params)

    def set_output_volume(self, volume):
        params = {
            "volume": volume
        }
        requests.get(self.audio_service_url + "/set_output_volume", params = params)
