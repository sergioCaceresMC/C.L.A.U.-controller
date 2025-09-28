#include <BluetoothSerial.h>

#define LED 17 //Led de comprobación de conexión bluetooth
#define NAME "Clau-v1" //Nombre de dispositivo que aparece en la conexión bluetooth

BluetoothSerial SerialBt; //Objeto para la comunicación

void setup() {
  Serial.begin(115200);
  SerialBt.begin(NAME);
  pinMode(LED, OUTPUT);
}

void loop() {
  SerialBt.println("Conectado");
  if (SerialBt.connected(10)){
    digitalWrite(LED, LOW);
  }else{
    digitalWrite(LED, HIGH);
  }
  delay(1000);
}
