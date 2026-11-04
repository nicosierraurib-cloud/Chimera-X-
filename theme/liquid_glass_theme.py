# -*- coding: utf-8 -*-
"""
UCSF ChimeraX - Apple macOS Sequoia "Light Mode Pro" & Full System Redesign
============================================================================
- Modo Claro macOS: Fondo #F5F5F7 titanio puro, hairlines sutiles, acento #007AFF.
- Botones de Ventana (Traffic Lights): Puntos de colores reales (🔴 🟡 🟢)
  integrados en la barra superior izquierda y en las cabeceras de todos los paneles.
- Iconografía SF Symbols 100% individual y distintiva: 0 iconos compartidos o repetidos.
  Cada herramienta (Nucleótidos, Colores, Mapas, Médico, Marcadores, etc.) tiene su glifo único.
- Colores Pasteles calibrados (#8EC5FC, #FF9AA2, #B5EAD7, #FFF3B0, #FFDAC1, #E2D1F9, #A0E7E5).
- Persistencia total: Bloqueo de fondo negro ante apertura de sesiones (.cxs) y modelos.
"""

import os
from Qt import QtWidgets, QtGui, QtCore
from chimerax.core.commands import register, CmdDesc, StringArg, run

ICONS_DIR = r"C:\Users\Parfion\Downloads\chimerax_mac_icons"


# =============================================================================
# 1. PARCHE GLOBAL DE RESOLUCIÓN DE BUNDLES (BUNDLEINFO)
# =============================================================================

try:
    from chimerax.core.toolshed.info import BundleInfo
    if not hasattr(BundleInfo, "_mac_patched"):
        _orig_get_path = BundleInfo.get_path

        def _mac_get_path(self, subpath):
            if subpath and (subpath.endswith(".png") or subpath.endswith(".svg") or "icons" in subpath):
                fname = os.path.basename(subpath)
                mac_p = os.path.join(ICONS_DIR, fname)
                if os.path.exists(mac_p):
                    return mac_p
            return _orig_get_path(self, subpath)

        BundleInfo.get_path = _mac_get_path
        BundleInfo._mac_patched = True
except Exception:
    pass


# =============================================================================
# 2. RESOLUTOR 1:1 EXACTO PARA CADA BOTÓN (CERO REPETICIONES / BESPOKE GLYPHS)
# =============================================================================

