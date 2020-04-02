import cv2

# inicialitza la transmissió de vídeo i el comptador de FPS
print("[INFO] starting video stream...")
cam = cv2.VideoCapture(0)
qrDecoder = cv2.QRCodeDetector()

while True:
    _, img = cam.read()
    data, bbox, _ = qrDecoder.detectAndDecode(img)

    # check if there is a QRCode in the image
    if bbox is not None:
        # display the image with lines
        for i in range(len(bbox)):
            # draw all lines
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
        if data:
            print("[+] QR Code detected, data:", data)
    # display the result
    cv2.imshow("img", img)
    if cv2.waitKey(1) == ord("q"):
        break

# atura el temporitzador i mostram alguna informació sobre els FPS
print("[INFO] elapsed time: {:.2f}".format(img.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(img.fps()))


cam.release()
cv2.destroyAllWindows()