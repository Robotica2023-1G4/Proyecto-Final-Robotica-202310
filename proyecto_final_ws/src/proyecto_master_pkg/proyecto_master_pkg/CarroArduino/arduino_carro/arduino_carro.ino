#include <SoftwareSerial.h>

char VarChar;

//Traccion tasera
#define entrada1 4 //Izquierda
#define entrada2 5 
#define entrada3 6 //Derecha
#define entrada4 7 

//Traccion delantera
#define entrada5 8 //Izquierda
#define entrada6 9 
#define entrada7 10 //Derecha
#define entrada8 11 

// TODO: Definir los pines de los encoders 
#define encoderPinATI 18
#define encoderPinBTI 17
#define encoderPinADI 19
#define encoderPinBDI 22
#define encoderPinATD 2
#define encoderPinBTD 23
#define encoderPinADD 3   
#define encoderPinBDD 24             

// Definir las variables de posición de los encoders
volatile int ticksTI = 0;
volatile int ticksDI = 0;
volatile int ticksTD = 0;
volatile int ticksDD = 0;

// Definir la direccion hacia la que ve el encoder (False -> Atras, Verdadero -> Adelante)
boolean dirTI = true;
boolean dirDI = true;
boolean dirTD = true;
boolean dirDD = true;

// variables para definiciòn del tiempo de muestreo
int k=1000;
volatile unsigned muestreoActual = 0;                     
volatile unsigned muestreoAnterior = 0;
volatile unsigned deltaMuestreo = 0;


void setup() {

  pinMode(entrada1,OUTPUT);
  pinMode(entrada2,OUTPUT);
  pinMode(entrada3,OUTPUT);
  pinMode(entrada4,OUTPUT);
  pinMode(entrada5,OUTPUT);
  pinMode(entrada6,OUTPUT);
  pinMode(entrada7,OUTPUT);
  pinMode(entrada8,OUTPUT);

  // Configurar los pines de los encoders como entradas
  pinMode(encoderPinATI, INPUT_PULLUP);
  pinMode(encoderPinBTI, INPUT_PULLUP);
  pinMode(encoderPinADI, INPUT_PULLUP);
  pinMode(encoderPinBDI, INPUT_PULLUP);
  pinMode(encoderPinATD, INPUT_PULLUP);
  pinMode(encoderPinBTD, INPUT_PULLUP);
  pinMode(encoderPinADD, INPUT_PULLUP);
  pinMode(encoderPinBDD, INPUT_PULLUP);

  // Habilitar las interrupciones para los pines de los encoders
  attachInterrupt(digitalPinToInterrupt(encoderPinATI), actualizarTI, RISING);
  attachInterrupt(digitalPinToInterrupt(encoderPinADI), actualizarDI, RISING);
  attachInterrupt(digitalPinToInterrupt(encoderPinATD), actualizarTD, RISING);
  attachInterrupt(digitalPinToInterrupt(encoderPinADD), actualizarDD, RISING);

  // Inicializar el puerto serie
  Serial.begin(9600);
}


void loop() {

  if (Serial.available()) {VarChar = Serial.read();}

  movimiento();

  muestreoActual = millis(); //Tiempo actual de muestreo

  deltaMuestreo =(double) muestreoActual - muestreoAnterior; // delta de muestreo 

  if ( deltaMuestreo >= k) // se asegura el tiempo de muestreo
  {   
    Serial.print(ticksTI); 
    Serial.print(","); 
    Serial.print(ticksDI);
    Serial.print(",");
    Serial.print(ticksTD);  
    Serial.print(",");
    Serial.print(ticksDD);
    Serial.print(",");
    Serial.println(deltaMuestreo);                
    muestreoAnterior = muestreoActual;// actualización del muestreo anterio

    ticksTI = 0; // actualización de la variable 
    ticksDI = 0; // actualización de la variable 
    ticksTD = 0; // actualización de la variable 
    ticksDD = 0; // actualización de la variable 
  }
}



