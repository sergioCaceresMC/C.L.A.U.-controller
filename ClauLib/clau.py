#==========================================================
# Librería que se encarga de la lógica para
# convertir las magnitudes del sensor a un vector procesado 
# Esta es la versión 1 que usa el BNO055
#==========================================================
import serial, time, json
import numpy as np
import paho.mqtt.client as mqtt

class Clau:
    
    def __init__(self, port = "COM3", clk = 115200, n_data = 10, name = "Clau"):
        if n_data < 10: 
            raise Exception("n_data es inferior a 10")
        self.name = name
        self.mqttStatus = False
        self.acc = np.array([0,0,0])
        self.gyr = np.array([0,0,0])
        self.quaternion_wijk = np.array([1.0, 0.0, 0.0, 0.0])
        self.clk = clk
        self.port = port
        self.n_data = n_data
        self.umbral = 10
        self.ser = serial.Serial(self.port, self.clk)

    # Resetear el valor del controlador a 0
    def calibrate(self):

        self.ser.write(b'1')
        #self.ser.write(f"1,".join(f"{x}," for x in self.angle_wijk))
        print("send...")
        for l in range(10):
            try:
                values = self.ser.readline().decode("utf-8").strip().split(",")
                if len(values) < self.n_data:
                    time.sleep(1)
                    continue
                return {
                    "angle": self.angle_wijk, 
                    "status": 200
                }
            except:
                pass
        return {"status": 500}

    # Obtener información del puerto
    def collect_data(self):
        try:
            # Espera datos en formato: ax,ay,az,gx,gy,gz,qx,qy,qz,qw,io1,io2
            raw_values = self.ser.readline().decode("utf-8").strip().split(",")

            values = [float(numeric_string) for numeric_string in raw_values]

            if len(raw_values) < 10 or len(raw_values) < self.n_data:
                return None  # En caso de línea incompleta no retorna nada
            
            data = self.update_data(*values[:10])
            if self.mqttStatus:
                #Enviar mqtt
                self.publish(data)
            return data

        except Exception:
            return None  

    # Actualizar información
    def update_data(self, gx, gy, gz, ax, ay, az, qx, qy, qz, qw):
        acc = np.array([ax, ay, az])
        gyr = np.radians(np.array([gx, gy, gz]))  # convertir °/s a rad/s
        quat = np.array([qx, qy, qz, qw]) # cuaternion calculado en el microchip
        
        self.quaternion_wijk = quat
        self.acc = acc
        self.gyr = gyr

        return {
            "acceleration": self.acc,
            "gyroscope": self.gyr,
            "quaternion": self.quaternion_wijk  # [x, y, z, w]
        }

    # Funciones para la comunicación mqtt con qos=0
    def init_mqtt(self, 
                   host = "localhost", 
                   port = 1883, 
                   topic = "CLAU", 
                   client_id = "clau_client",
                   keepalive = 20,
                   username = "admin",
                   password = "public"):
        if self.mqttStatus:
            self.stop_mqtt()
        try:
            self.client = mqtt.Client(client_id=client_id,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            clean_session=False)
            self.client.username_pw_set(username, password)
            self.client.connect(host, port, keepalive)
            
            #self.client.connect_async(host, port, keepalive)
            #self.client.loop_start()

            array_topic = topic.split("/")
            array_topic = [s for s in array_topic if s != ""]
            clean_topic  = "/"+"/".join(array_topic)
            self.topic = clean_topic+f"/{self.name}"
            self.mqttStatus = True
            return self.topic
        except:
            raise Exception("Fallo al conectarse")
    
    def disconect_mqtt(self):
        if self.mqttStatus:
            self.client.disconnect()
            self.mqttStatus = False
            return True
        return False

    def publish(self, data = {"status": True}):
        if not self.mqttStatus: return
        #Convertir a json
        msg = json.dumps(data)
        #Enviar con qos 0 
        return self.client.publish(self.topic, msg, qos=0)

    # Seters
    def set_name(self, name):
        self.name = name

    def set_clk(self, clk):
        self.clk = clk
        self.ser.close()
        self.ser = serial.Serial(self.port, self.clk)
        return self.clk
    
    def set_port(self, port):
        self.port = port
        self.ser.close()
        self.ser = serial.Serial(self.port, self.clk)
        return self.port

    def set_n_data(self, n_data):
        if n_data < 10:
            raise Exception("n_data es inferior a 10")
        self.n_data = n_data
        return self.n_data

    def set_shake_umbral(self, umbral):
        if umbral < 0:
            raise Exception("n_data es inferior a 10")
        self.umbral = umbral
        return self.umbral

    # Getters
    # Retorna la posición 3d con respecto a la posición inicial
    def get_quaternion(self):
        return self.quaternion_wijk

    def get_data(self):
        return {
            "port": self.port,
            "clock": self.clk,
            "acceleration": self.acc,
            "gyroscope": self.gyr,
            "quaternion": self.quaternion_wijk
        }
    
    def get_shake(self):
        data = self.acc
        acceleration = np.linalg.norm(data)
        if abs(acceleration) > self.umbral:
            return {
                "shakeStatus": True,
                "shakeMagnitude": acceleration,
            }
        else:
            return {
                "shakeStatus": False
            }


