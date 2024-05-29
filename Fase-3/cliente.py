import requests

# Entrenar el modelo
response = requests.post('http://localhost:5000/train')
print("Train response:", response.json())

# Esperar hasta que el entrenamiento esté completo
import time
while True:
    response = requests.get('http://localhost:5000/status')
    status = response.json()
    print("Status:", status)
    if status["train_status"] == "not training":
        break
    time.sleep(2)

# Realizar predicciones
data = {
    "age": 32,
    "salary": 10000
}
response = requests.post('http://localhost:5000/predict', json=data)
print("Predict response:", response.json())
