#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <TFT_eSPI.h>
#include <BluetoothSerial.h>

//================ Pines y variables ====================

#define I2C_SDA 21      // Pin de transmisión de información
#define I2C_SCL 22      // Pin de sincronización con el reloj
#define BTN1 16         // Pin para dedo índice
#define BTN2 4          // Pin para dedo corazón
#define LED 17          // Led de comprobación de conexión bluetooth
#define NAME "Clau-v1"  // Nombre de dispositivo

//==================== Conexiones =======================


BluetoothSerial SerialBt;
TwoWire I2CMPU = TwoWire(0);
Adafruit_MPU6050 mpu;

void setup(){
  Serial.begin(115200);
  SerialBt.begin(NAME);
  Serial.println("Iniciado");

  I2CMPU.begin(I2C_SDA, I2C_SCL);

  /*
  * Este fragmento tiene conflicto con algunas arquitecturas 
  * por lo que se evita el uso de while para detener la ejecución
  */
  if (!mpu.begin(104, &I2CMPU, 0x68)) {
    Serial.println("MPU6050 no detectado");
    //while (1){
    //  delay(10);
    //}
  }

  delay(100);   

  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu.setGyroRange(MPU6050_RANGE_2000_DEG);

  Serial.println("Iniciando...");
  delay(100);
}

void loop(){

  delay(7); // sampling rate 100hz aprox

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  printSerialData(a, g, temp);

  //Comprobación de conexión Bluetooth
  if (SerialBt.connected()){
    digitalWrite(LED, HIGH);
  }else{
    digitalWrite(LED, LOW);
  }
}

void printSerialData(sensors_event_t a, sensors_event_t g, sensors_event_t temp){
  Serial.print(g.gyro.x);
  Serial.print(", ");
  Serial.print(g.gyro.y);
  Serial.print(", ");
  Serial.print(g.gyro.z);
  Serial.print(", ");
  Serial.print(a.acceleration.x);
  Serial.print(", ");
  Serial.print(a.acceleration.y);
  Serial.print(", ");
  Serial.println(a.acceleration.z);
}

void printSerialBtData(sensors_event_t a, sensors_event_t g, sensors_event_t temp){
  SerialBt.print(g.gyro.x);
  SerialBt.print(", ");
  SerialBt.print(g.gyro.y);
  SerialBt.print(", ");
  SerialBt.print(g.gyro.z);
  SerialBt.print(", ");
  SerialBt.print(a.acceleration.x);
  SerialBt.print(", ");
  SerialBt.print(a.acceleration.y);
  SerialBt.print(", ");
  SerialBt.println(a.acceleration.z);
}