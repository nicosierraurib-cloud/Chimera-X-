import os
import sys
import gc
import math
import time
import ctypes
from functools import lru_cache
from Qt import QtWidgets, QtGui, QtCore
from chimerax.core.commands import register, CmdDesc, StringArg, run
from chimerax.core.colors import set_default_color_scheme
try:
    import numpy as _np
except Exception:
    _np = None
try:
    from chimerax.core import buildinfo as _cx_buildinfo
    _CX_VERSION = getattr(_cx_buildinfo, "version", "1.12")
except Exception:
    _CX_VERSION = "1.12"
try:
    gc.set_threshold(50000, 20, 20)
except Exception:
    pass
try:
    QtGui.QPixmapCache.setCacheLimit(65536)
except Exception:
    pass
_CURRENT_MODE = globals().get("_CURRENT_MODE", "gray")
_THEME_PALETTES = {
    "gray": {
        "win_bg": "#D5DBE5",
        "viewport_bg": "#DCE2EC",
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
        "canvas_rgb": (0.863, 0.886, 0.925, 1.0),
        "sideview_rgb": (1.0, 1.0, 1.0, 1.0),
        "status_bg": (0.835, 0.859, 0.898, 1.0),
        "status_text": (29, 29, 31, 255),
        "silhouette_color": "#2C2C2E",
        "dwm_dark": 0,
        "dwm_caption": 0x00E5DBD5,
        "dwm_text": 0x001F1D1D,
        "scheme": "light",
        "qcolor_bg": (228, 232, 240),
    },
    "dark": {
        "win_bg": "#1C1C1E",
        "viewport_bg": "#0D0E11",
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
        "canvas_rgb": (0.051, 0.055, 0.067, 1.0),
        "sideview_rgb": (0.086, 0.090, 0.106, 1.0),
        "status_bg": (0.110, 0.110, 0.118, 1.0),
        "status_text": (245, 245, 247, 255),
        "silhouette_color": "#E5E5EA",
        "dwm_dark": 1,
        "dwm_caption": 0x001E1C1C,
        "dwm_text": 0x00F7F5F5,
        "scheme": "dark",
        "qcolor_bg": (44, 44, 46),
    },
}
_SV_BG_ARRAYS = {}
if _np is not None:
    for _k, _v in _THEME_PALETTES.items():
        _SV_BG_ARRAYS[_k] = _np.array(_v["sideview_rgb"], dtype=_np.float32)
def normalize_mode(mode):
    if not mode:
        return "gray"
    m = mode.lower().strip()
    if m in ("dark", "oscuro", "night"):
        return "dark"
    return "gray"
def get_current_mode():
    app = QtWidgets.QApplication.instance()
    if app and hasattr(app, "_mac_current_mode"):
        return normalize_mode(app._mac_current_mode)
    return normalize_mode(_CURRENT_MODE)
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
@lru_cache(maxsize=512)
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
                if obj.isWindow():
                    if getattr(obj, "_mac_dwm_mode", None) != _CURRENT_MODE:
                        obj._mac_dwm_mode = _CURRENT_MODE
                        QtCore.QTimer.singleShot(10, lambda w=obj: apply_win11_rounded_corners(w))
                    if type(obj).__name__ == "MainWindow" and not getattr(obj, "_mac_startup_splash_done", False):
                        obj._mac_startup_splash_done = True
                        ses = getattr(obj, "_mac_session_ref", None) or globals().get("session", None)
                        show_mac_loading(ses, kind="startup")
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
class MacInternalCurtain(QtWidgets.QWidget):
    def __init__(self, parent_win, overlay_ref):
        super().__init__(parent_win)
        self._overlay_ref = overlay_ref
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.hide()
    def sync_to_parent(self):
        p = self.parentWidget()
        if p:
            r = p.rect()
            if self.geometry() != r:
                self.setGeometry(r)
            self.raise_()
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        ov = self._overlay_ref
        if ov is not None and ov._static_pixmap is not None and not ov._static_pixmap.isNull():
            painter.drawPixmap(0, 0, ov._static_pixmap)
        else:
            is_dark = get_current_mode() == "dark"
            bg = QtGui.QColor(21, 22, 25, 255) if is_dark else QtGui.QColor(228, 234, 242, 255)
            painter.fillRect(self.rect(), bg)
        painter.end()
class MacLoadingOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(
            None,
            QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint,
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self._session = None
        self._kind = "startup"
        self._label = ""
        self._progress = 0.06
        self._anim_phase = 0.0
        self._start_t = 0.0
        self._last_t = 0.0
        self._last_hide_t = 0.0
        self._appear_cooldown = 0.18
        self._disappear_cooldown = 0.42
        self._done_since_t = None
        self._pending_callbacks = []
        self._callbacks_ran = False
        self._dt_samples = []
        self._stable_count = 0
        self._target_fps = 60
        self._measured_fps = 60
        self._min_duration = 0.90
        self._max_duration = 1.75
        self._static_key = None
        self._static_pixmap = None
        self._emblem_key = None
        self._swoop_path = None
        self._hi_swoop_path = None
        self._x_font = None
        self._curtain = None
        self._msg_font = QtGui.QFont("Segoe UI", 10)
        self._msg_font.setWeight(QtGui.QFont.Weight.Medium)
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(15)
        self._timer.timeout.connect(self._on_tick)
    def _ensure_curtain(self):
        win = None
        if self._session and hasattr(self._session, "ui") and hasattr(self._session.ui, "main_window"):
            win = self._session.ui.main_window
        if not win:
            return None
        if self._curtain is None or self._curtain.parentWidget() is not win:
            self._curtain = MacInternalCurtain(win, self)
        return self._curtain
    def _hide_all(self):
        self._timer.stop()
        self._pending_callbacks.clear()
        self._last_hide_t = time.perf_counter()
        if self._curtain is not None:
            try:
                self._curtain.hide()
            except Exception:
                pass
        self.hide()
    def start_loading(self, session=None, kind="startup", label="", action_callback=None):
        now = time.perf_counter()
        if self.isVisible():
            if session is not None:
                self._session = session
            if label:
                self._label = label
            if action_callback is not None:
                self._pending_callbacks.append(action_callback)
                self._callbacks_ran = False
                self._done_since_t = None
                self._progress = min(self._progress, 0.35)
                self._start_t = now - self._appear_cooldown * 0.5
            self._sync_geometry()
            self.raise_()
            self.repaint()
            return
        if action_callback is None and kind != "startup" and (now - self._last_hide_t) < 0.45:
            return
        self._session = session
        self._kind = kind
        self._label = label
        self._progress = 0.06
        self._done_since_t = None
        self._pending_callbacks.clear()
        if action_callback is not None:
            self._pending_callbacks.append(action_callback)
        self._callbacks_ran = False
        self._start_t = now
        self._last_t = now
        self._dt_samples.clear()
        self._stable_count = 0
        scr = QtGui.QGuiApplication.primaryScreen()
        hz = scr.refreshRate() if scr else 60.0
        self._target_fps = 60 if hz >= 50.0 else 30
        self._measured_fps = self._target_fps
        if kind == "startup":
            self._appear_cooldown = 0.16
            self._min_duration = 1.30
            self._max_duration = 2.20
            self._disappear_cooldown = 0.45
        elif kind == "theme":
            self._appear_cooldown = 0.18
            self._min_duration = 0.92
            self._max_duration = 1.65
            self._disappear_cooldown = 0.42
        else:
            self._appear_cooldown = 0.16
            self._min_duration = 0.72
            self._max_duration = 1.35
            self._disappear_cooldown = 0.38
        self._sync_geometry()
        wi = max(1, self.width())
        hi = max(1, self.height())
        self._ensure_static_cache(wi, hi, get_current_mode() == "dark")
        curt = self._ensure_curtain()
        if curt is not None:
            curt.sync_to_parent()
            curt.show()
            curt.raise_()
            curt.repaint()
        self.setWindowOpacity(1.0)
        self.show()
        apply_win11_rounded_corners(self)
        self.raise_()
        self.repaint()
        QtWidgets.QApplication.sendPostedEvents(self, QtCore.QEvent.Type.Paint)
        QtWidgets.QApplication.processEvents(QtCore.QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents, 20)
        if not self._timer.isActive():
            self._timer.start()
    def _sync_geometry(self):
        win = None
        if self._session and hasattr(self._session, "ui") and hasattr(self._session.ui, "main_window"):
            win = self._session.ui.main_window
        if win and win.isVisible():
            geo = win.frameGeometry().adjusted(-2, -2, 2, 2)
            if geo.width() < 200 or geo.height() < 200:
                geo = win.geometry()
            if self.geometry() != geo:
                self.setGeometry(geo)
            if self._curtain is not None and self._curtain.isVisible():
                self._curtain.sync_to_parent()
        else:
            scr = QtGui.QGuiApplication.primaryScreen()
            if scr:
                ag = scr.availableGeometry()
                if self.geometry() != ag:
                    self.setGeometry(ag)
    def _on_tick(self):
        app = QtWidgets.QApplication.instance()
        if app and (app.activeModalWidget() or app.activePopupWidget()):
            self._hide_all()
            return
        if self._session and hasattr(self._session, "ui") and hasattr(self._session.ui, "main_window"):
            mw = self._session.ui.main_window
            if mw and mw.isMinimized():
                self._hide_all()
                return
        now = time.perf_counter()
        dt = max(0.001, min(0.08, now - self._last_t))
        self._last_t = now
        elapsed = now - self._start_t
        self._anim_phase += dt * 3.8
        self._sync_geometry()
        if not self._callbacks_ran and elapsed >= self._appear_cooldown:
            self._callbacks_ran = True
            cbs = list(self._pending_callbacks)
            self._pending_callbacks.clear()
            for cb in cbs:
                try:
                    cb()
                except Exception:
                    pass
            self._last_t = time.perf_counter()
            self._dt_samples.clear()
            self._stable_count = 0
            self.update()
            return
        if self._callbacks_ran:
            self._dt_samples.append(dt)
            if len(self._dt_samples) > 10:
                self._dt_samples.pop(0)
            avg_dt = sum(self._dt_samples) / len(self._dt_samples)
            raw_fps = int(round(1.0 / max(0.004, avg_dt)))
            self._measured_fps = min(self._target_fps, max(12, raw_fps))
            threshold_fps = 46 if self._target_fps >= 60 else 25
            if self._measured_fps >= threshold_fps:
                self._stable_count += 1
            else:
                self._stable_count = max(0, self._stable_count - 1)
        if self._session and hasattr(self._session, "main_view") and self._session.main_view:
            try:
                self._session.main_view.check_for_drawing_change()
            except Exception:
                pass
        if self._done_since_t is not None:
            hold_elapsed = now - self._done_since_t
            if hold_elapsed >= self._disappear_cooldown:
                if self._session and hasattr(self._session, "ui") and hasattr(self._session.ui, "main_window"):
                    mw = self._session.ui.main_window
                    if mw:
                        mw.update()
                self._hide_all()
                return
            self.update()
            return
        if not self._callbacks_ran:
            self._progress = min(0.24, 0.06 + (elapsed / max(0.05, self._appear_cooldown)) * 0.18)
        else:
            work_elapsed = max(0.0, elapsed - self._appear_cooldown)
            work_min = max(0.30, self._min_duration - self._appear_cooldown)
            work_max = max(0.60, self._max_duration - self._appear_cooldown)
            base_prog = min(0.90, 0.24 + (work_elapsed / work_min) * 0.66)
            if work_elapsed >= work_min and (self._stable_count >= 6 or work_elapsed >= work_max):
                self._progress = min(1.0, self._progress + dt * 3.2)
                if self._progress >= 0.995:
                    self._progress = 1.0
                    self._done_since_t = now
            else:
                if base_prog > self._progress:
                    self._progress = base_prog
                else:
                    self._progress = min(0.93, self._progress + dt * 0.22)
        self.update()
    def _get_messages(self):
        p = self._progress
        fps = self._measured_fps
        tgt = self._target_fps
        if self._kind == "theme":
            if p < 0.32:
                left = "Aplicando paleta visual..."
                right = f"v{_CX_VERSION} \u2022 Iniciando recursos..."
            elif p < 0.66:
                left = "Sincronizando paneles y visor 3D..."
                right = f"v{_CX_VERSION} \u2022 Compilando shaders..."
            elif p < 0.94:
                left = f"Estabilizando fotogramas ({fps} / {tgt} FPS)..."
                right = f"v{_CX_VERSION} \u2022 Sincronizando {tgt} Hz..."
            else:
                left = f"Interfaz lista ({tgt} FPS)"
                right = f"v{_CX_VERSION} \u2022 {tgt} FPS estables"
        elif self._kind == "action":
            act = self._label if self._label else "herramienta"
            if p < 0.35:
                left = f"Ejecutando: {act}..."
                right = f"v{_CX_VERSION} \u2022 Procesando..."
            elif p < 0.68:
                left = "Actualizando geometr\u00eda molecular..."
                right = f"v{_CX_VERSION} \u2022 Renderizando vista..."
            elif p < 0.94:
                left = f"Estabilizando fotogramas ({fps} / {tgt} FPS)..."
                right = f"v{_CX_VERSION} \u2022 Sincronizando {tgt} Hz..."
            else:
                left = f"Vista estabilizada ({tgt} FPS)"
                right = f"v{_CX_VERSION} \u2022 {tgt} FPS estables"
        else:
            if p < 0.28:
                left = "Cargando m\u00f3dulos..."
                right = f"v{_CX_VERSION} \u2022 Iniciando recursos..."
            elif p < 0.56:
                left = "Inicializando motor OpenGL 3D..."
                right = f"v{_CX_VERSION} \u2022 Cargando paquetes..."
            elif p < 0.88:
                left = f"Estabilizando fotogramas ({fps} / {tgt} FPS)..."
                right = f"v{_CX_VERSION} \u2022 Sincronizando {tgt} Hz..."
            else:
                left = f"Entorno listo ({tgt} FPS)"
                right = f"v{_CX_VERSION} \u2022 {tgt} FPS estables"
        return left, right
    def _ensure_static_cache(self, wi, hi, is_dark):
        key = (wi, hi, is_dark)
        if self._static_key == key and self._static_pixmap is not None:
            return
        self._static_key = key
        w = float(wi)
        h = float(hi)
        pix = QtGui.QPixmap(wi, hi)
        bg_outer = QtGui.QColor(21, 22, 25, 255) if is_dark else QtGui.QColor(228, 234, 242, 255)
        pix.fill(bg_outer)
        p = QtGui.QPainter(pix)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        p.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
        outer_border = QtGui.QPen(QtGui.QColor("#32343C") if is_dark else QtGui.QColor("#B8C3D4"))
        outer_border.setWidthF(1.0)
        p.setPen(outer_border)
        p.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        p.drawRect(QtCore.QRectF(0.5, 0.5, w - 1.0, h - 1.0))
        cw = min(680.0, max(500.0, w * 0.58))
        ch = min(460.0, max(340.0, h * 0.62))
        cx = w * 0.5
        cy = h * 0.5
        card_rect = QtCore.QRectF(cx - cw * 0.5, cy - ch * 0.5, cw, ch)
        for i in range(6, 0, -1):
            sp = float(i) * 2.5
            s_alpha = int((26 if is_dark else 11) * (7 - i) / 6.0)
            s_path = QtGui.QPainterPath()
            s_path.addRoundedRect(card_rect.adjusted(-sp, -sp + 3.0, sp, sp + 5.0), 14.0 + sp * 0.4, 14.0 + sp * 0.4)
            p.fillPath(s_path, QtGui.QColor(0, 0, 0, s_alpha))
        card_path = QtGui.QPainterPath()
        card_path.addRoundedRect(card_rect, 13.0, 13.0)
        card_fill = QtGui.QColor("#1F2024") if is_dark else QtGui.QColor("#F4F5F8")
        card_border = QtGui.QColor("#383A42") if is_dark else QtGui.QColor("#D4DBE6")
        p.fillPath(card_path, card_fill)
        cpen = QtGui.QPen(card_border)
        cpen.setWidthF(1.2)
        p.setPen(cpen)
        p.drawPath(card_path)
        rad = min(cw, ch) * 0.195
        tx = card_rect.left() + cw * 0.48
        ty = card_rect.top() + ch * 0.44
        uc_font = QtGui.QFont("Segoe UI", int(rad * 0.24))
        uc_font.setWeight(QtGui.QFont.Weight.Black)
        p.setFont(uc_font)
        p.setPen(QtGui.QColor("#AEB4C0") if is_dark else QtGui.QColor("#222428"))
        fm_uc = QtGui.QFontMetricsF(uc_font)
        p.drawText(QtCore.QPointF(tx, ty - rad * 0.24), "UC")
        uc_w = fm_uc.horizontalAdvance("UC")
        p.drawText(QtCore.QPointF(tx + uc_w - 1.0, ty - rad * 0.14), "SF")
        cx_font = QtGui.QFont("Segoe UI", int(rad * 0.43))
        cx_font.setWeight(QtGui.QFont.Weight.Bold)
        p.setFont(cx_font)
        p.setPen(QtGui.QColor("#F2F4F8") if is_dark else QtGui.QColor("#222428"))
        p.drawText(QtCore.QPointF(tx, ty + rad * 0.34), "Chimera X")
        bar_margin = 44.0
        bar_x = card_rect.left() + bar_margin
        bar_w = cw - bar_margin * 2.0
        bar_y = card_rect.bottom() - 54.0
        bar_h = 7.0
        track_path = QtGui.QPainterPath()
        track_path.addRoundedRect(QtCore.QRectF(bar_x, bar_y, bar_w, bar_h), 3.5, 3.5)
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.fillPath(track_path, QtGui.QColor("#32343A") if is_dark else QtGui.QColor("#DCDFE5"))
        p.end()
        self._static_pixmap = pix
        em_key = round(rad, 2)
        if self._emblem_key != em_key:
            self._emblem_key = em_key
            swoop = QtGui.QPainterPath()
            swoop.moveTo(rad * 0.68, rad * 0.30)
            swoop.cubicTo(rad * 0.05, -rad * 0.25, -rad * 0.85, -rad * 0.32, -rad * 0.66, rad * 0.08)
            swoop.cubicTo(-rad * 0.45, rad * 0.48, rad * 0.25, rad * 0.85, rad * 0.78, rad * 1.06)
            swoop.cubicTo(rad * 0.58, rad * 0.86, -rad * 0.22, rad * 0.36, -rad * 0.38, rad * 0.02)
            swoop.cubicTo(-rad * 0.50, -rad * 0.18, rad * 0.08, -rad * 0.08, rad * 0.62, rad * 0.38)
            swoop.closeSubpath()
            self._swoop_path = swoop
            hi_swoop = QtGui.QPainterPath()
            hi_swoop.moveTo(rad * 0.58, rad * 0.34)
            hi_swoop.cubicTo(rad * 0.02, -rad * 0.14, -rad * 0.55, -rad * 0.18, -rad * 0.42, rad * 0.08)
            hi_swoop.cubicTo(-rad * 0.26, rad * 0.38, rad * 0.22, rad * 0.72, rad * 0.56, rad * 0.88)
            self._hi_swoop_path = hi_swoop
            xf = QtGui.QFont("Times New Roman", int(rad * 1.05))
            xf.setBold(True)
            xf.setItalic(True)
            self._x_font = xf
    def paintEvent(self, event):
        wi = max(1, self.width())
        hi = max(1, self.height())
        is_dark = get_current_mode() == "dark"
        self._ensure_static_cache(wi, hi, is_dark)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
        painter.drawPixmap(0, 0, self._static_pixmap)
        w = float(wi)
        h = float(hi)
        cw = min(680.0, max(500.0, w * 0.58))
        ch = min(460.0, max(340.0, h * 0.62))
        cx = w * 0.5
        cy = h * 0.5
        card_left = cx - cw * 0.5
        card_top = cy - ch * 0.5
        card_bottom = card_top + ch
        bob = math.sin(self._anim_phase) * 2.2
        em_cx = card_left + cw * 0.295
        em_cy = card_top + ch * 0.45 + bob
        rad = min(cw, ch) * 0.195
        ring_shadow_pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 55 if is_dark else 28))
        ring_shadow_pen.setWidthF(rad * 0.145)
        painter.setPen(ring_shadow_pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QtCore.QPointF(em_cx, em_cy + 3.5), rad, rad)
        ring_pen = QtGui.QPen(QtGui.QColor("#8EBDF8"))
        ring_pen.setWidthF(rad * 0.145)
        ring_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(ring_pen)
        painter.drawEllipse(QtCore.QPointF(em_cx, em_cy), rad, rad)
        glow_pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 135 if is_dark else 165))
        glow_pen.setWidthF(rad * 0.08)
        glow_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(glow_pen)
        angle_deg = int((self._anim_phase * 75.0) % 360.0) * 16
        painter.drawArc(
            QtCore.QRectF(em_cx - rad, em_cy - rad, rad * 2.0, rad * 2.0),
            angle_deg,
            52 * 16,
        )
        painter.save()
        painter.translate(em_cx, em_cy)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.fillPath(self._swoop_path, QtGui.QColor("#5C626E") if is_dark else QtGui.QColor("#3E434C"))
        if is_dark:
            hi_pen = QtGui.QPen(QtGui.QColor("#E4E8F0"))
            hi_pen.setWidthF(rad * 0.075)
            hi_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(hi_pen)
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
            painter.drawPath(self._hi_swoop_path)
        node_pt = QtCore.QPointF(-rad * 0.02, -rad * 0.04)
        node_r = rad * 0.115 * (1.0 + 0.08 * math.sin(self._anim_phase * 2.0))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QColor("#808794") if is_dark else QtGui.QColor("#3E434C"))
        painter.drawEllipse(node_pt, node_r, node_r)
        painter.restore()
        painter.setFont(self._x_font)
        x_rect = QtCore.QRectF(em_cx - rad * 0.10, em_cy - rad * 1.18, rad * 1.35, rad * 1.25)
        painter.setPen(QtGui.QColor(0, 0, 0, 70 if is_dark else 42))
        painter.drawText(x_rect.translated(2.0, 3.5), QtCore.Qt.AlignmentFlag.AlignCenter, "X")
        painter.setPen(QtGui.QColor("#FF5E57"))
        painter.drawText(x_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "X")
        bar_margin = 44.0
        bar_x = card_left + bar_margin
        bar_w = cw - bar_margin * 2.0
        bar_y = card_bottom - 54.0
        bar_h = 7.0
        fill_w = max(12.0, bar_w * float(self._progress))
        fill_rect = QtCore.QRectF(bar_x, bar_y, fill_w, bar_h)
        fill_path = QtGui.QPainterPath()
        fill_path.addRoundedRect(fill_rect, 3.5, 3.5)
        grad = QtGui.QLinearGradient(bar_x, bar_y, bar_x + fill_w, bar_y)
        grad.setColorAt(0.0, QtGui.QColor("#8EC5FC"))
        grad.setColorAt(0.5, QtGui.QColor("#A0E7E5"))
        grad.setColorAt(1.0, QtGui.QColor("#B5EAD7"))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.fillPath(fill_path, QtGui.QBrush(grad))
        shimmer_pos = (self._anim_phase * 0.45) % 1.0
        sx = bar_x + shimmer_pos * fill_w
        s_grad = QtGui.QLinearGradient(sx - 35.0, bar_y, sx + 35.0, bar_y)
        s_grad.setColorAt(0.0, QtGui.QColor(255, 255, 255, 0))
        s_grad.setColorAt(0.5, QtGui.QColor(255, 255, 255, 130))
        s_grad.setColorAt(1.0, QtGui.QColor(255, 255, 255, 0))
        painter.fillPath(fill_path, QtGui.QBrush(s_grad))
        left_msg, right_msg = self._get_messages()
        painter.setFont(self._msg_font)
        painter.setPen(QtGui.QColor("#8E94A0") if is_dark else QtGui.QColor("#3A3D45"))
        text_rect = QtCore.QRectF(bar_x, bar_y + 13.0, bar_w, 22.0)
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter, left_msg)
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter, right_msg)
        painter.end()
