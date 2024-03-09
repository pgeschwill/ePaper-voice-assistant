from flask import Flask, request, jsonify
from random import randrange
from urllib.parse import quote
import os

app = Flask(__name__)
PATH_TO_THIS_FILE = os.path.dirname(os.path.abspath(__file__))
PATH_TO_RESPONSE_FILES = os.path.join(PATH_TO_THIS_FILE, "wav")

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
    os.system(f"aplay {file_name_to_play}")
    return jsonify(success=True)

@app.route("/generate_response", methods=['GET'])
def generate_response():
    phrase = request.args.get("phrase")
    print(f"Generating speech for phrase '{phrase}'...")
    os.system(f'curl -s -G -d "text={quote(phrase)}" -d "voice=de_DE/thorsten_low" http://mimic3:59125/api/tts --output -| aplay')
    return jsonify(success=True)

@app.route("/play_wav", methods=['GET'])
def play_wav():
    filename = request.args.get("filename")
    os.system(f"aplay {os.path.join(PATH_TO_RESPONSE_FILES, filename)}.wav")
    return jsonify(success=True)

@app.route("/set_output_volume", methods=['GET'])
def set_output_volume():
    volume = request.args.get("volume")
    os.system(f"amixer --quiet sset PCM {volume}%")
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)