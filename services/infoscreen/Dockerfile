FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

ADD pyproject.toml .
ADD uv.lock .

RUN apt-get update && apt-get install -y gcc

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --group infoscreen --locked

FROM python:3.11-slim-bookworm

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

RUN apt-get update && apt-get install -y curl

CMD ["python", "/services/infoscreen/infoscreen_service.py"]