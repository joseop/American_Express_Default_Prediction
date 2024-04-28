import pandas as pd
from sklearn.model_selection import train_test_split

# Carga el archivo CSV en un DataFrame de pandas
data = pd.read_csv("data/data_full.csv")

# División en entrenamiento y prueba (90% para entrenamiento, 10% para prueba)
train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)

# Guarda los conjuntos de datos en archivos CSV separados si es necesario
train_data.to_csv("data/train_data.csv", index=False)
test_data.to_csv("data/test_data.csv", index=False)
