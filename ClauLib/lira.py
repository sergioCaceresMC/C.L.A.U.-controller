#==========================================================
# Librería que se encarga de la lógica para
# leer y procesar las coordenadas proporcionadas por el sensor 
#==========================================================
import serial
import time
import numpy as np

class Lira:
    def __init__(self, port="COM3", clk=115200):
        self.port = port
        self.clk = clk
        self.ser = serial.Serial(self.port, self.clk)
    
    def collect_data(self):
        try:
            # Espera datos en formato: x1,y1,x2,y2,
            raw_values = self.ser.readline().decode("utf-8").strip().split(",")

            values = [float(numeric_string) for numeric_string in raw_values]

            if len(raw_values) < 2:
                return None
        
            return self.update_data(*values[:10])

        except Exception as e:
            print(e)
            return None  

    
