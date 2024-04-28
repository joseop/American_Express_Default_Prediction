import argparse
from loguru import logger
import os
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', required=True, type=str, help='a csv file with input data (no targets)')
parser.add_argument('--predictions_file', required=True, type=str, help='a csv file where predictions will be saved to')
parser.add_argument('--model_file', required=True, type=str, help='a pkl file with a model already stored (see train.py)')

args = parser.parse_args()

model_file  = args.model_file
input_file  = args.input_file
predictions_file = args.predictions_file

if not os.path.isfile(model_file):
    logger.error(f"model file {model_file} does not exist")
    exit(-1)

if not os.path.isfile(input_file):
    logger.error(f"input file {input_file} does not exist")
    exit(-1)
    
    
logger.info("loading input data")
# Cargar los datos de entrada
df = pd.read_csv(input_file, sep='\t')

# Preprocesamiento de datos similar al realizado durante el entrenamiento del modelo

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

logger.info("loading model")
# Cargar el modelo entrenado
with open(model_file, 'rb') as f:
    m = pickle.load(f)
    
logger.info("making predictions")
# Realizar predicciones con el modelo cargado
preds = m.predict(X)

logger.info(f"saving predictions to {predictions_file}")
# Guardar las predicciones en un archivo CSV
pd.DataFrame(preds.reshape(-1,1), columns=['preds']).to_csv(predictions_file, index=False)
