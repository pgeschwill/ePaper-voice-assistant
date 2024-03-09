FROM python:3.11.2

ADD requirements.txt .

RUN apt-get update && apt-get install -y \
  alsa-utils \
  alsa-tools \
  libasound2-plugins \
  portaudio19-dev

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "/services/voice_assistant/launch_voice_assistant.py"]
