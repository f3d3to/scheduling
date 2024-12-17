#!/bin/bash

# Función para mostrar el árbol de directorios excluyendo carpetas específicas
mostrar_arbol_directorios() {
  local ruta="$1"
  local excluir=("${@:2}") # Obtiene todos los argumentos después del primero

  find "$ruta" -type d \( ${excluir[@]/#/'-path '*} \) -prune -o -print | sed 's;[^/]*/;|__;g;s;__|; |;g'
}

# Solicitar la ruta al usuario
read -p "Introduce la ruta del directorio: " ruta

# Solicitar las carpetas a excluir (opcional)
read -p "Introduce las carpetas a excluir (separadas por espacios, o presiona Enter para ninguna): " excluir

# Convertir la entrada del usuario en un array
IFS=' ' read -r -a excluir <<< "$excluir"

# Llamar a la función para mostrar el árbol
mostrar_arbol_directorios "$ruta" "${excluir[@]}"