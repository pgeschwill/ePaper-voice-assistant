FROM ghcr.io/astral-sh/uv:python3.11-alpine

ADD pyproject.toml .
ADD uv.lock .

RUN apk update && apk add --no-cache curl
RUN uv sync --group weather --locked

CMD ["uv", "run", "/services/weather/weather_service.py"]