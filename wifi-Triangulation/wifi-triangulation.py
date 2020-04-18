import os
os.sys.path.append('/home/toni/Escritorio/wifi-Triangulation/venv/lib/python3.6/site-packages')
os.sys.path.append('/usr/lib/python3.6/lib-dynload')

from scapy.all import *
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, RadioTap
from threading import Thread
import matplotlib.pyplot as plt
import time
import math

dict_wifi = {}
dict_poss = {"96:4d:29:11:56:8b": [0, 0, 0],
             "9a:cf:31:12:42:69": [0.6, 0, 0],
             "60:ab:67:97:7f:9e": [0, 1, 0],
             "9a:1b:eb:af:c9:56": [0, 2, 0]}

plt.figure()

def triangulate(points):
    ws = sum((p[2]) for p in points.values())
    points = tuple((x, y, (signal / ws)) for (x, y, signal) in points.values())

    return [sum(p[0] * p[2] for p in points),  # x
            sum(p[1] * p[2] for p in points),  # y
            1]


def generate_plot(points):
    xaxis = []
    yaxis = []
    for (x, y, signal) in points.values():
        if signal >= 1:
            xaxis.append(x)
            yaxis.append(y)
    print(xaxis)

    color = list('Blue' for i in range(len(xaxis)-1))
    color.append('Green')

    plt.scatter(xaxis, yaxis, color=color)

    for i in range(len(xaxis)-2):
        plt.plot([xaxis[i], xaxis[i+1]], [yaxis[i], yaxis[i+1]], 'k-')
        plt.plot([xaxis[i], xaxis[-1]], [yaxis[i], yaxis[-1]], 'r-')
    plt.plot([xaxis[0], xaxis[-2]], [yaxis[0], yaxis[-2]], 'k-')
    plt.plot([xaxis[-2], xaxis[-1]], [yaxis[-2], yaxis[-1]], 'r-')

    plt.xlabel('x-axis')
    plt.ylabel('y-axis')

    # plt.savefig('fo.png')
    plt.draw()
    plt.pause(0.001)
    plt.clf()


def calc_distance(signalLevelInDb, freqInMHz):
    # distance = 10 ^ ((27.55 - (20 * log10(frequencyInMHz)) + signalLevelInDb)/20)
    exp = (27.55 - (20 * (math.log10(freqInMHz))) + abs(signalLevelInDb)) / 20.0
    return 10 ** exp


def callback(packet):
    if packet.haslayer(Dot11Beacon):
        bssid = packet[Dot11].addr2
        ssid = packet[Dot11Elt].info.decode()
        channel = packet[Dot11Beacon].network_stats().get("channel")
        frequency = packet[0][RadioTap].Channel
        try:
            dbm_signal = packet.dBm_AntSignal
            distance = calc_distance(dbm_signal, frequency)
        except:
            dbm_signal = "N/A"
            distance = 9999

        dict_wifi[bssid] = [ssid, dbm_signal, channel, frequency, distance]


def print_all():
    count = 0
    while True:
        os.system("clear")
        print("{:<20} {:<15} {:<10} {:<10} {:<10} {:<15}".format('MAC', 'ssid', 'dBm_Signal', 'Channel', 'frequency',
                                                                 'distance'))
        for k, v in dict_wifi.copy().items():
            ssid, dBm_Signal, Channel, frequency, distance = v
            print("{:<20} {:<15} {:<10} {:<10} {:<10} {:<15}".format(k, ssid, dBm_Signal, Channel, frequency, distance))
        time.sleep(0.5)
        count += 1
        if count % 20 == 0:
            for k in dict_poss.keys():
                if k in dict_wifi:
                    dict_poss[k][2] = (75 + dict_wifi[k][1])*(75 + dict_wifi[k][1])*(75 + dict_wifi[k][1])
                else:
                    dict_poss[k][2] = 0
            dict_poss["cotxe"] = triangulate(dict_poss)
            generate_plot(dict_poss)

            dict_wifi.clear()


def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel from 1 to 14 each 0.5s
        ch = ch % 14 + 1
        time.sleep(0.5)

def snif():
    sniff(prn=callback, iface=interface)

if __name__ == "__main__":
    plt.ion()
    plt.show()

    interface = "wlx00c0ca665094"

    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    # start sniffing
    channel_changr = Thread(target=snif)
    channel_changr.daemon = True
    channel_changr.start()

    print_all()
