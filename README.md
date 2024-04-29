# American Express - Default Prediction
-----------------------------

## Como usar
Ejecute el cuaderno `01 - Analisis de datos, modelos e interacciones` para extraer los datos de prueba, tratarlos y mostrar los resultados del modelado predictivo

-------------

## Instrucciones Docker
Clonar el repositorio y abrir la terminal en esta carpeta, ejecutar los siguientes comandos para la creacion y ejecucion del contenedor

1. docker build -t american . --> crear la imagen

2. docker run -p 3000:3000 -it --name american american --> hacer un docker con la iamgen creada y ver el cmd del docker en tiempo real

3.docker start {id del contenedor} --> inicializa el contenedor 

4. docker exec -it {id del contenedor} /bin/bash --> entrar a los archivos del docker

5. docker ps ---> ver docker creados

6. docker images --> ver imagenes creadas

7. explorar archivos y las predicciones resultantes

   
-------------
### Miembros del equipo

- Andres Felipe Graciano Monsalve CC71375739 Ingeniería de Sistemas

- Jose Carlos Ortiz Padilla CC 1003059949 Ingeniería de sistemas

- Sulay Gisela Martínez Barreto CC 1038137981 Ingeniería de sistemas
