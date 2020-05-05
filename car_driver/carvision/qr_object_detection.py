from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
from pyzbar import pyzbar
from threading import Thread


class CarVision(Thread):
    running = False

    def __init__(self, arduino_module):
        super().__init__()

        self.arduino_module = arduino_module

        print("[INFO] loading AI model...")
        self.net = cv2.dnn.readNetFromCaffe('carvision/model/Mode.prototxt.txt', 'carvision/model/Mode.caffemodel')

        self.stat = 0
        self.code = 0

    def run(self):
        print("[INFO] Starting vision module...")
        self.running = True

        cap = VideoStream(src=0).start()
        # cap = VideoStream(usePiCamera=True).start()

        time.sleep(2.0)
        while self.running:
            frame = cap.read()
            frame = imutils.resize(frame, width=600)

            self.check_for_code(frame)
            self.check_for_object(frame)

            self.arduino_module.send(self.stat)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord("q"):
                break


        print("[INFO] Stoping vision module...")
        cap.stop()
        cv2.destroyAllWindows()
        self.running = False

    def check_for_object(self, frame):
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        self.net.setInput(blob)
        detections = self.net.forward()

        (h, w) = frame.shape[:2]

        self.stat = 2
        color = (255, 0, 0)
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                if (endY - startY) / h < 0.95 and (endX - startX) / w < 0.95:
                    if endY / h > 0.6 and (startX / w < 0.8 and endX / w > 0.2):
                        self.stat = 0
                        color = (0, 0, 255)
                    elif endY / h > 0.4:
                        if self.stat > 1:
                            self.stat = 1
                            color = (0, 255, 255)

                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    def check_for_code(self, frame):
        codes = pyzbar.decode(frame)
        self.code = 0
        for code in codes:
            self.code = code.data.decode("utf-8")
            (x, y, w, h) = code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def stop(self):
        self.running = False
