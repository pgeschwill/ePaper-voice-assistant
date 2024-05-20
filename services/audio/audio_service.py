from flask import Flask, request, jsonify
from random import randrange
import os
import requests
import wave
import alsaaudio
import json

app = Flask(__name__)

with open("/config/config.json") as config_file:
   config = json.load(config_file)

PLAYBACK_DEVICE_NAME = config["audio"]["playback_device_name"]
INITIAL_VOLUME_PERCENT = config["audio"]["initial_volume_percent"]
PATH_TO_THIS_FILE = os.path.dirname(os.path.abspath(__file__))
PATH_TO_RESPONSE_FILES = os.path.join(PATH_TO_THIS_FILE, "wav")
MIMIC3_URL = "http://mimic3:59125/api/tts"

@app.route("/health", methods=['GET'])
def health():
    return jsonify(success=True)

@app.route("/play_response", methods=['GET'])
def play_response():
    response_type = request.args.get("response_type")
    all_files = os.listdir(PATH_TO_RESPONSE_FILES)
    response_files = [file for file in all_files if file.startswith(response_type)]
    num_response_files = len(response_files)
    file_index_to_play = randrange(0, num_response_files)
    file_name_to_play = os.path.join(PATH_TO_RESPONSE_FILES, response_files[file_index_to_play])
    play(file_name_to_play)
    return jsonify(success=True)

@app.route("/generate_response", methods=['GET'])
def generate_response():
    phrase = request.args.get("phrase")
    print(f"Generating speech for phrase '{phrase}'...")
    output_filename = "output.wav"
    params = {
        "text": phrase,
        "voice": "de_DE/thorsten_low"
    }
    response = requests.get(MIMIC3_URL, params = params)
    with open(output_filename, "wb") as out_file:
        out_file.write(response.content)
    play(output_filename)
    return jsonify(success=True)

@app.route("/generate_wav", methods=['GET'])
def generate_wav():
    phrase = request.args.get("phrase")
    filename = request.args.get("filename")
    print(f"Generating wav for phrase '{phrase}'...")
    output_filename = f"{os.path.normpath(os.path.join(PATH_TO_RESPONSE_FILES, filename))}"
    if not output_filename.startswith(PATH_TO_RESPONSE_FILES) or not output_filename.endswith(".wav"):
        return jsonify(error="Illegal path", message="Illegal path for output file.", success=False), 400
    params = {
        "text": phrase,
        "voice": "de_DE/thorsten_low"
    }
    response = requests.get(MIMIC3_URL, params = params)
    with open(output_filename, "wb") as out_file:
        out_file.write(response.content)
    return jsonify(success=True)

@app.route("/play_wav", methods=['GET'])
def play_wav():
    filename = request.args.get("filename")
    full_filename = f"{os.path.normpath(os.path.join(PATH_TO_RESPONSE_FILES, filename))}.wav"
    if not full_filename.startswith(PATH_TO_RESPONSE_FILES) or not os.path.exists(full_filename):
        return jsonify(error="Not Found", message="The requested file could not be found.", success=False), 404
    play(full_filename)
    return jsonify(success=True)

@app.route("/set_output_volume", methods=['GET'])
def set_output_volume():
    volume = request.args.get("volume")
    rc = private_set_output_volume(volume)
    return jsonify(success=rc)

def private_set_output_volume(volume):
    rc = False
    if 0 <= int(volume) <= 100:
        mixer = alsaaudio.Mixer(control="PCM")
        mixer.setvolume(int(volume))
        rc = True
    return rc

def play(filename):
    with wave.open(filename, "rb") as f:

        denominator = 1
        # 8bit is unsigned in wav files
        if f.getsampwidth() == 1:
            denominator = 8
        # Otherwise we assume signed data, little endian
        elif f.getsampwidth() == 2:
            denominator = 16
        elif f.getsampwidth() == 3:
            denominator = 24
        elif f.getsampwidth() == 4:
            denominator = 32
        else:
            raise ValueError('Unsupported format')

        periodsize = f.getframerate() // denominator

        device = alsaaudio.PCM(channels=f.getnchannels(), rate=f.getframerate(), format=2, periodsize=periodsize, device=PLAYBACK_DEVICE_NAME)
        
        while True:
            frames = f.readframes(periodsize)
            if not frames:
                break
            device.write(frames)

if __name__ == '__main__':
    private_set_output_volume(INITIAL_VOLUME_PERCENT)
    app.run(host='0.0.0.0', port=5000)