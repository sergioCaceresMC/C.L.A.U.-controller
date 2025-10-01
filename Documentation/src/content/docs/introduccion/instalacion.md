---
title: Instalación
description: Una guía para instalar, conectar y controlar un cubo por medio de python.
---

Lo primero será agregar las dependencias para el uso del proyecto. Para ello puedes usar pip install e instalar los requerimientos que trae el modulo ClauLib

```console
pip install .\ClauLib\requirements.txt
```

## Ejemplo de visualización

Dentro de esta librería encontraras el modulo _simple_clau_gui_ que contiene un visualizador sencillo de la rotación del controlador. Además de que te permite establecer en qué puerto, la velocidad del reloj serial, el número de datos que obtienes por línea y si deseas o no que te muestre los logs.

```py
from ClauLib.simple_clau_gui import cube_view

if __name__ == "__main__":
    cube_view(port="COM5", logs=False)
```
