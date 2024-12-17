# Utiliza una imagen base de Node.js
FROM node:18-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el resto del código fuente de la aplicación
ADD /frontend /app
# Instala las dependencias del proyecto
RUN npm install

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 5173
