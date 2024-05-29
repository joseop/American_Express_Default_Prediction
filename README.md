# American Express - Default Prediction
-----------------------------
# Fase 1
## Como usar
Ejecute el cuaderno `01 - Analisis de datos, modelos e interacciones` para extraer los datos de prueba, tratarlos y mostrar los resultados del modelado predictivo

-------------
# Fase 2
## Instrucciones Docker
Clonar el repositorio y abrir la terminal en esta carpeta fase 2, ejecutar los siguientes comandos para la creacion y ejecucion del contenedor

1. Crear la imagen
```console
 docker build -t american .
```

2. Hacer un docker con la iamgen creada y ver el cmd del docker en tiempo real
```console
 docker run -p 3000:3000 -it --name american american
```
3. Inicializa el contenedor 
```console
docker start {id del contenedor}
```
4. Entrar a los archivos del docker
```console
docker exec -it {id del contenedor} /bin/bash
```

Eexplorar archivos y las predicciones resultantes

-------------
# Fase 3
## Instrucciones Api Rest con Docker
Clonar el repositorio y abrir la terminar el la raiz de la carpeta fase 3, a continuacion ejecutar los siguientes comandos

1. Construir el contenedor
```console
 docker build -t api .
```
2. Ejecutar el contendor
```console
 docker run -it -p 5000:5000 api
```
3. Ejecutar el cliente
```console
 python client3.py
```

-------------
### Miembros del equipo

- Andres Felipe Graciano Monsalve CC71375739 Ingeniería de Sistemas

- Jose Carlos Ortiz Padilla CC 1003059949 Ingeniería de sistemas

- Sulay Gisela Martínez Barreto CC 1038137981 Ingeniería de sistemas
