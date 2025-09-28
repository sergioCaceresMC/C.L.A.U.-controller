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
          label: "Guias",
          items: [
            // Each item here is one entry in the navigation menu.
            {
              label: "Ejemplo de implementación",
              slug: "guias/ejemplo-de-implementacion",
            },
          ],
        },
        {
          label: "Modelo físico",
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
