from flask import Flask, request, jsonify
from random import randrange
from urllib.parse import quote
import os
import re
import subprocess
import requests

app = Flask(__name__)
PATH_TO_THIS_FILE = os.path.dirname(os.path.abspath(__file__))
PATH_TO_RESPONSE_FILES = os.path.join(PATH_TO_THIS_FILE, "wav")
MIMIC3_URL = "http://mimic3:59125/api/tts"
OS_COMMANDS = {
    "set_output_volume": "amixer",
    "play_wav": "aplay"
}

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
    command = [OS_COMMANDS["play_wav"], file_name_to_play]
    subprocess.run(command)
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
    play_command = [OS_COMMANDS["play_wav"], output_filename]
    subprocess.run(play_command)
    return jsonify(success=True)

@app.route("/play_wav", methods=['GET'])
def play_wav():
    filename = request.args.get("filename")
    full_filename = f"{os.path.join(PATH_TO_RESPONSE_FILES, filename)}.wav"
    if not os.path.exists(full_filename):
        return jsonify(success=False)
    command = [OS_COMMANDS["play_wav"], full_filename]
    subprocess.run(command)
    return jsonify(success=True)

@app.route("/set_output_volume", methods=['GET'])
def set_output_volume():
    volume = request.args.get("volume")
    if not re.match("\d{2}", volume):
        return jsonify(success=False)
    print(f"Setting volume to {volume}")
    command = [OS_COMMANDS["set_output_volume"], "-q", "sset", "PCM", f"{volume}%"]
    subprocess.run(command)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)