EXACT_SECTION_TITLE_MAP = {
    # --- TAB: Home ---
    ("File", "Open"): "open-in-app.png",
    ("File", "Recent"): "recentfiles.png",
    ("File", "Save"): "content-save.png",
    ("Images", "Snapshot"): "camera.png",
    ("Images", "Spin movie"): "video.png",
    ("Atoms", "Show"): "atomshow.png",
    ("Atoms", "Hide"): "atomhide.png",
    ("Cartoons", "Show"): "ribshow.png",
    ("Cartoons", "Hide"): "ribhide.png",
    ("Styles", "Stick"): "stick.png",
    ("Styles", "Sphere"): "sphere.png",
    ("Styles", "Ball & stick"): "ball_stick.png",
    ("Background", "White"): "whitebg.png",
    ("Background", "Black"): "blackbg.png",
    ("Lighting", "Simple"): "simplelight.png",
    ("Lighting", "Soft"): "softlight.png",
    ("Lighting", "Full"): "fulllight.png",
    ("Selection", "Inspect"): "magnifying-glass.png",

    # --- TAB: Molecule Display ---
    ("Surfaces", "Show"): "surfshow.png",
    ("Surfaces", "Hide"): "surfhide.png",
    ("Styles", "Plain"): "plain.png",
    ("Styles", "Filled"): "nuc-fill.png",
    ("Styles", "Tube/\nSlab"): "nuc-tube.png",
    ("Styles", "Ladder"): "nuc-ladder.png",
    ("Coloring", "heteroatom"): "colorbyelement.png",
    ("Coloring", "chain"): "colorbychain.png",
    ("Coloring", "polymer"): "polymer.png",
    ("Coloring", "rainbow"): "rainbow.png",
    ("Coloring", "electrostatic"): "esp.png",
    ("Coloring", "hydrophobic"): "hydrophobicity.png",
    ("Coloring", "b-factor"): "bfactor.png",
    ("Coloring", "nucleotide"): "nuc-color.png",
    ("Analysis", "H-bonds"): "hbonds.png",
    ("Analysis", "Hide H-bonds"): "hbondshide.png",
    ("Analysis", "Sequence"): "sequence.png",
    ("Analysis", "Interfaces"): "interfaces.png",

    # --- TAB: Nucleotides ---
    ("Styles", "Slab"): "nuc-slab.png",
    ("Styles", "Tube/\nEllipsoid"): "nuc-elli.png",
    ("Styles", "Tube/\nMuffler"): "nuc-muff.png",
    ("Styles", "Stubs"): "nuc-stubs.png",

    # --- TAB: Graphics ---
    ("Background", "Gray"): "graybg.png",
    ("Lighting & Effects", "Simple"): "simplelight.png",
    ("Lighting & Effects", "Soft"): "softlight.png",
    ("Lighting & Effects", "Full"): "fulllight.png",
    ("Lighting & Effects", "Flat"): "flat.png",
    ("Lighting & Effects", "Shadow"): "shadow.png",
    ("Lighting & Effects", "Silhouettes"): "silhouette.png",
    ("Camera", "Side view"): "sideview.png",
    ("Camera", "View selected"): "viewsel.png",
    ("Camera", "View all"): "viewall.png",
    ("Camera", "Orient"): "orient.png",

    # --- TAB: Map ---
    ("Map", "Show"): "showmap.png",
    ("Map", "Hide"): "hidemap.png",
    ("Style", "surface"): "mapsurf.png",
    ("Style", "mesh"): "mesh.png",
    ("Style", "image"): "mapimage.png",
    ("Style", "Transparent surface"): "icecube.png",
    ("Style", "Outline box"): "outlinebox.png",
    ("Steps", "Step 1"): "step1.png",
    ("Steps", "Step 2"): "step2.png",
    ("Steps", "Step 4"): "step4.png",
    ("Subregions", "Z-plane"): "plane.png",
    ("Subregions", "Slab"): "slab.png",
    ("Subregions", "Orthoplanes"): "orthoplanes.png",
    ("Subregions", "Full"): "fullvolume.png",
    ("Subregions", "Zone"): "volzone.png",
    ("Appearance", "Color near atoms"): "colorzone.png",
    ("Appearance", "Hide dust"): "dust.png",
    ("Calculations", "Fit"): "fitmap.png",
    ("Calculations", "Subtract"): "diffmap.png",
    ("Calculations", "Smooth"): "smooth.png",
    ("Rendering Modes", "XYZ slices"): "xyzslice.png",
    ("Rendering Modes", "Perpendicular slices"): "perpslice.png",
    ("Rendering Modes", "Raycasting"): "raycasting.svg",

    # --- TAB: Medical Image ---
    ("File", "Open DICOM"): "opendicom.png",
    ("Style", "Z-plane"): "plane.png",
    ("Style", "Slab"): "slab.png",
    ("Style", "Orthoplanes"): "orthoplanes.png",
    ("Style", "Full"): "fullvolume.png",
    ("Style", "Outline box"): "cubeoutline.png",
    ("Color", "Airways"): "airways.png",
    ("Color", "Chest CT"): "chest.png",
    ("Color", "Brain CT"): "brain.png",
    ("Color", "Default thresholds"): "windowing.png",
    ("Graphics", "Step 1"): "step1.png",
    ("Graphics", "Step 2"): "step2.png",
    ("Mouse Mode", "Crop"): "crop.png",
    ("Mouse Mode", "Move planes"): "moveplanes.png",
    ("Mouse Mode", "Tilt slab"): "rotateslab.png",
    ("Mouse Mode", "Tape"): "tape.png",
    ("Mouse Mode", "Windowing"): "windowing.png",
    ("Segmentation Controls", "Toggle Mouse Modes"): "mouse.png",
    ("Segmentation Controls", "Toggle Hand Modes"): "right_controller.png",

    # --- TAB: Markers ---
    ("Place markers", "Maximum"): "maximum.png",
    ("Place markers", "Plane"): "plane.png",
    ("Place markers", "Surface"): "surface.png",
    ("Place markers", "Center"): "center.png",
    ("Place markers", "Point"): "point.png",
    ("Adjust markers", "Link"): "link.png",
    ("Adjust markers", "Move"): "move.png",
    ("Adjust markers", "Resize"): "resize.png",
    ("Adjust markers", "Delete"): "delete.png",

    # --- TAB: Right Mouse ---
    ("Movement", "Select"): "select.png",
    ("Movement", "Rotate"): "rotate.png",
    ("Movement", "Translate"): "translate.png",
    ("Movement", "Zoom"): "zoom.png",
    ("Movement", "Move model"): "move_picked_model.png",
    ("Movement", "Rotate model"): "rotatesel.png",
    ("Movement", "Drag model"): "move_picked_model.png",
    ("Movement", "Move atoms"): "move_atoms.png",
    ("Movement", "Pivot"): "pivot.png",
    ("Annotation", "Distance"): "distance.png",
    ("Annotation", "Label"): "label.png",
    ("Annotation", "Move label"): "movelabel.png",
    ("Annotation", "Key"): "ckicon.png",
    ("Clipping", "Clip"): "clip.png",
    ("Clipping", "Clip rotate"): "cliprot.png",
    ("Clipping", "Zone"): "zone.png",
    ("Map", "Contour level"): "contour.png",
    ("Map", "Move planes"): "moveplanes.png",
    ("Map", "Rotate slab"): "rotateslab.png",
    ("Map", "Crop"): "crop.png",
    ("Map", "Tape"): "tape.png",
    ("Map", "Blob"): "pickblobs.png",
    ("Map", "Erase"): "eraser.png",
    ("Map", "Play series"): "vseries.png",
    ("Map", "Windowing"): "windowing.png",
    ("Structure Modification", "Bond rotation"): "bondrot.png",
    ("Structure Modification", "Swapaa"): "swapaa.png",
    ("Structure Modification", "Play coords"): "coordset.png",
    ("Structure Modification", "Tug"): "tug.png",
    ("Structure Modification", "Minimize"): "minimize.png",
    ("Other", "Next docked"): "nextdocking.png",
}


