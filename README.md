# UCSF ChimeraX 

Subsistema Qt6/QSS, motor i18n e iconografia vectorial para **UCSF ChimeraX** (1.11+).

## Arquitectura

* **Inyeccion (`.pth`):** Carga automatica en arranque desde `site-packages/mac_sequoia_theme.pth` hacia `~/chimerax_start/liquid_glass_theme.py`.
* **Resolucion de Iconos (`O(1)`):** Interceptores sobre `BundleInfo.get_path` y `MouseMode.icon_location` mediante tablas hash en memoria (`_FAST_SECTION_TITLE_MAP`, `_FAST_TITLE_MAP`, `_MOUSE_MODE_ICON_MAP`).
* **Toolbar (`TabbedToolbar._Section`):** Mutacion directa de `QAction` y `QToolButton` en las 8 pestañas nativas sin invocar `_redo_layout()`. Resaltado vectorial con canal alfa (`_make_mac_highlight_icon`).
* **Ventana y DWM (`dwmapi.dll`):** `FramelessWindowHint` con controles `MacTrafficLightButton` e integracion nativa con atributos DWM `20`, `33`, `35` y `36`.
* **Vistas Web y Lienzo:** Inyeccion CSS/JS cacheada en `Log`, `FileHistory` y `RapidAccess`, con renderizado nativo `QPainter` (`MacHeroCanvasWidget`).

## Prestaciones

* **Latencia `O(1)`:** Diccionarios i18n inversos (`_REVERSE_TO_EN`), QSS, JS/HTML y `QIcon`/`QPixmap` precompilados con `@lru_cache`.
* **Cobertura Vectorial 100%:** 230 PNG (`128x128`, supermuestreo `4x` LANCZOS desde `512x512`) y 222 SVG para los 152 proveedores de toolbar y 42 modos `MouseMode` (incluyendo alias `*-dark.png` y `*_wht.png`).
* **Persistencia Determinista:** Estado atomico en disco para tema (`theme_mode.txt`) e idioma (`language.txt`), con orden canonico fijo en `QMenuBar` (`_CANONICAL_MENU_ORDER`).
* **Control de Sesiones (`.cxs`):** Hooks en `end restore session`, `session open`, `open models` y `remove models` para preservar el color del viewport 3D.
* **Sincronizacion de Cuadros:** `MacLoadingOverlay` y `MacInternalCurtain` acoplados a la frecuencia del monitor (`60 Hz` / `30 Hz`) mediante `check_for_drawing_change`.

## Estructura

### Repositorio

```text
Chimera-X-/
├── install.py
├── LICENSE
├── README.md
├── hooks/
│   └── mac_sequoia_theme.pth
├── theme/
│   └── liquid_glass_theme.py
├── icons/                                  # 230 PNG (128x128 RGBA)
├── svg/                                    # 222 SVG
├── scripts/
│   ├── generate_all_vector_icons.py
│   ├── refine_weak_icons.py
│   └── generate_svgs.py
└── packages/
    └── chimerax/                           # Espejo de reemplazo por modulo
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

### Despliegue

```text
~/chimerax_start/
├── liquid_glass_theme.py
├── theme_mode.txt                          # gray | dark
├── language.txt                            # en_US | zh_CN | es_LA | hi_IN | ar_SA | fr_FR
└── icons/

~/Downloads/chimerax_mac_icons/

