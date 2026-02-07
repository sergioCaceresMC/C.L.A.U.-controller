#include <Wire.h>
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include <BluetoothSerial.h>


//#define I2C_SDA 21       // Pin de transmisión de información
//#define I2C_SCL 22       // Pin de sincronización con el reloj
//#define BTN1 34          // Pin para dedo índice
//#define BTN2 5           // Pin para dedo corazón
#define INTERRUPT_PIN 2    // pin de interrupción
#define LED 16             // LED de actividad
#define NAME "Clau-ceeibis-v1"

MPU6050 mpu;
BluetoothSerial SerialBt;

volatile bool mpuInterrupt = false;
void dmpDataReady() { mpuInterrupt = true; }

bool dmpReady = false;
uint8_t fifoBuffer[64];
uint16_t packetSize;

Quaternion q;
float q_offset_w = 1, q_offset_x = 0, q_offset_y = 0, q_offset_z = 0;
bool calibrated = false;

//Variables para la impresión
int16_t ax, ay, az;
int16_t gx, gy, gz;
float qw, qx, qy, qz;

//======================== SetUP ======================

void setup() {
  Serial.begin(115200);
  SerialBt.begin(NAME);
  pinMode(LED, OUTPUT);

  Wire.begin();
  Wire.setClock(400000);

  Serial.println("Iniciando MPU6050...");
  mpu.initialize();
  pinMode(INTERRUPT_PIN, INPUT);

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 no detectado");
    //while (1) delay(100);
  }
  Serial.println("MPU6050 detectado");

  // DMP
  uint8_t devStatus = mpu.dmpInitialize();
  mpu.setXGyroOffset(220);
  mpu.setYGyroOffset(76);
  mpu.setZGyroOffset(-85);
  mpu.setZAccelOffset(1788);

  // ------------------ Calibración
  if (devStatus == 0) {
    mpu.CalibrateAccel(6);
    mpu.CalibrateGyro(6);
    mpu.PrintActiveOffsets();

    mpu.setDMPEnabled(true);
    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
    packetSize = mpu.dmpGetFIFOPacketSize();
    dmpReady = true;
    Serial.println("DMP listo");
    Serial.println("Iniciando...");
  } else {
    Serial.print("DMP Initialization failed (code ");
    Serial.print(devStatus);
    Serial.println(")");
    while(1) delay(100);
  }
}

void loop() {

  delay(8); // sampling rate 100hz aprox

  // Calibración por Serial
  if (SerialBt.available()) {
    if (SerialBt.read() == '1'){
      for(int i=0; i<5; i++){
        digitalWrite(LED, LOW);
        delay(50);
        digitalWrite(LED, HIGH);
        delay(50);
      }
      calibrateQuaternion(); //Calibración por puerto serial
    }

  }

  if (!dmpReady) return;

  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
    mpu.dmpGetQuaternion(&q, fifoBuffer);

    // Obtener cuaterniones
    qw = q.w; 
    qx = q.x; 
    qy = q.y; 
    qz = q.z;
    applyCalibration(qw, qx, qy, qz); // Se aplica la calibración

    // Obtener gyro
    mpu.getRotation(&gx, &gy, &gz);

    // Obtener acelerómetro
    mpu.getAcceleration(&ax, &ay, &az);

    // Imprimir por serial
    printSerialData();

    // Imprimir por Bluteooth
    if (SerialBt.connected()) {
      printSerialBtData();
    }

    // Comprobación de conexión Bluetooth
    digitalWrite(LED, SerialBt.connected() ? HIGH : LOW);
  }
}

// ======================= Calibraciones =============
// Calibrar cuaternión actual como 1,0,0,0
void calibrateQuaternion() {
  q_offset_w = q.w;
  q_offset_x = q.x;
  q_offset_y = q.y;
  q_offset_z = q.z;
  calibrated = true;
  Serial.println("Calibrado → cuaternión será 1,0,0,0");
}

// Aplica la calibración
void applyCalibration(float &w, float &x, float &y, float &z) {
  if (!calibrated) return;

  // Conjugado del offset
  float ow = q_offset_w;
  float ox = -q_offset_x;
  float oy = -q_offset_y;
  float oz = -q_offset_z;

  float rw = ow*w - ox*x - oy*y - oz*z;
  float rx = ow*x + ox*w + oy*z - oz*y;
  float ry = ow*y - ox*z + oy*w + oz*x;
  float rz = ow*z + ox*y - oy*x + oz*w;

  w = rw; x = rx; y = ry; z = rz;
}

// ======================= Envio de datos =============
void printSerialData(){ 
  Serial.print(gx, 4); Serial.print(",");
  Serial.print(gy, 4); Serial.print(",");
  Serial.print(gz, 4); Serial.print(",");

  Serial.print(ax, 4); Serial.print(",");
  Serial.print(ay, 4); Serial.print(",");
  Serial.print(az, 4); Serial.print(",");

  Serial.print(qx, 6); Serial.print(", ");
  Serial.print(qy, 6); Serial.print(", ");
  Serial.print(qz, 6); Serial.print(", ");
  Serial.println(qw, 6);
}

void printSerialBtData(){ 
  SerialBt.print(gx, 4); SerialBt.print(",");
  SerialBt.print(gy, 4); SerialBt.print(",");
  SerialBt.print(gz, 4); SerialBt.print(",");

  SerialBt.print(ax, 4); SerialBt.print(",");
  SerialBt.print(ay, 4); SerialBt.print(",");
  SerialBt.print(az, 4); SerialBt.print(",");

  SerialBt.print(qx, 6); SerialBt.print(", ");
  SerialBt.print(qy, 6); SerialBt.print(", ");
  SerialBt.print(qz, 6); SerialBt.print(", ");
  SerialBt.println(qw, 6);
}
