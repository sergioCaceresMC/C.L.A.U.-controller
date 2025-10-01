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
          label: "Microcontrolador",
          items: [
            // Each item here is one entry in the navigation menu.
            {
              label: "Cálculo de ángulos",
              slug: "modelo-fisico/calculo-de-angulos",
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
