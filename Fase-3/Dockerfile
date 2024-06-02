# Usa la imagen base de Python 3.10.6
FROM python:3.10.6

# Copia los archivos de la carpeta "data" al directorio "/app/data" en el contenedor
COPY ./data /app/data

# Copia el archivo de dependencias "biblioteca.txt" al directorio "/app" en el contenedor
COPY biblioteca.txt /app/

# Establece el directorio de trabajo en "/app"
WORKDIR /app

# Instala las dependencias desde el archivo "biblioteca.txt"
RUN pip install --no-cache-dir -r biblioteca.txt

# Copia el script "predict.py" al directorio "/app" en el contenedor
COPY apirest.py /app/

# Expone el puerto 3000
EXPOSE 3000

# Comando por defecto al ejecutar el contenedor
CMD ["sh", "-c", "python apirest.py"]

