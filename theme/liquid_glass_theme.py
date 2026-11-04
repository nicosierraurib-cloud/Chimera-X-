import os
from Qt import QtWidgets, QtGui, QtCore
from chimerax.core.commands import register, CmdDesc, StringArg, run

ICONS_DIR = r"C:\Users\Parfion\Downloads\chimerax_mac_icons"

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

EXACT_SECTION_TITLE_MAP = {
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
    ("Rendering Modes", "Raycasting"): "raycasting.svg",
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

def resolve_mac_icon(title, description="", section="", tab=""):
    key = (section, title)
    if key in EXACT_SECTION_TITLE_MAP:
        fname = EXACT_SECTION_TITLE_MAP[key]
        fp = os.path.join(ICONS_DIR, fname)
        if os.path.exists(fp):
            return fp
    norm_title = title.lower().strip()
    if tab == "Markers" and norm_title == "move":
        p = os.path.join(ICONS_DIR, "mark_move.png")
        if os.path.exists(p):
            return p
    if norm_title == "drag model":
        p = os.path.join(ICONS_DIR, "drag_model.png")
        if os.path.exists(p):
            return p
    if norm_title == "move model":
        p = os.path.join(ICONS_DIR, "move_picked_model.png")
        if os.path.exists(p):
            return p
    if norm_title == "inspect":
        p = os.path.join(ICONS_DIR, "magnifying-glass.png")
        if os.path.exists(p):
            return p
    if norm_title == "zoom":
        p = os.path.join(ICONS_DIR, "zoom.png")
        if os.path.exists(p):
            return p
    for (sec, t), fname in EXACT_SECTION_TITLE_MAP.items():
        if t.lower().strip() == norm_title:
            fp = os.path.join(ICONS_DIR, fname)
            if os.path.exists(fp):
                return fp
    direct = os.path.join(ICONS_DIR, f"{norm_title}.png")
    if os.path.exists(direct):
        return direct
    return None

class MacWindowResizeFilter(QtCore.QObject):
    def __init__(self, window, margin=6):
        super().__init__(window)
        self.win = window
        self.margin = margin

    def eventFilter(self, obj, event):
        if obj is not self.win:
            return False
        if event.type() == QtCore.QEvent.Type.MouseMove:
            if not self.win.isMaximized():
                edge = self._get_edge(event.pos())
                self._update_cursor(edge)
        elif event.type() == QtCore.QEvent.Type.MouseButtonPress:
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
        if pos.x() <= m:
            edges |= QtCore.Qt.Edge.LeftEdge.value
        elif pos.x() >= w - m:
            edges |= QtCore.Qt.Edge.RightEdge.value
        if pos.y() <= m:
            edges |= QtCore.Qt.Edge.TopEdge.value
        elif pos.y() >= h - m:
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
    def __init__(self, main_window):
        super().__init__(main_window)
        self.win = main_window
        self.setFixedHeight(34)
        self.setStyleSheet("background-color: #F5F5F7; border-bottom: 1px solid rgba(0, 0, 0, 0.08);")
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(8)

        btn_close = QtWidgets.QPushButton(self)
        btn_close.setFixedSize(12, 12)
        btn_close.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("QPushButton { background-color: #FF5F56; border: 1px solid #E0443E; border-radius: 6px; } QPushButton:hover { background-color: #FF3B30; }")
        btn_close.clicked.connect(self.win.close)
        layout.addWidget(btn_close)

        btn_min = QtWidgets.QPushButton(self)
        btn_min.setFixedSize(12, 12)
        btn_min.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_min.setStyleSheet("QPushButton { background-color: #FFBD2E; border: 1px solid #DEA123; border-radius: 6px; } QPushButton:hover { background-color: #FF9500; }")
        btn_min.clicked.connect(self.win.showMinimized)
        layout.addWidget(btn_min)

        btn_zoom = QtWidgets.QPushButton(self)
        btn_zoom.setFixedSize(12, 12)
        btn_zoom.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_zoom.setStyleSheet("QPushButton { background-color: #27C93F; border: 1px solid #1AAB29; border-radius: 6px; } QPushButton:hover { background-color: #34C759; }")
        def toggle_zoom():
            if self.win.isMaximized():
                self.win.showNormal()
            else:
                self.win.showMaximized()
        btn_zoom.clicked.connect(toggle_zoom)
        layout.addWidget(btn_zoom)

        layout.addSpacing(16)
        self.title_lbl = QtWidgets.QLabel("ChimeraX", self)
        self.title_lbl.setStyleSheet("color: #1D1D1F; font-size: 13px; font-weight: 600; background: transparent; border: none;")
        layout.addWidget(self.title_lbl)
        layout.addStretch()

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
        self.setFixedHeight(26)
        self.setStyleSheet("background-color: #F2F2F7; border-bottom: 1px solid rgba(0, 0, 0, 0.08);")
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(6)
        btn_close = QtWidgets.QPushButton(self)
        btn_close.setFixedSize(11, 11)
        btn_close.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("QPushButton { background-color: #FF5F56; border: 1px solid #E0443E; border-radius: 5.5px; } QPushButton:hover { background-color: #FF3B30; }")
        btn_close.clicked.connect(self.dock.close)
        layout.addWidget(btn_close)
        btn_min = QtWidgets.QPushButton(self)
        btn_min.setFixedSize(11, 11)
        btn_min.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_min.setStyleSheet("QPushButton { background-color: #FFBD2E; border: 1px solid #DEA123; border-radius: 5.5px; } QPushButton:hover { background-color: #FF9500; }")
        def toggle_min():
            w = self.dock.widget()
            if w:
                w.setVisible(not w.isVisible())
        btn_min.clicked.connect(toggle_min)
        layout.addWidget(btn_min)
        btn_zoom = QtWidgets.QPushButton(self)
        btn_zoom.setFixedSize(11, 11)
        btn_zoom.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_zoom.setStyleSheet("QPushButton { background-color: #27C93F; border: 1px solid #1AAB29; border-radius: 5.5px; } QPushButton:hover { background-color: #34C759; }")
        def toggle_float():
            self.dock.setFloating(not self.dock.isFloating())
        btn_zoom.clicked.connect(toggle_float)
        layout.addWidget(btn_zoom)
        self.label = QtWidgets.QLabel(self.dock.windowTitle(), self)
        self.label.setStyleSheet("color: #1D1D1F; font-size: 11px; font-weight: 600; padding-left: 6px; background: transparent; border: none;")
        layout.addWidget(self.label)
        layout.addStretch()
        self.dock.windowTitleChanged.connect(self.label.setText)

def install_dock_traffic_lights(session=None):
    if not session or not hasattr(session, "ui") or not hasattr(session.ui, "main_window"):
        return
    win = session.ui.main_window
    if not win:
        return
    for dw in win.findChildren(QtWidgets.QDockWidget):
        if not getattr(dw, "_mac_dock_styled", False):
            title_bar = MacDockTitleBar(dw)
            dw.setTitleBarWidget(title_bar)
            dw._mac_dock_styled = True

try:
    from chimerax.ui.gui import _Qt
    if not hasattr(_Qt, "_mac_dock_patched"):
        _orig_qt_init = _Qt.__init__
        def _mac_qt_init(self, tool_window, title, has_statusbar, hide_title_bar, main_window, close_destroys):
            _orig_qt_init(self, tool_window, title, has_statusbar, hide_title_bar, main_window, close_destroys)
            if not hide_title_bar and hasattr(self, "dock_widget"):
                title_bar = MacDockTitleBar(self.dock_widget)
                self.dock_widget.setTitleBarWidget(title_bar)
                self.dock_widget._mac_dock_styled = True
        _Qt.__init__ = _mac_qt_init
        _Qt._mac_dock_patched = True
except Exception:
    pass

def install_window_traffic_lights(session=None):
    if not session or not hasattr(session, "ui") or not hasattr(session.ui, "main_window"):
        return
    win = session.ui.main_window
    if not win or getattr(win, "_mac_frameless_installed", False):
        return
    flags = win.windowFlags()
    win.setWindowFlags(flags | QtCore.Qt.WindowType.FramelessWindowHint)
    win.show()
    header = MacWindowHeader(win)
    mb = win.menuBar()
    top_container = QtWidgets.QWidget(win)
    top_container._is_mac_top = True
    vbox = QtWidgets.QVBoxLayout(top_container)
    vbox.setContentsMargins(0, 0, 0, 0)
    vbox.setSpacing(0)
    vbox.addWidget(header)
    if mb:
        vbox.addWidget(mb)
    win.setMenuWidget(top_container)
    resize_filter = MacWindowResizeFilter(win)
    win.installEventFilter(resize_filter)
    win._mac_resize_filter = resize_filter
    win._mac_frameless_installed = True

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
                icon_path = resolve_mac_icon(bi.title, getattr(bi, "description", ""), sec_name, tab_name)
                if icon_path and os.path.exists(icon_path):
                    bi.icon = QtGui.QIcon(icon_path)
                    bi.highlight_icon = None
                    modified = True
            if modified and hasattr(section, "_redo_layout"):
                try:
                    section._redo_layout()
                except Exception:
                    pass
    for b in ttb.findChildren(QtWidgets.QToolButton):
        b.setIconSize(QtCore.QSize(28, 28))
        b.update()

MACOS_LIGHT_PRO_QSS = """
QWidget {
    font-family: "SF Pro Text", "Helvetica Neue", "Helvetica", -apple-system, sans-serif;
    font-size: 12px;
    color: #1D1D1F;
    selection-background-color: rgba(0, 122, 255, 0.35);
    selection-color: #000000;
    outline: none;
}
QMainWindow {
    background-color: #F5F5F7;
}
QMenuBar {
    background: #F5F5F7;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    padding: 3px 6px;
    color: #1D1D1F;
}
QMenuBar::item {
    background: transparent;
    padding: 4px 10px;
    border-radius: 5px;
    font-weight: 500;
}
QMenuBar::item:selected {
    background: rgba(0, 0, 0, 0.06);
    color: #000000;
}
QMenu {
    background-color: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(0, 0, 0, 0.12);
    border-radius: 10px;
    padding: 5px;
}
QMenu::item {
    padding: 6px 24px 6px 12px;
    border-radius: 6px;
    color: #1D1D1F;
}
QMenu::item:selected {
    background-color: #007AFF;
    color: #FFFFFF;
}
QMenu::separator {
    height: 1px;
    background: rgba(0, 0, 0, 0.08);
    margin: 4px 6px;
}
QDockWidget {
    background-color: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    margin: 3px;
}
QDockWidget::title {
    text-align: left;
    background: #F2F2F7;
    padding: 4px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
QDockWidget::close-button, QDockWidget::float-button {
    width: 0px;
    height: 0px;
    margin: 0px;
    padding: 0px;
    border: none;
    background: transparent;
}
QTreeView, QListView, QTableView {
    background-color: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 4px;
    color: #1D1D1F;
    alternate-background-color: rgba(0, 0, 0, 0.02);
}
QTreeView::item, QListView::item {
    padding: 4px 6px;
    border-radius: 6px;
}
QTreeView::item:hover, QListView::item:hover {
    background: rgba(0, 0, 0, 0.04);
    color: #000000;
}
QTreeView::item:selected, QListView::item:selected {
    background-color: #007AFF;
    color: #FFFFFF;
}
QPushButton {
    background-color: rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 6px;
    padding: 4px 12px;
    color: #1D1D1F;
    font-weight: 500;
    font-size: 11px;
}
QPushButton:hover {
    background-color: rgba(0, 0, 0, 0.09);
    border: 1px solid rgba(0, 0, 0, 0.16);
}
QTextEdit, QPlainTextEdit {
    background-color: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    padding: 8px;
    color: #1D1D1F;
    font-family: "SF Mono", "JetBrains Mono", "Consolas", monospace;
    font-size: 11px;
}
QLineEdit {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 12px;
    padding: 6px 14px;
    color: #1D1D1F;
    font-family: "SF Mono", "JetBrains Mono", "Consolas", monospace;
    font-size: 12px;
    selection-background-color: #007AFF;
}
QLineEdit:focus {
    border: 1.5px solid #007AFF;
    background: #FFFFFF;
}
QStatusBar {
    background: #F5F5F7;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    color: rgba(60, 60, 67, 0.7);
    font-size: 11px;
}
QScrollBar:vertical {
    width: 6px;
    background: transparent;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 0.2);
    min-height: 24px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(0, 0, 0, 0.4);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
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
    app.setStyle("Fusion")
    font = QtGui.QFont("SF Pro Text", 11)
    if not font.exactMatch():
        font = QtGui.QFont("Helvetica Neue", 11)
    if not font.exactMatch():
        font = QtGui.QFont("Helvetica", 11)
    font.setStyleHint(QtGui.QFont.StyleHint.SansSerif)
    app.setFont(font)
    app.setStyleSheet(MACOS_LIGHT_PRO_QSS)

    install_window_traffic_lights(session)
    install_dock_traffic_lights(session)

    QtCore.QTimer.singleShot(100, lambda: install_dock_traffic_lights(session))
    QtCore.QTimer.singleShot(300, lambda: install_dock_traffic_lights(session))
    QtCore.QTimer.singleShot(600, lambda: install_dock_traffic_lights(session))

    apply_mac_icons_to_all_tabs(session)
    QtCore.QTimer.singleShot(80, lambda: apply_mac_icons_to_all_tabs(session))
    QtCore.QTimer.singleShot(300, lambda: apply_mac_icons_to_all_tabs(session))
    QtCore.QTimer.singleShot(600, lambda: apply_mac_icons_to_all_tabs(session))

    for tw in app.findChildren(QtWidgets.QTabWidget):
        try:
            tw.currentChanged.connect(lambda idx: QtCore.QTimer.singleShot(50, lambda: apply_mac_icons_to_all_tabs(session)))
        except Exception:
            pass

    configure_3d_canvas(session)

    if session and hasattr(session, "triggers") and not getattr(session, "_mac_triggers_added", False):
        def on_session_restored(*args):
            QtCore.QTimer.singleShot(100, lambda: configure_3d_canvas(session))
            QtCore.QTimer.singleShot(150, lambda: apply_mac_icons_to_all_tabs(session))
            QtCore.QTimer.singleShot(200, lambda: install_dock_traffic_lights(session))
        try:
            session.triggers.add_handler("end restore session", on_session_restored)
            session.triggers.add_handler("session open", on_session_restored)
            session.triggers.add_handler("open models", on_session_restored)
            session._mac_triggers_added = True
        except Exception:
            pass

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

try:
    cmd_desc = CmdDesc(
        optional=[("mode", StringArg)],
        synopsis="macOS Sequoia Light Pro Mode"
    )
    register("liquidglass", cmd_desc, liquidglass_cmd)
except Exception:
    pass

current_session = globals().get("session", None)
apply_theme(current_session, mode="light")