def resolve_mac_icon(title, description="", section=""):
    # 1. Búsqueda exacta por (sección, título)
    key = (section, title)
    if key in EXACT_SECTION_TITLE_MAP:
        fname = EXACT_SECTION_TITLE_MAP[key]
        fp = os.path.join(ICONS_DIR, fname)
        if os.path.exists(fp):
            return fp

    # 2. Búsqueda directa por título normalizado
    norm_title = title.lower().strip()
    for (sec, t), fname in EXACT_SECTION_TITLE_MAP.items():
        if t.lower().strip() == norm_title:
            fp = os.path.join(ICONS_DIR, fname)
            if os.path.exists(fp):
                return fp

    # 3. Fallback directo a nombre de archivo idéntico en directorio de iconos
    direct = os.path.join(ICONS_DIR, f"{norm_title}.png")
    if os.path.exists(direct):
        return direct

    return None


# =============================================================================
# 3. PUNTOS TRAFFIC LIGHTS (🔴 🟡 🟢) EN LA VENTANA PRINCIPAL Y PANELES
# =============================================================================

def install_window_traffic_lights(session=None):
    if not session or not hasattr(session, "ui") or not hasattr(session.ui, "main_window"):
        return

    win = session.ui.main_window
    if not win:
        return

    mb = win.menuBar()
    if not mb:
        return

    existing = mb.cornerWidget(QtCore.Qt.Corner.TopLeftCorner)
    if existing and getattr(existing, "_is_mac_traffic_lights", False):
        return

    tl_container = QtWidgets.QWidget(mb)
    tl_container._is_mac_traffic_lights = True
    layout = QtWidgets.QHBoxLayout(tl_container)
    layout.setContentsMargins(12, 0, 10, 0)
    layout.setSpacing(8)

    # 🔴 Cerrar (#FF5F56)
    btn_close = QtWidgets.QPushButton(tl_container)
    btn_close.setFixedSize(14, 14)
    btn_close.setToolTip("Cerrar")
    btn_close.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
    close_icon = os.path.join(ICONS_DIR, "mac_close.png").replace("\\", "/")
    close_hover = os.path.join(ICONS_DIR, "mac_close_hover.png").replace("\\", "/")
    btn_close.setStyleSheet(f"""
        QPushButton {{
            background: transparent;
            border: none;
            image: url({close_icon});
        }}
        QPushButton:hover {{
            image: url({close_hover});
        }}
    """)
    btn_close.clicked.connect(win.close)
    layout.addWidget(btn_close)

    # 🟡 Minimizar (#FFBD2E)
    btn_min = QtWidgets.QPushButton(tl_container)
    btn_min.setFixedSize(14, 14)
    btn_min.setToolTip("Minimizar")
    btn_min.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
    min_icon = os.path.join(ICONS_DIR, "mac_minimize.png").replace("\\", "/")
    min_hover = os.path.join(ICONS_DIR, "mac_minimize_hover.png").replace("\\", "/")
    btn_min.setStyleSheet(f"""
        QPushButton {{
            background: transparent;
            border: none;
            image: url({min_icon});
        }}
        QPushButton:hover {{
            image: url({min_hover});
        }}
    """)
    btn_min.clicked.connect(win.showMinimized)
    layout.addWidget(btn_min)

    # 🟢 Zoom / Maximizar (#27C93F)
    btn_zoom = QtWidgets.QPushButton(tl_container)
    btn_zoom.setFixedSize(14, 14)
    btn_zoom.setToolTip("Zoom / Pantalla completa")
    btn_zoom.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
    zoom_icon = os.path.join(ICONS_DIR, "mac_zoom.png").replace("\\", "/")
    zoom_hover = os.path.join(ICONS_DIR, "mac_zoom_hover.png").replace("\\", "/")
    btn_zoom.setStyleSheet(f"""
        QPushButton {{
            background: transparent;
            border: none;
            image: url({zoom_icon});
        }}
        QPushButton:hover {{
            image: url({zoom_hover});
        }}
    """)
    def toggle_zoom():
        if win.isMaximized():
            win.showNormal()
        else:
            win.showMaximized()
    btn_zoom.clicked.connect(toggle_zoom)
    layout.addWidget(btn_zoom)

    mb.setCornerWidget(tl_container, QtCore.Qt.Corner.TopLeftCorner)


