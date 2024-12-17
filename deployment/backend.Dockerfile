FROM python:3.10-slim

WORKDIR /app

# Instalar y actualizar herramientas
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

ADD ../deployment/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

ADD ../backend /app

EXPOSE 8000


ENV DJANGO_SETTINGS_MODULE=core.settings
