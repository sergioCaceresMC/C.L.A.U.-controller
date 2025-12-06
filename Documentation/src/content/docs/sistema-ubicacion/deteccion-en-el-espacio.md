---
title: Detección en el espacio
description: Procedimiento para configurar la detección del controlador en el espacio.
---

El controlador C.L.A.U. no posee de forma interna el sistema para detectar la posición en el espacio. En su lugar es necesario usar sensores externos.
Dentro de esta librería se ofrecen 2 alternativas:

- **Sistema LIRa**: Se usa el controlador L.I.Ra. para detectar la posición del controlador C.L.A.U. usando puntos de emisión infrarroja. El sistema LIRa realiza un seguimiento de hasta cuatro puntos de forma automática y con un bajo costo computacional.

- **Uso de una cámara externa**: Se usa una _webcam_ o equivalente y usando la librería de OpenCV se realiza un seguimiento de las manos de la persona. Este método trae problemas asociados al coste computacional, por lo que no se sugiere para equipos de bajos requisitos.