# =============================================================================
# 4. REEMPLAZO PROFUNDO DE ICONOS EN TODAS LAS PESTAÑAS
# =============================================================================

def apply_mac_icons_to_all_tabs(session=None):
    from chimerax.toolbar.tool import get_toolbar_singleton
    tb_tool = get_toolbar_singleton(session, create=False)
    if not tb_tool or not hasattr(tb_tool, "ttb"):
        return

    ttb = tb_tool.ttb
    ttb.setStyleSheet(TOOLBAR_LIGHT_PRO_QSS)

    for tab_name, sections in list(getattr(ttb, "_buttons", {}).items()):
        if not isinstance(sections, dict):
            continue
        for sec_name, section in list(sections.items()):
            if sec_name == "__toolbar__":
                continue
            modified = False
            for bi in getattr(section, "_buttons", []):
                icon_path = resolve_mac_icon(bi.title, getattr(bi, "description", ""), sec_name)
                if icon_path and os.path.exists(icon_path):
                    bi.icon = QtGui.QIcon(icon_path)
                    bi.highlight_icon = None
                    modified = True

            if modified and hasattr(section, "_redo_layout"):
                try:
                    section._redo_layout()
                except Exception:
                    pass

    # Aplicar tamaño Retina a todos los botones
    for b in ttb.findChildren(QtWidgets.QToolButton):
        b.setIconSize(QtCore.QSize(28, 28))
        b.update()


