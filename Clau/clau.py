#==========================================================
# Librería que se encarga de la lógica para
# convertir las magnitudes del sensor a un vector procesado 
#==========================================================
import serial
import numpy as np
from ahrs.filters import Madgwick

class Clau:
    
    def __init__(self, 
                 port = "COM3", 
                 xyz = [0,0,0], 
                 wijk = np.array([1.0, 0.0, 0.0, 0.0]), 
                 clk = 100):
        self.position_xyz = xyz
        self.quaternion_wijk = wijk
        self.clk = clk
        self.port = port

        self.madgwick = Madgwick()
        self.ser = serial.Serial(self.port, self.clk, timeout=1)

    # Resetear el valor del controlador a 0
    def calibrate(self, 
                  xyz = [0,0,0], 
                  wijk = np.array([1.0, 0.0, 0.0, 0.0])):
        self.position_xyz = xyz
        self.angle_ijk = wijk
        return [{"position": self.position_xyz}, {"angle": self.angle_ijk}]

    # Obtener información del puerto
    def collect_data(self):
        while True:
            try:
                line = self.ser.readline().decode("utf-8").strip()

                # Espera datos en formato: ax,ay,az,gx,gy,gz,io1,io2
                values = line.split(",")
                if len(values) != 8:
                    continue
                
                dataPos = self.update_data(values[0],values[1],values[2],
                                values[3],values[4],values[5])
                dataIn = [{"input1": values[6]}, {"input2": values[7]}]
                
                return np.concatenate((dataPos, dataIn))
            except:
                raise Exception("Error en la toma de datos")
        

    # Actualizar información
    def update_data(self, ax, ay, az, gx, gy, gz):
        acc = np.array([ax, ay, az])
        gyr = np.array([gx, gy, gz])
        self.quaternion_wijk = self.madgwick.updateIMU(
            q=self.quaternion_wijk, gyr=gyr, acc=acc)
        
        return [
            {"position": self.position_xyz},
            {"quaternion": self.quaternion_wijk}
        ]

    def update_clk(self, clk):
        self.clk = clk
        return self.clk
    
    def update_port(self, port):
        self.port = port
        return self.port

    # Retorna la posición 3d con respecto a la posición inicial
    def get_postition():
        pass

    def get_quaternion(self):
        return self.quaternion_wijk

    def get_euler_angles():
        pass

    def get_data(self):
        return [
            {"port": self.port},
            {"clock": self.clk},
            {"postition": self.position_xyz},
            {"quaternion": self.quaternion_wijk}
        ]