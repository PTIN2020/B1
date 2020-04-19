import serial

arduino = serial.Serial('/dev/ttyACM0', 9600) #abrimos la conexion por el puerto serial.

print("Starting!")

while True:
      comando = raw_input('Introduce un comando: ') #Input
      arduino.write(comando) #Mandar un comando hacia Arduino
	# Esta parte del codigo es prescindible, pero de momento la usaremos por tal de verificar el funcionamiento del mismo
      if comando == 'D':
            print('ENCIENDE DERECHO')
      elif comando == 'I':
            print('ENCIENDE IZQUIERDO')
      elif comando == 'S':
            print('APAGA MOTORES')

arduino.close() #Finalizamos la comunicacion