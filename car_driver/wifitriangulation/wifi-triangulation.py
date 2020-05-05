import os
from scapy.all import *
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, RadioTap
from threading import Thread
import matplotlib.pyplot as plt
import time
import math


# sudo ifconfig wlx00c0ca665094 down
# sudo iwconfig wlx00c0ca665094 mode monitor
# sudo ifconfig wlx00c0ca665094 up


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


class WifiTriangulation(Thread):
    running = True
    dict_wifi = {}
    dict_poss = {"b2:75:41:37:32:db": [1.95878, 3.8125, 0],
                 "9a:cf:31:12:42:69": [0.6, 0, 0],
                 "30:b5:c2:c8:58:83": [1.95878, 3.95878, 0],
                 "78:29:ed:83:f5:85": [1.8111, 3.95878, 0]}
    interface = "wlx00c0ca665094"

    def run(self) -> None:
        # start the channel changer
        channel_changer = Thread(target=self.change_channel)
        channel_changer.daemon = True
        channel_changer.start()

        # start sniffing
        channel_changr = Thread(target=self.snif)
        channel_changr.daemon = True
        channel_changr.start()

        self.print_all()
        print("[INFO] Wifi triangulation finished")

    def generate_plot(self, points):
        xaxis = []
        yaxis = []
        for (x, y, signal) in points.values():
            if signal >= 1:
                xaxis.append(x)
                yaxis.append(y)

        color = list('Blue' for i in range(len(xaxis) - 1))
        color.append('Green')

        plt.scatter(xaxis, yaxis, color=color)

        for i in range(len(xaxis) - 2):
            plt.plot([xaxis[i], xaxis[i + 1]], [yaxis[i], yaxis[i + 1]], 'k-')
            plt.plot([xaxis[i], xaxis[-1]], [yaxis[i], yaxis[-1]], 'r-')
        if len(xaxis) >= 2:
            plt.plot([xaxis[0], xaxis[-2]], [yaxis[0], yaxis[-2]], 'k-')
            plt.plot([xaxis[-2], xaxis[-1]], [yaxis[-2], yaxis[-1]], 'r-')

        plt.xlabel('x-axis')
        plt.ylabel('y-axis')

        # plt.savefig('fo.png')
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
                pass
                # print("[Warning] dbm_signal not mesurable")
            else:
                self.dict_wifi[bssid] = [ssid, dbm_signal, channel, frequency, distance]

    def print_all(self):
        while self.running:
            time.sleep(8)
            for k in self.dict_poss.keys():
                if k in self.dict_wifi:
                    self.dict_poss[k][2] = (75 + self.dict_wifi[k][1]) * (75 + self.dict_wifi[k][1]) * (
                            75 + self.dict_wifi[k][1])
                else:
                    self.dict_poss[k][2] = 0
            self.dict_poss["cotxe"] = triangulate(self.dict_poss)
            self.generate_plot(self.dict_poss)

            self.dict_wifi.clear()

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


if __name__ == "__main__":
    wifi = WifiTriangulation()
    wifi.start()
    print("starting")
    time.sleep(35)
    print("stop")
    wifi.stop()
    wifi.join()
    print("end")
