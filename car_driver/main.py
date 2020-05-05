from carvision.qr_object_detection import CarVision
import time
import random

c = CarVision()
c.start()
print("eee")
stop = 0
while stop < 300:
    print(c.stat)
    print(c.code)
    stop += 1
    time.sleep(0.1)
c.stop()
c.join()
print("dfaskjdhfkasdgfahsdfhadskfh")
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
