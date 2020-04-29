from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
from pyzbar import pyzbar


def check_for_object(frame):
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    (h, w) = frame.shape[:2]

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            if (endY - startY)/h > 0.8 or (endX - startX)/w > 0.8:
                color = (0, 0, 255)
            else:
                color = (255, 0, 0)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)


def check_qr_code_pyzbar(frame):
    codes = pyzbar.decode(frame)

    for barcode in codes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        data = barcode.data.decode("utf-8")
        cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def chech_video_videostream(video=0):
    print("[INFO] starting video stream...")
    cap = VideoStream(src=video).start()
    # cap = VideoStream(usePiCamera=True).start()

    time.sleep(2.0)

    while True:
        frame = cap.read()
        frame = imutils.resize(frame, width=600)

        check_for_object(frame)
        check_qr_code_pyzbar(frame)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cap.stop()
    cv2.destroyAllWindows()


print("[INFO] loading AI model...")
net = cv2.dnn.readNetFromCaffe('model/Mode.prototxt.txt', 'model/Mode.caffemodel')

print("[INFO] loading QR code detector...")
qrDecoder = cv2.QRCodeDetector()

chech_video_videostream()
