# Detección en tiempo real de objetos y codigos QR
Captura d'imatges a partir d'un vídeo o de la càmera web per a processar-a través del nostre model per detectar objectes i codis QR, per tal de poder detectar persones i objectes que són al centre de la imatge i obtenir informació dels codis QR llegits

## instal·lació

Per procedir a la seva instal·lació, serà necessari descarregar el repositori i instal·lar els paquets enumerats en el document requirements.txt
```console
$ git clone https://github.com/ToniCifre/real-time-object-detection.git
$ cd real-time-object-detection
$ pip install -r requirements.txt
```


## Funcionament

L'arxiu `qr_object_detection.py`, és l'encarregat d'executar el reconeixement d'objectes juntament amb el dels codis QR a parir de la càmera web de el dispositiu.

Un cop el programa és executat, es mostrarà una finestra amb els frames capturats per la teva webcam on es mostrarà amb un rectangle de color blau els objectes que la nostra AI és capaç de reconèixer i amb un rectangle de color vermell es mostrés es codis QR que està detectant, a més de la informació que contenen sobre de l'requadre

Per veure una mostra de com funciona, podeu observar els següents resultats:
 - [Prova de reconeixement de codis QR i clients](/real-time-object-detection/Videos/resultats/Deteccion-de-clientes-y-QR.avi)
 - [Prova de reconeixement de clients](/real-time-object-detection/Videos/resultats/Deteccion-de-clientes.mp4)
 - [Prova de reconeixement de clients i objectes](/real-time-object-detection/Videos/resultats/Deteccion-de-clientes-y-objetos.mp4)

Aquests programes en Python encara estan sent depurats, de manera que no és fàcil d'usar i comprovar per parts externes.