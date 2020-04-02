# Detección en tiempo real de objetos y codigos QR
Captura de imágenes a partir de un video o de la webcam para procesarlas a través de nuestro modelo para detectar objetos y códigos QR, con el fin de poder detectar personas y objetos que están en el centro de la imagen y obtener información de los códigos QR leídos

## instal·lació

Para proceder a su instalación, sera necesario descargar el repositorio e instalar los paquetes enumerados en el documento requirements.txt
```console
$ git clone https://github.com/ToniCifre/real-time-object-detection.git
$ cd real-time-object-detection
$ pip install -r requirements.txt
```


## Funcionament

El archivo `qr_object_detection.py`, es el encargado de ejecutar el reconocimiento de objetos juntamente con el de los códigos QR

Una vez el programa es ejecutado, se mostrará una ventana con los frames capturados por tu webcam donde se mostrará con un rectángulo de color azul los objetos que nuestra AI es capaz de reconocer y con un rectángulo de color rojo se mostrara se códigos QR que está detectando, además de la información que contienen encima del recuadro