def show_mac_loading(session=None, kind="startup", label="", action_callback=None):
    app = QtWidgets.QApplication.instance()
    if not app:
        if action_callback is not None:
            action_callback()
        return
    ov = getattr(app, "_mac_loading_overlay", None)
    if ov is None or type(ov).__name__ != "MacLoadingOverlay" or not hasattr(ov, "_hide_all"):
        if ov is not None:
            try:
                ov.hide()
                ov.deleteLater()
            except Exception:
                pass
        ov = MacLoadingOverlay()
        app._mac_loading_overlay = ov
    ov.start_loading(session=session, kind=kind, label=label, action_callback=action_callback)
_SKIP_DLG_TITLES = frozenset(("open", "save", "recent", "open dicom", "snapshot", "spin movie"))
class MacToolbarActionFilter(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = None
    def eventFilter(self, obj, event):
        try:
            if (
                event.type() == QtCore.QEvent.Type.MouseButtonRelease
                and event.button() == QtCore.Qt.MouseButton.LeftButton
                and isinstance(obj, QtWidgets.QToolButton)
                and obj.isEnabled()
                and not getattr(obj, "_mac_running_deferred", False)
            ):
                pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
                if obj.rect().contains(pos):
                    if obj.popupMode() == QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup:
                        return False
                    if obj.popupMode() == QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup and pos.x() >= obj.width() - 18:
                        return False
                    txt = obj.text().replace("\n", " ").strip()
                    if txt.lower() not in _SKIP_DLG_TITLES:
                        obj.setDown(False)
                        def _exec_btn(b=obj):
                            try:
                                b._mac_running_deferred = True
                                b.click()
                            finally:
                                b._mac_running_deferred = False
                        show_mac_loading(self.session, kind="action", label=txt, action_callback=_exec_btn)
                        return True
        except Exception:
            pass
        return False
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
        for mode_key, label_text in (("gray", "Gris"), ("dark", "Oscuro")):
            mb = QtWidgets.QPushButton(label_text, self)
            mb.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            mb.setFixedHeight(20)
            def _on_mode_click(checked=False, m=mode_key, lt=label_text):
                ses = self._session_getter() if self._session_getter else None
                set_current_mode(m)
                show_mac_loading(ses, kind="theme", label=lt, action_callback=lambda s=ses, md=m: apply_theme(s, mode=md))
            mb.clicked.connect(_on_mode_click)
            layout.addWidget(mb)
            self._mode_btns[mode_key] = mb
        self.refresh_theme()
    def refresh_theme(self):
        pal = get_palette_dict()
        self.setStyleSheet(f"background-color: {pal['win_bg']}; border: none;")
        self.title_lbl.setStyleSheet(f"color: {pal['text']}; font-size: 13px; font-weight: 600; background: transparent; border: none;")
        cur_m = get_current_mode()
        for m_key, btn in self._mode_btns.items():
            if m_key == cur_m:
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
    cur_mode = get_current_mode()
    state_key = (cur_mode, is_hidden_title, dw.windowTitle().strip())
    if getattr(w, "_mac_card_state", None) == state_key:
        return
    w._mac_card_state = state_key
    pal = get_palette_dict(cur_mode)
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
        if type(existing_tb).__name__ != "MacDockTitleBar":
            title_bar = MacDockTitleBar(dw)
            dw.setTitleBarWidget(title_bar)
            dw._mac_dock_styled = True
            dw._mac_dock_ver = 5
        elif hasattr(existing_tb, "refresh_theme"):
            existing_tb.refresh_theme()
        style_dock_content_card(dw, is_hidden_title=False)
try:
    from chimerax.ui.gui import _Qt
    if getattr(_Qt, "_mac_dock_ver", 0) != 5:
        _orig_qt_init = getattr(_Qt, "_orig_mac_qt_init", _Qt.__init__)
        _Qt._orig_mac_qt_init = _orig_qt_init
        def _mac_qt_init(self, tool_window, title, has_statusbar, hide_title_bar, main_window, close_destroys):
            _orig_qt_init(self, tool_window, title, has_statusbar, hide_title_bar, main_window, close_destroys)
            if hasattr(self, "dock_widget"):
                if not hide_title_bar and title not in _HIDDEN_TITLE_DOCKS:
                    title_bar = MacDockTitleBar(self.dock_widget)
                    self.dock_widget.setTitleBarWidget(title_bar)
                    self.dock_widget._mac_dock_styled = True
                    self.dock_widget._mac_dock_ver = 5
                    QtCore.QTimer.singleShot(50, lambda dw=self.dock_widget: style_dock_content_card(dw, False))
                else:
                    QtCore.QTimer.singleShot(50, lambda dw=self.dock_widget: style_dock_content_card(dw, True))
        _Qt.__init__ = _mac_qt_init
        _Qt._mac_dock_patched = True
        _Qt._mac_dock_ver = 5
except Exception:
    pass
def install_window_traffic_lights(session=None):
    if not session or not hasattr(session, "ui") or not hasattr(session.ui, "main_window"):
        return
    win = session.ui.main_window
    if not win:
        return
    win._mac_session_ref = session
    existing_hdr = getattr(win, "_mac_header_widget", None)
    if getattr(win, "_mac_frameless_ver", 0) == 5 and existing_hdr is not None and type(existing_hdr).__name__ == "MacWindowHeader":
        apply_win11_rounded_corners(win)
        existing_hdr._session_getter = lambda: session
        existing_hdr.refresh_theme()
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
    win._mac_frameless_ver = 5
@lru_cache(maxsize=8)
def _cached_main_qss(mode_key):
    pal = _THEME_PALETTES[mode_key]
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
def build_main_qss(pal=None):
    return _cached_main_qss(get_current_mode())
@lru_cache(maxsize=8)
def _cached_toolbar_qss(mode_key):
    pal = _THEME_PALETTES[mode_key]
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
def build_toolbar_qss(pal=None):
    return _cached_toolbar_qss(get_current_mode())
@lru_cache(maxsize=8)
def _cached_log_css(mode_key):
    pal = _THEME_PALETTES[mode_key]
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
def build_log_css(pal=None):
    return _cached_log_css(get_current_mode())
@lru_cache(maxsize=8)
def _cached_log_js(mode_key):
    pal = _THEME_PALETTES[mode_key]
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
def build_log_js(pal=None):
    return _cached_log_js(get_current_mode())
def apply_mac_icons_to_all_tabs(session=None):
    from chimerax.toolbar.tool import get_toolbar_singleton
    tb_tool = get_toolbar_singleton(session, create=False)
    if not tb_tool or not hasattr(tb_tool, "ttb"):
        return
    ttb = tb_tool.ttb
    tb_qss = build_toolbar_qss()
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
    app = QtWidgets.QApplication.instance()
    tb_filter = getattr(app, "_mac_tb_action_filter", None) if app else None
    if app and (tb_filter is None or type(tb_filter).__name__ != "MacToolbarActionFilter"):
        tb_filter = MacToolbarActionFilter(app)
        app._mac_tb_action_filter = tb_filter
    if tb_filter is not None:
        tb_filter.session = session
    icon_sz = QtCore.QSize(28, 28)
    for b in ttb.findChildren(QtWidgets.QToolButton):
        if not getattr(b, "_mac_btn_sized", False):
            b.setIconSize(icon_sz)
            if b.popupMode() == QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup:
                b.setMinimumWidth(max(b.minimumWidth(), 64))
            b._mac_btn_sized = True
        if tb_filter is not None and not getattr(b, "_mac_filter_installed", False):
            b.installEventFilter(tb_filter)
            b._mac_filter_installed = True
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
                    p.runJavaScript(build_log_js())
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
    cur_mode = get_current_mode()
    pal = get_palette_dict(cur_mode)
    r, g, b = pal["qcolor_bg"]
    bg_qcol = QtGui.QColor(r, g, b)
    js_code = build_log_js()
    from chimerax.ui.widgets.htmlview import HtmlView
    if hasattr(session, "logger") and hasattr(session.logger, "logs"):
        for lg in session.logger.logs:
            if hasattr(lg, "_actually_show") and getattr(lg, "_mac_shown_mode", None) != cur_mode:
                try:
                    lg._actually_show()
                    lg._mac_shown_mode = cur_mode
                except Exception:
                    pass
    for hv in win.findChildren(HtmlView):
        page = hv.page()
        if page:
            page.setBackgroundColor(bg_qcol)
            page.runJavaScript(js_code)
def configure_3d_canvas(session, recolor=False):
    if session:
        try:
            pal = get_palette_dict()
            run(session, f"set bg {pal['viewport_bg']}", log=False)
            run(session, "lighting soft", log=False)
            run(session, f"graphics silhouettes true color {pal['silhouette_color']} width 1.2", log=False)
            if recolor:
                run(session, "color byhetero", log=False)
        except Exception:
            pass
try:
    from chimerax.graphics import Drawing
    from chimerax.graphics.drawing import rgba_drawing
    class MacRoundedFrameOverlay(Drawing):
        def __init__(self, name="mac_viewport_frame", is_sideview=False):
            super().__init__(name)
            self.use_lighting = False
            self.is_sideview = is_sideview
            self._last_key = None
        def draw(self, renderer, draw_pass):
            if getattr(renderer, "image_save", False) or _np is None:
                return
            try:
                ww, wh = renderer.render_size()
                if ww <= 24 or wh <= 24:
                    return
                pal = get_palette_dict()
                outer_col = pal["card_bg"] if self.is_sideview else pal["win_bg"]
                border_col = pal["border_soft"] if self.is_sideview else pal["border"]
                key = (ww, wh, outer_col, border_col, self.is_sideview)
                if self._last_key != key:
                    self._last_key = key
                    img = QtGui.QImage(ww, wh, QtGui.QImage.Format.Format_RGBA8888)
                    img.fill(QtGui.QColor(outer_col))
                    p = QtGui.QPainter(img)
                    p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
                    p.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Clear)
                    path = QtGui.QPainterPath()
                    if self.is_sideview:
                        rect = QtCore.QRectF(4.0, 4.0, float(ww - 8), float(wh - 6))
                        rad = 10.0
                        bw = 1.2
                    else:
                        rect = QtCore.QRectF(8.0, 3.0, float(ww - 12), float(wh - 7))
                        rad = 16.0
                        bw = 1.5
                    path.addRoundedRect(rect, rad, rad)
                    p.fillPath(path, QtCore.Qt.GlobalColor.transparent)
                    p.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceOver)
                    pen = QtGui.QPen(QtGui.QColor(border_col))
                    pen.setWidthF(bw)
                    p.setPen(pen)
                    p.drawPath(path)
                    p.end()
                    ptr = img.constBits()
                    ptr.setsize(img.sizeInBytes())
                    arr = _np.frombuffer(ptr, dtype=_np.uint8).reshape((wh, img.bytesPerLine() // 4, 4))[:, :ww, :]
                    arr = _np.ascontiguousarray(arr[::-1, :, :])
                    rgba_drawing(self, arr, pos=(-1, -1), size=(2, 2), opaque=False)
            except Exception:
                return
            super().draw(renderer, draw_pass)
except Exception:
    MacRoundedFrameOverlay = None
def install_viewport_rounded_frame(session=None):
    if not session or not hasattr(session, "main_view") or not session.main_view or MacRoundedFrameOverlay is None:
        return
    mv = session.main_view
    try:
        old_ovs = [o for o in getattr(mv, "_overlays", []) if getattr(o, "name", "") == "mac_viewport_frame"]
        if old_ovs:
            for o in old_ovs:
                o._last_key = None
        else:
            mv.add_overlay(MacRoundedFrameOverlay("mac_viewport_frame", is_sideview=False))
        mv.redraw_needed = True
    except Exception:
        pass
try:
    from chimerax.sideview.tool import SideViewCanvas, OrthoOverlay
    if getattr(SideViewCanvas, "_mac_patch_ver", 0) != 4:
        _raw_sv_render = getattr(SideViewCanvas, "_true_orig_sv_render", SideViewCanvas.render)
        while getattr(_raw_sv_render, "__closure__", None):
            _found_inner = False
            for _cell in _raw_sv_render.__closure__:
                _c = _cell.cell_contents
                if callable(_c) and getattr(_c, "__name__", "") in ("render", "_mac_sv_render"):
                    _raw_sv_render = _c
                    _found_inner = True
                    break
            if not _found_inner:
                break
        SideViewCanvas._true_orig_sv_render = _raw_sv_render
        def _mac_sv_render(self):
            try:
                if self.view is not None and _np is not None:
                    cur_m = get_current_mode()
                    self.view._background_rgba = _SV_BG_ARRAYS.get(cur_m, _SV_BG_ARRAYS["gray"])
                    if MacRoundedFrameOverlay is not None:
                        has_frame = any(getattr(o, "name", "") == "mac_sideview_frame" for o in getattr(self.view, "_overlays", []))
                        if not has_frame:
                            self.view.add_overlay(MacRoundedFrameOverlay("mac_sideview_frame", is_sideview=True))
            except Exception:
                pass
            return _raw_sv_render(self)
        SideViewCanvas.render = _mac_sv_render
        SideViewCanvas._mac_patch_ver = 4
    if getattr(OrthoOverlay, "_mac_patch_ver", 0) != 2:
        _orig_ortho_draw = getattr(OrthoOverlay, "_orig_mac_ortho_draw", OrthoOverlay.draw)
        OrthoOverlay._orig_mac_ortho_draw = _orig_ortho_draw
        def _mac_ortho_draw(self, renderer, draw_pass):
            try:
                vc = self.vertex_colors
                if _np is not None and vc is not None and len(vc) == 12 and vc[0][0] == 255 and vc[0][1] == 255:
                    new_vc = _np.array(vc, dtype=_np.uint8, copy=True)
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
        OrthoOverlay._mac_patch_ver = 2
except Exception:
    pass
try:
    from chimerax.ui.statusbar import _StatusBarOpenGL
    if getattr(_StatusBarOpenGL, "_mac_patch_ver", 0) != 2:
        _orig_sb_set_colors = getattr(_StatusBarOpenGL, "_orig_mac_set_colors", _StatusBarOpenGL.set_colors)
        _StatusBarOpenGL._orig_mac_set_colors = _orig_sb_set_colors
        def _mac_sb_set_colors(self):
            pal = get_palette_dict()
            self.background_color = pal["status_bg"]
            self.text_color = pal["status_text"]
            if self._opengl_context is None:
                return
            from chimerax.graphics import remember_current_opengl_context, restore_current_opengl_context
            cc = remember_current_opengl_context()
            if self._renderer.make_current():
                self._renderer.set_background_color(self.background_color)
            restore_current_opengl_context(cc)
        _StatusBarOpenGL.set_colors = _mac_sb_set_colors
        _StatusBarOpenGL._mac_patch_ver = 2
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
    cur_m = get_current_mode()
    pal = get_palette_dict(cur_m)
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
            if hasattr(tool, "opengl_canvas") and hasattr(tool, "view") and tool.view is not None and _np is not None:
                tool.view._background_rgba = _SV_BG_ARRAYS.get(cur_m, _SV_BG_ARRAYS["gray"])
                if MacRoundedFrameOverlay is not None:
                    old_ovs = [o for o in getattr(tool.view, "_overlays", []) if getattr(o, "name", "") == "mac_sideview_frame"]
                    if old_ovs:
                        for o in old_ovs:
                            o._last_key = None
                    else:
                        tool.view.add_overlay(MacRoundedFrameOverlay("mac_sideview_frame", is_sideview=True))
                tool.opengl_canvas.render()
        except Exception:
            pass
    if hasattr(session, "ui") and hasattr(session.ui, "main_window") and session.ui.main_window:
        sbar = getattr(session.ui.main_window, "_status_bar", None)
        if sbar and hasattr(sbar, "set_colors"):
            try:
                sbar.set_colors()
                sbar.status(getattr(sbar, "_last_message", ""), getattr(sbar, "_last_color", "CanvasText"))
            except Exception:
                pass
def _deferred_theme_sync(session=None):
    apply_mac_icons_to_all_tabs(session)
    install_dock_traffic_lights(session)
    apply_light_to_all_html_views(session)
    apply_light_to_sideview_and_sequences(session)
    install_viewport_rounded_frame(session)
def apply_theme(session=None, mode=None):
    global _CURRENT_MODE
    set_current_mode(mode if mode is not None else get_current_mode())
    pal = get_palette_dict(_CURRENT_MODE)
    app = QtWidgets.QApplication.instance()
    if not app:
        return
    if getattr(app, "_mac_fusion_set", False) is False:
        app.setStyle("Fusion")
        app._mac_fusion_set = True
    if not hasattr(app, "_mac_win_polish_filter"):
        polish_filter = MacGlobalWindowPolishFilter(app)
        app.installEventFilter(polish_filter)
        app._mac_win_polish_filter = polish_filter
    for top_w in app.topLevelWidgets():
        if top_w.isVisible():
            apply_win11_rounded_corners(top_w)
    if not getattr(app, "_mac_font_set", False):
        font = QtGui.QFont("SF Pro Text", 11)
        if not font.exactMatch():
            font = QtGui.QFont("Helvetica Neue", 11)
        if not font.exactMatch():
            font = QtGui.QFont("Segoe UI", 10)
        font.setStyleHint(QtGui.QFont.StyleHint.SansSerif)
        app.setFont(font)
        app._mac_font_set = True
    if getattr(app, "_mac_pal_mode", None) != _CURRENT_MODE:
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
        app._mac_pal_mode = _CURRENT_MODE
    main_qss = build_main_qss()
    if getattr(app, "_mac_applied_qss", None) != main_qss:
        app.setStyleSheet(main_qss)
        app._mac_applied_qss = main_qss
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
        log_css = build_log_css()
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
    configure_3d_canvas(session, recolor=False)
    install_viewport_rounded_frame(session)
    QtCore.QTimer.singleShot(160, lambda: _deferred_theme_sync(session))
    if not getattr(app, "_mac_tabs_hooked", False):
        for tw in app.findChildren(QtWidgets.QTabWidget):
            try:
                tw.currentChanged.connect(lambda idx: QtCore.QTimer.singleShot(30, lambda: apply_mac_icons_to_all_tabs(session)))
            except Exception:
                pass
        app._mac_tabs_hooked = True
    if session and hasattr(session, "triggers") and not getattr(session, "_mac_triggers_added", False):
        def on_session_restored(*args):
            def _sync_after_restore():
                configure_3d_canvas(session, recolor=False)
                _deferred_theme_sync(session)
            show_mac_loading(session, kind="action", label="Modelo 3D", action_callback=_sync_after_restore)
        for _trig_name in ("end restore session", "session open", "open models", "add models"):
            try:
                session.triggers.add_handler(_trig_name, on_session_restored)
            except Exception:
                pass
        session._mac_triggers_added = True
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
                def _start_with_splash():
                    show_mac_loading(self, kind="startup", action_callback=lambda s=self: apply_theme(s, mode=_CURRENT_MODE))
                QtCore.QTimer.singleShot(40, _start_with_splash)
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
            run(session, "set bg black", log=False)
            run(session, "graphics silhouettes false", log=False)
            run(session, "lighting simple", log=False)
        except Exception:
            pass
def reload_theme_from_disk(session=None, mode=None):
    global _CURRENT_MODE
    if mode is not None:
        set_current_mode(mode)
    def _do_reload():
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
    show_mac_loading(session, kind="theme", action_callback=_do_reload)
def liquidglass_cmd(session, mode=None):
    if mode and mode.lower() in ("off", "disable", "reset", "default"):
        remove_theme(session)
    else:
        reload_theme_from_disk(session, mode=mode)
try:
    cmd_desc = CmdDesc(
        optional=[("mode", StringArg)],
        synopsis="macOS Sequoia Gray & Dark Pro Mode"
    )
    register("liquidglass", cmd_desc, liquidglass_cmd)
except Exception:
    pass
current_session = globals().get("session", None)
apply_theme(current_session, mode=_CURRENT_MODE)
