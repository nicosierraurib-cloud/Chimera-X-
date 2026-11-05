# UCSF ChimeraX — Rediseño Visual

Modificación de interfaz (Qt/QSS) e iconografía vectorial para **UCSF ChimeraX** (basado en `RBVI/ChimeraX`).

## Especificaciones

* **UI / QSS:** Viewport en `#F5F5F7`, iluminación difusa (`lighting soft`) y contornos en `#3A3A3C` (`1.2px`). Paneles en `rgba(255, 255, 255, 0.96)`, bordes de `1px` (`rgba(0, 0, 0, 0.08)`), radio de `12px` y barra superior segmentada.
* **Controles de Ventana:** Integrados en ventana principal y paneles acoplables (`Log`, `Model Panel`, `Sequence Viewer`): Cerrar (`#FF5F56`), Minimizar (`#FFBD2E`), Maximizar (`#27C93F`).
* **Persistencia (`.cxs`):** Interceptores en `end restore session`, `session open` y `open models` para bloquear la reversión del fondo a negro.
* **Iconografía:** +200 iconos (`128x128` PNG) compilados desde SVG mediante Python, mapeados a la estructura nativa de paquetes.

### Paleta Semántica
* `#8EC5FC` — Cadenas principales, nitrógeno.
* `#FF9AA2` — Oxígeno, cargas negativas, alertas.
* `#B5EAD7` — Cadenas complementarias, mínimos energéticos, timina.
* `#FFF3B0` — Azufre, purinas (A/G), factor B.
* `#FFDAC1` — Tocones de nucleótidos, torsión de enlaces.
* `#E2D1F9` — Superficies moleculares, neuroanatomía.
* `#A0E7E5` — Puentes de hidrógeno, hidrofobicidad.

## Estructura

```text
Chimera-X-/
├── theme/liquid_glass_theme.py
├── hooks/mac_sequoia_theme.pth
├── icons/
├── packages/
├── svg/
└── scripts/
    ├── generate_all_vector_icons.py
    └── generate_svgs.py
```

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Las marcas y nomenclaturas de UCSF ChimeraX pertenecen a sus respectivos titulares y a la Universidad de California, San Francisco (UCSF).
