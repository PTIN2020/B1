from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
from pyzbar import pyzbar
from threading import Thread


class CarVision(Thread):

    def __init__(self):
        super().__init__()
        print("[INFO] loading AI model...")
        self.net = cv2.dnn.readNetFromCaffe('carvision/model/Mode.prototxt.txt', 'carvision/model/Mode.caffemodel')
        print("[INFO] loading QR code detector...")
        self.qrDecoder = cv2.QRCodeDetector()

    def run(self):
        self.chech_video_videostream()

    def chech_video_videostream(self, video=0):
        print("[INFO] starting video stream...")
        cap = VideoStream(src=video).start()
        # cap = VideoStream(usePiCamera=True).start()

        time.sleep(2.0)

        while True:
            frame = cap.read()
            frame = imutils.resize(frame, width=600)

            self.check_for_object(frame)
            self.check_qr_code_pyzbar(frame)

            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) == ord("q"):
                break

        cap.stop()
        cv2.destroyAllWindows()

    def check_for_object(self, frame):
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        self.net.setInput(blob)
        detections = self.net.forward()

        (h, w) = frame.shape[:2]

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                if endY / h > 0.6 and (startX / w < 0.8 and endX / w > 0.2):
                    color = (0, 0, 255)
                elif endY / h > 0.4:
                    color = (0, 255, 255)
                else:
                    color = (255, 0, 0)
                if (endY - startY) / h < 0.9 and (endX - startX) / w < 0.9:
                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    def check_qr_code_pyzbar(self, frame):
        codes = pyzbar.decode(frame)

        for barcode in codes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            data = barcode.data.decode("utf-8")
            cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)