<ChimeraX_User_Site_Packages>/
├── mac_sequoia_theme.pth
└── chimerax/
```

Rutas `<ChimeraX_User_Site_Packages>`:
* **Windows:** `%LOCALAPPDATA%\UCSF\ChimeraX\<version>\Python311\site-packages`
* **macOS:** `~/Library/Application Support/ChimeraX/<version>/site-packages`
* **Linux:** `~/.local/share/ChimeraX/<version>/site-packages`

## Configuracion

```text
liquid_glass_theme
├── Estado
│   ├── _MODE_STATE_FILE                    -> ~/chimerax_start/theme_mode.txt
│   ├── _LANG_STATE_FILE                    -> ~/chimerax_start/language.txt
│   ├── _CURRENT_MODE                       -> "gray" | "dark"
│   └── _CURRENT_LANG                       -> "en_US" | "zh_CN" | "es_LA" | "hi_IN" | "ar_SA" | "fr_FR"
│
├── Paletas (_THEME_PALETTES)
│   ├── gray
│   │   ├── win_bg / card_bg                -> #D5DBE5 / #E4E8F0
│   │   ├── header_bg / border / sep_color  -> #C8D0DE / #AEB9CC / #8FA3C2
│   │   ├── text / accent / silhouette      -> #1D1D1F / #0066CC / #2C2C2E
│   │   ├── canvas_rgb / sideview_rgb       -> (0.835, 0.859, 0.898, 1.0) / (1.0, 1.0, 1.0, 1.0)
│   │   └── dwm (dark, caption, text)       -> (0, 0x00E5DBD5, 0x001F1D1D)
│   └── dark
│       ├── win_bg / card_bg                -> #1C1C1E / #2C2C2E
│       ├── header_bg / border / sep_color  -> #25262B / #3E4047 / #5E6E8C
│       ├── text / accent / silhouette      -> #F5F5F7 / #0A84FF / #E5E5EA
│       ├── canvas_rgb / sideview_rgb       -> (0.110, 0.110, 0.118, 1.0) / (0.086, 0.090, 0.106, 1.0)
│       └── dwm (dark, caption, text)       -> (1, 0x001E1C1C, 0x00F7F5F5)
│
├── Paleta Vectorial (Iconos)
│   ├── C_DARK                              -> #3A3A3C (contorno estructural)
│   ├── C_BLUE / C_CYAN                     -> #8EC5FC / #A0E7E5
│   ├── C_CORAL / C_RED_SLASH               -> #FF9AA2 / #E05263
│   ├── C_MINT                              -> #B5EAD7
│   ├── C_YELLOW / C_GOLD                   -> #FFF3B0 / #FFD670
│   └── C_PEACH / C_LAV                     -> #FFDAC1 / #E2D1F9
│
└── Hooks
    ├── BundleInfo.get_path                 -> _mac_get_path
    ├── MouseMode.icon_location             -> _mac_mm_icon_location
    ├── ToolbarTool                         -> _mac_build_tabs, _mac_build_home_tab, _mac_color_scheme_changed, _mac_fill_context_menu
    ├── _Section                            -> _mac_update_button_action, _mac_add_button_highlight, _mac_remove_button_highlight, _mac_redo_layout
    ├── _Qt.__init__                        -> _mac_qt_init
    ├── Log._actually_show                  -> _mac_actually_show
    ├── FileHistory                         -> _mac_fh_history_html, _mac_fh_update_html
    └── session.triggers                    -> "end restore session", "session open", "open models", "remove models"
```

## Instalacion

### Automatizada

**Windows:**
```powershell
& "C:\Program Files\ChimeraX 1.12\bin\python.exe" install.py
```

**macOS:**
```bash
/Applications/ChimeraX-1.12.app/Contents/bin/python3 install.py
```

**Linux:**
```bash
python3 install.py
```

### Manual

1. Copiar `theme/liquid_glass_theme.py` a `~/chimerax_start/liquid_glass_theme.py`.
2. Copiar el contenido de `icons/` y `svg/` a `~/chimerax_start/icons/`.
3. Crear `<ChimeraX_User_Site_Packages>/mac_sequoia_theme.pth`:

```python
import sys, os; p = r'<RUTA_ABSOLUTA_A_CHIMERAX_START>'; sys.path.insert(0, p) if os.path.exists(p) and p not in sys.path else None; import liquid_glass_theme
```

### Compilacion de Iconos

```powershell
& "C:\Program Files\ChimeraX 1.12\bin\python.exe" scripts\generate_all_vector_icons.py
& "C:\Program Files\ChimeraX 1.12\bin\python.exe" scripts\refine_weak_icons.py
& "C:\Program Files\ChimeraX 1.12\bin\python.exe" scripts\generate_svgs.py
```

## Comandos

* **Cabecera UI:** `Gray` | `Dark` | `Language` (`en_US`, `zh_CN`, `es_LA`, `hi_IN`, `ar_SA`, `fr_FR`).
* **Consola ChimeraX:** `theme gray` | `theme dark`.

## Licencia

MIT. Las marcas y paquetes base de UCSF ChimeraX pertenecen a los Regentes de la Universidad de California (UCSF / RBVI).
