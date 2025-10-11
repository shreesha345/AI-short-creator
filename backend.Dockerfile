FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

RUN mkdir -p /app/data

COPY ./backend ./backend

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "python", "backend/main.py"]
