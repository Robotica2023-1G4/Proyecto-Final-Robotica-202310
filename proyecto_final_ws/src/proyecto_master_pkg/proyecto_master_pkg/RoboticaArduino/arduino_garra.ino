#include <Servo.h>

const int servoPin1 = 2;
const int servoPin2 = 3;
const int servoPin3 = 5;
const int servoPin4 = 4;

const int servoPin5 = 6;
const int servoPin6 = 7;

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

void setup() {
  // Configurar los pines de los servos
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo3.attach(servoPin3);
  servo4.attach(servoPin4);
  servo5.attach(servoPin5);
  servo6.attach(servoPin6);
  // Incializa angulos
  servo1.write(100);
  servo2.write(0);
  servo3.write(0);
  servo4.write(90);
  servo5.write(20);
  servo6.write(170);


  // Inicializar comunicación serial
  Serial.begin(9600);
}

void loop() {
  
  // Esperar a recibir datos por el puerto serial
  if (Serial.available() > 0) {
    /*int movRot = Serial.parseInt();
    int movj1 = Serial.parseInt();
    int movj2 = Serial.parseInt();
    int movg = Serial.parseInt();*/

    // Leer la cadena de texto recibida por el puerto serial (Si algo descomentar esto y comentar lo de atras)
    String message = Serial.readStringUntil('\n');
    
    int movRot, movj1, movj2, movj3, movrotg, movg;
    // Extraer valores de la cadena de texto
    sscanf(message.c_str(), "%d,%d,%d,%d,%d,%d", &movRot, &movj1, &movj2, &movj3, &movrotg, &movg);

    servo1.write(movRot);
    servo2.write(movj1);
    servo3.write(movj2);
    servo4.write(movj3);   
    servo5.write(movrotg);
    servo6.write(movg); 
    

    //Convertir a grados negativos y positivos
    int rot1 = servo1.read();
    int J1 = servo2.read();
    int J2 =servo3.read();
    int J3 = servo4.read();
    int rotg = servo5.read();
    int g = servo6.read();
    // Imprimir los valores de los servos
    Serial.print(rot1);
    Serial.print(",");
    Serial.print(J1);
    Serial.print(",");
    Serial.print(J2);
    Serial.print(",");
    Serial.print(J3);
    Serial.print(",");
    Serial.print(rotg);
    Serial.print(",");
    Serial.println(g);
    
  }              
}