# Usa una imagen base de Python
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Crea el directorio data dentro del contenedor
RUN mkdir data

# Copia la base de datos dentro del directorio de datos del contenedor.
COPY data/bdContaCasa.db /app/data/bdContaCasa.db

# Copia el código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que la aplicación Flet escuchará
EXPOSE 8000

# Define el volumen para la base de datos SQLite
VOLUME /app/data

# Comando para ejecutar la aplicación Flet
CMD ["python", "main.py"]