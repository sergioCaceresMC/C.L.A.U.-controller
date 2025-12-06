// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// https://astro.build/config
export default defineConfig({
  integrations: [
    starlight({
      title: "C.L.A.U. - v1",
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/withastro/starlight",
        },
      ],
      sidebar: [
        {
          label: "Introducción",
          items: [
            // Each item here is one entry in the navigation menu.
            {
              label: "Instalación",
              slug: "introduccion/instalacion",
            },
            {
              label: "Primeros pasos",
              slug: "introduccion/primeros-pasos",
            },
            {
              label: "Configuración",
              slug: "introduccion/configuracion",
            },
            {
              label: "Recolección de datos",
              slug: "introduccion/recoleccion_datos",
            },
            {
              label: "Novedades",
              slug: "introduccion/novedades",
            },
            {
              label: "Referencias",
              slug: "introduccion/referencias",
            },
          ],
        },
        {
          label: "Sistema de ubicación",
          items: [
            // Each item here is one entry in the navigation menu.
            {
              label: "Detección en el espacio",
              slug: "sistema-ubicacion/deteccion-en-el-espacio",
            },
          ],
        },
        {
          label: "Microcontrolador",
          items: [
            // Each item here is one entry in the navigation menu.
            {
              label: "Circuito",
              slug: "microcontrolador/circuito",
            },
            {
              label: "Cálculo de ángulos",
              slug: "microcontrolador/bno055",
            },
            {
              label: "Cálculo de ángulos",
              slug: "microcontrolador/mpu6050",
            },
          ],
        },
        {
          label: "Reference",
          autogenerate: { directory: "reference" },
        },
      ],
    }),
  ],
});
