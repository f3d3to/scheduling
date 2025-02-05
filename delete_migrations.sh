#!/bin/bash

# Directorio raíz del proyecto Django
PROJECT_DIR="."

# Verificar si el directorio existe
if [ ! -d "$PROJECT_DIR" ]; then
  echo "Error: El directorio del proyecto no existe: $PROJECT_DIR"
  exit 1
fi

# Buscar y eliminar archivos de migraciones
echo "Buscando archivos de migraciones en $PROJECT_DIR..."
find "$PROJECT_DIR" -type f -path "*/migrations/*.py" ! -name "__init__.py" | while read -r file; do
  echo "Eliminando archivo: $file"
  rm -f "$file"
done

# Eliminar archivos compilados de migraciones (__pycache__)
echo "Buscando y eliminando archivos compilados de migraciones (__pycache__)..."
find "$PROJECT_DIR" -type f -path "*/migrations/__pycache__/*.pyc" | while read -r file; do
  echo "Eliminando archivo compilado: $file"
  rm -f "$file"
done

echo "Proceso completado."