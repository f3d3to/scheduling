#!/bin/bash

# Directorio raíz del proyecto Django
PROJECT_DIR="."

# Verificar si el directorio existe
if [ ! -d "$PROJECT_DIR" ]; then
  echo "Error: El directorio del proyecto no existe: $PROJECT_DIR"
  exit 1
fi

# Buscar y eliminar directorios __pycache__
echo "Buscando y eliminando directorios __pycache__ en $PROJECT_DIR..."
find "$PROJECT_DIR" -type d -name "__pycache__" | while read -r dir; do
  echo "Eliminando directorio: $dir"
  rm -rf "$dir"
done

echo "Proceso completado."