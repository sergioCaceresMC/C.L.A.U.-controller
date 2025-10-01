#==========================================================
# Librería que se encarga de la lógica para
# convertir las magnitudes del sensor a un vector procesado 
# Esta es la versión 1 que usa el BNO055
#==========================================================
import serial
import time
import numpy as np

class ClauBNO055:
    
    def __init__(self, port = "COM3", clk = 115200, n_data = 10):
        self.acc = np.array([0,0,0])
        self.gyr = np.array([0,0,0])
        self.quaternion_wijk = np.array([1.0, 0.0, 0.0, 0.0])
        self.clk = clk
        self.port = port
        self.n_data = n_data
        self.ser = serial.Serial(self.port, self.clk)

    # Resetear el valor del controlador a 0
    def calibrate(self, 
                  xyz = [0,0,0], 
                  wijk = np.array([1.0, 0.0, 0.0, 0.0])):
        self.position_xyz = xyz
        self.angle_ijk = wijk
        self.ser.write(b'1')
        print("send...")
        for i in range(10):
            try:
                values = self.ser.readline().decode("utf-8").strip().split(",")
                if len(values) == self.n_data:
                    time.sleep(1)
                    continue
                return {
                    "position": self.position_xyz, 
                    "angle": self.angle_ijk, 
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
                return None  # línea incompleta
            
            return self.update_data(*values[:10])

        except Exception as e:
            print(e)
            return None  

    # Actualizar información
    def update_data(self, ax, ay, az, gx, gy, gz, qx, qy, qz, qw):
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

    def set_clk(self, clk):
        self.clk = clk
        return self.clk
    
    def set_port(self, port):
        self.port = port
        return self.port

    def set_n_data(self, n_data):
        self.n_data = n_data
        return self.n_data

    # Retorna la posición 3d con respecto a la posición inicial
    def get_postition(self):
        raise Exception("No implementado")

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