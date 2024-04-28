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

# Copia el script "train.py" al directorio "/app" en el contenedor
COPY ./scripts/train.py /app/


# Copia el script "predict.py" al directorio "/app" en el contenedor
COPY ./scripts/predict.py /app/

# Comando por defecto al ejecutar el contenedor
CMD ["sh", "-c", "python train.py --data_file=data/train_data.csv --model_file=modelo_final.pkl && python predict.py --input_file=data/test_data.csv --predictions_file=data/prediction_file.csv --model_file=modelo_final.pkl"]

