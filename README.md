# UCSF ChimeraX — Subsistema de Interfaz Liquid Glass e Iconografia Vectorial

Modificacion estructural de interfaz grafica (Qt6 / QSS / QPainter), motor de localizacion multilingue y reemplazo integral de activos vectoriales para **UCSF ChimeraX** (compatible con la arquitectura `RBVI/ChimeraX` 1.11+).

---

## 1. Arquitectura del Sistema

El subsistema opera mediante inyeccion temprana en el proceso de arranque de Python a traves de un archivo de ruta `.pth` alojado en el directorio `site-packages` del usuario. Durante la inicializacion del interprete embebido de ChimeraX, el modulo principal (`liquid_glass_theme.py`) instala interceptores de clase, filtros de eventos globales en `QApplication` y disparadores de sesion (`session.triggers`) sin alterar los binarios compilados de la instalacion base.

### Componentes de Interceptacion en Tiempo de Ejecucion

* **Resolucion de Activos (`BundleInfo.get_path` y `MouseMode.icon_location`):** Redireccion en tiempo constante `O(1)` mediante tablas hash en memoria (`_SUBPATH_BASENAME_CACHE`, `_FAST_SECTION_TITLE_MAP`, `_FAST_TITLE_MAP`, `_MOUSE_MODE_ICON_MAP`) hacia el repositorio local de iconos vectoriales (`128x128` PNG/SVG).
* **Mutacion Directa de `TabbedToolbar._Section`:** Actualizacion en vivo de instancias `QAction` y `QToolButton` en las 8 pestañas nativas (`Home`, `Molecule Display`, `Nucleotides`, `Graphics`, `Map`, `Medical Image`, `Markers`, `Right Mouse`), evitando llamadas destructivas a `_redo_layout()` y sustituyendo el resaltado nativo (`Qt.green`) por composicion vectorial con canal alfa (`_make_mac_highlight_icon`).
* **Integracion con Desktop Window Manager (`dwmapi.dll`):** Configuracion de atributos nativos de ventana en Windows 11 (`DWMWA_USE_IMMERSIVE_DARK_MODE = 20`, `DWMWA_WINDOW_CORNER_PREFERENCE = 33`, `DWMWA_CAPTION_COLOR = 35`, `DWMWA_TEXT_COLOR = 36`).
* **Contenedor Superior y Barras de Acoplamiento (`MacTopMenuBar`, `MacWindowHeader`, `MacDockTitleBar`):** Encapsulacion sin bordes (`FramelessWindowHint`) con controles de ventana vectoriales (`MacTrafficLightButton`), selector de modo cromatico en tiempo real y conmutador de idioma persistente.
* **Sincronizacion de Vistas Web y Lienzo (`RapidAccess`, `FileHistory`, `Log`):** Inyeccion de hojas de estilo CSS y rutinas JavaScript precompiladas en cache (`_cached_log_js`, `_cached_no_hist_html`) junto con un lienzo nativo `QPainter` (`MacHeroCanvasWidget`) cuando no existen historiales activos.

---

## 2. Prestaciones Tecnicas y Ventajas Logradas

1. **Complejidad Temporal `O(1)` en Conmutacion de Estado:**
   * Precompilacion de diccionarios de traduccion directa e inversa (`_REVERSE_TO_EN`), resolucion de rutas de iconos y generacion de hojas de estilo mediante `@lru_cache`.
   * Reutilizacion de instancias `QIcon` y `QPixmap` en memoria (`_QICON_CACHE`, `_HIGHLIGHT_ICON_CACHE`, `_cached_static_logo_pixmap`), eliminando lecturas redundantes de disco durante cambios de pestaña o tema.
2. **Cobertura Vectorial Completa (100% de Proveedores de Barra de Herramientas y Modos de Raton):**
   * 230 activos PNG y 222 activos SVG renderizados con supermuestreo `4x` (`512x512` a `128x128` mediante filtro `Image.Resampling.LANCZOS`).
   * Cobertura total sobre los 152 proveedores declarados en `METADATA` (`ChimeraX :: Provider :: toolbar`) y los 42 modos interactivos de raton y realidad virtual (`MouseMode`), incluyendo sincronizacion de alias oscuros (`*-dark.png`, `*_wht.png`).
3. **Persistencia Determinista de Idioma y Tema:**
   * Almacenamiento atomico en disco de la preferencia de idioma (`language.txt`) y del esquema de color (`theme_mode.txt`).
   * Ordenamiento invariante de la barra de menus principal (`_CANONICAL_MENU_ORDER`: `File`, `Edit`, `Select`, `Actions`, `Presets`, `Favorites`, `Tools`, `Help`) inmune a duplicaciones o desordenamientos tras recargas en caliente o cambios de tema.
