---
title: Recolección de datos
description: Cómo recolectar datos en el sensor.
---

Podemos definir una función propia para recolectar los datos del controlador usando la libreria _serial_ de python. Pero dentro del objeto Clau tenemos la función _collect_data_ que no tiene parámetros.

La función utiliza el valor de _n_data_ para saber cuantos datos se ingresan en cada linea del controlador. En caso de una lectura incompleta de datos, la función retorna `None`.

Esta función se ejecuta una sola vez, así que en caso de querer los datos del sensor para un análisis en tiempo real es necesario usar la función dentro de un bucle.

```py
from ClauLib.clau import Clau

clau_obj = Clau(port="COM3", clk=115200, n_data=10)
clau_obj.calibrate()

# Obtención de un solo dato
data = clau_obj.collect_data()
print(data)

# Obtención de datos de forma consecutiva
while True:
    data = clau_obj.collect_data()

    # Comprobación de que existen datos leídos
    if not data:
        continue
    print(data)
```

## Detección de inputs

La razón por la que en configuración podemos definir el número de datos por línea del puerto serie, es porque el controlador C.L.A.U. puede medir por defecto los valores de 2 botones capacitivos ubicados en los dedos índice y corazón, además de la agitación del control.
Estas entradas pueden modificarse a conveniencia del desarrollador. Pero la librería proporcionada ya trae herramientas para la detección y análisis de las entradas.

### Botones dactilares

En los botones podemos contar con cuatro estados posibles:

- Estado 0: Ningún boton presionado.
- Estado 1: Botón 1 presionado.
- Estado 2: Botón 2 presionado.
- Estado 3: Ambos botones presionados.

Estas señales se pueden obtener dentro del diccionario que retorna la función `get_data()` junto con el resto de atributos del objeto. Pero también viene incluido en el resultado de `collect_data()` y `update_data()` aunque este último es una función que tiene proposito lógico interno y no está orientada al uso del desarrollador.

La llave del diccionario para obtener el valor es _input_:

```py
from ClauLib.clau import Clau

clau_obj = Clau(port="COM3", clk=115200, n_data=10)
clau_obj.calibrate()

# Obtención de datos de forma consecutiva
while True:
    data = clau_obj.collect_data()

    # Comprobación de que existen datos leídos
    if not data:
        continue
    print(data["input"])
```

### Agitaciones y su magnitud

En ocaciones podemos querer detectar una agitación en el controlador, para ello podemos usar la función _get_shake_ que viene incluida en la librería del controlador.

Este resultado se obtiene calculando la magnitud del vector aceleración y comparandolo con un umbral que se puede establecer con _set_shake_umbral_.

Un ejemplo de respuesta es el siguiente:

```py
{
    "shakeStatus": True
    "shakeMagnitude": 20.123
}
```

Un ejemplo de lectura de datos es el siguiente:

```py
from ClauLib.clau import Clau

clau_obj = Clau(port="COM3", clk=115200, n_data=10)

# Establecimiento del umbral en 22m/s^2
clau_obj.set_shake_umbral(22)

if clau_obj.calibrate()

while True:
    data = clau_obj.collect_data()
    if not data:
        continue

    # Obtención de los datos referentes a la agitación
    shake = clau_obj.get_shake()
    if shake["shakeStatus"]: print(shake["shakeMagnitude"])
```
