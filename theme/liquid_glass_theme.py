import os
import sys
import gc
import ctypes
from functools import lru_cache
from Qt import QtWidgets, QtGui, QtCore
from chimerax.core.commands import register, CmdDesc, StringArg, run
from chimerax.core.colors import set_default_color_scheme
try:
    gc.set_threshold(50000, 20, 20)
except Exception:
    pass
try:
    QtGui.QPixmapCache.setCacheLimit(65536)
except Exception:
    pass
_CURRENT_MODE = globals().get("_CURRENT_MODE", "light")
_THEME_PALETTES = {
    "light": {
        "win_bg": "#F5F5F7",
        "card_bg": "#FFFFFF",
        "alt_bg": "#F9FAFC",
        "header_bg": "#F0F3F9",
        "border": "#D5DFEE",
        "border_soft": "#E2E8F2",
        "sep_color": "#BACBE6",
        "text": "#1D1D1F",
        "text_hover": "#000000",
        "text_muted": "rgba(60, 60, 67, 0.65)",
        "btn_bg": "#F4F6FB",
        "btn_hover": "#E8EEF8",
        "btn_pressed": "#DCE5F4",
        "menu_btn_bg": "#FFFFFF",
        "tab_unselected": "rgba(186, 203, 230, 0.22)",
        "tab_hover": "rgba(186, 203, 230, 0.40)",
        "accent": "#007AFF",
        "code_bg": "#F4F7FC",
        "table_th_bg": "#F2F5FA",
        "scroll_thumb": "rgba(142, 158, 184, 0.45)",
        "scroll_hover": "rgba(110, 130, 165, 0.70)",
        "canvas_rgb": (0.961, 0.961, 0.969, 1.0),
        "silhouette_color": "#3A3A3C",
        "dwm_dark": 0,
        "dwm_caption": 0x00F7F5F5,
        "dwm_text": 0x001F1D1D,
        "scheme": "light",
        "qcolor_bg": (255, 255, 255),
    },
    "gray": {
        "win_bg": "#D5DBE5",
        "card_bg": "#E4E8F0",
        "alt_bg": "#DCE1EB",
        "header_bg": "#C8D0DE",
        "border": "#AEB9CC",
        "border_soft": "#B8C3D4",
        "sep_color": "#8FA3C2",
        "text": "#1D1D1F",
        "text_hover": "#000000",
        "text_muted": "rgba(29, 29, 31, 0.68)",
        "btn_bg": "#ECEFF5",
        "btn_hover": "#DAE1ED",
        "btn_pressed": "#CCD5E5",
        "menu_btn_bg": "#EEF1F7",
        "tab_unselected": "rgba(143, 163, 194, 0.25)",
        "tab_hover": "rgba(143, 163, 194, 0.42)",
        "accent": "#0066CC",
        "code_bg": "#DAE0EB",
        "table_th_bg": "#CFD6E3",
        "scroll_thumb": "rgba(100, 116, 145, 0.48)",
        "scroll_hover": "rgba(75, 92, 122, 0.75)",
        "canvas_rgb": (0.835, 0.859, 0.898, 1.0),
        "silhouette_color": "#2C2C2E",
        "dwm_dark": 0,
        "dwm_caption": 0x00E5DBD5,
        "dwm_text": 0x001F1D1D,
        "scheme": "light",
        "qcolor_bg": (228, 232, 240),
    },
    "dark": {
        "win_bg": "#1C1C1E",
        "card_bg": "#2C2C2E",
        "alt_bg": "#242426",
        "header_bg": "#25262B",
        "border": "#3E4047",
        "border_soft": "#36383F",
        "sep_color": "#5E6E8C",
        "text": "#F5F5F7",
        "text_hover": "#FFFFFF",
        "text_muted": "rgba(235, 235, 245, 0.62)",
        "btn_bg": "#383940",
        "btn_hover": "#454750",
        "btn_pressed": "#50535E",
        "menu_btn_bg": "#383940",
        "tab_unselected": "rgba(94, 110, 140, 0.22)",
        "tab_hover": "rgba(94, 110, 140, 0.38)",
        "accent": "#0A84FF",
        "code_bg": "#222327",
        "table_th_bg": "#34353B",
        "scroll_thumb": "rgba(160, 170, 190, 0.38)",
        "scroll_hover": "rgba(190, 200, 220, 0.62)",
        "canvas_rgb": (0.110, 0.110, 0.118, 1.0),
        "silhouette_color": "#E5E5EA",
        "dwm_dark": 1,
        "dwm_caption": 0x001E1C1C,
        "dwm_text": 0x00F7F5F5,
        "scheme": "dark",
        "qcolor_bg": (44, 44, 46),
    },
}
def normalize_mode(mode):
    if not mode:
        return "light"
    m = mode.lower().strip()
    if m in ("gray", "grey", "gris", "grisaceo"):
        return "gray"
    if m in ("dark", "oscuro", "night"):
        return "dark"
    return "light"
def get_current_mode():
    app = QtWidgets.QApplication.instance()
    if app and hasattr(app, "_mac_current_mode"):
        return app._mac_current_mode
    return _CURRENT_MODE
def set_current_mode(mode):
    global _CURRENT_MODE
    norm = normalize_mode(mode)
    _CURRENT_MODE = norm
    app = QtWidgets.QApplication.instance()
    if app:
        app._mac_current_mode = norm
    return norm
def get_palette_dict(mode=None):
    return _THEME_PALETTES[normalize_mode(mode or get_current_mode())]
try:
    set_default_color_scheme(get_palette_dict()["scheme"])
except Exception:
    pass
