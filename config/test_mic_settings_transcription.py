import json
from os import path

import speech_recognition as sr
from vosk import KaldiRecognizer, Model

# Use this script to play around with the microphone settings
# to make sure that the captured audio is of apropriate quality.
# In my case, lowering the chunk size from the default 1024 to 512
# caused a drastic increase in recognition accuracy.
# I assume this is because this setting essentially controls compression,
# i.e. how much audio data is squeezed into each frame.
# When recording with 1024, the recorded audio appeared sped up and choppy

PATH_TO_THIS_FILE = path.dirname(path.abspath(__file__))
DEVICE_INDEX = 1  # Use source.list_working_microphones() to get the index
CHUNK_SIZE = 512
MIC_TEST_FILE = path.join(PATH_TO_THIS_FILE, "mic_test.wav")
PATH_TO_VOSK_MODEL = path.join(
    PATH_TO_THIS_FILE, "../services/audio/vosk-model-small-de-0.15"
)
PHRASE_TIME_LIMIT = 5

r = sr.Recognizer()
with sr.Microphone(device_index=DEVICE_INDEX, chunk_size=CHUNK_SIZE) as source:
    print("Say something!")
    print(source.SAMPLE_RATE)
    print(source.SAMPLE_WIDTH)
    audio = r.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT)

    # Save recorded audio to file for playback later
    with open(MIC_TEST_FILE, "wb") as f:
        f.write(audio.get_wav_data())

# Transcribe the recorded audio with VOSK
print("Starting transcription")
r = sr.Recognizer()
with sr.AudioFile(MIC_TEST_FILE) as source:
    audio = r.record(source)  # read the entire audio file
    recognizer = KaldiRecognizer(Model(PATH_TO_VOSK_MODEL), 16000)
    raw_audio = audio.get_raw_data(convert_rate=16000, convert_width=2)
    if recognizer.AcceptWaveform(raw_audio):
        result_final = json.loads(recognizer.FinalResult())
        print(result_final["text"])
    else:
        result_partial = json.loads(recognizer.PartialResult())
        print(result_partial["partial"])