void movimiento(){

  switch(VarChar) { 

    case 'W':
      digitalWrite(entrada1,HIGH);
      digitalWrite(entrada2,LOW);
      digitalWrite(entrada3,HIGH);
      digitalWrite(entrada4,LOW);
      digitalWrite(entrada5,HIGH);
      digitalWrite(entrada6,LOW); 
      digitalWrite(entrada7,HIGH);
      digitalWrite(entrada8,LOW);
      break;

    case 'S':
      digitalWrite(entrada1,LOW);
      digitalWrite(entrada2,HIGH);
      digitalWrite(entrada3,LOW);
      digitalWrite(entrada4,HIGH);
      digitalWrite(entrada5,LOW);
      digitalWrite(entrada6,HIGH);
      digitalWrite(entrada7,LOW);
      digitalWrite(entrada8,HIGH);
      break;
      
    case 'Q':
      digitalWrite(entrada1,LOW);
      digitalWrite(entrada2,HIGH);
      digitalWrite(entrada3,HIGH);   //aTRAS IZQUIERDA
      digitalWrite(entrada4,LOW);
      digitalWrite(entrada5,HIGH);
      digitalWrite(entrada6,LOW); 
      digitalWrite(entrada7,LOW);    // NO ES  ADELANTE IZQ
      digitalWrite(entrada8,HIGH);
      break;
      
    case 'E':
      digitalWrite(entrada1,HIGH);
      digitalWrite(entrada2,LOW);
      digitalWrite(entrada3,LOW);
      digitalWrite(entrada4,HIGH);
      digitalWrite(entrada5,LOW);
      digitalWrite(entrada6,HIGH);
      digitalWrite(entrada7,HIGH);
      digitalWrite(entrada8,LOW);
      break;

    case 'A':
      digitalWrite(entrada1,HIGH);
      digitalWrite(entrada2,LOW);
      digitalWrite(entrada3,LOW);
      digitalWrite(entrada4,HIGH);
      digitalWrite(entrada5,HIGH);
      digitalWrite(entrada6,LOW);
      digitalWrite(entrada7,LOW);
      digitalWrite(entrada8,HIGH);
      break;

    case 'D':
      digitalWrite(entrada1,LOW);
      digitalWrite(entrada2,HIGH);
      digitalWrite(entrada3,HIGH);
      digitalWrite(entrada4,LOW);
      digitalWrite(entrada5,LOW);
      digitalWrite(entrada6,HIGH);
      digitalWrite(entrada7,HIGH);
      digitalWrite(entrada8,LOW);
      break;

    case '0': 
      digitalWrite(entrada1,LOW);
      digitalWrite(entrada2,LOW);
      digitalWrite(entrada3,LOW);
      digitalWrite(entrada4,LOW);
      digitalWrite(entrada5,LOW);
      digitalWrite(entrada6,LOW);
      digitalWrite(entrada7,LOW);
      digitalWrite(entrada8,LOW);
      break;
  }
}

void actualizarTI() {
  int val = digitalRead(encoderPinBTI);
  if(val == LOW) {
    dirTI = false; //Reversa
    ticksTI--;
  }
  else{
    dirTI = true; //Adelante
    ticksTI++;
  }
}

void actualizarDI() {
  int val = digitalRead(encoderPinBDI);
  if(val == LOW) {
    dirDI = true; //Adelante
    ticksDI++;
  }
  else{
    dirDI = false; //Atras
    ticksDI--;
  }
}

void actualizarTD() {
  int val = digitalRead(encoderPinBTD);
  if(val == LOW) {
    dirTD = false; //Reversa
    ticksTD--;
  }
  else{
    dirTD = true; //Adelante
    ticksTD++;
  }
}

void actualizarDD() {
  int val = digitalRead(encoderPinBDD);
  if(val == LOW) {
    dirDD = false; //Reversa
    ticksDD--;
  }
  else{
    dirDD = true; //Adelante
    ticksDD++;
  }
}
