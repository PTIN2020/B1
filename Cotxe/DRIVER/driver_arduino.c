int ledi = 2;
int ledd = 4;
int leds = 12;
void setup () {
   pinMode(ledi, OUTPUT); //LED 13 como salida
   pinMode(ledi, OUTPUT); //LED 13 como salida
   Serial.begin(9600); //Inicializo el puerto serial a 9600 baudios
   digitalWrite(leds,HIGH);
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
         digitalWrite(leds,LOW);
         digitalWrite(ledd, HIGH);
      } else if (c == 'I') { //Enciendo el motor izquierdo
         digitalWrite(leds,LOW);
         digitalWrite(ledi, HIGH);
      } else if (c == 'S') { //Apago los motores
         digitalWrite(ledi, LOW);
         digitalWrite(ledd, LOW);
         digitalWrite(leds,HIGH);
      }
   }
}
