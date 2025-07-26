FROM ghcr.io/astral-sh/uv:python3.11-alpine

ADD pyproject.toml .
ADD uv.lock .

RUN uv sync --group refresher --locked --no-dev

CMD ["uv", "run", "/services/refresher/refresher_service.py"]