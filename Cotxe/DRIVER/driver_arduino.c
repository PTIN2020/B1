int ledi = 13;
int ledd = 12;
void setup () {
   pinMode(led, OUTPUT); //LED 13 como salida
   Serial.begin(9600); //Inicializo el puerto serial a 9600 baudios
}

/*
	Este pequeño driver, de momento controla leds por tal de que se enciendan y se apaguen,
	estos leds simulan a los motores del coche, de momento implementaremos tres funciones muy sencillas:
	- ENcender el motor derecho.
	- Encender el motor izquierdo.
	- Detener los motores.
*/
void loop () {
   if (Serial.available()) { //Si está disponible
      char c = Serial.read(); //Guardamos la lectura en una variable char
      if (c == 'D') { //Enciendo el motor derecho
         digitalWrite(ledd, HIGH);
      } else if (c == 'I') { //Enciendo el motor izquierdo
         digitalWrite(ledi, HIGH
      } else if (c == 'S') { //Apago los motores
         digitalWrite(ledi, LOW);
	 digitalWrite(ledd, LOW);
      }
   }
}
