# HoteleriaDjangoRestFramework

Este es un proyecto en donde se pretende hacer uso de django para resolver un problema, el problema en cuestion se encuentra en el fichero enunciado.

El proyecto se puede correr usando docker o los comandos de django por defecto.

## Instalación

Para instalar y ejecutar este proyecto, sigue estos pasos:

1.  **ejecutar un built con el Dockerfile incluido:**
    ```docker build -t test/docker-django .
2.  **correr un contenedor con la imagen:**
    ```docker run -p 8000:8000 test/docker-django

## Instrucciones:

Cada vez que se ejecute el build se borraran los datos y se cargaran datos de las habitaciones, las habitaciones cargadas son de la 101 a la 105, 201 a 205... hasta 605.

## Endpoints:
los endpoints disponibles son los siguientes:

1.  GET /api/rooms/:                            lista rooms
2.  GET /api/rooms/<int:id>/status/:            muestra el estado de un cuarto
3.  GET /api/reservations/:                     lista reservations
4.  GET /api/reservations/<int:id>/:            obtiene reservation
5.  POST /api/reservations/:                    crea reservations
6.  PUT /api/reservations/<int:id>/:            modifica reservations
7.  POST /api/reservations/<int:id>/checkin:    check in reservation
8.  POST /api/reservations/<int:id>/checkout:   check out reservation
9.  POST /api/reservations/<int:id>/cancelled:  cancela reservation
