FROM python:3.12.2-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m venv /install && \
    /install/bin/pip install --upgrade pip setuptools wheel && \
    /install/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12.2-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /usr/sbin/nologin appuser

WORKDIR /app

COPY --from=builder /install /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /app /app

RUN chown -R appuser:appuser /app /opt/venv

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]