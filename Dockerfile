FROM python:3.11-slim

WORKDIR /app

# Ставим uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Сначала зависимости (кэшируется)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Потом код
COPY src/ ./src/
RUN mkdir -p models

CMD ["uv", "run", "--no-sync", "python", "-m", "src.pipeline"]