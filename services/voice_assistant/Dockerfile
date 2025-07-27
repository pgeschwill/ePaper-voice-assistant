FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

ADD pyproject.toml .
ADD uv.lock .

RUN apt-get update && apt-get install -y \
  alsa-utils \
  alsa-tools \
  libasound2-plugins \
  portaudio19-dev \
  gcc
RUN uv sync --group voice-assistant --locked --no-dev

CMD ["uv", "run", "/services/voice_assistant/launch_voice_assistant.py"]
