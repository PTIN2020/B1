from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2


# Llegim el nostre model serielitzat
print("[INFO] loading model...")
net = cv2.dnn.readNetFromTensorflow('Models/model_ssdlite.pb')


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

	# Use the given image as input, which needs to be blob(s).
	net.setInput(cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False))
	# Runs a forward pass to compute the net output
	networkOutput = net.forward()

	for detection in networkOutput[0, 0]:
		score = float(detection[2])
		if score > 0.2:
			rows, cols, channels = frame.shape
			left = detection[3] * cols
			top = detection[4] * rows
			right = detection[5] * cols
			bottom = detection[6] * rows

			# draw a red rectangle around detected objects
			cv2.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), thickness=2)

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

