# Detección en tiempo real de objetos y codigos QR
Captura d'imatges a partir de la càmera web per a processar-a través del nostre model per detectar objectes i codis QR, per tal de poder detectar persones i objectes que són al centre de la imatge i obtenir informació dels codis QR llegits

## instal·lació

Per procedir a la seva instal·lació d'aquest modul, serà necessari descarregar el repositori i instal·lar els paquets enumerats en el document requirements.txt
```console
$ git clone https://github.com/PTIN2020/B1.git
$ cd B1/car_driver/carvision
$ pip install -r requirements.txt
```


## Funcionament

L'arxiu `qr_object_detection.py`, és l'encarregat d'executar el reconeixement d'objectes juntament amb el dels codis QR a parir de la càmera web de el dispositiu.

Un cop el programa és executat, en aquesta versió de mostra, es mostrarà una finestra amb els frames capturats per la webcam amb els objectes detectats per la AI, delimitats amb un rectangle de diferents colors depenen de la proximitat:
- Blau: El cotxe seguirà la linneà amb normalitat.
- Groc: S'enviarà una senyal al controlador del cotxe per a disminuir la velocitat.
- Vermell: El cotxe s'aturarà fins nova senyal
![Deterrió de proximitat](/car_driver/carvision/videos/resultats/Sensor_de_proximitat.gif)

Per altra banda, també s'encarregarà de cercar codis QR per tal d'identificar les parades i així reforçarà el posicionament.
Un com es rebi una notificació per a anar a una parada en concret, el cotxe utilitzarà la ubicació per arribar fins a l'aturada, però per quedar-se exactament en el seu lloc cercarà el codi QR de l'aturada i un cop el trobi enviarà la notificació al client informant que ja ha arribat
![Deterrió de proximitat](/car_driver/carvision/videos/resultats/sensor_aturades.gif)


Per veure algunes mostres del funcionament i la seva evolució, podeu observar els següents vídeos:
 - [Prova de reconeixement de codis QR i clients](/car_driver/carvision/videos/resultats/Deteccion-de-clientes-y-QR.avi)
 - [Prova de reconeixement de clients](/car_driver/carvision/videos/resultats/Deteccion-de-clientes.mp4)
 - [Prova de reconeixement de clients i objectes](/car_driver/carvision/videos/resultats/Deteccion-de-clientes-y-objetos.mp4)



