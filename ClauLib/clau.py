#==========================================================
# Librería que se encarga de la lógica para
# convertir las magnitudes del sensor a un vector procesado 
#==========================================================
import serial
import time
import numpy as np
from ahrs.filters import Madgwick

class Clau:
    
    def __init__(self, 
                 port = "COM3", 
                 xyz = [0,0,0], 
                 wijk = np.array([1.0, 0.0, 0.0, 0.0]), 
                 clk = 115200,
                 n_data = 8):
        self.position_xyz = xyz
        self.quaternion_wijk = wijk
        self.clk = clk
        self.port = port
        self.n_data = n_data

        #para el cálculo de posición
        self.velocity = np.zeros(3)   # [vx, vy, vz]
        self.last_time = None
        self.gravity = np.array([0, 0, 9.51])  # m/s²

        self.madgwick = Madgwick()
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
            # Espera datos en formato: ax,ay,az,gx,gy,gz,io1,io2
            raw_values = self.ser.readline().decode("utf-8").strip().split(",")

            values = [float(numeric_string) for numeric_string in raw_values]

            if len(raw_values) != self.n_data:
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

        # Tiempo delta
        now = time.time()
        if(self.last_time):
            dt = now - self.last_time
        else:
            dt = 0.0001
        self.last_time = now

        self.quaternion_wijk = quat
        rot_matrix = np.array([
            [1 - 2*(qy**2 + qz**2),     2*(qx*qy - qz*qw),      2*(qx*qz + qy*qw)],
            [2*(qx*qy + qz*qw),         1 - 2*(qx**2 + qz**2),  2*(qy*qz - qx*qw)],
            [2*(qx*qz - qy*qw),         2*(qy*qz + qx*qw),      1 - 2*(qx**2 + qy**2)]
        ])

        acc_world = rot_matrix @ acc

        # Restar gravedad
        acc_world = acc_world - self.gravity

        # Integración simple (velocidad y posición)
        self.velocity += acc_world * dt
        self.position_xyz += self.velocity * dt

        return {
            "position": self.position_xyz,
            "quaternion": self.quaternion_wijk  # [x, y, z, w]
        }

    def update_clk(self, clk):
        self.clk = clk
        return self.clk
    
    def update_port(self, port):
        self.port = port
        return self.port

    # Retorna la posición 3d con respecto a la posición inicial
    def get_postition(self):
        return self.position_xyz

    def get_quaternion(self):
        return self.quaternion_wijk

    # def get_euler_angles():
    #     pass

    def get_data(self):
        return [
            {"port": self.port},
            {"clock": self.clk},
            {"postition": self.position_xyz},
            {"quaternion": self.quaternion_wijk}
        ]