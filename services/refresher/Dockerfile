FROM ghcr.io/astral-sh/uv:python3.11-alpine

ADD pyproject.toml .
ADD uv.lock .

RUN uv sync --group refresher --locked

CMD ["uv", "run", "/services/refresher/refresher_service.py"]