4. **Estabilidad del Viewport OpenGL y Sesiones `.cxs`:**
   * Ganchos sobre los eventos `end restore session`, `session open`, `open models` y `remove models` que impiden la reversion no solicitada del color de fondo a negro, respetando a la vez los cambios manuales ejecutados por el usuario mediante el comando `set bgColor`.
5. **Estabilizacion de Fotogramas en Transiciones (`MacLoadingOverlay`):**
   * Cortina interna (`MacInternalCurtain`) y superposicion sincronizada con la frecuencia de refresco del monitor primario (`60 Hz` / `30 Hz`), verificando la estabilidad de renderizado del motor OpenGL (`check_for_drawing_change`) antes de liberar la vista.

---

## 3. Mapa de Archivos del Repositorio y Despliegue

### 3.1 Estructura del Repositorio

```text
Chimera-X-/
├── install.py                              # Instalador automatizado multiplataforma
├── LICENSE                                 # Licencia MIT
├── README.md                               # Documentacion tecnica del sistema
├── hooks/
│   └── mac_sequoia_theme.pth               # Punto de entrada de inyeccion en site-packages
├── theme/
│   └── liquid_glass_theme.py               # Motor principal Qt6/QSS, i18n, DWM e interceptores
├── icons/                                  # 230 iconos rasterizados (128x128 RGBA PNG)
├── svg/                                    # 222 contenedores vectoriales SVG
├── scripts/
│   ├── generate_all_vector_icons.py        # Generador base de iconos vectoriales (512->128)
│   ├── refine_weak_icons.py                # Generador avanzado de alta densidad y alias
│   └── generate_svgs.py                    # Empaquetador de activos PNG a contenedores SVG
└── packages/
    └── chimerax/                           # Arbol espejo de reemplazo directo por paquete
        ├── basic_actions/lib/
        ├── bond_rot/
        ├── color_key/icons/
        ├── label/
        ├── map/icons/
        ├── map_eraser/
        ├── map_series/
        ├── markers/icons/
        ├── medical_toolbar/icons/
        ├── meeting/
        ├── mouse_modes/icons/
        ├── nucleotides/icons/
        ├── orthopick/icons/
        ├── pick_blobs/
        ├── rest_server/static/
        ├── segger/
        ├── segmentations/icons/
        ├── sel_inspector/icons/
        ├── shortcuts/icons/
        ├── std_commands/
        ├── struct_measure/
        ├── swapaa/
        ├── tape_measure/
        ├── toolbar/icons/
        ├── tug/
        ├── ui/html/fonts/
        ├── ui/icons/
        ├── viewdock/icons/
        ├── vive/
        └── zone/
```

### 3.2 Arbol de Despliegue en el Sistema Anfitrion

```text
~/chimerax_start/
├── liquid_glass_theme.py                   # Modulo activo cargado en el arranque
├── theme_mode.txt                          # Estado persistente del modo visual (light | gray | dark)
├── language.txt                            # Estado persistente del idioma (en_US | zh_CN | es_LA | hi_IN | ar_SA | fr_FR)
└── icons/                                  # Repositorio primario de iconos en tiempo de ejecucion

~/Downloads/chimerax_mac_icons/             # Repositorio secundario de respaldo de iconos

<ChimeraX_User_Site_Packages>/
├── mac_sequoia_theme.pth                   # Hook de carga automatica al iniciar Python
└── chimerax/                               # Paquetes locales con activos graficos sincronizados
```

Rutas predeterminadas para `<ChimeraX_User_Site_Packages>`:
* **Windows:** `%LOCALAPPDATA%\UCSF\ChimeraX\<version>\Python311\site-packages`
* **macOS:** `~/Library/Application Support/ChimeraX/<version>/site-packages`
* **Linux:** `~/.local/share/ChimeraX/<version>/site-packages`

---

## 4. Arbol de Ajustes y Parametros del Subsistema

