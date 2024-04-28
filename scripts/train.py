import pandas as pd
import pickle
from loguru import logger
import argparse
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix

parser = argparse.ArgumentParser()
parser.add_argument('--data_file', required=True, type=str, help='a csv file with train data')
parser.add_argument('--model_file', required=True, type=str, help='where the trained model will be stored')
parser.add_argument('--overwrite_model', default=False, action='store_true', help='if sets overwrites the model file if it exists')

args = parser.parse_args()

model_file = args.model_file
data_file  = args.data_file
overwrite = args.overwrite_model

if os.path.isfile(model_file):
    if overwrite:
        logger.info(f"overwriting existing model file {model_file}")
    else:
        logger.info(f"model file {model_file} exists. exitting. use --overwrite_model option")
        exit(-1)

logger.info("loading train data")

#llamo el archivo del dataframe

#asignando las columnas del datafull.txt al df convirtiendolo al csv
df = pd.read_csv(data_file, sep='\t')
#df.head()

#df.info()

#llenando las columnas faltantes
column =  df.select_dtypes(include=['object']).columns.to_list()
sub_df = df[column]
sub_df.isna().sum()

df['D_64'].mode()[0]
df['D_64'].fillna(df['D_64'].mode()[0], inplace=True)
sub_df = df[column]
sub_df.isna().sum()
df['S_2'] = pd.to_datetime(df['S_2'])
df['D_63'].value_counts()
df['D_64'].value_counts()
df = pd.get_dummies(df, columns=['D_63', 'D_64'])
df.rename(columns={'D_64_-1': 'D_64_I'}, inplace=True)
df[['D_63_CO', 'D_63_CR', 'D_63_CL', 'D_63_XZ', 'D_63_XZ', 'D_63_XM', 'D_63_XL', 'D_64_O', 'D_64_U', 'D_64_R',
    'D_64_I', 'target']]

def completar_na(sub_df):
    for colum in sub_df.columns:
        df[colum].fillna(df[colum].mode()[0], inplace=True)

category = ['B_30', 'B_38', 'D_114', 'D_116', 'D_117', 'D_120', 'D_126', 'D_66', 'D_68']

#columnas_C = df[category]

sub_df = df[category]
sub_df.isna().sum()
completar_na(sub_df)

sub_df = df[category]
sub_df.isna().sum()

columnas_S = df.filter(like='S_').drop('S_2', axis=1)
sub_df = df[columnas_S.columns].loc[:, df[columnas_S.columns].isna().any()]
sub_df.isna().sum()
completar_na(sub_df)

columnas_D = df.filter(like='D_')
sub_df = df[columnas_D.columns].loc[:, df[columnas_D.columns].isna().any()]
sub_df.isna().sum()
completar_na(sub_df)

columnas_P = df.filter(like='P_')
sub_df = df[columnas_P.columns].loc[:, df[columnas_P.columns].isna().any()]
sub_df.isna().sum()
completar_na(sub_df)

columnas_B = df.filter(like='B_')
sub_df = df[columnas_B.columns].loc[:, df[columnas_B.columns].isna().any()]
sub_df.isna().sum()
completar_na(sub_df)

columnas_R = df.filter(like='R_')
sub_df = df[columnas_R.columns].loc[:, df[columnas_R.columns].isna().any()]
sub_df.isna().sum()
completar_na(sub_df)

####Modelos
# 'customer_ID' es una variable categórica y 'S_2' es una variable de tipo fecha

# Codificar 'customer_ID' usando Label Encoding

label_encoder = LabelEncoder()
df['customer_ID_encoded'] = label_encoder.fit_transform(df['customer_ID'])

# Tratamiento de la variable de fecha 'S_2'
df['S_2'] = pd.to_datetime(df['S_2'])  # Convertir a tipo datetime
df['year'] = df['S_2'].dt.year  # Extraer el año
df['month'] = df['S_2'].dt.month  # Extraer el mes

# Eliminar las columnas originales 'customer_ID' y 'S_2' que ya no son necesarias
df.drop(['customer_ID', 'S_2'], axis=1, inplace=True)

# Separar las características (X) y la variable objetivo (y)
X = df.drop('target', axis=1)  # Quitamos la columna 'target' del DataFrame para obtener las características
y = df['target']  # Columna 'target' como variable objetivo
#train y.fit con x y
# Dividir el conjunto de datos en entrenamiento y prueba (por ejemplo, 80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicializar los modelos
logistic_regression = LogisticRegression()

# Entrenar los modelos
logistic_regression.fit(X_train, y_train)

# Predicciones en el conjunto de prueba
y_pred_lr = logistic_regression.predict(X_test)

###Logistic Regression

# Define el modelo de regresión logística
logistic_regression = LogisticRegression(max_iter=10000)

# Define el espacio de búsqueda de hiperparámetros
param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],  # Valores para la fuerza de regularización
    'penalty': ['l1', 'l2'],  # Tipo de regularización (L1 o L2)
}

# Realiza una búsqueda grid para encontrar los mejores hiperparámetros
grid_search = GridSearchCV(logistic_regression, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Definir el modelo de regresión logística con los mejores parámetros encontrados
best_logistic_regression = LogisticRegression(C=0.1, penalty='l2', max_iter=10000)

# Entrenar el modelo con los mejores parámetros utilizando todo el conjunto de entrenamiento
best_logistic_regression.fit(X_train, y_train)

# Evaluar el modelo en el conjunto de prueba (X_test, y_test)
accuracy = best_logistic_regression.score(X_test, y_test)

# Realizar predicciones en el conjunto de prueba
y_pred = best_logistic_regression.predict(X_test)
y_pred_proba = best_logistic_regression.predict_proba(X_test)[:, 1]

# Calcular y mostrar la matriz de confusión
conf_matrix = confusion_matrix(y_test, y_pred)

m=best_logistic_regression
with open(model_file, "wb") as f:
    pickle.dump(m, f)