_CANDIDATE_ICON_DIRS = (
    r"C:\Users\Parfion\Downloads\chimerax_mac_icons",
    os.path.expanduser("~/Downloads/chimerax_mac_icons"),
    os.path.expanduser("~/chimerax_start/icons"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons") if "__file__" in globals() else "",
)
ICONS_DIR = next((d for d in _CANDIDATE_ICON_DIRS if d and os.path.exists(d)), _CANDIDATE_ICON_DIRS[0])
_EXISTING_ICONS = frozenset(os.listdir(ICONS_DIR)) if os.path.exists(ICONS_DIR) else frozenset()
_QICON_CACHE = {}
_SUBPATH_BASENAME_CACHE = {}
def get_cached_qicon(file_path):
    icon = _QICON_CACHE.get(file_path)
    if icon is None and file_path and os.path.exists(file_path):
        icon = QtGui.QIcon(file_path)
        _QICON_CACHE[file_path] = icon
    return icon
try:
    from chimerax.core.toolshed.info import BundleInfo
    if not hasattr(BundleInfo, "_mac_patched"):
        _orig_get_path = BundleInfo.get_path
        def _mac_get_path(self, subpath):
            if subpath:
                cached = _SUBPATH_BASENAME_CACHE.get(subpath)
                if cached is None:
                    fname = os.path.basename(subpath)
                    cached = os.path.join(ICONS_DIR, fname) if fname in _EXISTING_ICONS else False
                    _SUBPATH_BASENAME_CACHE[subpath] = cached
                if cached:
                    return cached
            return _orig_get_path(self, subpath)
        BundleInfo.get_path = _mac_get_path
        BundleInfo._mac_patched = True
except Exception:
    pass
try:
    import chimerax.ui.widgets.tabbedtoolbar as _ttb_mod
    if not getattr(_ttb_mod, "_mac_split_cached", False):
        _ttb_mod.split_title = lru_cache(maxsize=512)(_ttb_mod.split_title)
        _ttb_mod._mac_split_cached = True
except Exception:
    pass
_RAW_MAP = {
    ("File", "Open"): "open-in-app.png",
    ("File", "Recent"): "recentfiles.png",
    ("File", "Save"): "content-save.png",
    ("File", "Close"): "close-box.png",
    ("File", "Exit"): "exit.png",
    ("Undo", "Undo"): "undo-variant.png",
    ("Undo", "Redo"): "redo-variant.png",
    ("Images", "Snapshot"): "camera.png",
    ("Images", "Spin movie"): "video.png",
    ("Viewing", "Virtual reality"): "vr.png",
    ("Viewing", "OpenXR"): "xr.png",
    ("Selection", "Inspect"): "magnifying-glass.png",
    ("Atoms", "Show"): "atomshow.png",
    ("Atoms", "Hide"): "atomhide.png",
    ("Cartoons", "Show"): "ribshow.png",
    ("Cartoons", "Hide"): "ribhide.png",
    ("Surfaces", "Show"): "surfshow.png",
    ("Surfaces", "Hide"): "surfhide.png",
    ("Styles", "Stick"): "stick.png",
    ("Styles", "Sphere"): "sphere.png",
    ("Styles", "Ball & stick"): "ball_stick.png",
    ("Styles", "Plain"): "nuc-atoms.png",
    ("Styles", "Filled"): "nuc-fill.png",
    ("Styles", "Tube/\nSlab"): "nuc-box.png",
    ("Styles", "Ladder"): "nuc-ladder.png",
    ("Styles", "Slab"): "nuc-slab.png",
    ("Styles", "Tube/\nEllipsoid"): "nuc-elli.png",
    ("Styles", "Tube/\nMuffler"): "nuc-muff.png",
    ("Styles", "Stubs"): "nuc-stubs.png",
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
    ("Background", "White"): "whitebg.png",
    ("Background", "Gray"): "graybg.png",
    ("Background", "Black"): "blackbg.png",
    ("Lighting", "Simple"): "simplelight.png",
    ("Lighting", "Soft"): "softlight.png",
    ("Lighting", "Full"): "fulllight.png",
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
    ("Rendering Modes", "Raycasting"): "raycasting.png",
    ("File", "Open DICOM"): "opendicom.png",
    ("Color", "Airways"): "airways.png",
    ("Color", "Chest CT"): "chest.png",
    ("Color", "Brain CT"): "brain.png",
    ("Color", "Default thresholds"): "initialcurve.png",
    ("Graphics", "Step 1"): "step1.png",
    ("Graphics", "Step 2"): "step2.png",
    ("Mouse Mode", "Crop"): "crop.png",
    ("Mouse Mode", "Move planes"): "moveplanes.png",
    ("Mouse Mode", "Tilt slab"): "rotateslab.png",
    ("Mouse Mode", "Tape"): "tape.png",
    ("Mouse Mode", "Windowing"): "windowing.png",
    ("Segmentation Controls", "Toggle Mouse Modes"): "mouse.png",
    ("Segmentation Controls", "Toggle Hand Modes"): "right_controller.png",
    ("Place markers", "Maximum"): "mark_maximum.png",
    ("Place markers", "Plane"): "mark_plane.png",
    ("Place markers", "Surface"): "mark_surface.png",
    ("Place markers", "Center"): "mark_center.png",
    ("Place markers", "Point"): "mark_point.png",
    ("Adjust markers", "Link"): "mark_link.png",
    ("Adjust markers", "Move"): "mark_move.png",
    ("Adjust markers", "Resize"): "mark_resize.png",
    ("Adjust markers", "Delete"): "mark_delete.png",
    ("Movement", "Select"): "select.png",
    ("Movement", "Rotate"): "rotate.png",
    ("Movement", "Translate"): "translate.png",
    ("Movement", "Zoom"): "zoom.png",
    ("Movement", "Move model"): "move_picked_model.png",
    ("Movement", "Rotate model"): "rotatesel.png",
    ("Movement", "Drag model"): "drag_model.png",
    ("Movement", "Move atoms"): "move_atoms.png",
    ("Movement", "Rotate atoms"): "rotate_atoms.png",
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
_FAST_SECTION_TITLE_MAP = {}
_FAST_TITLE_MAP = {}
for (sec, title), fname in _RAW_MAP.items():
    if fname in _EXISTING_ICONS:
        p = os.path.join(ICONS_DIR, fname)
        _FAST_SECTION_TITLE_MAP[(sec.lower().strip(), title.lower().strip())] = p
        if (sec, title) != ("Subregions", "Full"):
            _FAST_TITLE_MAP[title.lower().strip()] = p
_SPECIAL_MAP = {
    ("markers", "move"): "mark_move.png",
    ("", "drag model"): "drag_model.png",
    ("", "move model"): "move_picked_model.png",
    ("", "inspect"): "magnifying-glass.png",
    ("", "zoom"): "zoom.png",
}
for (tb, t), fn in _SPECIAL_MAP.items():
    if fn in _EXISTING_ICONS:
        p = os.path.join(ICONS_DIR, fn)
        _FAST_SECTION_TITLE_MAP[(tb, t)] = p
        if not tb:
            _FAST_TITLE_MAP[t] = p
def resolve_mac_icon(title, description="", section="", tab=""):
    t_key = title.lower().strip()
    sec_key = section.lower().strip()
    tab_key = tab.lower().strip()
    if tab_key == "markers" and t_key == "move":
        return _FAST_SECTION_TITLE_MAP.get(("markers", "move"))
    res = _FAST_SECTION_TITLE_MAP.get((sec_key, t_key))
    if res:
        return res
    res = _FAST_TITLE_MAP.get(t_key)
    if res:
        return res
    direct_name = f"{t_key}.png"
    if direct_name in _EXISTING_ICONS:
        return os.path.join(ICONS_DIR, direct_name)
    return None
def apply_win11_rounded_corners(widget):
    try:
        pal = get_palette_dict()
        hwnd = int(widget.winId())
        dwm = ctypes.windll.dwmapi.DwmSetWindowAttribute
        pref = ctypes.c_int(2)
        dwm(hwnd, 33, ctypes.byref(pref), ctypes.sizeof(pref))
        dark = ctypes.c_int(pal["dwm_dark"])
        dwm(hwnd, 20, ctypes.byref(dark), ctypes.sizeof(dark))
        cap_color = ctypes.c_int(pal["dwm_caption"])
        dwm(hwnd, 35, ctypes.byref(cap_color), ctypes.sizeof(cap_color))
        txt_color = ctypes.c_int(pal["dwm_text"])
        dwm(hwnd, 36, ctypes.byref(txt_color), ctypes.sizeof(txt_color))
    except Exception:
        pass
class MacGlobalWindowPolishFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        try:
            if event.type() == QtCore.QEvent.Type.Show and isinstance(obj, QtWidgets.QWidget):
                if obj.isWindow() and getattr(obj, "_mac_dwm_mode", None) != _CURRENT_MODE:
                    obj._mac_dwm_mode = _CURRENT_MODE
                    QtCore.QTimer.singleShot(10, lambda w=obj: apply_win11_rounded_corners(w))
        except Exception:
            pass
        return False
class MacTrafficLightButton(QtWidgets.QAbstractButton):
    def __init__(self, fill_color, border_color, hover_color, glyph="", diameter=12, parent=None):
        super().__init__(parent)
        self._fill = QtGui.QColor(fill_color)
        self._border = QtGui.QColor(border_color)
        self._hover = QtGui.QColor(hover_color)
        self._glyph = glyph
        self._diameter = diameter
        self.setFixedSize(diameter, diameter)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover, True)
    def sizeHint(self):
        return QtCore.QSize(self._diameter, self._diameter)
    def enterEvent(self, event):
        self.update()
        super().enterEvent(event)
    def leaveEvent(self, event):
        self.update()
        super().leaveEvent(event)
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        hovered = self.underMouse()
        d = float(self._diameter)
        rect = QtCore.QRectF(0.75, 0.75, d - 1.5, d - 1.5)
        painter.setBrush(QtGui.QBrush(self._hover if hovered else self._fill))
        pen = QtGui.QPen(self._border)
        pen.setWidthF(1.0)
        painter.setPen(pen)
        painter.drawEllipse(rect)
        if hovered and self._glyph:
            gpen = QtGui.QPen(QtGui.QColor(29, 29, 31, 195))
            gpen.setWidthF(1.35)
            gpen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(gpen)
            c = d / 2.0
            r = d * 0.21
            if self._glyph == "close":
                painter.drawLine(QtCore.QPointF(c - r, c - r), QtCore.QPointF(c + r, c + r))
                painter.drawLine(QtCore.QPointF(c + r, c - r), QtCore.QPointF(c - r, c + r))
            elif self._glyph == "min":
                painter.drawLine(QtCore.QPointF(c - r * 1.15, c), QtCore.QPointF(c + r * 1.15, c))
            elif self._glyph == "zoom":
                painter.drawLine(QtCore.QPointF(c - r * 1.1, c), QtCore.QPointF(c + r * 1.1, c))
                painter.drawLine(QtCore.QPointF(c, c - r * 1.1), QtCore.QPointF(c, c + r * 1.1))
        painter.end()
class MacWindowResizeFilter(QtCore.QObject):
    def __init__(self, window, margin=6):
        super().__init__(window)
        self.win = window
        self.margin = margin
    def eventFilter(self, obj, event):
        if obj is not self.win:
            return False
        ev_type = event.type()
        if ev_type == QtCore.QEvent.Type.MouseMove:
            if not self.win.isMaximized():
                edge = self._get_edge(event.pos())
                self._update_cursor(edge)
        elif ev_type == QtCore.QEvent.Type.MouseButtonPress:
            if event.button() == QtCore.Qt.MouseButton.LeftButton and not self.win.isMaximized():
                edge = self._get_edge(event.pos())
                if edge:
                    wh = self.win.windowHandle()
                    if wh and hasattr(wh, "startSystemResize"):
                        wh.startSystemResize(edge)
                        return True
        return False
    def _get_edge(self, pos):
        w = self.win.width()
        h = self.win.height()
        m = self.margin
        edges = 0
        px = pos.x()
        py = pos.y()
        if px <= m:
            edges |= QtCore.Qt.Edge.LeftEdge.value
        elif px >= w - m:
            edges |= QtCore.Qt.Edge.RightEdge.value
        if py <= m:
            edges |= QtCore.Qt.Edge.TopEdge.value
        elif py >= h - m:
            edges |= QtCore.Qt.Edge.BottomEdge.value
        return QtCore.Qt.Edge(edges) if edges else None
    def _update_cursor(self, edge):
        if not edge:
            self.win.unsetCursor()
            return
        is_l = bool(edge & QtCore.Qt.Edge.LeftEdge)
        is_r = bool(edge & QtCore.Qt.Edge.RightEdge)
        is_t = bool(edge & QtCore.Qt.Edge.TopEdge)
        is_b = bool(edge & QtCore.Qt.Edge.BottomEdge)
        if (is_t and is_l) or (is_b and is_r):
            self.win.setCursor(QtCore.Qt.CursorShape.SizeFDiagCursor)
        elif (is_t and is_r) or (is_b and is_l):
            self.win.setCursor(QtCore.Qt.CursorShape.SizeBDiagCursor)
        elif is_l or is_r:
            self.win.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
        elif is_t or is_b:
            self.win.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
class MacWindowHeader(QtWidgets.QWidget):
    def __init__(self, main_window, session_getter=None):
        super().__init__(main_window)
        self.win = main_window
        self._session_getter = session_getter
        self.setFixedHeight(32)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(8)
        btn_close = MacTrafficLightButton("#FF5F56", "#E0443E", "#FF3B30", "close", 12, self)
        btn_close.clicked.connect(self.win.close)
        layout.addWidget(btn_close)
        btn_min = MacTrafficLightButton("#FFBD2E", "#DEA123", "#FF9500", "min", 12, self)
        btn_min.clicked.connect(self.win.showMinimized)
        layout.addWidget(btn_min)
        btn_zoom = MacTrafficLightButton("#27C93F", "#1AAB29", "#34C759", "zoom", 12, self)
        def toggle_zoom():
            if self.win.isMaximized():
                self.win.showNormal()
            else:
                self.win.showMaximized()
        btn_zoom.clicked.connect(toggle_zoom)
        layout.addWidget(btn_zoom)
        layout.addSpacing(14)
        self.title_lbl = QtWidgets.QLabel("ChimeraX", self)
        layout.addWidget(self.title_lbl)
        layout.addStretch()
        self._mode_btns = {}
        for mode_key, label_text in (("light", "Claro"), ("gray", "Gris"), ("dark", "Oscuro")):
            mb = QtWidgets.QPushButton(label_text, self)
            mb.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            mb.setFixedHeight(20)
            mb.clicked.connect(lambda checked=False, m=mode_key: apply_theme(self._session_getter() if self._session_getter else None, mode=m))
            layout.addWidget(mb)
            self._mode_btns[mode_key] = mb
        self.refresh_theme()
    def refresh_theme(self):
        pal = get_palette_dict()
        self.setStyleSheet(f"background-color: {pal['win_bg']}; border: none;")
        self.title_lbl.setStyleSheet(f"color: {pal['text']}; font-size: 13px; font-weight: 600; background: transparent; border: none;")
        for m_key, btn in self._mode_btns.items():
            if m_key == get_current_mode():
                btn.setStyleSheet(
                    f"QPushButton {{ background-color: {pal['accent']}; color: #FFFFFF; border: none; border-radius: 9px; padding: 1px 10px; font-size: 10px; font-weight: 600; }}"
                )
            else:
                btn.setStyleSheet(
                    f"QPushButton {{ background-color: {pal['btn_bg']}; color: {pal['text']}; border: 1px solid {pal['border']}; border-radius: 9px; padding: 1px 10px; font-size: 10px; font-weight: 500; }}"
                    f"QPushButton:hover {{ background-color: {pal['btn_hover']}; }}"
                )
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            wh = self.win.windowHandle()
            if wh and hasattr(wh, "startSystemMove"):
                wh.startSystemMove()
    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.win.isMaximized():
                self.win.showNormal()
            else:
                self.win.showMaximized()
class MacDockTitleBar(QtWidgets.QWidget):
    def __init__(self, dock_widget):
        super().__init__(dock_widget)
        self.dock = dock_widget
        self.setFixedHeight(30)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(14, 4, 14, 2)
        layout.setSpacing(6)
        btn_close = MacTrafficLightButton("#FF5F56", "#E0443E", "#FF3B30", "close", 12, self)
        btn_close.clicked.connect(self.dock.close)
        layout.addWidget(btn_close)
        btn_min = MacTrafficLightButton("#FFBD2E", "#DEA123", "#FF9500", "min", 12, self)
        def toggle_min():
            w = self.dock.widget()
            if w:
                w.setVisible(not w.isVisible())
        btn_min.clicked.connect(toggle_min)
        layout.addWidget(btn_min)
        btn_zoom = MacTrafficLightButton("#27C93F", "#1AAB29", "#34C759", "zoom", 12, self)
        def toggle_float():
            self.dock.setFloating(not self.dock.isFloating())
            if self.dock.isFloating():
                apply_win11_rounded_corners(self.dock)
        btn_zoom.clicked.connect(toggle_float)
        layout.addWidget(btn_zoom)
        self.label = QtWidgets.QLabel(self.dock.windowTitle(), self)
        layout.addWidget(self.label)
        layout.addStretch()
        self.dock.windowTitleChanged.connect(self.label.setText)
        self.refresh_theme()
    def refresh_theme(self):
        pal = get_palette_dict()
        self.label.setStyleSheet(f"color: {pal['text']}; font-size: 11px; font-weight: 600; padding-left: 6px; background: transparent; border: none;")
        self.update()
    def paintEvent(self, event):
        pal = get_palette_dict()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        w = float(self.width())
        h = float(self.height())
        r = 12.0
        left = 4.5
        right = w - 4.5
        top = 3.5
        bottom = h
        path = QtGui.QPainterPath()
        path.moveTo(left, bottom)
        path.lineTo(left, top + r)
        path.arcTo(QtCore.QRectF(left, top, 2.0 * r, 2.0 * r), 180.0, -90.0)
        path.lineTo(right - r, top)
        path.arcTo(QtCore.QRectF(right - 2.0 * r, top, 2.0 * r, 2.0 * r), 90.0, -90.0)
        path.lineTo(right, bottom)
        path.closeSubpath()
        painter.fillPath(path, QtGui.QColor(pal["header_bg"]))
        pen = QtGui.QPen(QtGui.QColor(pal["border"]))
        pen.setWidthF(1.0)
        painter.setPen(pen)
        painter.drawPath(path)
        painter.end()
_HIDDEN_TITLE_DOCKS = frozenset(("Toolbar", "Command Line Interface", ""))
def style_dock_content_card(dw, is_hidden_title=False):
    w = dw.widget()
    if not w:
        return
    pal = get_palette_dict()
    w.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
    lay = w.layout()
    if is_hidden_title:
        title = dw.windowTitle().strip()
        if title == "Command Line Interface":
            w.setObjectName("MacCliCard")
            w.setStyleSheet(f"QWidget#MacCliCard {{ background-color: {pal['win_bg']}; border: none; }}")
            if lay:
                lay.setContentsMargins(10, 4, 10, 4)
                lay.setSpacing(8)
        return
    w.setObjectName("MacDockCard")
    w.setStyleSheet(
        f"QWidget#MacDockCard {{"
        f" background-color: {pal['card_bg']};"
        f" border-left: 1px solid {pal['border']};"
        f" border-right: 1px solid {pal['border']};"
        f" border-bottom: 1px solid {pal['border']};"
        f" border-bottom-left-radius: 12px;"
        f" border-bottom-right-radius: 12px;"
        f" margin-left: 4px;"
        f" margin-right: 4px;"
        f" margin-bottom: 4px;"
        f"}}"
    )
    if lay:
        lay.setContentsMargins(8, 6, 8, 8)
    for sa in w.findChildren(QtWidgets.QScrollArea):
        sa.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
def install_dock_traffic_lights(session=None):
    if not session or not hasattr(session, "ui") or not hasattr(session.ui, "main_window"):
        return
    win = session.ui.main_window
    if not win:
        return
    for dw in win.findChildren(QtWidgets.QDockWidget):
        title = dw.windowTitle().strip()
        existing_tb = dw.titleBarWidget()
        if title in _HIDDEN_TITLE_DOCKS:
            if existing_tb is None or type(existing_tb).__name__ == "MacDockTitleBar":
                empty = QtWidgets.QWidget(dw)
                empty.setFixedHeight(0)
                dw.setTitleBarWidget(empty)
            style_dock_content_card(dw, is_hidden_title=True)
            continue
        if existing_tb is not None and type(existing_tb).__name__ != "MacDockTitleBar" and existing_tb.height() == 0:
            style_dock_content_card(dw, is_hidden_title=True)
            continue
        if True:
            title_bar = MacDockTitleBar(dw)
            dw.setTitleBarWidget(title_bar)
            dw._mac_dock_styled = True
            dw._mac_dock_ver = 4
        else:
            if hasattr(existing_tb, "refresh_theme"):
                existing_tb.refresh_theme()
        style_dock_content_card(dw, is_hidden_title=False)
try:
    from chimerax.ui.gui import _Qt
    if getattr(_Qt, "_mac_dock_ver", 0) != 4:
        _orig_qt_init = getattr(_Qt, "_orig_mac_qt_init", _Qt.__init__)
        _Qt._orig_mac_qt_init = _orig_qt_init
        def _mac_qt_init(self, tool_window, title, has_statusbar, hide_title_bar, main_window, close_destroys):
            _orig_qt_init(self, tool_window, title, has_statusbar, hide_title_bar, main_window, close_destroys)
            if hasattr(self, "dock_widget"):
                if not hide_title_bar and title not in _HIDDEN_TITLE_DOCKS:
                    title_bar = MacDockTitleBar(self.dock_widget)
                    self.dock_widget.setTitleBarWidget(title_bar)
                    self.dock_widget._mac_dock_styled = True
                    self.dock_widget._mac_dock_ver = 4
                    QtCore.QTimer.singleShot(50, lambda dw=self.dock_widget: style_dock_content_card(dw, False))
                else:
                    QtCore.QTimer.singleShot(50, lambda dw=self.dock_widget: style_dock_content_card(dw, True))
        _Qt.__init__ = _mac_qt_init
        _Qt._mac_dock_patched = True
        _Qt._mac_dock_ver = 4
except Exception:
    pass
def install_window_traffic_lights(session=None):
    if not session or not hasattr(session, "ui") or not hasattr(session.ui, "main_window"):
        return
    win = session.ui.main_window
    if not win:
        return
    if getattr(win, "_mac_frameless_ver", 0) == 99:
        apply_win11_rounded_corners(win)
        if hasattr(win, "_mac_header_widget") and win._mac_header_widget:
            win._mac_header_widget.refresh_theme()
        return
    flags = win.windowFlags()
    if not (flags & QtCore.Qt.WindowType.FramelessWindowHint):
        win.setWindowFlags(flags | QtCore.Qt.WindowType.FramelessWindowHint)
        win.show()
    apply_win11_rounded_corners(win)
    mb = win.menuBar()
    existing_mw = win.menuWidget()
    if existing_mw and getattr(existing_mw, "_is_mac_top", False):
        for child in existing_mw.findChildren(QtWidgets.QMenuBar):
            mb = child
            break
    if mb:
        mb.setParent(None)
    header = MacWindowHeader(win, session_getter=lambda: session)
    win._mac_header_widget = header
    top_container = QtWidgets.QWidget(win)
    top_container._is_mac_top = True
    vbox = QtWidgets.QVBoxLayout(top_container)
    vbox.setContentsMargins(0, 0, 0, 0)
    vbox.setSpacing(0)
    vbox.addWidget(header)
    if mb:
        vbox.addWidget(mb)
        mb.show()
    win.setMenuWidget(top_container)
    if not hasattr(win, "_mac_resize_filter"):
        resize_filter = MacWindowResizeFilter(win)
        win.installEventFilter(resize_filter)
        win._mac_resize_filter = resize_filter
    win._mac_frameless_installed = True
    win._mac_frameless_ver = 4
def build_main_qss(pal):
    return f"""
QWidget {{
    font-family: "SF Pro Text", "Helvetica Neue", "Segoe UI", -apple-system, sans-serif;
    font-size: 12px;
    color: {pal['text']};
    selection-background-color: {pal['accent']};
    selection-color: #FFFFFF;
    outline: none;
}}
QMainWindow, QDialog, QMessageBox {{
    background-color: {pal['win_bg']};
    color: {pal['text']};
}}
QMainWindow::separator, QSplitter::handle {{
    background-color: transparent;
    width: 2px;
    height: 2px;
    border: none;
}}
QMenuBar {{
    background: {pal['win_bg']};
    border-bottom: 1px solid {pal['border']};
    padding: 2px 10px 4px 10px;
    color: {pal['text']};
}}
QMenuBar::item {{
    background: transparent;
    padding: 4px 10px;
    border-radius: 8px;
    font-weight: 500;
    color: {pal['text']};
}}
QMenuBar::item:selected {{
    background: {pal['tab_hover']};
    color: {pal['text_hover']};
}}
QMenu {{
    background-color: {pal['card_bg']};
    border: 1px solid {pal['border']};
    border-radius: 12px;
    padding: 6px;
    color: {pal['text']};
}}
QMenu::item {{
    padding: 6px 24px 6px 12px;
    border-radius: 8px;
    color: {pal['text']};
}}
QMenu::item:selected {{
    background-color: {pal['accent']};
    color: #FFFFFF;
}}
QMenu::separator {{
    height: 1px;
    background: {pal['border_soft']};
    margin: 4px 8px;
}}
QToolTip {{
    background-color: {pal['card_bg']};
    color: {pal['text']};
    border: 1px solid {pal['border']};
    border-radius: 8px;
    padding: 4px 8px;
}}
QDockWidget {{
    background-color: transparent;
    border: none;
}}
QDockWidget::title {{
    text-align: left;
    background: transparent;
    padding: 4px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}}
QDockWidget::close-button, QDockWidget::float-button {{
    width: 0px;
    height: 0px;
    margin: 0px;
    padding: 0px;
    border: none;
    background: transparent;
}}
QTreeView, QListView, QTableView, QTreeWidget, QTableWidget {{
    background-color: {pal['card_bg']};
    border: 1px solid {pal['border_soft']};
    border-radius: 10px;
    padding: 4px;
    color: {pal['text']};
    alternate-background-color: {pal['alt_bg']};
}}
QHeaderView {{
    background-color: transparent;
    border: none;
}}
QHeaderView::section {{
    background-color: {pal['table_th_bg']};
    color: {pal['text']};
    border: none;
    border-bottom: 1px solid {pal['border']};
    border-right: 1px solid {pal['border_soft']};
    padding: 5px 8px;
    font-weight: 600;
    font-size: 11px;
}}
QHeaderView::section:first {{
    border-top-left-radius: 8px;
}}
QHeaderView::section:last {{
    border-top-right-radius: 8px;
    border-right: none;
}}
QTreeView::item, QListView::item, QTreeWidget::item {{
    padding: 4px 6px;
    border-radius: 7px;
    color: {pal['text']};
}}
QTreeView::item:hover, QListView::item:hover, QTreeWidget::item:hover {{
    background: {pal['tab_unselected']};
    color: {pal['text_hover']};
}}
QTreeView::item:selected, QListView::item:selected, QTreeWidget::item:selected {{
    background-color: {pal['accent']};
    color: #FFFFFF;
}}
QCheckBox, QRadioButton {{
    spacing: 6px;
    color: {pal['text']};
}}
QCheckBox::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 5px;
    border: 1.5px solid {pal['border']};
    background-color: {pal['card_bg']};
}}
QCheckBox::indicator:hover {{
    border-color: {pal['accent']};
}}
QCheckBox::indicator:checked {{
    background-color: {pal['accent']};
    border-color: {pal['accent']};
}}
QRadioButton::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 8px;
    border: 1.5px solid {pal['border']};
    background-color: {pal['card_bg']};
}}
QRadioButton::indicator:hover {{
    border-color: {pal['accent']};
}}
QRadioButton::indicator:checked {{
    background-color: {pal['card_bg']};
    border: 4.5px solid {pal['accent']};
}}
QSlider::groove:horizontal {{
    height: 6px;
    background: {pal['border_soft']};
    border-radius: 3px;
}}
QSlider::sub-page:horizontal {{
    background: {pal['accent']};
    border-radius: 3px;
}}
QSlider::add-page:horizontal {{
    background: {pal['border_soft']};
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: #FFFFFF;
    border: 1.5px solid {pal['accent']};
    width: 15px;
    height: 15px;
    margin: -5px 0;
    border-radius: 8px;
}}
QSlider::groove:vertical {{
    width: 6px;
    background: {pal['border_soft']};
    border-radius: 3px;
}}
QSlider::sub-page:vertical {{
    background: {pal['border_soft']};
    border-radius: 3px;
}}
QSlider::add-page:vertical {{
    background: {pal['accent']};
    border-radius: 3px;
}}
QSlider::handle:vertical {{
    background: #FFFFFF;
    border: 1.5px solid {pal['accent']};
    width: 15px;
    height: 15px;
    margin: 0 -5px;
    border-radius: 8px;
}}
QProgressBar {{
    background-color: {pal['border_soft']};
    border: 1px solid {pal['border']};
    border-radius: 7px;
    text-align: center;
    color: {pal['text']};
    font-size: 10px;
    font-weight: 600;
    min-height: 14px;
}}
QProgressBar::chunk {{
    background-color: {pal['accent']};
    border-radius: 6px;
}}
QPushButton {{
    background-color: {pal['btn_bg']};
    border: 1px solid {pal['border']};
    border-radius: 8px;
    padding: 2px 7px;
    margin: 0px;
    color: {pal['text']};
    font-weight: 500;
    font-size: 11px;
}}
QPushButton:hover {{
    background-color: {pal['btn_hover']};
    border: 1px solid {pal['sep_color']};
}}
QPushButton:pressed {{
    background-color: {pal['btn_pressed']};
}}
QToolButton::menu-button {{
    background-color: {pal['menu_btn_bg']};
    border: 1px solid {pal['border']};
    border-radius: 6px;
    width: 14px;
    margin: 2px 1px;
    subcontrol-origin: padding;
    subcontrol-position: right;
}}
QToolButton::menu-button:hover {{
    background-color: {pal['btn_hover']};
    border: 1px solid {pal['sep_color']};
}}
QToolButton::menu-button:pressed {{
    background-color: {pal['btn_pressed']};
}}
QTextEdit, QPlainTextEdit {{
    background-color: {pal['card_bg']};
    border: 1px solid {pal['border']};
    border-radius: 10px;
    padding: 8px;
    color: {pal['text']};
    font-family: "SF Mono", "JetBrains Mono", "Consolas", monospace;
    font-size: 11px;
}}
QLineEdit {{
    background: {pal['card_bg']};
    border: 1px solid {pal['border']};
    border-radius: 11px;
    padding: 5px 12px;
    color: {pal['text']};
    font-family: "SF Mono", "JetBrains Mono", "Consolas", monospace;
    font-size: 11px;
    selection-background-color: {pal['accent']};
}}
QLineEdit:focus {{
    border: 1.5px solid {pal['accent']};
    background: {pal['card_bg']};
}}
QComboBox {{
    background-color: {pal['card_bg']};
    border: 1px solid {pal['border']};
    border-radius: 11px;
    padding: 4px 12px;
    color: {pal['text']};
    font-family: "SF Mono", "JetBrains Mono", "Consolas", monospace;
    font-size: 11px;
    selection-background-color: {pal['accent']};
}}
QComboBox:hover {{
    border: 1px solid {pal['sep_color']};
}}
QComboBox:focus, QComboBox:on {{
    border: 1.5px solid {pal['accent']};
    background-color: {pal['card_bg']};
}}
QComboBox QLineEdit {{
    border: none;
    background: transparent;
    padding: 0px;
    border-radius: 0px;
    color: {pal['text']};
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    border: none;
    border-top-right-radius: 11px;
    border-bottom-right-radius: 11px;
    background: transparent;
}}
QComboBox QAbstractItemView {{
    background-color: {pal['card_bg']};
    border: 1px solid {pal['border']};
    border-radius: 10px;
    padding: 4px;
    color: {pal['text']};
    selection-background-color: {pal['accent']};
    selection-color: #FFFFFF;
}}
QSpinBox, QDoubleSpinBox {{
    background-color: {pal['card_bg']};
    border: 1px solid {pal['border']};
    border-radius: 9px;
    padding: 3px 8px;
    color: {pal['text']};
}}
QGroupBox {{
    background-color: {pal['card_bg']};
    border: 1px solid {pal['border_soft']};
    border-radius: 12px;
    margin-top: 8px;
    padding: 8px;
    color: {pal['text']};
}}
QScrollArea {{
    background: transparent;
    border: none;
}}
QGraphicsView {{
    background-color: {pal['card_bg']};
    border: 1px solid {pal['border_soft']};
    border-radius: 10px;
}}
QStatusBar {{
    background: {pal['win_bg']};
    border-top: 1px solid {pal['border']};
    color: {pal['text_muted']};
    font-size: 11px;
}}
QStatusBar QToolButton {{
    background: {pal['card_bg']};
    border: 1px solid {pal['border']};
    border-radius: 8px;
    padding: 2px;
    margin: 1px 2px;
    color: {pal['text']};
}}
QStatusBar QToolButton:hover {{
    background: {pal['btn_hover']};
    border: 1px solid {pal['sep_color']};
}}
QScrollBar:vertical {{
    width: 7px;
    background: transparent;
    margin: 3px 1px;
}}
QScrollBar::handle:vertical {{
    background: {pal['scroll_thumb']};
    min-height: 24px;
    border-radius: 3.5px;
}}
QScrollBar::handle:vertical:hover {{
    background: {pal['scroll_hover']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    height: 7px;
    background: transparent;
    margin: 1px 3px;
}}
QScrollBar::handle:horizontal {{
    background: {pal['scroll_thumb']};
    min-width: 24px;
    border-radius: 3.5px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {pal['scroll_hover']};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""
def build_toolbar_qss(pal):
    return f"""
QTabWidget {{
    background: transparent;
    border: none;
}}
QTabWidget::pane {{
    background: {pal['card_bg']};
    border: 1px solid {pal['border']};
    border-radius: 16px;
    margin: 2px 8px 5px 8px;
    padding: 4px 6px;
}}
QTabBar {{
    background: transparent;
    margin-left: 8px;
}}
QTabBar::tab {{
    background: {pal['tab_unselected']};
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 5px 15px;
    margin: 2px 3px;
    color: {pal['text_muted']};
    font-weight: 500;
    font-size: 11px;
}}
QTabBar::tab:hover:!selected {{
    background: {pal['tab_hover']};
    color: {pal['text']};
}}
QTabBar::tab:selected {{
    background: {pal['card_bg']};
    border: 1px solid {pal['border']};
    color: {pal['text']};
    font-weight: 600;
}}
QToolBar {{
    background: transparent;
    border: none;
    spacing: 4px;
    padding: 2px 4px;
}}
QToolBar::separator {{
    background-color: {pal['sep_color']};
    width: 2px;
    border-radius: 1px;
    margin-top: 8px;
    margin-bottom: 8px;
    margin-left: 8px;
    margin-right: 8px;
    border: none;
}}
QFrame[frameShape="5"], QFrame[frameShape="4"] {{
    background-color: {pal['sep_color']};
    border: none;
    border-radius: 1px;
    color: {pal['sep_color']};
    width: 2px;
}}
QToolButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 4px 6px;
    margin: 1px;
    color: {pal['text']};
    font-size: 10px;
    font-weight: 500;
}}
QToolButton[popupMode="1"] {{
    padding-right: 20px;
}}
QToolButton:hover {{
    background: {pal['btn_hover']};
    border: 1px solid {pal['border']};
    color: {pal['text_hover']};
}}
QToolButton:pressed {{
    background: {pal['btn_pressed']};
}}
QToolButton:checked {{
    background: rgba(0, 122, 255, 0.18);
    border: 1px solid {pal['accent']};
    color: {pal['accent']};
    font-weight: 600;
}}
QToolButton::menu-button {{
    background-color: {pal['menu_btn_bg']};
    border: 1px solid {pal['border']};
    border-radius: 6px;
    width: 14px;
    margin: 2px 1px;
    subcontrol-origin: padding;
    subcontrol-position: right;
}}
QToolButton::menu-button:hover {{
    background-color: {pal['btn_hover']};
    border: 1px solid {pal['sep_color']};
}}
QToolButton::menu-button:pressed {{
    background-color: {pal['btn_pressed']};
}}
QLabel {{
    color: {pal['text_muted']};
    font-size: 9px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}}
