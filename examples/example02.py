from ClauLib.clau import Clau

if __name__ == "__main__":

    # Definición de objetos controlador
    clau_left = Clau(port="COM5", n_data=10)
    clau_right = Clau(port="COM5", n_data=10)

    send = ""
    nData = 1000
    file1 = open("myfile.txt","w")

    while send != "1":
        send = input("Ingrese 1 para calibrar los objetos: ")
    
    print(send)

    #Calibramos los ocontroladores para determinar la orientación 0
    clau_left.calibrate()
    clau_right.calibrate()

    #Captura de datos y procesamiento
    print("Iniciando captura de datos")
    for i in range(nData):
        data_left = clau_left.collect_data()
        data_right = clau_right.collect_data()
        line = (
            str(i) + 
            ", right: " + str(data_right) + 
            ", left: " + str(data_left) + "\n"
        )
        file1.write(line)

    print("Datos guardados correctamente")
    file1.close()
    