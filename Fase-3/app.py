from flask import Flask, jsonify, request
import pandas as pd
import pickle
from loguru import logger
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix
from threading import Thread
from time import sleep

app = Flask(__name__)

train_status = "not training"
model = None
model_file = "/app/modelo_final.pkl"

def preprocess_data(df):
    # Aquí se incluirá el código de preprocesamiento de datos de tus scripts
    # (por ejemplo, rellenar valores nulos, codificación, etc.)
    pass

def train_model():
    global train_status, model
    train_status = "training"

    # Cargar los datos de entrenamiento
    df = pd.read_csv("/app/data/train_data.csv")

    # Preprocesar los datos
    df = preprocess_data(df)

    # Separar características y objetivo
    X = df.drop('target', axis=1)
    y = df['target']

    # Dividir el conjunto de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inicializar y entrenar el modelo
    logistic_regression = LogisticRegression(max_iter=10000)
    param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100], 'penalty': ['l1', 'l2']}
    grid_search = GridSearchCV(logistic_regression, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    model = grid_search.best_estimator_

    # Guardar el modelo entrenado
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)

    train_status = "not training"

@app.route("/train", methods=['POST'])
def train():
    if train_status == "training":
        return jsonify({"error": "Training already in progress"}), 400
    
    # Iniciar el entrenamiento en un hilo separado para no bloquear la API
    Thread(target=train_model).start()
    return jsonify({"message": "Training started"}), 202

@app.route("/predict", methods=['POST'])
def predict():
    global model
    if model is None:
        if os.path.isfile(model_file):
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
        else:
            return jsonify({"error": "Model not trained"}), 400

    data = request.get_json()
    df = pd.DataFrame([data])
    df = preprocess_data(df)
    
    # Realizar la predicción
    prediction = model.predict(df)
    return jsonify({"prediction": prediction.tolist()}), 200

@app.route("/status", methods=['GET'])
def status():
    return jsonify({"train_status": train_status}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