"""
def build_log_css(pal):
    return f"""
:root {{ color-scheme: {pal['scheme']}; }}
html, body {{
    background-color: {pal['card_bg']} !important;
    color: {pal['text']} !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", "Helvetica Neue", sans-serif !important;
    font-size: 12px !important;
    line-height: 1.45 !important;
    margin: 6px 10px !important;
}}
a {{
    color: {pal['accent']} !important;
    text-decoration: none !important;
}}
a:hover {{
    text-decoration: underline !important;
}}
pre, code, .cxcmd {{
    background-color: {pal['code_bg']} !important;
    color: {pal['text']} !important;
    border: 1px solid {pal['border_soft']} !important;
    border-left: 3.5px solid {pal['sep_color']} !important;
    border-radius: 9px !important;
    padding: 5px 10px !important;
    margin: 5px 0 !important;
    font-family: "SF Mono", "Consolas", monospace !important;
    font-size: 11px !important;
}}
table {{
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border: 1px solid {pal['border']} !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    margin: 6px 0 !important;
    font-size: 11px !important;
}}
th, td {{
    border-bottom: 1px solid {pal['border_soft']} !important;
    border-right: 1px solid {pal['border_soft']} !important;
    padding: 5px 10px !important;
}}
th:last-child, td:last-child {{
    border-right: none !important;
}}
tr:last-child td {{
    border-bottom: none !important;
}}
th {{
    background-color: {pal['table_th_bg']} !important;
    color: {pal['text']} !important;
    font-weight: 600 !important;
}}
"""
def build_log_js(pal):
    css_one_line = (
        f'html, body {{ background-color: {pal["card_bg"]} !important; color: {pal["text"]} !important; '
        f'font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", "Helvetica Neue", sans-serif !important; font-size: 12px !important; }} '
        f'a {{ color: {pal["accent"]} !important; text-decoration: none !important; }} '
        f'pre, code, .cxcmd {{ background-color: {pal["code_bg"]} !important; color: {pal["text"]} !important; '
        f'border: 1px solid {pal["border_soft"]} !important; border-left: 3.5px solid {pal["sep_color"]} !important; '
        f'border-radius: 9px !important; padding: 5px 10px !important; font-family: "SF Mono", Menlo, Consolas, monospace !important; }} '
        f'table {{ border-collapse: separate !important; border-spacing: 0 !important; border: 1px solid {pal["border"]} !important; '
        f'border-radius: 10px !important; overflow: hidden !important; }} '
        f'th, td {{ border-bottom: 1px solid {pal["border_soft"]} !important; border-right: 1px solid {pal["border_soft"]} !important; padding: 5px 10px !important; }} '
        f'th {{ background-color: {pal["table_th_bg"]} !important; color: {pal["text"]} !important; }}'
    )
    return f"""
