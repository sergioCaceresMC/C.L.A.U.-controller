#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <BluetoothSerial.h>

//================ Pines y variables ====================

#define I2C_SDA 21      // Pin de transmisión de información 
#define I2C_SCL 22      // Pin de sincronización con el reloj  
#define BTN1 34         // Pin para dedo índice
#define BTN2 5          // Pin para dedo corazón
#define LED 2           // Led de comprobación de conexión bluetooth
#define NAME "Clau-v2"  // Nombre de dispositivo

imu::Quaternion q_ref(0, 0, 0, 1);  // identidad
bool calibrated = false;
int btn1 = 0;
int btn2 = 0;

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

  pinMode(BTN1, INPUT);
  pinMode(BTN2, INPUT); 

  if (!bno.begin()){
    Serial.println("BNO055 no detectado");
    /*while (1){
      delay(10);
    }*/
  }
  delay(100);   

  uint8_t system = 0, gyro = 0, accel = 0, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  Serial.print("Estado de calibración -> ");
  Serial.print("Sys: "); Serial.print(system);
  Serial.print(" Gyro: "); Serial.print(gyro);
  Serial.print(" Accel: "); Serial.print(accel);
  Serial.print(" Mag: "); Serial.println(mag);
  
  Serial.println("Iniciando...");
  delay(100);
}

void loop(){

  delay(8); // sampling rate 100hz aprox

  if(SerialBt.available() != 0){
    char message = SerialBt.read();
    Serial.println(message);
    if(message == '1'){
      calibrated = false;
      for(int i=0; i<5; i++){
        digitalWrite(LED, LOW);
        delay(50);
        digitalWrite(LED, HIGH);
        delay(50);
      }
    }
  }

  imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER); 
  imu::Vector<3> gyr = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);  
  imu::Quaternion quat = bno.getQuat();

  // Inicializamos con la primera lectura
  if (!calibrated) {
    recalibrate(quat);
  }

  // Calcular cuaternión corregido
  imu::Quaternion q_corr = quatMultiply(quatConjugate(q_ref), quat);

  //printSerialData(acc, gyr, q_corr); //Para pruebas con conexión directa
  printSerialBtData(acc, gyr, q_corr); //Para pruebas en bluetooth

  //Comprobación de conexión Bluetooth
  digitalWrite(LED, SerialBt.connected() ? HIGH : LOW);
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
  Serial.print(q.w(), 6); Serial.print(", ");

  btn1 = digitalRead(BTN1);
  btn2 = digitalRead(BTN2);
  Serial.print(btn1); Serial.print(", ");
  Serial.println(btn2);
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
  SerialBt.print(q.w(), 6); SerialBt.print(", ");

  btn1 = digitalRead(BTN1);
  btn2 = digitalRead(BTN2);
  SerialBt.print(btn1); SerialBt.print(", ");
  SerialBt.println(btn2);

}

void recalibrate(imu::Quaternion q_now) {
  // Guardar referencia
  q_ref = q_now;

  // Normalizar por seguridad
  float norm = sqrt(q_ref.w()*q_ref.w() + q_ref.x()*q_ref.x() + q_ref.y()*q_ref.y() + q_ref.z()*q_ref.z());
  q_ref = imu::Quaternion(q_ref.w()/norm, q_ref.x()/norm, q_ref.y()/norm, q_ref.z()/norm);
  calibrated = true;
}

imu::Quaternion quatMultiply(const imu::Quaternion& q1, const imu::Quaternion& q2) {
  return imu::Quaternion(
    q1.w()*q2.w() - q1.x()*q2.x() - q1.y()*q2.y() - q1.z()*q2.z(),
    q1.w()*q2.x() + q1.x()*q2.w() + q1.y()*q2.z() - q1.z()*q2.y(),
    q1.w()*q2.y() - q1.x()*q2.z() + q1.y()*q2.w() + q1.z()*q2.x(),
    q1.w()*q2.z() + q1.x()*q2.y() - q1.y()*q2.x() + q1.z()*q2.w()
  );
}

imu::Quaternion quatConjugate(const imu::Quaternion& q) {
  return imu::Quaternion(q.w(), -q.x(), -q.y(), -q.z());
}
