---
title: Configuración
description: Configuraciones clave para el uso de C.L.A.U.
---

El objeto Clau contiene los siguientes parámetros para su inicialización:

- _port_: Puerto serial en que el controlador está conectado.
- _clk_: Velocidad del reloj usada para la comunicación serial.
- _n_data_: Número de datos esperados al momento de recopilar las mediciones del sensor.

Es necesario que el usuario verifique el puerto del dispositivo, aunque este objeto tiene un valor por defecto.

Es posible cambiar los valores de cada variable usando los siguientes comandos:

```py
from ClauLib.clau import Clau
clau_obj = Clau(port="COM3", clk=115200, n_data=10)

# Cambiar el valor del puerto
clau_obj.set_port("COM5")

# Cambiar el valor del reloj
clau_obj.set_clk(9600)

# Cambiar el número de datos esperados
clau_obj.set_n_data(12)
```

## Calibración

El objeto Clau trae una función para reiniciar la calibración del controlador. Esta función envia un código determinado al controlador para indicarle que se realiza una nueva calibración, además de indicar el nuevo valor de los cuaterniones a 1,0,0,0.
Esta calibración devuelve el valor guardado.

Es necesario realizar la calibración al momento de conectar o empezar a usar el controlador para evitar lecturas falsas en las funciones de shake.

```py
...

# Calibración a 0
clau_obj.calibrate()
```