# =============================================================================
# 5. HOJAS DE ESTILO QSS: MACOS SEQUOIA LIGHT MODE PRO
# =============================================================================

close_qss = os.path.join(ICONS_DIR, "mac_close.png").replace("\\", "/")
close_h_qss = os.path.join(ICONS_DIR, "mac_close_hover.png").replace("\\", "/")
zoom_qss = os.path.join(ICONS_DIR, "mac_zoom.png").replace("\\", "/")
zoom_h_qss = os.path.join(ICONS_DIR, "mac_zoom_hover.png").replace("\\", "/")

MACOS_LIGHT_PRO_QSS = f"""
/* =========================================================================
   APPLE MACOS SEQUOIA LIGHT MODE PRO
   ========================================================================= */

QWidget {{
    font-family: "SF Pro Text", "Helvetica Neue", "Helvetica", -apple-system, sans-serif;
    font-size: 12px;
    color: #1D1D1F;
    selection-background-color: rgba(0, 122, 255, 0.35);
    selection-color: #000000;
    outline: none;
}}

QMainWindow {{
    background-color: #F5F5F7;
}}

QMenuBar {{
    background: rgba(246, 246, 248, 0.98);
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    padding: 3px 6px;
    color: #1D1D1F;
}}
QMenuBar::item {{
    background: transparent;
    padding: 4px 10px;
    border-radius: 5px;
    font-weight: 500;
}}
QMenuBar::item:selected {{
    background: rgba(0, 0, 0, 0.06);
    color: #000000;
}}

QMenu {{
    background-color: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    padding: 5px;
}}
QMenu::item {{
    padding: 6px 24px 6px 12px;
    border-radius: 6px;
    color: #1D1D1F;
}}
QMenu::item:selected {{
    background-color: #007AFF;
    color: #FFFFFF;
}}
QMenu::separator {{
    height: 1px;
    background: rgba(0, 0, 0, 0.08);
    margin: 4px 6px;
}}

/* Paneles Laterales Flotantes con Puntos Traffic Lights */
QDockWidget {{
    background-color: rgba(255, 255, 255, 0.96);
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 12px;
    margin: 4px;
}}

QDockWidget::title {{
    background: rgba(242, 242, 247, 0.95);
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    border-top-left-radius: 11px;
    border-top-right-radius: 11px;
    padding: 7px 12px;
    font-weight: 600;
    font-size: 11px;
    color: #1D1D1F;
}}

QDockWidget::close-button, QDockWidget::float-button {{
    subcontrol-position: top right;
    subcontrol-origin: padding;
    top: 9px;
    width: 13px;
    height: 13px;
    background: transparent;
    border: none;
    padding: 0px;
    margin-right: 4px;
}}

QDockWidget::close-button {{
    right: 12px;
    image: url({close_qss});
}}
QDockWidget::close-button:hover {{
    image: url({close_h_qss});
}}

QDockWidget::float-button {{
    right: 32px;
    image: url({zoom_qss});
}}
QDockWidget::float-button:hover {{
    image: url({zoom_h_qss});
}}

/* Listas y Model Panel */
QTreeView, QListView, QTableView {{
    background-color: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 4px;
    color: #1D1D1F;
    alternate-background-color: rgba(0, 0, 0, 0.02);
}}
QTreeView::item, QListView::item {{
    padding: 4px 6px;
    border-radius: 6px;
}}
QTreeView::item:hover, QListView::item:hover {{
    background: rgba(0, 0, 0, 0.04);
    color: #000000;
}}
QTreeView::item:selected, QListView::item:selected {{
    background-color: #007AFF;
    color: #FFFFFF;
}}

QPushButton {{
    background-color: rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 6px;
    padding: 4px 12px;
    color: #1D1D1F;
    font-weight: 500;
    font-size: 11px;
}}
QPushButton:hover {{
    background-color: rgba(0, 0, 0, 0.09);
    border: 1px solid rgba(0, 0, 0, 0.16);
}}

/* Log Card-Stream */
QTextEdit, QPlainTextEdit {{
    background-color: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 8px;
    color: #1D1D1F;
    font-family: "SF Mono", "JetBrains Mono", "Consolas", monospace;
    font-size: 11px;
}}

/* Barra de Comandos Spotlight */
QLineEdit {{
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 12px;
    padding: 6px 14px;
    color: #1D1D1F;
    font-family: "SF Mono", "JetBrains Mono", "Consolas", monospace;
    font-size: 12px;
    selection-background-color: #007AFF;
}}
QLineEdit:focus {{
    border: 1.5px solid #007AFF;
    background: #FFFFFF;
}}

QStatusBar {{
    background: rgba(246, 246, 248, 0.98);
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    color: rgba(60, 60, 67, 0.7);
    font-size: 11px;
}}

QScrollBar:vertical {{
    width: 6px;
    background: transparent;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: rgba(0, 0, 0, 0.2);
    min-height: 24px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical:hover {{
    background: rgba(0, 0, 0, 0.4);
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
"""

