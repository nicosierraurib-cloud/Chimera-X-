# UCSF ChimeraX — Apple macOS Sequoia "Light Mode Pro" & Vector Pastel Redesign

Rediseño visual integral de **UCSF ChimeraX** inspirado en las directrices de diseño de **Apple macOS Sequoia** (*Human Interface Guidelines*), con una iconografía vectorial completamente nueva en paleta pastel, puntos de control de ventana nativos (*Traffic Lights* 🔴 🟡 🟢) y arquitectura de persistencia contra reversión de color al cargar sesiones moleculares (`.cxs`).

Basado en el código fuente oficial de ChimeraX en [RBVI/ChimeraX](https://github.com/RBVI/ChimeraX).

---

## 🌟 Pilares del Rediseño

1. **Lienzo Pro en Modo Claro (*Titanium Light Mode*):**
   * Viewport 3D en gris titanio puro (`#F5F5F7`) con iluminación difusa suave (`lighting soft`) y siluetas moleculares nítidas en grafito (`#3A3A3C` de 1.2px).
   * Paneles flotantes estilo Finder / Xcode con fondo blanco translúcido (`rgba(255, 255, 255, 0.96)`), bordes sutiles de 1px (`rgba(0, 0, 0, 0.08)`) y esquinas redondeadas continuas (*squircles* de 12px).
   * Cinta de herramientas superior (*Unified Ribbon*) transformada en un selector segmentado limpio y acromático.

2. **Botones de Control de Ventana de macOS (*Traffic Lights*):**
   * 🔴 **Cerrar** (`#FF5F56` / `#FF9AA2`) con micro-icono `x` interactivo al pasar el cursor.
   * 🟡 **Minimizar** (`#FFBD2E` / `#FFE082`) con micro-icono `-` interactivo.
   * 🟢 **Zoom / Pantalla Completa** (`#27C93F` / `#A8E6CF`) con micro-icono `+` interactivo.
   * Totalmente funcionales tanto en la esquina superior izquierda de la ventana principal como en las cabeceras de todos los paneles acoplables (*Log*, *Model Panel*, *Sequence Viewer*).

3. **Iconografía Vectorial Pastel 100% Exclusiva (Cero Iconos Repetidos):**
   * Cada herramienta de cada pestaña cuenta con un diseño vectorial individual y distinguible que respeta fielmente la estructura y semántica de su función en el código de ChimeraX.
   * Paleta cromática pastelDisplay P3:
     * **Azul Pastel** (`#8EC5FC`): Cadenas proteicas, herramientas principales y nitrógeno.
     * **Coral / Rosa Pastel** (`#FF9AA2`): Oxígeno, alertas y cargas negativas.
     * **Menta Pastel** (`#B5EAD7`): Cadenas complementarias, mínimos energéticos y timina.
     * **Mantequilla Pastel** (`#FFF3B0`): Azufre, adenina/guanina y reflejos.
     * **Durazno Pastel** (`#FFDAC1`): Tocones de nucleótidos y rotación de enlaces.
     * **Lavanda Pastel** (`#E2D1F9`): Superficies moleculares y cerebelo.
     * **Cian Pastel** (`#A0E7E5`): Puentes de hidrógeno e hidrofobicidad.

4. **Persistencia Total ante Sesiones (`.cxs`):**
   * Bloqueo activo de la reversión a negro mediante interceptores en los eventos nativos `end restore session`, `session open` y `open models`.

---

## 📁 Estructura del Repositorio

```text
Chimera-X-/
├── README.md                      <- Documentación y guía de instalación
├── theme/
│   └── liquid_glass_theme.py      <- Motor QSS y controlador maestro de la UI
├── hooks/
│   └── mac_sequoia_theme.pth      <- Gancho de inicialización automática en Python
├── icons/                         <- +200 iconos exportados en formato PNG Retina (128x128)
│   ├── atomshow.png
│   ├── nuc-ladder.png
│   ├── ...
├── packages/                      <- Estructura espejada coincidente con los paquetes de ChimeraX
│   ├── basic_actions/lib/
│   ├── bond_rot/
│   ├── color_key/icons/
│   ├── label/
│   ├── map/icons/
│   ├── map_eraser/
│   ├── map_series/
│   ├── markers/icons/
│   ├── medical_toolbar/icons/
│   ├── mouse_modes/icons/
│   ├── nucleotides/icons/
│   ├── pick_blobs/
│   ├── segger/
│   ├── segmentations/icons/
│   ├── sel_inspector/icons/
│   ├── shortcuts/icons/
│   ├── std_commands/
│   ├── struct_measure/
│   ├── swapaa/
│   ├── tape_measure/
│   ├── toolbar/icons/
│   ├── tug/
│   └── ui/icons/
├── svg/                           <- Fuentes vectoriales puras en SVG
└── scripts/
    ├── generate_all_vector_icons.py <- Generador de iconos pastel con Pillow
    └── generate_svgs.py             <- Generador de código vectorial SVG
```

---

## 🎨 Catálogo de Iconos y Semántica Estructural

| Categoría | Herramienta / Archivo | Representación Estructural Vectorial |
|---|---|---|
| **Nucleótidos** | `nuc-ladder.png` | Doble hélice con peldaños de escalera horizontales en azul y menta pastel. |
| | `nuc-stubs.png` | Espina dorsal continua con espículas/tocones perpendiculares en durazno pastel. |
| | `nuc-fill.png` | Par de bases aromáticas purina (hexágono + pentágono fusionados) rellenos con borde grafito. |
| | `nuc-slab.png` | Bloques/losas 3D isométricas escalonadas en azul y coral pastel. |
| | `nuc-tube.png` | Tubo cilíndrico curvo continuo con brillo especular en lavanda pastel. |
| | `nuc-elli.png` | Disco elipsoide 3D suave en menta pastel inclinado a -30°. |
| | `nuc-muff.png` | Cápsula horizontal de silenciador cilíndrico en cian pastel con ranuras. |
| | `nuc-color.png` | 4 losetas con las bases A (coral), T (menta), C (azul) y G (mantequilla). |
| **Coloreado** | `colorbyelement.png` | Racimo tetraédrico CPK de 4 esferas elementales en tonos pastel calibrados. |
| | `colorbychain.png` | 3 cintas polipeptídicas paralelas en azul pastel, coral pastel y menta pastel. |
| | `polymer.png` | Collar de perlas poliméricas unidas por hilo conector en gradiente arcoíris pastel. |
| | `rainbow.png` | Espectro concéntrico de 5 arcos continuos de color pastel. |
| | `esp.png` | Dipolo electrostático con polos (+) azul y (-) coral con líneas de campo curvas. |
| | `hydrophobicity.png` | Gota de agua en cian pastel sobre membrana lipídica con ángulo de contacto. |
| | `bfactor.png` | Termómetro de mercurio coral con ondas térmicas de mantequilla a los lados. |
| **Crio-EM / Mapas** | `mesh.png` | Red de rejilla de alambre isométrica en azul pastel. |
| | `contour.png` | Curvas de nivel topográficas concéntricas con cumbre en menta pastel. |
| | `mapimage.png` | Tarjeta de corte tomográfico en escala de grises con líneas de escaneo. |
| | `plane.png` | Plano de corte Z semitransparente con vector normal vertical. |
| | `slab.png` | Losa volumétrica comprendida entre dos planos paralelos con cota de espesor. |
| | `orthoplanes.png` | 3 planos ortogonales intersecados en los ejes cartesianos XY, XZ y YZ. |
| | `fullvolume.png` | Cubo translúcido isométrico con esfera de densidad interior. |
| | `fitmap.png` | Átomo acoplándose a un bolsillo de densidad mediante flechas directrices. |
| | `diffmap.png` | Símbolo Delta griego ($\Delta$) en durazno pastel entre densidades. |
| | `smooth.png` | Campana gaussiana que filtra y suaviza picos con ruido de alta frecuencia. |
| **Médico** | `airways.png` | Árbol bronquial anatómico con tráquea y ramificaciones pulmonares. |
| | `chest.png` | Caja torácica anatómica con silueta de costillas bilaterales y columna. |
| | `brain.png` | Hemisferio cerebral con circunvoluciones y surcos en lavanda pastel. |
| | `opendicom.png` | Carpeta estilo macOS con cruz médica blanca central. |
| **Dinámica / Fuerza** | `bondrot.png` | Enlace químico con anillo elíptico de rotación de torsión en durazno. |
| | `distance.png` | Calibre de medición midiendo la separación atómica con cotas. |
| | `swapaa.png` | Sustitución de residuo: intercambio mutuo con flechas circulares. |
| | `tape.png` | Cinta métrica en amarillo pastel con marcas milimétricas de calibración. |
| | `tug.png` | Tracción atómica: átomo sujeto a un vector de fuerza elástica. |
| | `minimize.png` | Curva de potencial energético con el átomo posicionado en el mínimo global. |

---

## 🚀 Instalación y Uso

### Instalación Automática (Recomendada)

1. Copia el archivo de gancho automático:
   ```text
   hooks/mac_sequoia_theme.pth
   ```
   a la carpeta de paquetes de usuario de ChimeraX:
   ```text
   C:\Users\<TuUsuario>\AppData\Local\UCSF\ChimeraX\1.12\Python311\site-packages\
   ```
2. Asegúrate de que `theme/liquid_glass_theme.py` esté ubicado en tu carpeta de inicio:
   ```text
   C:\Users\<TuUsuario>\chimerax_start\liquid_glass_theme.py
   ```
3. ¡Listo! A partir de ese momento, ChimeraX arrancará siempre de forma automática con la interfaz clara y los iconos Mac pastel.

### Activación Manual en Caliente

Dentro de cualquier sesión abierta de ChimeraX, escribe en la línea de comandos inferior:
```text
liquidglass
```
o para desactivarlo:
```text
liquidglass off
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Las marcas y nomenclaturas de UCSF ChimeraX pertenecen a sus respectivos titulares y a la Universidad de California, San Francisco (UCSF).
