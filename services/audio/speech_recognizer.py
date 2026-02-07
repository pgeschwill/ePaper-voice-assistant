import json
import os
from contextlib import contextmanager
from ctypes import *

import speech_recognition as sr
from vosk import KaldiRecognizer, Model


class SpeechRecognizer:
    def __init__(self, config):
        self.path_to_this_file = os.path.dirname(os.path.abspath(__file__))
        self.path_to_vosk_model = os.path.join(
            self.path_to_this_file, "vosk-model-small-de-0.15"
        )
        self.path_to_response_files = os.path.join(self.path_to_this_file, "wav")
        self.model = Model(self.path_to_vosk_model)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.microphone_device_index = config["audio"]["mic_device_index"]
        self.mic_chunk_size = config["audio"]["mic_chunk_size"]
        self.recognition_count = 0
        self.max_recognitions_before_reset = 100  # Recreate recognizer every 100 recognitions
        ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
        self.c_error_handler = ERROR_HANDLER_FUNC(self.py_error_handler)

    def py_error_handler(self, filename, line, function, err, fmt):
        pass

    @contextmanager
    def noalsaerr(self):
        asound = cdll.LoadLibrary("libasound.so")
        asound.snd_lib_error_set_handler(self.c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)

    def get_text_from_audio(self, timeout=None, phrase_time_limit=None):
        with self.noalsaerr():
            r = sr.Recognizer()
            with sr.Microphone(
                device_index=self.microphone_device_index,
                chunk_size=self.mic_chunk_size,
            ) as source:
                audio = r.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
                recognized_text = ""
                try:
                    result = json.loads(self.recognize_vosk(audio))
                    recognized_text = result["text"]
                except Exception as e:
                    print("Exception: " + str(e))

        return recognized_text

    def recognize_vosk(self, audio_data):
        print("Starting voice recognition...")
        self.recognizer.AcceptWaveform(
            audio_data.get_raw_data(convert_rate=16000, convert_width=2)
        )
        recognized_text = self.recognizer.FinalResult()
        # Reset recognizer to prevent memory accumulation
        self.recognizer.Reset()
        
        # Periodically recreate the recognizer to prevent long-term memory accumulation
        self.recognition_count += 1
        if self.recognition_count >= self.max_recognitions_before_reset:
            print(f"Recreating VOSK recognizer after {self.recognition_count} recognitions to prevent memory leaks")
            del self.recognizer
            self.recognizer = KaldiRecognizer(self.model, 16000)
            self.recognition_count = 0
        
        return recognized_text