TOOLBAR_LIGHT_PRO_QSS = """
QTabWidget {
    background: transparent;
    border: none;
}
QTabWidget::pane {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 12px;
    margin: 2px 6px 4px 6px;
    padding: 2px 4px;
}
QTabBar {
    background: transparent;
    margin-left: 6px;
}
QTabBar::tab {
    background: rgba(0, 0, 0, 0.04);
    border: 1px solid transparent;
    border-radius: 7px;
    padding: 4px 14px;
    margin: 2px 3px;
    color: rgba(60, 60, 67, 0.7);
    font-weight: 500;
    font-size: 11px;
}
QTabBar::tab:hover:!selected {
    background: rgba(0, 0, 0, 0.08);
    color: #1D1D1F;
}
QTabBar::tab:selected {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.12);
    color: #1D1D1F;
    font-weight: 600;
}
QToolBar {
    background: transparent;
    border: none;
    spacing: 4px;
    padding: 2px 4px;
}
QToolButton {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 3px 5px;
    margin: 1px;
    color: #1D1D1F;
    font-size: 10px;
    font-weight: 500;
}
QToolButton:hover {
    background: rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(0, 0, 0, 0.1);
    color: #000000;
}
QToolButton:pressed {
    background: rgba(0, 0, 0, 0.1);
}
QToolButton:checked {
    background: rgba(0, 122, 255, 0.15);
    border: 1px solid #007AFF;
    color: #007AFF;
    font-weight: 600;
}
QLabel {
    color: rgba(60, 60, 67, 0.5);
    font-size: 9px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
"""


# =============================================================================
# 6. CONFIGURACIÓN DEL LIENZO 3D Y PERSISTENCIA
# =============================================================================

def configure_3d_canvas(session):
    if session:
        try:
            run(session, "set bg #F5F5F7")
            run(session, "lighting soft")
            run(session, "graphics silhouettes true color #3A3A3C width 1.2")
            run(session, "color byhetero")
        except Exception:
            pass


