import serial


class ArduinoConnector:

    def __init__(self):
        self.actual_code = 0
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 9600)
        except serial.serialutil.SerialException:
            print('[Error] connection to arduino')
            # exit(1)

    def send(self, code):
        if code != self.actual_code:
            if code == 0:
                print(0)
                # self.arduino.write('s')  # Stop
            elif code == 1:
                print(1)
                # self.arduino.write('m')  # Medium
            elif code == 2:
                print(2)
                # self.arduino.write('f')  # Full
            else:
                print('[Warning] Bad Code')
            self.actual_code = code

    def close(self):
        self.arduino.close()
