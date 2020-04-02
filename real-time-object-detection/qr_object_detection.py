from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
from pyzbar import pyzbar


def check_for_object(frame):
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.2:
            (h, w) = frame.shape[:2]
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            cv2.rectangle(frame, (startX, startY), (endX, endY), 150, 2)


def check_qr_code_cv2(frame):
    data, bbox, _ = qrDecoder.detectAndDecode(frame)

    if data:
        print("[+] QR Code detected, data:", data)
        if bbox is not None:
            for i in range(len(bbox)):
                cv2.line(frame, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)


def check_qr_code_pyzbar(frame):
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")
        cv2.putText(frame, barcodeData, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


def chech_video_videostream(video=0):
    print("[INFO] starting video stream...")
    # cap = cv2.VideoCapture('proba2.mp4')
    cap = VideoStream(src=video).start()
    time.sleep(2.0)
    fps = FPS().start()

    while True:
        frame = cap.read()
        frame = imutils.resize(frame, width=500)

        check_for_object(frame)
        check_qr_code_pyzbar(frame)

        cv2.imshow("Frame", frame)
        fps.update()

        if cv2.waitKey(1) == ord("q"):
            break

    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # una mica de neteja
    cap.stop()
    cv2.destroyAllWindows()


def chech_video_cv2(video=0):
    print("[INFO] starting video stream...")
    cap = cv2.VideoCapture(video)
    if (cap.isOpened() == False):
        print("[ERROR] Unable to read camera feed")

    # out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (600, 337))

    time.sleep(2.0)

    while True:
        _, frame = cap.read()
        if _:
            frame = imutils.resize(frame, width=600)

            check_for_object(frame)
            check_qr_code_pyzbar(frame)

            cv2.imshow("Frame", frame)
            # out.write(frame)

            if cv2.waitKey(1) == ord("q"):
                break
        else:
            break
    # una mica de neteja
    cap.release()
    # out.release()
    print("[INFO] finished")
    cv2.destroyAllWindows()


print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe('Models/Mode.prototxt.txt', 'Models/Mode.caffemodel')

print("[INFO] loading QR code detector...")
qrDecoder = cv2.QRCodeDetector()

chech_video_cv2(0)
# chech_video_cv2()
