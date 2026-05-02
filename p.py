import serial
import time

# Windows: 'COM3', 'COM4', etc.
# Linux: '/dev/ttyUSB0' o '/dev/ttyACM0'
# macOS: '/dev/tty.usbserial-XXXX'
puerto = 'COM3'
baudrate = 9600

arduino = serial.Serial(puerto, baudrate, timeout=1)
time.sleep(2)  # Espera a que Arduino reinicie

def main():
    
    # Esperar la primer respuesta
    respuesta = arduino.readline().decode('utf-8').strip()
    print("<Respuesta recibida>", respuesta)

    while(True):
        # Enviar una frase
        frase = input("Ingresa una frase: ")
        arduino.write((frase + '\n').encode('utf-8'))

        if (frase == "salir"):
            break
        # Leer respuesta
        respuesta = arduino.readline().decode('utf-8').strip()
        print("Respuesta recibida:", respuesta)

    arduino.close()

if __name__ == "__main__":
    main()