(function() {{
    var style = document.getElementById('_mac_light_style');
    if (!style) {{
        style = document.createElement('style');
        style.id = '_mac_light_style';
        if (document.head) document.head.appendChild(style);
    }}
    if (style) {{
        style.innerHTML = '{css_one_line}';
    }}
}})();
"""
def apply_mac_icons_to_all_tabs(session=None):
    from chimerax.toolbar.tool import get_toolbar_singleton
    tb_tool = get_toolbar_singleton(session, create=False)
    if not tb_tool or not hasattr(tb_tool, "ttb"):
        return
    ttb = tb_tool.ttb
    tb_qss = build_toolbar_qss(get_palette_dict())
    if getattr(ttb, "_mac_qss_str", None) != tb_qss:
        ttb.setStyleSheet(tb_qss)
        ttb._mac_qss_str = tb_qss
    for tab_name, sections in getattr(ttb, "_buttons", {}).items():
        if not isinstance(sections, dict):
            continue
        for sec_name, section in sections.items():
            if sec_name == "__toolbar__":
                continue
            modified = False
            for bi in getattr(section, "_buttons", []):
                icon_path = resolve_mac_icon(bi.title, getattr(bi, "description", ""), sec_name, tab_name)
                if icon_path:
                    cached_icon = get_cached_qicon(icon_path)
                    if cached_icon and (bi.icon is not cached_icon or bi.highlight_icon is not None):
                        bi.icon = cached_icon
                        bi.highlight_icon = None
                        modified = True
            if modified and hasattr(section, "_redo_layout"):
                try:
                    section._redo_layout()
                except Exception:
                    pass
    icon_sz = QtCore.QSize(28, 28)
    for b in ttb.findChildren(QtWidgets.QToolButton):
        if not getattr(b, "_mac_btn_sized", False):
            b.setIconSize(icon_sz)
            if b.popupMode() == QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup:
                b.setMinimumWidth(max(b.minimumWidth(), 64))
            b._mac_btn_sized = True
try:
    from chimerax.ui.widgets.tabbedtoolbar import _Section
    if not hasattr(_Section, "_mac_update_btn_patched"):
        _orig_update_button_action = _Section._update_button_action
        def _mac_update_button_action(self, button, action):
            _orig_update_button_action(self, button, action)
            button.setIconSize(QtCore.QSize(28, 28))
            button.setMinimumWidth(max(button.minimumWidth() + 8, 64))
        _Section._update_button_action = _mac_update_button_action
        _Section._mac_update_btn_patched = True
except Exception:
    pass
try:
    from chimerax.log.tool import Log
    if getattr(Log, "_mac_patch_ver", 0) != 2:
        _orig_actually_show = getattr(Log, "_orig_mac_actually_show", Log._actually_show)
        Log._orig_mac_actually_show = _orig_actually_show
        def _mac_actually_show(self):
            _orig_actually_show(self)
            if hasattr(self, "log_window") and self.log_window:
                p = self.log_window.page()
                if p:
                    pal = get_palette_dict()
                    r, g, b = pal["qcolor_bg"]
                    p.setBackgroundColor(QtGui.QColor(r, g, b))
                    p.runJavaScript(build_log_js(pal))
        Log._actually_show = _mac_actually_show
        Log._mac_patch_ver = 2
except Exception:
    pass
def apply_light_to_all_html_views(session=None):
    if not session or not hasattr(session, "ui") or not hasattr(session.ui, "main_window"):
        return
    win = session.ui.main_window
    if not win:
        return
    pal = get_palette_dict()
    r, g, b = pal["qcolor_bg"]
    bg_qcol = QtGui.QColor(r, g, b)
    js_code = build_log_js(pal)
    from chimerax.ui.widgets.htmlview import HtmlView
    for hv in win.findChildren(HtmlView):
        page = hv.page()
        if page:
            page.setBackgroundColor(bg_qcol)
            page.runJavaScript(js_code)
    if hasattr(session, "logger") and hasattr(session.logger, "logs"):
        for lg in session.logger.logs:
            if hasattr(lg, "_actually_show") and getattr(lg, "_mac_shown_mode", None) != _CURRENT_MODE:
                try:
                    lg._actually_show()
                    lg._mac_shown_mode = _CURRENT_MODE
                except Exception:
                    pass
def configure_3d_canvas(session):
    if session:
        try:
            pal = get_palette_dict()
            run(session, f"set bg {pal['win_bg']}")
            run(session, "lighting soft")
            run(session, f"graphics silhouettes true color {pal['silhouette_color']} width 1.2")
            run(session, "color byhetero")
        except Exception:
            pass
try:
    from chimerax.sideview.tool import SideViewCanvas, OrthoOverlay
    if getattr(SideViewCanvas, "_mac_patch_ver", 0) != 2:
        _orig_sv_render = getattr(SideViewCanvas, "_orig_mac_sv_render", SideViewCanvas.render)
        SideViewCanvas._orig_mac_sv_render = _orig_sv_render
        def _mac_sv_render(self):
            try:
                if self.view is not None:
                    self.view.set_background_color(get_palette_dict()["canvas_rgb"])
            except Exception:
                pass
            return _orig_sv_render(self)
        SideViewCanvas.render = _mac_sv_render
        SideViewCanvas._mac_patch_ver = 2
    if not hasattr(OrthoOverlay, "_mac_light_patched"):
        _orig_ortho_draw = OrthoOverlay.draw
        def _mac_ortho_draw(self, renderer, draw_pass):
            try:
                from numpy import array, uint8
                vc = self.vertex_colors
                if vc is not None and len(vc) == 12:
                    new_vc = array(vc, dtype=uint8, copy=True)
                    for i in range(8):
                        if new_vc[i][0] == 255 and new_vc[i][1] == 255 and new_vc[i][2] == 0:
                            new_vc[i] = [10, 132, 255, 255]
                    for i in range(8, 12):
                        if new_vc[i][0] == 255 and new_vc[i][1] == 0 and new_vc[i][2] == 0:
                            new_vc[i] = [224, 82, 99, 255]
                    self.vertex_colors = new_vc
            except Exception:
                pass
            return _orig_ortho_draw(self, renderer, draw_pass)
        OrthoOverlay.draw = _mac_ortho_draw
        OrthoOverlay._mac_light_patched = True
except Exception:
    pass
try:
    from chimerax.seq_view.seq_canvas import SeqCanvas
    if getattr(SeqCanvas, "_mac_patch_ver", 0) != 2:
        _orig_seq_init = getattr(SeqCanvas, "_orig_mac_seq_init", SeqCanvas.__init__)
        SeqCanvas._orig_mac_seq_init = _orig_seq_init
        def _mac_seq_init(self, parent, sv, alignment):
            pal = get_palette_dict()
            try:
                set_default_color_scheme(pal["scheme"])
            except Exception:
                pass
            _orig_seq_init(self, parent, sv, alignment)
            try:
                bg = QtGui.QColor(pal["card_bg"])
                self.label_scene.setBackgroundBrush(bg)
                self.main_scene.setBackgroundBrush(bg)
                self._reformat()
            except Exception:
                pass
        SeqCanvas.__init__ = _mac_seq_init
        SeqCanvas._mac_patch_ver = 2
except Exception:
    pass
def apply_light_to_sideview_and_sequences(session=None):
    if not session or not hasattr(session, "tools"):
        return
    pal = get_palette_dict()
    try:
        set_default_color_scheme(pal["scheme"])
    except Exception:
        pass
    for tool in session.tools.list():
        try:
            if hasattr(tool, "seq_canvas") and tool.seq_canvas:
                sc = tool.seq_canvas
                bg = QtGui.QColor(pal["card_bg"])
                if hasattr(sc, "label_scene"):
                    sc.label_scene.setBackgroundBrush(bg)
                if hasattr(sc, "main_scene"):
                    sc.main_scene.setBackgroundBrush(bg)
                if hasattr(sc, "_reformat"):
                    sc._reformat()
            if hasattr(tool, "opengl_canvas") and hasattr(tool, "view") and tool.view is not None:
                tool.view.set_background_color(pal["canvas_rgb"])
                tool.opengl_canvas._redraw()
        except Exception:
            pass
def apply_theme(session=None, mode=None):
    global _CURRENT_MODE
    if mode is not None:
        set_current_mode(mode)
    pal = get_palette_dict(_CURRENT_MODE)
    app = QtWidgets.QApplication.instance()
    if not app:
        return
    app.setStyle("Fusion")
    if not hasattr(app, "_mac_win_polish_filter"):
        polish_filter = MacGlobalWindowPolishFilter(app)
        app.installEventFilter(polish_filter)
        app._mac_win_polish_filter = polish_filter
    for top_w in app.topLevelWidgets():
        if top_w.isVisible():
            apply_win11_rounded_corners(top_w)
    font = QtGui.QFont("SF Pro Text", 11)
    if not font.exactMatch():
        font = QtGui.QFont("Helvetica Neue", 11)
    if not font.exactMatch():
        font = QtGui.QFont("Segoe UI", 10)
    font.setStyleHint(QtGui.QFont.StyleHint.SansSerif)
    app.setFont(font)
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(pal["win_bg"]))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(pal["text"]))
    palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(pal["card_bg"]))
    palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(pal["alt_bg"]))
    palette.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor(pal["text"]))
    palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(pal["btn_bg"]))
    palette.setColor(QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(pal["text"]))
    palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(pal["accent"]))
    palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor("#FFFFFF"))
    app.setPalette(palette)
    app.setStyleSheet(build_main_qss(pal))
    if session and hasattr(session, "ui") and session.ui:
        ui = session.ui
        is_dark = pal["scheme"] == "dark"
        ui.color_scheme = pal["scheme"]
        try:
            ui.styleHints().setColorScheme(
                QtCore.Qt.ColorScheme.Dark if is_dark else QtCore.Qt.ColorScheme.Light
            )
        except Exception:
            pass
        ui.dark_mode = (lambda: True) if is_dark else (lambda: False)
        log_css = build_log_css(pal)
        ui.dark_css = lambda css=log_css: css
        try:
            set_default_color_scheme(pal["scheme"])
        except Exception:
            pass
        try:
            ui.triggers.activate_trigger("color scheme changed", None)
        except Exception:
            pass
    install_window_traffic_lights(session)
    install_dock_traffic_lights(session)
    apply_mac_icons_to_all_tabs(session)
    apply_light_to_all_html_views(session)
    apply_light_to_sideview_and_sequences(session)
    configure_3d_canvas(session)
    QtCore.QTimer.singleShot(150, lambda: apply_mac_icons_to_all_tabs(session))
    QtCore.QTimer.singleShot(200, lambda: install_dock_traffic_lights(session))
    QtCore.QTimer.singleShot(250, lambda: apply_light_to_all_html_views(session))
    QtCore.QTimer.singleShot(300, lambda: apply_light_to_sideview_and_sequences(session))
    if not getattr(app, "_mac_tabs_hooked", False):
        for tw in app.findChildren(QtWidgets.QTabWidget):
            try:
                tw.currentChanged.connect(lambda idx: QtCore.QTimer.singleShot(40, lambda: apply_mac_icons_to_all_tabs(session)))
            except Exception:
                pass
        app._mac_tabs_hooked = True
    if session and hasattr(session, "triggers") and not getattr(session, "_mac_triggers_added", False):
        def on_session_restored(*args):
            QtCore.QTimer.singleShot(80, lambda: configure_3d_canvas(session))
            QtCore.QTimer.singleShot(120, lambda: apply_mac_icons_to_all_tabs(session))
            QtCore.QTimer.singleShot(160, lambda: install_dock_traffic_lights(session))
            QtCore.QTimer.singleShot(200, lambda: apply_light_to_all_html_views(session))
            QtCore.QTimer.singleShot(240, lambda: apply_light_to_sideview_and_sequences(session))
        try:
            session.triggers.add_handler("end restore session", on_session_restored)
            session.triggers.add_handler("session open", on_session_restored)
            session.triggers.add_handler("open models", on_session_restored)
            session._mac_triggers_added = True
        except Exception:
            pass
    if session and not getattr(session, "_mac_watcher_installed", False):
        theme_file = r"C:\Users\Parfion\chimerax_start\liquid_glass_theme.py"
        if os.path.exists(theme_file):
            watcher = QtCore.QFileSystemWatcher([theme_file], app)
            def _on_theme_file_changed(path):
                if os.path.exists(theme_file):
                    watcher.addPath(theme_file)
                    QtCore.QTimer.singleShot(150, lambda: reload_theme_from_disk(session, _CURRENT_MODE))
            watcher.fileChanged.connect(_on_theme_file_changed)
            session._mac_file_watcher = watcher
            session._mac_watcher_installed = True
try:
    from chimerax.core.session import Session
    if not hasattr(Session, "_mac_init_patched"):
        _orig_session_init = Session.__init__
        def _mac_session_init(self, *args, **kwargs):
            _orig_session_init(self, *args, **kwargs)
            try:
                QtCore.QTimer.singleShot(150, lambda: apply_theme(self, mode=_CURRENT_MODE))
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
def reload_theme_from_disk(session=None, mode=None):
    global _CURRENT_MODE
    if mode is not None:
        set_current_mode(mode)
    theme_file = r"C:\Users\Parfion\chimerax_start\liquid_glass_theme.py"
    if os.path.exists(theme_file):
        try:
            with open(theme_file, "r", encoding="utf-8") as f:
                code = f.read()
            ns = dict(globals())
            ns["session"] = session
            ns["_CURRENT_MODE"] = _CURRENT_MODE
            exec(compile(code, theme_file, "exec"), ns)
            return
        except Exception:
            pass
    apply_theme(session, mode=_CURRENT_MODE)
def liquidglass_cmd(session, mode=None):
    if mode and mode.lower() in ("off", "disable", "reset", "default"):
        remove_theme(session)
    else:
        reload_theme_from_disk(session, mode=mode)
try:
    cmd_desc = CmdDesc(
        optional=[("mode", StringArg)],
        synopsis="macOS Sequoia Light, Gray & Dark Pro Mode"
    )
    register("liquidglass", cmd_desc, liquidglass_cmd)
except Exception:
    pass
current_session = globals().get("session", None)
apply_theme(current_session, mode=_CURRENT_MODE)
