import voice_assistant as va
import json

if __name__ == '__main__':

    with open("config/config.json") as config_file:
        config = json.load(config_file)
    
    voice_assistant = va.VoiceAssistant(config)
    voice_assistant.listen()
