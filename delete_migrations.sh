#!/bin/bash

# Mensaje inicial
echo "Eliminando archivos en carpetas 'migrations'..."

# Encuentra todas las carpetas de migraciones en el proyecto
find . -path "*/migrations" -type d -print0 | while IFS= read -r -d