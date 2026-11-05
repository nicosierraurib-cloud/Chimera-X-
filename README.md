# UCSF ChimeraX — Rediseño Visual

Modificación de interfaz (Qt/QSS), motor de temas dual (**Gris** y **Oscuro**), pantalla de carga animada e iconografía vectorial para **UCSF ChimeraX** (basado en `RBVI/ChimeraX`).

## Especificaciones

* **Motor Dual (`Gris` / `Oscuro`) con Persistencia:** Selector rápido en la barra superior (`Gris` en `#D5DBE5` / `#E4E8F0` y `Oscuro` en `#1C1C1E` / `#2C2C2E`) con guardado automático de preferencia entre sesiones (`theme_mode.txt`).
* **Visor 3D y `Side View` Redondeados (`MacRoundedFrameOverlay`):** Viewport OpenGL principal enmarcado con radio de `16px` (`10px` en `Side View`), iluminación difusa (`lighting soft`), siluetas adaptativas (`1.2px`) y fondo de `Side View` dinámico (`#FFFFFF` en modo `Gris` y `#16171B` en modo `Oscuro`).
* **Pantalla de Carga Funcional (`MacLoadingOverlay`):** Superposición 100% opaca con cortina interna (`MacInternalCurtain`), emblema vectorial animado en tiempo real, detección automática de versión (`v1.12`), mensajes de progreso por etapa, *cooldown* al aparecer/desaparecer y estabilización real de fotogramas a `30` o `60 FPS` según la tasa de refresco del monitor.
* **Controles de Ventana (`QPainter`):** Botones circulares vectoriales con antialiasing en la ventana principal y paneles acoplables (`Log`, `Models`, `Side View`, `Sequence Viewer`, `Volume Viewer`): Cerrar (`#FF5F56`), Minimizar (`#FFBD2E`), Maximizar/Flotar (`#27C93F`).
* **Paneles Científicos e Histogramas:** Sincronización cromática en `Log` (HTML/CSS), `Sequence Viewer`, `Side View` e histogramas de densidad de `Volume Viewer`, con interceptores en `end restore session`, `session open`, `open models` y `add models`.
* **Iconografía:** +200 iconos únicos (`128x128` PNG y `.svg` vectoriales) diferenciados por función, con caché `@lru_cache` `O(1)` en memoria y mapeados a la estructura nativa de paquetes.

### Paleta Semántica
* `#8EC5FC` — Cadenas principales, nitrógeno.
* `#FF9AA2` — Oxígeno, cargas negativas, alertas.
* `#B5EAD7` — Cadenas complementarias, mínimos energéticos, timina.
* `#FFF3B0` — Azufre, purinas (A/G), factor B.
* `#FFDAC1` — Tocones de nucleótidos, torsión de enlaces.
* `#E2D1F9` — Superficies moleculares, neuroanatomía.
* `#A0E7E5` — Puentes de hidrógeno, hidrofobicidad.

## Instalación

En Windows (doble clic):
```bat
install_windows.bat
```

O mediante Python en cualquier plataforma:
```bash
python install.py
```

Comandos disponibles dentro de ChimeraX:
* `liquidglass gray` — Activa el tema **Gris**.
* `liquidglass dark` — Activa el tema **Oscuro**.
* `liquidglass` — Recarga el tema activo desde el disco.
* `liquidglass off` — Restaura el aspecto por defecto.

## Estructura

```text
Chimera-X-/
├── install.py                          # Instalador multiplataforma
├── install_windows.bat                 # Instalador de 1 clic para Windows
├── theme/liquid_glass_theme.py         # Controlador QSS, OpenGL, pantalla de carga y temas
├── hooks/mac_sequoia_theme.pth         # Inyección automática en el arranque
├── icons/                              # Activos PNG (128x128)
├── packages/                           # Árbol de módulos espejado de ChimeraX
├── svg/                                # Fuentes vectoriales (.svg)
└── scripts/
    ├── generate_all_vector_icons.py    # Compilador PNG (Pillow)
    ├── generate_svgs.py                # Generador de trazados SVG
    └── refine_weak_icons.py            # Refinamiento de iconos específicos
```

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Las marcas y nomenclaturas de UCSF ChimeraX pertenecen a sus respectivos titulares y a la Universidad de California, San Francisco (UCSF).