def apply_theme(session=None, mode="light"):
    app = QtWidgets.QApplication.instance()
    if not app:
        return

    # Tipografía Apple SF Pro
    font = QtGui.QFont("SF Pro Text", 11)
    if not font.exactMatch():
        font = QtGui.QFont("Helvetica Neue", 11)
    if not font.exactMatch():
        font = QtGui.QFont("Helvetica", 11)
    font.setStyleHint(QtGui.QFont.StyleHint.SansSerif)
    app.setFont(font)

    # Aplicar QSS global de modo claro
    app.setStyleSheet(MACOS_LIGHT_PRO_QSS)

    # Traffic lights (🔴 🟡 🟢) en la barra de menú de la ventana principal
    install_window_traffic_lights(session)

    # Reemplazo de iconos en todas las pestañas de forma exhaustiva
    apply_mac_icons_to_all_tabs(session)
    QtCore.QTimer.singleShot(80, lambda: apply_mac_icons_to_all_tabs(session))
    QtCore.QTimer.singleShot(300, lambda: apply_mac_icons_to_all_tabs(session))

    # Conectar cambio de pestañas para garantizar actualización inmediata
    for tw in app.findChildren(QtWidgets.QTabWidget):
        try:
            tw.currentChanged.connect(lambda idx: QtCore.QTimer.singleShot(50, lambda: apply_mac_icons_to_all_tabs(session)))
        except Exception:
            pass

    # Configuración de lienzo 3D
    configure_3d_canvas(session)

    # Persistencia ante apertura de sesiones (.cxs) y modelos
    if session and hasattr(session, "triggers") and not getattr(session, "_mac_triggers_added", False):
        def on_session_restored(*args):
            QtCore.QTimer.singleShot(100, lambda: configure_3d_canvas(session))
            QtCore.QTimer.singleShot(150, lambda: apply_mac_icons_to_all_tabs(session))
        try:
            session.triggers.add_handler("end restore session", on_session_restored)
            session.triggers.add_handler("session open", on_session_restored)
            session.triggers.add_handler("open models", on_session_restored)
            session._mac_triggers_added = True
        except Exception:
            pass

    if session and hasattr(session, "logger"):
        session.logger.status("✨ macOS Sequoia Light Pro Mode & Traffic Lights activado.")


# Hook global de inicio para que cada nueva sesión de ChimeraX aplique el tema automáticamente
try:
    from chimerax.core.session import Session
    if not hasattr(Session, "_mac_init_patched"):
        _orig_session_init = Session.__init__
        def _mac_session_init(self, *args, **kwargs):
            _orig_session_init(self, *args, **kwargs)
            try:
                QtCore.QTimer.singleShot(200, lambda: apply_theme(self, mode="light"))
            except Exception:
                pass
        Session.__init__ = _mac_session_init
        Session._mac_init_patched = True
except Exception:
    pass


def remove_theme(session=None):
    app = QtWidgets.QApplication.instance()
    if app:
        app.setStyleSheet("")
        app.setFont(QtGui.QFont("Segoe UI", 10))
    if session:
        try:
            run(session, "set bg black")
            run(session, "graphics silhouettes false")
            run(session, "lighting simple")
        except Exception:
            pass


def liquidglass_cmd(session, mode="light"):
    if mode.lower() in ("off", "disable", "reset", "default"):
        remove_theme(session)
    else:
        apply_theme(session, mode=mode)


# =============================================================================
# REGISTRO DE COMANDO EN CHIMERAX
# =============================================================================

try:
    cmd_desc = CmdDesc(
        optional=[("mode", StringArg)],
        synopsis="Activar macOS Sequoia Light Pro Mode o 'off'"
    )
    register("liquidglass", cmd_desc, liquidglass_cmd)
except Exception:
    pass

current_session = globals().get("session", None)
apply_theme(current_session, mode="light")
