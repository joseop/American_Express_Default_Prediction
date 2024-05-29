# American Express - Default Prediction
-----------------------------
# Fase 1
## Como usar
Ejecute el cuaderno `01 - Analisis de datos, modelos e interacciones` para extraer los datos de prueba, tratarlos y mostrar los resultados del modelado predictivo

-------------
# Fase 2
## Instrucciones Docker
Clonar el repositorio y abrir la terminal en esta carpeta fase 2, ejecutar los siguientes comandos para la creacion y ejecucion del contenedor

1. docker build -t american . --> crear la imagen

2. docker run -p 3000:3000 -it --name american american --> hacer un docker con la iamgen creada y ver el cmd del docker en tiempo real

3.docker start {id del contenedor} --> inicializa el contenedor 

4. docker exec -it {id del contenedor} /bin/bash --> entrar a los archivos del docker

5. docker ps ---> ver docker creados

6. docker images --> ver imagenes creadas

7. explorar archivos y las predicciones resultantes

-------------
# Fase 3
## Instrucciones Api Rest con Docker
Clonar el repositorio y abrir la terminar el la raiz de la carpeta fase 3, a continuacion ejecutar los siguientes comandos

1. ```bash docker build -t api . ``` --> Construir el contenedor
2. docker run -it -p 5000:5000 api  --> Ejecutar el contenedor
3. python client3.py  --> Ejecutar el cliente



-------------
### Miembros del equipo

- Andres Felipe Graciano Monsalve CC71375739 Ingeniería de Sistemas

- Jose Carlos Ortiz Padilla CC 1003059949 Ingeniería de sistemas

- Sulay Gisela Martínez Barreto CC 1038137981 Ingeniería de sistemas
