FROM ghcr.io/astral-sh/uv:python3.11-alpine

ADD pyproject.toml .
ADD uv.lock .

RUN apk update && apk add --no-cache curl
RUN uv sync --group google --locked

CMD ["uv", "run", "/services/google/google_service.py"]