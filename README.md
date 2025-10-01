# C.L.A.U. controller

Este es un proyecto de uso libre que busca crear un sistema de captura de movimiento sencillo y económico múltiple aplicación.

El controlador C.L.A.U. ha sido diseñado para ofrecer un uso sencillo y práctico, y se compone de dos sistemas independientes.

- El primero es el dispositivo C.L.A.U., encargado de registrar y enviar los datos de orientación, aceleración y giro, utilizando un sensor MPU6050 o BNO055.

- El segundo es el dispositivo L.I.Ra., que determina la posición del controlador C.L.A.U. en un plano mediante un sensor infrarrojo. Pero es capaz de modificarse para detectar otras fuentes de luz infrarroja.

## Instalación

Puedes descargar todo el proyecto con su documentación oficial usando git:

```bash
git clone https://github.com/sergioCaceresMC/C.L.A.U.-controller.git
```

## Acceso a documentación

La documentación está creada sobre _starlight_ de astro. y contiene la explicación completa acerca de cómo puedes replicar, conectar e implementar el controlador C.L.A.U. en tus proyectos.

Para abrir la documentación necesitas:

1. Tener instalado Node.js.
2. Dirigirte a la carpeta _Documentation_ dentro del proyecto.
3. Ejecutar el comando `npm run dev` o `npm run build` para generar el sitio de producción.

## Consideraciones de uso

Este proyecto está en desarrollo. Puedes modificarlo a tu gusto y utilizarlo en proyectos siempre que cumplas la licencia anexa.