```text
liquid_glass_theme
├── Estado Global y Persistencia
│   ├── _MODE_STATE_FILE                    -> ~/chimerax_start/theme_mode.txt
│   ├── _LANG_STATE_FILE                    -> ~/chimerax_start/language.txt
│   ├── _CURRENT_MODE                       -> "light" | "gray" | "dark" (por defecto: "gray")
│   └── _CURRENT_LANG                       -> "en_US" | "zh_CN" | "es_LA" | "hi_IN" | "ar_SA" | "fr_FR"
│
├── Paletas Cromaticas (_THEME_PALETTES)
│   ├── light
│   │   ├── win_bg / viewport_bg            -> #F5F5F7
│   │   ├── card_bg / menu_btn_bg           -> #FFFFFF
│   │   ├── header_bg                       -> #F0F3F9
│   │   ├── border / border_soft            -> #D5DFEE / #E2E8F2
│   │   ├── sep_color                       -> #BACBE6
│   │   ├── text / accent                   -> #1D1D1F / #007AFF
│   │   ├── canvas_rgb / sideview_rgb       -> (0.961, 0.961, 0.969, 1.0) / (1.0, 1.0, 1.0, 1.0)
│   │   ├── silhouette_color                -> #3A3A3C
│   │   └── dwm (dark, caption, text)       -> (0, 0x00F7F5F5, 0x001F1D1D)
│   │
│   ├── gray
│   │   ├── win_bg / viewport_bg            -> #D5DBE5
│   │   ├── card_bg / alt_bg                -> #E4E8F0 / #DCE1EB
│   │   ├── header_bg                       -> #C8D0DE
│   │   ├── border / border_soft            -> #AEB9CC / #B8C3D4
│   │   ├── sep_color                       -> #8FA3C2
│   │   ├── text / accent                   -> #1D1D1F / #0066CC
│   │   ├── canvas_rgb / sideview_rgb       -> (0.835, 0.859, 0.898, 1.0) / (1.0, 1.0, 1.0, 1.0)
│   │   ├── silhouette_color                -> #2C2C2E
│   │   └── dwm (dark, caption, text)       -> (0, 0x00E5DBD5, 0x001F1D1D)
│   │
│   └── dark
│       ├── win_bg / viewport_bg            -> #1C1C1E
│       ├── card_bg / alt_bg                -> #2C2C2E / #242426
│       ├── header_bg                       -> #25262B
│       ├── border / border_soft            -> #3E4047 / #36383F
│       ├── sep_color                       -> #5E6E8C
│       ├── text / accent                   -> #F5F5F7 / #0A84FF
│       ├── canvas_rgb / sideview_rgb       -> (0.110, 0.110, 0.118, 1.0) / (0.086, 0.090, 0.106, 1.0)
│       ├── silhouette_color                -> #E5E5EA
│       └── dwm (dark, caption, text)       -> (1, 0x001E1C1C, 0x00F7F5F5)
│
├── Paleta Vectorial Semantica (Generadores de Iconos)
│   ├── C_DARK                              -> rgba(58, 58, 60, 255)      # Contornos estructurales (14px-16px @ 512px)
│   ├── C_BLUE                              -> rgba(142, 197, 252, 255)   # Cadenas principales, nitrogeno, geometria primaria
│   ├── C_CORAL                             -> rgba(255, 154, 162, 255)   # Oxigeno, cursores activos, alertas y cortes
│   ├── C_RED_SLASH                         -> rgba(224, 82, 99, 255)     # Trazos diagonales de ocultacion
│   ├── C_MINT                              -> rgba(181, 234, 215, 255)   # Cadenas secundarias, superficies y enlaces
│   ├── C_YELLOW / C_GOLD                   -> rgba(255, 243, 176, 255)   # Iluminacion, azufre, purinas, factor B
│   ├── C_PEACH                             -> rgba(255, 218, 193, 255)   # Torsion de enlaces, planos de corte
│   ├── C_LAV                               -> rgba(226, 209, 249, 255)   # Mapas de densidad, neuroanatomia, VR
│   └── C_CYAN                              -> rgba(160, 231, 229, 255)   # Puentes de hidrogeno, lentes opticas, cajas
│
└── Interceptores y Eventos Registrados
    ├── BundleInfo.get_path                 -> _mac_get_path
    ├── MouseMode.icon_location             -> _mac_mm_icon_location
    ├── ToolbarTool._build_tabs             -> _mac_build_tabs
    ├── ToolbarTool.build_home_tab          -> _mac_build_home_tab
    ├── ToolbarTool._color_scheme_changed   -> _mac_color_scheme_changed
    ├── ToolbarTool.fill_context_menu       -> _mac_fill_context_menu
    ├── _Section._update_button_action      -> _mac_update_button_action (iconSize 28x28)
    ├── _Section.add_button_highlight       -> _mac_add_button_highlight
    ├── _Section.remove_button_highlight    -> _mac_remove_button_highlight
    ├── _Section._redo_layout               -> _mac_redo_layout
    ├── _Qt.__init__                        -> _mac_qt_init (inyeccion de MacDockTitleBar)
    ├── Log._actually_show                  -> _mac_actually_show
    ├── FileHistory.history_html            -> _mac_fh_history_html
    ├── FileHistory.update_html             -> _mac_fh_update_html
    └── session.triggers                    -> "end restore session", "session open", "open models", "remove models"
```

