from carvision.qr_object_detection import CarVision
import time
import random

# CarVision().start()
# print("eee")
input()
from apiconnection.soketclient import socket
lat = 1.3232
lon = 3.9548
estat = 'ocupat'
while True:
    lat += random.uniform(-1, 1)
    lon += random.uniform(-1, 1)
    socket.update_position(lat, lon)
    time.sleep(1)
    if random.uniform(0, 6) > 5:
        if estat != 'ocupat':
            estat = 'ocupat'
            socket.update_status('ocupat')
    elif random.uniform(0, 6) < 1:
        if estat != 'lliure':
            estat = 'lliure'
            socket.update_status('lliure')

socket.disconnect()