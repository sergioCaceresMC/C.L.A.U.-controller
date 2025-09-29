#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
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
TwoWire I2CBNO = TwoWire(0);
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x29, &I2CBNO);

void setup(){
  Serial.begin(115200);
  SerialBt.begin(NAME);
  Serial.println("Iniciado");
  
  I2CBNO.begin(I2C_SDA, I2C_SCL);

  pinMode(LED, OUTPUT);
  
  if (!bno.begin()){
    Serial.println("BNO055 no detectado");
    while (1){
      delay(10);
    }
  }
  delay(100);   

  uint8_t system = 0, gyro = 0, accel = 0, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  Serial.print("Estado de calibración -> ");
  Serial.print("Sys: "); Serial.print(system);
  Serial.print(" Gyro: "); Serial.print(gyro);
  Serial.print(" Accel: "); Serial.print(accel);
  Serial.print(" Mag: "); Serial.println(mag);
  /*
  while(SerialBt.available() == 0){
    char message = SerialBt.read();
    if(message == '1'){
      for(int i=0; i<5; i++){
        digitalWrite(LED, LOW);
        delay(50);
        digitalWrite(LED, HIGH);
        delay(50);
      }
      break;
    }
  }*/

  Serial.println("Iniciando...");
  delay(100);
}

void loop(){

  delay(8); // sampling rate 100hz aprox

  imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER); 
  imu::Vector<3> gyr = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);  
  imu::Quaternion quat = bno.getQuat();

  printSerialData(acc, gyr, quat); //Para pruebas con conexión directa
  printSerialBtData(acc, gyr, quat); //Para pruebas en bluetooth

  //Comprobación de conexión Bluetooth
  if (SerialBt.connected()){
    digitalWrite(LED, HIGH);
  }else{
    digitalWrite(LED, LOW);
  }
}

void printSerialData(imu::Vector<3> acc, imu::Vector<3> gyr, imu::Quaternion q){
  Serial.print(gyr.x(), 4); Serial.print(", "); 
  Serial.print(gyr.y(), 4); Serial.print(", "); 
  Serial.print(gyr.z(), 4); Serial.print(", "); 

  Serial.print(acc.x(), 4); Serial.print(", "); 
  Serial.print(acc.y(), 4); Serial.print(", "); 
  Serial.print(acc.z(), 4); Serial.print(", ");

  Serial.print(q.x(), 6); Serial.print(", ");
  Serial.print(q.y(), 6); Serial.print(", ");
  Serial.print(q.z(), 6); Serial.print(", ");
  Serial.println(q.w(), 6);
}

void printSerialBtData(imu::Vector<3> acc, imu::Vector<3> gyr, imu::Quaternion q){
  SerialBt.print(gyr.x(), 4); SerialBt.print(", "); 
  SerialBt.print(gyr.y(), 4); SerialBt.print(", "); 
  SerialBt.print(gyr.z(), 4); SerialBt.print(", "); 
  
  SerialBt.print(acc.x(), 4); SerialBt.print(", "); 
  SerialBt.print(acc.y(), 4); SerialBt.print(", "); 
  SerialBt.print(acc.z(), 4); SerialBt.print(", ");
  
  SerialBt.print(q.x(), 6); SerialBt.print(", ");
  SerialBt.print(q.y(), 6); SerialBt.print(", ");
  SerialBt.print(q.z(), 6); SerialBt.print(", ");
  SerialBt.println(q.w(), 6);
}
