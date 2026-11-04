# UCSF ChimeraX — Rediseño Visual

Modificación de interfaz (Qt/QSS) e iconografía vectorial para **UCSF ChimeraX** (basado en `RBVI/ChimeraX`).

## Especificaciones

* **UI / QSS:** Viewport 3D y `Side View` en `#F5F5F7`, iluminación difusa (`lighting soft`) y contornos en `#3A3A3C` (`1.2px`). Paneles y tarjetas en `#FFFFFF` con cabeceras en `#F0F3F9`, bordes suaves en `#D5DFEE` (`1px`), radio de `12px` (`16px` en barra de herramientas), separadores verticales en azul pastel (`#BACBE6`) y esquinas redondeadas nativas DWM en Windows 11.
* **Controles de Ventana (`QPainter`):** Botones circulares vectoriales con antialiasing integrados en la ventana principal y paneles acoplables (`Log`, `Models`, `Side View`, `Sequence Viewer`): Cerrar (`#FF5F56`), Minimizar (`#FFBD2E`), Maximizar/Flotar (`#27C93F`).
* **Modo Claro Integral y Persistencia (`.cxs`):** Visor HTML (`Log`), `Sequence Viewer`, `Side View` y diálogos secundarios sincronizados en tema claro, con interceptores en `end restore session`, `session open` y `open models` y recarga en vivo (`QFileSystemWatcher`).
* **Iconografía:** +200 iconos únicos (`128x128` PNG y `.svg` vectoriales) diferenciados por función, con caché `O(1)` en memoria y mapeados a la estructura nativa de paquetes.

### Paleta Semántica
* `#8EC5FC` — Cadenas principales, nitrógeno.
* `#FF9AA2` — Oxígeno, cargas negativas, alertas.
* `#B5EAD7` — Cadenas complementarias, mínimos energéticos, timina.
* `#FFF3B0` — Azufre, purinas (A/G), factor B.
* `#FFDAC1` — Tocones de nucleótidos, torsión de enlaces.
* `#E2D1F9` — Superficies moleculares, neuroanatomía.
* `#A0E7E5` — Puentes de hidrógeno, hidrofobicidad.

## Instalación

```bash
python install.py
```

Dentro de la línea de comandos de ChimeraX puedes recargar o desactivar el tema en vivo:
* `liquidglass` — Recarga el tema desde el disco.
* `liquidglass off` — Restaura el aspecto por defecto.

## Estructura

```text
Chimera-X-/
├── install.py                          # Instalador automático de 1 clic
├── theme/liquid_glass_theme.py         # Controlador QSS, DWM e interceptores de sesión
├── hooks/mac_sequoia_theme.pth         # Inyección automática en el arranque
├── icons/                              # Activos PNG (128x128)
├── packages/                           # Árbol de iconos espejado de ChimeraX
├── svg/                                # Fuentes vectoriales (.svg)
└── scripts/
    ├── deduplicate_and_redesign.py     # Rediseño vectorial diferenciado por función
    ├── generate_all_vector_icons.py    # Compilador PNG (Pillow)
    └── generate_svgs.py                # Generador de trazados SVG
```

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Las marcas y nomenclaturas de UCSF ChimeraX pertenecen a sus respectivos titulares y a la Universidad de California, San Francisco (UCSF).
