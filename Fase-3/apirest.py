import os
import pandas as pd
import pickle
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

model_file = 'model.pkl'

def preprocess_data(df):
    # Preprocesamiento de datos similar al realizado durante el entrenamiento del modelo
    column = df.select_dtypes(include=['object']).columns.to_list()
    df['D_64'].fillna(df['D_64'].mode()[0], inplace=True)
    df = pd.get_dummies(df, columns=['D_63', 'D_64'])
    df.rename(columns={'D_64_-1': 'D_64_I'}, inplace=True)

    category = ['B_30', 'B_38', 'D_114', 'D_116', 'D_117', 'D_120', 'D_126', 'D_66', 'D_68']
    for col in category:
        df[col].fillna(df[col].mode()[0], inplace=True)

    columnas_S = df.filter(like='S_').drop('S_2', axis=1)
    for col in columnas_S.columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    columnas_D = df.filter(like='D_')
    for col in columnas_D.columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    columnas_P = df.filter(like='P_')
    for col in columnas_P.columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    columnas_B = df.filter(like='B_')
    for col in columnas_B.columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    columnas_R = df.filter(like='R_')
    for col in columnas_R.columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    label_encoder = LabelEncoder()
    df['customer_ID_encoded'] = label_encoder.fit_transform(df['customer_ID'])

    df['S_2'] = pd.to_datetime(df['S_2'])
    df['year'] = df['S_2'].dt.year
    df['month'] = df['S_2'].dt.month

    df.drop(['customer_ID', 'S_2'], axis=1, inplace=True)

    return df

@app.route('/train', methods=['POST'])
def train():
    # Este endpoint no recibe archivo, usa datos de entrenamiento estándar
    data_file = 'data/train_data.csv'  # Asegúrate de tener este archivo de datos disponible
    df = pd.read_csv(data_file, sep='\t')
    df = preprocess_data(df)

    X = df.drop('target', axis=1)
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logistic_regression = LogisticRegression(max_iter=10000)
    param_grid = {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear']  # Necesario para L1
    }
    grid_search = GridSearchCV(logistic_regression, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    best_logistic_regression = grid_search.best_estimator_
    best_logistic_regression.fit(X_train, y_train)

    with open(model_file, "wb") as f:
        pickle.dump(best_logistic_regression, f)

    return jsonify({'message': 'Modelo entrenado y guardado exitosamente'})

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        df = pd.read_csv(filepath, sep='\t')
        df = preprocess_data(df)
        X = df.drop('target', axis=1, errors='ignore')

        with open(model_file, 'rb') as f:
            model = pickle.load(f)

        predictions = model.predict(X)
        return jsonify(predictions.tolist())

@app.route('/')
def hello():
    return jsonify({'message': 'Hola American express'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