---

## 5. Instalacion

### 5.1 Requisitos

* **UCSF ChimeraX** version 1.11 o 1.12+ instalado en el sistema.
* Acceso de escritura al directorio de usuario (`~/chimerax_start` y `site-packages` de usuario de ChimeraX).

### 5.2 Instalacion Automatizada (Recomendada)

Ejecutar el script `install.py` utilizando el interprete de Python embebido de ChimeraX o cualquier interprete Python 3.9+ del sistema:

**En Windows (PowerShell):**

```powershell
& "C:\Program Files\ChimeraX 1.12\bin\python.exe" install.py
```

**En macOS:**

```bash
/Applications/ChimeraX-1.12.app/Contents/bin/python3 install.py
```

**En Linux:**

```bash
/usr/bin/chimerax -m pip --version >/dev/null 2>&1 && python3 install.py
```

El instalador ejecuta las siguientes operaciones:
1. Crea el directorio `~/chimerax_start/` y copia `theme/liquid_glass_theme.py`.
2. Sincroniza la totalidad de archivos `.png` y `.svg` desde `icons/` y `svg/` hacia `~/chimerax_start/icons/` y `~/Downloads/chimerax_mac_icons/`.
3. Localiza todas las instalaciones de usuario de ChimeraX (`site-packages`), genera el archivo `mac_sequoia_theme.pth` apuntando a `~/chimerax_start` y despliega el arbol `packages/chimerax/`.

### 5.3 Instalacion Manual

1. Copiar `theme/liquid_glass_theme.py` en `~/chimerax_start/liquid_glass_theme.py`.
2. Copiar el contenido de `icons/` y `svg/` dentro de `~/chimerax_start/icons/`.
3. Crear el archivo `mac_sequoia_theme.pth` dentro del directorio `site-packages` de usuario de ChimeraX con la siguiente instruccion en una sola linea (ajustando `<RUTA_ABSOLUTA_A_CHIMERAX_START>`):

```python
import sys, os; p = r'<RUTA_ABSOLUTA_A_CHIMERAX_START>'; sys.path.insert(0, p) if os.path.exists(p) and p not in sys.path else None; import liquid_glass_theme
```

### 5.4 Recompilacion de Iconos Vectoriales (Opcional)

Para regenerar desde codigo los 230 activos PNG (`128x128`) y sus contenedores SVG correspondientes:

```powershell
& "C:\Program Files\ChimeraX 1.12\bin\python.exe" scripts\generate_all_vector_icons.py
& "C:\Program Files\ChimeraX 1.12\bin\python.exe" scripts\refine_weak_icons.py
& "C:\Program Files\ChimeraX 1.12\bin\python.exe" scripts\generate_svgs.py
```

---

## 6. Uso y Comandos en Tiempo de Ejecucion

El subsistema expone controles directos en la cabecera superior derecha de la ventana principal:
* **Conmutadores de Tema (`Light` / `Gray` / `Dark`):** Aplican de inmediato la paleta cromatica, actualizan el viewport 3D y persisten la seleccion en `~/chimerax_start/theme_mode.txt`.
* **Selector de Idioma (`Language`):** Despliega el panel modal (`MacLanguageSelector`) con soporte para `English (US)`, `Mandarin (zh_CN)`, `Espanol (es_LA)`, `Hindi (hi_IN)`, `Arabe (ar_SA)` y `Frances (fr_FR)`, persistiendo la seleccion en `~/chimerax_start/language.txt`.

Tambien se registran comandos directos en la consola de ChimeraX (CLI):
* `theme light` — Activa la paleta clara.
* `theme gray` — Activa la paleta gris acero.
* `theme dark` — Activa la paleta oscura.

---

## 7. Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulte el archivo `LICENSE` para mas detalles. Las marcas, nombres comerciales y paquetes base de UCSF ChimeraX son propiedad de los Regentes de la Universidad de California, San Francisco (UCSF) y del Resource for Biocomputing, Visualization, and Informatics (RBVI).
