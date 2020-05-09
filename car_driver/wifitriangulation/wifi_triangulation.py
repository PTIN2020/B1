from typing import Optional, Callable, Any, Iterable, Mapping

from scapy.all import *
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, RadioTap
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
import math
from skimage import io


# sudo ifconfig wlx00c0ca665094 down
# sudo iwconfig wlx00c0ca665094 mode monitor
# sudo ifconfig wlx00c0ca665094 up

# {"b2:75:41:37:32:db": [1.95878, 3.8125, 0],
#  "9a:cf:31:12:42:69": [0.6, 0, 0],
#  "30:b5:c2:c8:58:83": [1.95878, 3.95878, 0],
#  "78:29:ed:83:f5:85": [1.8111, 3.95878, 0]}

# maze = io.imread('wifitriangulation/terminal2posicionament.png')
#
# patches = []
# for (x, y, signal) in dict_poss.values():
#     patches.append(Circle((int(x), int(y)), radius=5, color='red'))
#
# fig, ax = plt.subplots(1)
# ax.imshow(maze)
# for p in patches:
#     ax.add_patch(p)
# plt.show()

def triangulate(points):
    ws = sum((p[2]) for p in points.values())
    if ws == 0:
        return [0, 0, 1]
    points = tuple((x, y, (signal / ws)) for (x, y, signal) in points.values())

    return [sum(p[0] * p[2] for p in points),  # x
            sum(p[1] * p[2] for p in points),  # y
            1]


def calc_distance(signalLevelInDb, freqInMHz):
    # distance = 10 ^ ((27.55 - (20 * log10(frequencyInMHz)) + signalLevelInDb)/20)
    exp = (27.55 - (20 * (math.log10(freqInMHz))) + abs(signalLevelInDb)) / 20.0
    return 10 ** exp


def read_csv():
    dict_poss = {}
    import csv
    with open('wifitriangulation/wifi_dictionary.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            dict_poss[row[0]] = [int(num) for num in row[1:]]
    return dict_poss


class WifiTriangulation(Thread):
    running = True
    dict_wifi = {}
    dict_poss = read_csv()

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.position = "16.0;15.2"

    def run(self) -> None:
        print("[INFO] Starting wifi module ...")

        os.system("ifconfig wlx00c0ca665094 down")
        time.sleep(1)
        os.system("iwconfig wlx00c0ca665094 mode monitor")
        time.sleep(1)
        os.system("ifconfig wlx00c0ca665094 up")
        time.sleep(3)

        # start the channel changer
        channel_changer = Thread(target=self.change_channel)
        channel_changer.daemon = True
        channel_changer.start()

        # start sniffing
        channel_changr = Thread(target=self.snif)
        channel_changr.daemon = True
        channel_changr.start()

        self.triangulating()
        print("[INFO] Wifi module finished")

    def generate_plot(self, dict_poss):
        x_axis = []
        y_axis = []
        for (x, y, signal) in dict_poss.values():
            if signal >= 0:
                x_axis.append(x)
                y_axis.append(y)

        color = list('Blue' for i in range(len(x_axis) - 1))
        color.append('Green')

        maze = io.imread('wifitriangulation/terminal2posicionament.png')
        fig, ax = plt.subplots(1)
        ax.imshow(maze)

        plt.scatter(x_axis, y_axis, color=color)

        for i in range(len(x_axis) - 1):
            plt.plot([x_axis[i], x_axis[-1]], [y_axis[i], y_axis[-1]], 'r-')

        plt.draw()
        plt.pause(0.001)
        plt.clf()

    def callback(self, packet):
        if packet.haslayer(Dot11Beacon):
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode()
            channel = packet[Dot11Beacon].network_stats().get("channel")
            frequency = packet[0][RadioTap].Channel
            try:
                dbm_signal = packet.dBm_AntSignal
                distance = calc_distance(dbm_signal, frequency)
            except Exception:
                dbm_signal = -75
                distance = 9999
                # print("[Warning] dbm_signal not mesurable")
            self.dict_wifi[bssid] = [ssid, dbm_signal, channel, frequency, distance]

    def triangulating(self):
        while self.running:
            time.sleep(8)
            for k in self.dict_poss.keys():
                if k in self.dict_wifi:
                    self.dict_poss[k][2] = pow((75 + self.dict_wifi[k][1]), 3)
                else:
                    self.dict_poss[k][2] = 0
            self.dict_poss["cotxe"] = triangulate(self.dict_poss)
            self.generate_plot(self.dict_poss)

            self.dict_wifi.clear()

        print("[INFO] Stoping wifi module...")

    def change_channel(self):
        ch = 1
        while self.running:
            os.system(f"iwconfig {self.interface} channel {ch}")
            ch = ch % 14 + 1
            time.sleep(0.5)

    def snif(self):
        sniff(prn=self.callback, iface=self.interface)

    def stop(self):
        self.running = False
