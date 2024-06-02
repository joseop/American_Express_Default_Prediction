
# API REST con Flask

Esta aplicación expone dos endpoints para el entrenamiento y predicción de un modelo de regresión logística.

## Instrucciones para Docker

### Crear la imagen

```sh
docker build -t american .
```

### Ejecutar un contenedor con la imagen creada

```sh
docker run -p 3000:3000 -it --name american american
```

### Entrar al contenedor

```sh
docker exec -it [container_id] /bin/bash
```

### Ver contenedores creados

```sh
docker ps
```

### Ver imágenes creadas

```sh
docker images
```

## Enviar una solicitud de entrenamiento

### Para enviar una solicitud al endpoint `/train`, sigue estos pasos:

1. **Crear una nueva solicitud**:
    - Haz clic en el botón "New" y selecciona "Request".

2. **Configurar la solicitud**:
    - Asigna un nombre a la solicitud, por ejemplo, "Train Model".
    - Selecciona una colección o crea una nueva para guardar la solicitud.
    - Haz clic en "Save to [Collection Name]".

3. **Configurar los detalles de la solicitud**:
    - Método: Selecciona `POST`.
    - URL: Introduce la URL del endpoint `/train`. Si estás ejecutando Flask localmente en el puerto 3000, la URL será `http://127.0.0.1:3000/train`.

4. **Enviar la solicitud**:
    - Haz clic en "Send".

## Para enviar un archivo a la API REST que acabamos de crear utilizando Postman, sigue estos pasos:

### Enviar un archivo para predecir

1. **Abrir Postman**:
    - Inicia Postman en tu máquina.

2. **Crear una nueva solicitud**:
    - Haz clic en el botón "New" y selecciona "Request".

3. **Configurar la solicitud**:
    - Asigna un nombre a la solicitud, por ejemplo, "Predict File".
    - Selecciona una colección o crea una nueva para guardar la solicitud.
    - Haz clic en "Save to [Collection Name]".

4. **Configurar los detalles de la solicitud**:
    - Método: Selecciona `POST`.
    - URL: Introduce la URL del endpoint `/predict`. Si estás ejecutando Flask localmente en el puerto 3000, la URL será `http://127.0.0.1:3000/predict`.

5. **Añadir el archivo**:
    - Ve a la pestaña "Body".
    - Selecciona "form-data".
    - En la clave, escribe `file`.
    - En el valor, selecciona el tipo "File" desde el menú desplegable.
    - Haz clic en "Choose Files" y selecciona el archivo que deseas enviar.

6. **Enviar la solicitud**:
    - Haz clic en "Send".
