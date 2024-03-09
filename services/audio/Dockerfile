FROM python:3.11.2-slim

ADD requirements.txt .

RUN apt-get update && apt-get install -y \
  alsa-utils \
  alsa-tools \
  curl

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "/services/audio/audio_service.py"]