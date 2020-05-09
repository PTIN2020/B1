from carvision.qr_object_detection import CarVision
# from wifitriangulation.wifi_triangulation import WifiTriangulation
from driverconnection.arduino_connector import ArduinoConnector

# QT_X11_NO_MITSHM=1 python main.py

# wifi_module = WifiTriangulation("wlx00c0ca665094")
# wifi_module.start()

arduino_module = ArduinoConnector()

vision_module = CarVision(arduino_module)
vision_module.start()

stop = 0
while vision_module.running:
    if input('[Info] pres q to exit') == 'q':
        print('[INFO] ...')
        vision_module.stop()

# wifi_module.stop()
vision_module.join()
# wifi_module.join()

print('END')

# input()
# from car_driver.apiconnection.soketclient import socket
# lat = 1.3232
# lon = 3.9548
# estat = 'ocupat'
# while True:
#     lat += random.uniform(-1, 1)
#     lon += random.uniform(-1, 1)
#     socket.update_position(lat, lon)
#     time.sleep(1)
#     if random.uniform(0, 6) > 5:
#         if estat != 'ocupat':
#             estat = 'ocupat'
#             socket.update_status('ocupat')
#     elif random.uniform(0, 6) < 1:
#         if estat != 'lliure':
#             estat = 'lliure'
#             socket.update_status('lliure')
#
# socket.disconnect()
