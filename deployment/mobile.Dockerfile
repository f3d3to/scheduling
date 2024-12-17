# Usar la imagen base de Dart como construcción inicial
FROM dart:stable AS build

# Instalar Flutter
RUN git clone https://github.com/flutter/flutter.git /flutter
ENV PATH="/flutter/bin:/flutter/bin/cache/dart-sdk/bin:${PATH}"

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    xz-utils \
    zip \
    libglu1-mesa \
    git \
    ca-certificates

# Evitar problemas con permisos de root
RUN useradd -m flutteruser
USER flutteruser

# Configurar Flutter para Web
RUN flutter doctor && flutter config --enable-web

# Crear directorio de trabajo
WORKDIR /app

# Agregar pubspec.yml para obtener dependencias
COPY --chown=flutteruser:flutteruser mobile/pubspec.* ./
RUN flutter pub get

# Agregar el código fuente de la aplicación
COPY --chown=flutteruser:flutteruser mobile/ /app

# Construir la versión web
RUN flutter build web

