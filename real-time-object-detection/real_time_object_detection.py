from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2


# Llegim el nostre model serielitzat
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe('Models/Mode.prototxt.txt', 'Models/Mode.caffemodel')


# inicialitza la transmissió de vídeo i el comptador de FPS
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
cam = cv2.VideoCapture(0)
time.sleep(2.0)
# fps = FPS().start()

while True:
	# agafa el fotograma del flux de vídeo i modifiquem el tamany
	# frame = vs.read()
	_, frame = cam.read()
	frame = imutils.resize(frame, width=600)

	# agafem les dimensions del marc i obtenim en un bloc
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (600, 600)),
		0.007843, (300, 300), 127.5)

	# passam el bloc per la xarxa i obtenim les deteccions
	net.setInput(blob)
	detections = net.forward()

	# loop sobre les deteccions
	for i in np.arange(0, detections.shape[2]):
		# extreure la confiança (és a dir, la probabilitat) associada a la predicció
		confidence = detections[0, 0, i, 2]

		# filtra les deteccions febles assegurant que la `confiança 'és superior a la confiança mínima
		if confidence > 0.2:
			# calcula les coordenades (x, y) de la caixa de delimitació per a l'objecte
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# dibuixa la predicció al frame
			cv2.rectangle(frame, (startX, startY), (endX, endY), 150, 2)

	# mostra el frame de sortida i mirem si l'usuari apreta la lletra 'q'
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# si s’ha premut la tecla `q`, trenca’t del bucle
	if key == ord("q"):
		break

	# actualitzar el comptador FPS
	# fps.update()

# atura el temporitzador i mostram alguna informació sobre els FPS
# fps.stop()
# print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
# print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# una mica de neteja
cam.release()
cv2.destroyAllWindows()
# vs.stop()