# voice-assistant

An e-Paper info panel that also works as a voice assistant. It displays contents of google docs documents, google calendar items and weather information. You can talk to it to add items to a document (e.g. a shopping list), announce the weather, tell the time or whatever you configure it to do. Speech recognition and synthesis are handled locally without any cloud service.

## Bill of materials

* Raspberry Pi 4 (4GB)
* [7.3" 7-Color e-Paper Screen](https://www.waveshare.com/7.3inch-e-paper-hat-f.htm)
* [USB Speaker](https://www.amazon.com/-/de/dp/B075M7FHM1/ref=sr_1_3?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=H1U4UNFH9GEM&keywords=usb%2Bmini%2Bspeaker&qid=1706385254&sprefix=usb%2Bminii%2Bspeake%2Caps%2C189&sr=8-3&th=1)
* [Samson Go Microphone](https://samsontech.com/products/microphones/usb-microphones/gomic/)
* USB Flash Drive as boot medium

## Setup

### Configuration

The setup requires a config.json file in the config folder. There is an [example file](https://github.com/pgeschwill/ePaper-voice-assistant/blob/main/config/example_config.json) which illustrates the available options for customization.

### Case

The components are assembled within a wooden case to which the e-Paper screen is mounted. The microphone sticks out of the case to make sure it can record properly.

### Raspberry Pi

The setup has been tested with Raspberry Pi OS version 12 (bookworm). I decided to install the OS on a USB Flash drive instead of a micro SD card to increase read/write performance and improve longevity of the system. [Here](https://www.pcwelt.de/article/1157252/raspberry-pi-4-so-starten-sie-per-usb-stick.html) is a German article that describes how to set this up. 
You do of course need a local installation of docker to run the services.
Additionally, I am running an instance of [portainer](https://docs.portainer.io/start/install-ce/server/docker/linux) to monitor the services.

### Google API

The voice assistant can insert text into specifed google docs documents and delete the contents of a given document. Additionally, the Google service can retrieve calendar items from a calendar available in your google cloud app.

### Audio

When placing the case somewhere in your room, pay attention to the correct pickup pattern (cardioud or omnidirectional) because it will greatly affect the recording quality. The script [`test_mic_settings_transcription.py`](https://github.com/pgeschwill/ePaper-voice-assistant/blob/main/config/test_mic_settings_transcription.py) can be used to check the recording quality.

It is recommended to use USB speakers with the Raspberry Pi instead of the headphone jack because the audio quality is usually much better.

### Speech recognition and synthesis

I went for [VOSK](https://github.com/alphacep/vosk-api) for offline speech recognition because it worked best for my purpose and it allows plugging in several voice models. The German voice model that I am using is included in the repo but can be replaced or new models can be added.

Speech synthesis is also done offline using [Mycroft mimic3](https://github.com/MycroftAI/mimic3) which works well enough for my purposes. Mimic3 supports several voice models in many different languages. Mycroft does not recommend running its models with Raspberry Pi models earlier than the Raspberry Pi 4 because the performance is too low. In my experience, using the speech synthesis for shorter text snippets works just fine. Longer text of more than a couple of sentences requires waiting for several seconds which may be undesirable.

Apart from on-the-fly speech recognition, the voice assistant in this solution uses prepared .wav files for quicker responses. With a running mimic3 container (using `docker compose up mimic3 -d`), you can create these files yourself by calling `curl -s -G --data-urlencode "text=Hello, this is a test phrase." -d "voice=de_DE/thorsten_low" localhost:59125/api/tts > output.wav`. Use the given installed voice for the voice parameter.

### e-Paper Screen

This code base only works with the screen listed in the bill of materials. Each waveshare screen has its own dedicated drivers which are maintained by the waveshare team on their [github](https://github.com/waveshareteam/e-Paper). I decided to directly include the [driver](https://github.com/pgeschwill/ePaper-voice-assistant/tree/main/services/infoscreen/driver) in this repo because the screen logic is essentially hardwired to this screen model.

### Clear e-paper screen on shutdown

It is recommended to clear the screen when not using it for extended periods to prevent burn-in.
In order to clear the screen on shutting down the system, the script [`clear_screen_on_shutdown.sh`](https://github.com/pgeschwill/ePaper-voice-assistant/blob/main/services/infoscreen/clear_screen_on_shutdown.sh) is included which wraps a python script that contains the logic for clearing the screen.
This bash script needs to be registered with systemd such that it is called on each shutdown.

On RaspberryPi OS, this is done by first applying execute permission to the script with `chmod +x path/to/clear_screen_on_shutdown.sh`.
Subsequently, create a systemd service by calling `sudo nano /etc/systemd/system/clear-screen-on-shutdown.service` and filling the file with this info:

``` bash
[Unit]
Description=Clear ePaper screen before shutdown
Before=shutdown.target reboot.target halt.target

[Service]
Type=oneshot
RemainAfterExit=true
ExecStart=/bin/true
ExecStop=/path/to/repo/services/infoscreen/clear_screen_on_shutdown.sh

[Install]
WantedBy=multi-user.target
```

In order for this to work properly, you need to have a venv in the appropriate location which is equipped with the depedencies listed in the [`requirements.txt`](https://github.com/pgeschwill/ePaper-voice-assistant/blob/main/services/infoscreen/requirements.txt) file of the infoscreen module.

Finally, reload the daemon and enable the service

``` bash
sudo systemctl daemon-reload
sudo systemctl enable clear-screen-on-shutdown.service
```

## Sources
I was inspired to do this project by several sources which are listed below:

* https://www.techwithtim.net/tutorials/voice-assistant/wake-keyword
* https://community.element14.com/challenges-projects/element14-presents/project-videos/w/documents/4628/raspberry-pi-e-ink-task-organizer----episode-422
* https://github.com/KalebClark/InfoWindow
* https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3

## Todo

* General
    * Add proper logging
* Infoscreen
    * Add possibility to display images/photos
    * Async screen update
    * Make font handling more flexible
* Weather
    * Check out One-Call API
    * pregenerate weather audio at fixed intervals to reduce synthesis overhead