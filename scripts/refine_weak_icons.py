import os
import io
import math
import base64
import shutil
from PIL import Image, ImageDraw
S = 512
OUT_S = 128
C_DARK = (58, 58, 60, 255)
C_WHITE = (255, 255, 255, 255)
C_BLUE = (142, 197, 252, 255)
C_CORAL = (255, 154, 162, 255)
C_RED_SLASH = (224, 82, 99, 255)
C_MINT = (181, 234, 215, 255)
C_YELLOW = (255, 243, 176, 255)
C_GOLD = (255, 214, 112, 255)
C_PEACH = (255, 218, 193, 255)
C_LAV = (226, 209, 249, 255)
C_CYAN = (160, 231, 229, 255)
C_MUTED_BLUE = (205, 226, 248, 255)
C_MUTED_CORAL = (252, 205, 210, 255)
C_MUTED_MINT = (210, 240, 228, 255)
def new_canvas():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)
def circle(d, cx, cy, r, fill=None, outline=C_DARK, width=14):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)
def rrect(d, box, rad, fill=None, outline=C_DARK, width=14):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)
def line_cap(d, p1, p2, fill=C_DARK, width=16):
    d.line([p1, p2], fill=fill, width=width)
    r = width / 2.0 - 1
    x1, y1 = p1
    x2, y2 = p2
    d.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=fill)
    d.ellipse([x2 - r, y2 - r, x2 + r, y2 + r], fill=fill)
def arrow_head(d, tip, angle_deg, size=44, fill=C_DARK):
    tx, ty = tip
    rad = math.radians(angle_deg)
    a1 = rad + math.radians(145)
    a2 = rad - math.radians(145)
    p1 = (tx + size * math.cos(a1), ty + size * math.sin(a1))
    p2 = (tx + size * math.cos(a2), ty + size * math.sin(a2))
    d.polygon([tip, p1, p2], fill=fill)
def draw_slash(d):
    line_cap(d, (96, 416), (416, 96), fill=C_WHITE, width=34)
    line_cap(d, (96, 416), (416, 96), fill=C_RED_SLASH, width=20)
def icon_open_in_app():
    img, d = new_canvas()
    rrect(d, [64, 120, 448, 416], 36, fill=C_PEACH, outline=C_DARK, width=14)
    d.polygon([(64, 170), (210, 170), (246, 120), (100, 120)], fill=C_YELLOW, outline=C_DARK)
    rrect(d, [64, 195, 448, 416], 34, fill=C_YELLOW, outline=C_DARK, width=14)
    line_cap(d, (256, 360), (256, 225), fill=C_DARK, width=22)
    arrow_head(d, (256, 200), -90, size=58, fill=C_BLUE)
    d.polygon([(256, 200), (212, 252), (300, 252)], fill=C_BLUE, outline=C_DARK, width=12)
    return img
def icon_video():
    img, d = new_canvas()
    circle(d, 155, 145, 52, fill=C_LAV, outline=C_DARK, width=14)
    circle(d, 275, 145, 52, fill=C_MINT, outline=C_DARK, width=14)
    d.polygon([(350, 240), (456, 185), (456, 365), (350, 310)], fill=C_PEACH, outline=C_DARK, width=14)
    rrect(d, [76, 195, 360, 375], 36, fill=C_BLUE, outline=C_DARK, width=14)
    d.arc([155, 225, 285, 345], start=30, end=300, fill=C_WHITE, width=18)
    d.arc([155, 225, 285, 345], start=30, end=300, fill=C_DARK, width=14)
    arrow_head(d, (274, 245), -40, size=40, fill=C_CORAL)
    return img
def icon_atomhide():
    img, d = new_canvas()
    line_cap(d, (150, 330), (256, 170), fill=C_DARK, width=18)
    line_cap(d, (256, 170), (362, 330), fill=C_DARK, width=18)
    circle(d, 256, 170, 54, fill=C_MUTED_BLUE, outline=C_DARK, width=14)
    circle(d, 150, 330, 50, fill=C_MUTED_MINT, outline=C_DARK, width=14)
    circle(d, 362, 330, 50, fill=C_MUTED_CORAL, outline=C_DARK, width=14)
    draw_slash(d)
    return img
def _draw_helix_ribbon(d, c_front, c_back):
    pts_back1 = [(85, 340), (165, 170), (225, 170), (145, 340)]
    pts_back2 = [(235, 340), (315, 170), (375, 170), (295, 340)]
    d.polygon(pts_back1, fill=c_back, outline=C_DARK, width=12)
    d.polygon(pts_back2, fill=c_back, outline=C_DARK, width=12)
    pts_front1 = [(145, 340), (225, 340), (315, 170), (235, 170)]
    pts_front2 = [(295, 340), (375, 340), (435, 220), (365, 220)]
    d.polygon(pts_front1, fill=c_front, outline=C_DARK, width=14)
    d.polygon(pts_front2, fill=c_front, outline=C_DARK, width=14)
    d.polygon([(395, 185), (455, 235), (380, 265)], fill=C_PEACH, outline=C_DARK, width=12)
def icon_ribshow():
    img, d = new_canvas()
    _draw_helix_ribbon(d, C_BLUE, C_MINT)
    return img
def icon_ribhide():
    img, d = new_canvas()
    _draw_helix_ribbon(d, C_MUTED_BLUE, C_MUTED_MINT)
    draw_slash(d)
    return img
def icon_surfhide():
    img, d = new_canvas()
    circle(d, 210, 275, 98, fill=C_MUTED_MINT, outline=C_DARK, width=14)
    circle(d, 310, 240, 86, fill=C_LAV, outline=C_DARK, width=14)
    circle(d, 270, 325, 76, fill=C_MUTED_BLUE, outline=C_DARK, width=14)
    draw_slash(d)
    return img
def icon_stick():
    img, d = new_canvas()
    d.polygon([(90, 355), (245, 200), (275, 230), (120, 385)], fill=C_BLUE, outline=C_DARK, width=14)
    d.polygon([(245, 200), (405, 355), (375, 385), (215, 230)], fill=C_CORAL, outline=C_DARK, width=14)
    d.polygon([(235, 210), (235, 90), (277, 90), (277, 210)], fill=C_MINT, outline=C_DARK, width=14)
    circle(d, 256, 215, 28, fill=C_YELLOW, outline=C_DARK, width=12)
    return img
def icon_simplelight():
    img, d = new_canvas()
    for i in range(8):
        ang = math.radians(i * 45)
        p1 = (256 + 125 * math.cos(ang), 256 + 125 * math.sin(ang))
        p2 = (256 + 185 * math.cos(ang), 256 + 185 * math.sin(ang))
        line_cap(d, p1, p2, fill=C_DARK, width=22)
        line_cap(d, p1, p2, fill=C_GOLD, width=12)
    circle(d, 256, 256, 92, fill=C_YELLOW, outline=C_DARK, width=15)
    return img
def icon_softlight():
    img, d = new_canvas()
    circle(d, 195, 195, 78, fill=C_GOLD, outline=C_DARK, width=14)
    rrect(d, [115, 245, 425, 375], 62, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 220, 245, 68, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 315, 255, 56, fill=C_BLUE, outline=C_DARK, width=14)
    d.rounded_rectangle([128, 255, 412, 362], radius=50, fill=C_BLUE)
    return img
def icon_fulllight():
    img, d = new_canvas()
    for i in range(8):
        ang = math.radians(i * 45)
        p1 = (256 + 135 * math.cos(ang), 256 + 135 * math.sin(ang))
        p2 = (256 + 198 * math.cos(ang), 256 + 198 * math.sin(ang))
        line_cap(d, p1, p2, fill=C_DARK, width=20)
    circle(d, 256, 256, 110, fill=C_GOLD, outline=C_DARK, width=15)
    circle(d, 222, 222, 46, fill=C_WHITE, outline=C_DARK, width=10)
    return img
def icon_flat():
    img, d = new_canvas()
    pts = []
    for i in range(6):
        ang = math.radians(i * 60 - 30)
        pts.append((256 + 160 * math.cos(ang), 256 + 160 * math.sin(ang)))
    d.polygon([ (256, 256), pts[0], pts[1], pts[2] ], fill=C_BLUE, outline=C_DARK, width=14)
    d.polygon([ (256, 256), pts[2], pts[3], pts[4] ], fill=C_MINT, outline=C_DARK, width=14)
    d.polygon([ (256, 256), pts[4], pts[5], pts[0] ], fill=C_PEACH, outline=C_DARK, width=14)
    return img
def icon_silhouette():
    img, d = new_canvas()
    circle(d, 256, 256, 152, fill=C_LAV, outline=C_DARK, width=28)
    circle(d, 212, 212, 52, fill=C_BLUE, outline=None, width=0)
    return img
def icon_colorbyelement():
    img, d = new_canvas()
    box = [86, 86, 426, 426]
    d.pieslice(box, 180, 270, fill=C_BLUE, outline=C_DARK, width=14)
    d.pieslice(box, 270, 360, fill=C_CORAL, outline=C_DARK, width=14)
    d.pieslice(box, 0, 90, fill=C_MINT, outline=C_DARK, width=14)
    d.pieslice(box, 90, 180, fill=C_YELLOW, outline=C_DARK, width=14)
    return img
def icon_colorbychain():
    img, d = new_canvas()
    circle(d, 195, 195, 76, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 317, 195, 76, fill=C_CORAL, outline=C_DARK, width=14)
    circle(d, 256, 310, 76, fill=C_MINT, outline=C_DARK, width=14)
    circle(d, 195, 195, 32, fill=C_WHITE, outline=C_DARK, width=12)
    circle(d, 317, 195, 32, fill=C_WHITE, outline=C_DARK, width=12)
    circle(d, 256, 310, 32, fill=C_WHITE, outline=C_DARK, width=12)
    return img
def icon_rainbow():
    img, d = new_canvas()
    d.pieslice([66, 110, 446, 490], 180, 360, fill=C_CORAL, outline=C_DARK, width=14)
    d.pieslice([106, 150, 406, 450], 180, 360, fill=C_YELLOW, outline=C_DARK, width=12)
    d.pieslice([146, 190, 366, 410], 180, 360, fill=C_MINT, outline=C_DARK, width=12)
    d.pieslice([186, 230, 326, 370], 180, 360, fill=C_BLUE, outline=C_DARK, width=12)
    d.pieslice([222, 266, 290, 334], 180, 360, fill=C_WHITE, outline=C_DARK, width=12)
    rrect(d, [50, 295, 462, 345], 22, fill=C_WHITE, outline=C_DARK, width=12)
    return img
def icon_hydrophobicity():
    img, d = new_canvas()
    d.polygon([(145, 120), (80, 260), (210, 260)], fill=C_BLUE, outline=C_DARK, width=14)
    d.pieslice([80, 200, 210, 345], 0, 180, fill=C_BLUE, outline=C_DARK, width=14)
    d.ellipse([94, 215, 196, 330], fill=C_BLUE)
    for y in (120, 210, 300, 390):
        line_cap(d, (256, y), (256, y + 36), fill=C_DARK, width=14)
    circle(d, 368, 256, 76, fill=C_GOLD, outline=C_DARK, width=14)
    return img
def icon_bfactor():
    img, d = new_canvas()
    pts = [(70, 360), (150, 180), (235, 340), (320, 140), (410, 280)]
    for i in range(len(pts) - 1):
        col = C_BLUE if i < 2 else C_CORAL
        line_cap(d, pts[i], pts[i + 1], fill=C_DARK, width=26)
        line_cap(d, pts[i], pts[i + 1], fill=col, width=14)
    circle(d, 150, 180, 36, fill=C_BLUE, outline=C_DARK, width=12)
    circle(d, 320, 140, 44, fill=C_CORAL, outline=C_DARK, width=12)
    d.arc([255, 75, 385, 205], 200, 340, fill=C_DARK, width=12)
    return img
def icon_hbonds():
    img, d = new_canvas()
    for x in (195, 256, 317):
        circle(d, x, 256, 16, fill=C_CYAN, outline=C_DARK, width=10)
    circle(d, 108, 256, 58, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 404, 256, 58, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_hbondshide():
    img = icon_hbonds()
    d = ImageDraw.Draw(img)
    draw_slash(d)
    return img
def icon_nuc_slab():
    img, d = new_canvas()
    line_cap(d, (110, 95), (110, 415), fill=C_DARK, width=20)
    line_cap(d, (402, 95), (402, 415), fill=C_DARK, width=20)
    for y, col in ((130, C_BLUE), (256, C_CORAL), (382, C_MINT)):
        rrect(d, [110, y - 34, 402, y + 34], 14, fill=col, outline=C_DARK, width=14)
    return img
def icon_nuc_box():
    img, d = new_canvas()
    for y, col in ((135, C_CORAL), (256, C_MINT), (377, C_YELLOW)):
        rrect(d, [160, y - 34, 415, y + 34], 12, fill=col, outline=C_DARK, width=14)
    rrect(d, [92, 80, 172, 432], 38, fill=C_BLUE, outline=C_DARK, width=14)
    return img
def icon_nuc_elli():
    img, d = new_canvas()
    for y, col in ((135, C_CORAL), (256, C_MINT), (377, C_LAV)):
        d.ellipse([155, y - 36, 420, y + 36], fill=col, outline=C_DARK, width=14)
    rrect(d, [92, 80, 172, 432], 38, fill=C_BLUE, outline=C_DARK, width=14)
    return img
def icon_nuc_muff():
    img, d = new_canvas()
    for y, col in ((135, C_PEACH), (256, C_CYAN), (377, C_LAV)):
        rrect(d, [155, y - 36, 420, y + 36], 36, fill=col, outline=C_DARK, width=14)
    rrect(d, [92, 80, 172, 432], 38, fill=C_BLUE, outline=C_DARK, width=14)
    return img
def icon_sideview():
    img, d = new_canvas()
    d.polygon([(115, 256), (415, 110), (415, 402)], fill=C_PEACH, outline=C_DARK, width=14)
    line_cap(d, (245, 95), (245, 417), fill=C_BLUE, width=24)
    line_cap(d, (245, 95), (245, 417), fill=C_DARK, width=12)
    line_cap(d, (385, 95), (385, 417), fill=C_BLUE, width=24)
    line_cap(d, (385, 95), (385, 417), fill=C_DARK, width=12)
    rrect(d, [68, 216, 148, 296], 18, fill=C_YELLOW, outline=C_DARK, width=14)
    circle(d, 325, 256, 42, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_viewsel():
    img, d = new_canvas()
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        cx = 256 + sx * 155
        cy = 256 + sy * 155
        line_cap(d, (cx, cy), (cx - sx * 70, cy), fill=C_DARK, width=18)
        line_cap(d, (cx, cy), (cx, cy - sy * 70), fill=C_DARK, width=18)
    circle(d, 256, 256, 78, fill=C_CORAL, outline=C_DARK, width=14)
    circle(d, 256, 256, 28, fill=C_YELLOW, outline=C_DARK, width=12)
    return img
def icon_viewall():
    img, d = new_canvas()
    rrect(d, [76, 76, 436, 436], 42, fill=C_MUTED_BLUE, outline=C_DARK, width=14)
    circle(d, 190, 220, 54, fill=C_CORAL, outline=C_DARK, width=14)
    circle(d, 320, 215, 50, fill=C_MINT, outline=C_DARK, width=14)
    circle(d, 256, 320, 56, fill=C_YELLOW, outline=C_DARK, width=14)
    return img
def icon_orient():
    img, d = new_canvas()
    line_cap(d, (230, 275), (230, 95), fill=C_DARK, width=22)
    arrow_head(d, (230, 75), -90, size=52, fill=C_BLUE)
    line_cap(d, (230, 275), (415, 275), fill=C_DARK, width=22)
    arrow_head(d, (435, 275), 0, size=52, fill=C_CORAL)
    line_cap(d, (230, 275), (105, 400), fill=C_DARK, width=22)
    arrow_head(d, (90, 415), 135, size=52, fill=C_MINT)
    circle(d, 230, 275, 42, fill=C_YELLOW, outline=C_DARK, width=14)
    return img
def icon_mesh():
    img, d = new_canvas()
    circle(d, 256, 256, 162, fill=C_MUTED_BLUE, outline=C_DARK, width=15)
    d.ellipse([160, 94, 352, 418], outline=C_DARK, width=12)
    d.ellipse([94, 160, 418, 352], outline=C_DARK, width=12)
    line_cap(d, (94, 256), (418, 256), fill=C_DARK, width=12)
    line_cap(d, (256, 94), (256, 418), fill=C_DARK, width=12)
    return img
def icon_orthoplanes():
    img, d = new_canvas()
    d.polygon([(256, 75), (425, 165), (256, 256), (87, 165)], fill=C_YELLOW, outline=C_DARK, width=14)
    d.polygon([(87, 165), (256, 256), (256, 435), (87, 345)], fill=C_BLUE, outline=C_DARK, width=14)
    d.polygon([(256, 256), (425, 165), (425, 345), (256, 435)], fill=C_MINT, outline=C_DARK, width=14)
    return img
def icon_fitmap():
    img, d = new_canvas()
    rrect(d, [82, 110, 430, 402], 95, fill=C_LAV, outline=C_DARK, width=14)
    line_cap(d, (160, 310), (256, 190), fill=C_DARK, width=20)
    line_cap(d, (256, 190), (352, 310), fill=C_DARK, width=20)
    circle(d, 160, 310, 40, fill=C_BLUE, outline=C_DARK, width=12)
    circle(d, 256, 190, 44, fill=C_CORAL, outline=C_DARK, width=12)
    circle(d, 352, 310, 40, fill=C_MINT, outline=C_DARK, width=12)
    return img
def icon_smooth():
    img, d = new_canvas()
    pts = [(76, 385)]
    for x in range(76, 437, 12):
        t = (x - 256) / 95.0
        y = 385 - int(245 * math.exp(-t * t))
        pts.append((x, y))
    pts.append((436, 385))
    d.polygon(pts, fill=C_MINT, outline=C_DARK, width=15)
    return img
def icon_airways():
    img, d = new_canvas()
    d.ellipse([82, 150, 238, 415], fill=C_CYAN, outline=C_DARK, width=14)
    d.ellipse([274, 150, 430, 415], fill=C_CYAN, outline=C_DARK, width=14)
    line_cap(d, (256, 85), (256, 235), fill=C_DARK, width=26)
    line_cap(d, (256, 235), (170, 315), fill=C_DARK, width=22)
    line_cap(d, (256, 235), (342, 315), fill=C_DARK, width=22)
    return img
def icon_chest():
    img, d = new_canvas()
    rrect(d, [96, 88, 416, 424], 70, fill=C_PEACH, outline=C_DARK, width=14)
    line_cap(d, (256, 100), (256, 410), fill=C_DARK, width=22)
    for y in (165, 235, 305, 365):
        line_cap(d, (130, y), (382, y), fill=C_CORAL, width=26)
        line_cap(d, (130, y), (382, y), fill=C_DARK, width=14)
    return img
def icon_brain():
    img, d = new_canvas()
    circle(d, 205, 225, 95, fill=C_CORAL, outline=C_DARK, width=14)
    circle(d, 305, 225, 95, fill=C_LAV, outline=C_DARK, width=14)
    circle(d, 256, 305, 85, fill=C_PEACH, outline=C_DARK, width=14)
    d.arc([155, 175, 265, 285], 20, 210, fill=C_DARK, width=12)
    d.arc([255, 175, 365, 285], 330, 160, fill=C_DARK, width=12)
    return img
def icon_initialcurve():
    img, d = new_canvas()
    rrect(d, [76, 76, 436, 436], 32, fill=C_MUTED_BLUE, outline=C_DARK, width=14)
    pts = []
    for x in range(105, 410, 15):
        t = (x - 256) / 45.0
        s = 1.0 / (1.0 + math.exp(-t))
        y = int(375 - 235 * s)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        line_cap(d, pts[i], pts[i + 1], fill=C_CORAL, width=24)
        line_cap(d, pts[i], pts[i + 1], fill=C_DARK, width=14)
    return img
def icon_moveplanes():
    img, d = new_canvas()
    d.polygon([(110, 310), (256, 245), (402, 310), (256, 375)], fill=C_MINT, outline=C_DARK, width=14)
    d.polygon([(110, 205), (256, 140), (402, 205), (256, 270)], fill=C_BLUE, outline=C_DARK, width=14)
    line_cap(d, (256, 75), (256, 435), fill=C_DARK, width=18)
    arrow_head(d, (256, 60), -90, size=48, fill=C_CORAL)
    arrow_head(d, (256, 450), 90, size=48, fill=C_CORAL)
    return img
def icon_rotateslab():
    img, d = new_canvas()
    d.polygon([(95, 265), (285, 155), (417, 245), (227, 355)], fill=C_LAV, outline=C_DARK, width=14)
    d.arc([85, 85, 427, 427], 200, 340, fill=C_DARK, width=16)
    arrow_head(d, (405, 195), 45, size=48, fill=C_BLUE)
    return img
def icon_tape():
    img, d = new_canvas()
    rrect(d, [64, 175, 448, 337], 26, fill=C_YELLOW, outline=C_DARK, width=14)
    for x in range(120, 410, 54):
        h = 65 if ((x - 120) // 54) % 2 == 0 else 42
        line_cap(d, (x, 180), (x, 180 + h), fill=C_DARK, width=14)
    return img
def icon_mark_maximum():
    img, d = new_canvas()
    d.polygon([(76, 405), (256, 155), (436, 405)], fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 256, 145, 56, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_mark_plane():
    img, d = new_canvas()
    d.polygon([(76, 305), (256, 210), (436, 305), (256, 400)], fill=C_MINT, outline=C_DARK, width=14)
    line_cap(d, (256, 165), (256, 295), fill=C_DARK, width=18)
    circle(d, 256, 155, 56, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_mark_surface():
    img, d = new_canvas()
    d.pieslice([76, 200, 436, 520], 180, 360, fill=C_CYAN, outline=C_DARK, width=14)
    circle(d, 256, 175, 56, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_mark_center():
    img, d = new_canvas()
    circle(d, 256, 256, 160, fill=C_MUTED_BLUE, outline=C_DARK, width=14)
    circle(d, 256, 256, 105, fill=C_LAV, outline=C_DARK, width=12)
    circle(d, 256, 256, 52, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_mark_point():
    img, d = new_canvas()
    line_cap(d, (76, 256), (436, 256), fill=C_DARK, width=18)
    line_cap(d, (256, 76), (256, 436), fill=C_DARK, width=18)
    circle(d, 256, 256, 64, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_mark_link():
    img, d = new_canvas()
    rrect(d, [130, 224, 382, 288], 20, fill=C_YELLOW, outline=C_DARK, width=14)
    circle(d, 130, 256, 62, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 382, 256, 62, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_mark_move():
    img, d = new_canvas()
    line_cap(d, (256, 80), (256, 432), fill=C_DARK, width=18)
    line_cap(d, (80, 256), (432, 256), fill=C_DARK, width=18)
    arrow_head(d, (256, 64), -90, size=44, fill=C_DARK)
    arrow_head(d, (256, 448), 90, size=44, fill=C_DARK)
    arrow_head(d, (64, 256), 180, size=44, fill=C_DARK)
    arrow_head(d, (448, 256), 0, size=44, fill=C_DARK)
    circle(d, 256, 256, 64, fill=C_BLUE, outline=C_DARK, width=14)
    return img
def icon_mark_resize():
    img, d = new_canvas()
    circle(d, 256, 256, 148, fill=C_MUTED_BLUE, outline=C_DARK, width=14)
    line_cap(d, (135, 377), (377, 135), fill=C_DARK, width=18)
    arrow_head(d, (392, 120), -45, size=46, fill=C_DARK)
    circle(d, 256, 256, 58, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_mark_delete():
    img, d = new_canvas()
    circle(d, 225, 245, 96, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 335, 335, 68, fill=C_CORAL, outline=C_DARK, width=14)
    line_cap(d, (305, 305), (365, 365), fill=C_DARK, width=18)
    line_cap(d, (365, 305), (305, 365), fill=C_DARK, width=18)
    return img
def icon_select():
    img, d = new_canvas()
    rrect(d, [185, 185, 425, 425], 28, fill=C_MUTED_BLUE, outline=C_DARK, width=14)
    pts = [(95, 85), (95, 335), (168, 275), (225, 390), (272, 368), (215, 255), (305, 255)]
    d.polygon(pts, fill=C_YELLOW, outline=C_DARK, width=14)
    return img
def icon_rotate():
    img, d = new_canvas()
    circle(d, 256, 256, 148, fill=C_MUTED_BLUE, outline=C_DARK, width=15)
    arrow_head(d, (392, 195), 65, size=54, fill=C_DARK)
    circle(d, 256, 256, 58, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_translate():
    img, d = new_canvas()
    line_cap(d, (256, 76), (256, 436), fill=C_DARK, width=22)
    line_cap(d, (76, 256), (436, 256), fill=C_DARK, width=22)
    for pt, ang in (((256, 58), -90), ((256, 454), 90), ((58, 256), 180), ((454, 256), 0)):
        arrow_head(d, pt, ang, size=52, fill=C_BLUE)
    circle(d, 256, 256, 42, fill=C_YELLOW, outline=C_DARK, width=14)
    return img
def icon_move_picked_model():
    img, d = new_canvas()
    rrect(d, [136, 136, 376, 376], 36, fill=C_BLUE, outline=C_DARK, width=14)
    line_cap(d, (256, 70), (256, 442), fill=C_DARK, width=18)
    line_cap(d, (70, 256), (442, 256), fill=C_DARK, width=18)
    arrow_head(d, (256, 55), -90, size=44, fill=C_CORAL)
    arrow_head(d, (457, 256), 0, size=44, fill=C_CORAL)
    return img
def icon_rotatesel():
    img, d = new_canvas()
    d.arc([76, 76, 436, 436], 200, 120, fill=C_DARK, width=18)
    arrow_head(d, (410, 180), 55, size=50, fill=C_DARK)
    rrect(d, [156, 156, 356, 356], 36, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_drag_model():
    img, d = new_canvas()
    rrect(d, [110, 150, 350, 390], 36, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 355, 155, 58, fill=C_PEACH, outline=C_DARK, width=14)
    line_cap(d, (255, 255), (355, 155), fill=C_DARK, width=18)
    return img
def icon_move_atoms():
    img, d = new_canvas()
    line_cap(d, (140, 350), (256, 165), fill=C_DARK, width=20)
    line_cap(d, (256, 165), (372, 350), fill=C_DARK, width=20)
    circle(d, 140, 350, 48, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 372, 350, 48, fill=C_MINT, outline=C_DARK, width=14)
    circle(d, 256, 165, 56, fill=C_CORAL, outline=C_DARK, width=14)
    arrow_head(d, (256, 68), -90, size=48, fill=C_DARK)
    return img
def icon_pivot():
    img, d = new_canvas()
    circle(d, 256, 256, 148, fill=C_LAV, outline=C_DARK, width=14)
    line_cap(d, (76, 256), (436, 256), fill=C_DARK, width=16)
    line_cap(d, (256, 76), (256, 436), fill=C_DARK, width=16)
    circle(d, 256, 256, 56, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_distance():
    img, d = new_canvas()
    line_cap(d, (130, 256), (382, 256), fill=C_DARK, width=20)
    for x in (200, 256, 312):
        line_cap(d, (x, 220), (x, 292), fill=C_DARK, width=14)
    circle(d, 115, 256, 56, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 397, 256, 56, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_label():
    img, d = new_canvas()
    d.polygon([(86, 130), (350, 130), (430, 256), (350, 382), (86, 382)], fill=C_YELLOW, outline=C_DARK, width=14)
    circle(d, 345, 256, 26, fill=C_BLUE, outline=C_DARK, width=12)
    line_cap(d, (145, 220), (265, 220), fill=C_DARK, width=16)
    line_cap(d, (145, 290), (235, 290), fill=C_DARK, width=16)
    return img
def icon_movelabel():
    img, d = new_canvas()
    rrect(d, [76, 140, 330, 360], 28, fill=C_YELLOW, outline=C_DARK, width=14)
    line_cap(d, (130, 220), (270, 220), fill=C_DARK, width=16)
    line_cap(d, (130, 280), (230, 280), fill=C_DARK, width=16)
    line_cap(d, (385, 130), (385, 380), fill=C_DARK, width=18)
    arrow_head(d, (385, 110), -90, size=44, fill=C_CORAL)
    arrow_head(d, (385, 400), 90, size=44, fill=C_CORAL)
    return img
def icon_ckicon():
    img, d = new_canvas()
    cols = (C_BLUE, C_MINT, C_YELLOW, C_CORAL)
    for i, c in enumerate(cols):
        x0 = 76 + i * 90
        rrect(d, [x0, 165, x0 + 90, 347], 12, fill=c, outline=C_DARK, width=14)
    return img
def icon_zone():
    img, d = new_canvas()
    circle(d, 256, 256, 156, fill=C_MINT, outline=C_DARK, width=14)
    circle(d, 256, 256, 62, fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_vseries():
    img, d = new_canvas()
    rrect(d, [76, 110, 436, 402], 32, fill=C_LAV, outline=C_DARK, width=14)
    d.polygon([(205, 175), (205, 337), (345, 256)], fill=C_MINT, outline=C_DARK, width=14)
    return img
def icon_bondrot():
    img, d = new_canvas()
    rrect(d, [96, 224, 416, 288], 22, fill=C_PEACH, outline=C_DARK, width=14)
    d.arc([165, 115, 347, 397], 210, 150, fill=C_DARK, width=18)
    arrow_head(d, (335, 170), 45, size=48, fill=C_CORAL)
    return img
def icon_coordset():
    img, d = new_canvas()
    rrect(d, [86, 120, 346, 380], 28, fill=C_BLUE, outline=C_DARK, width=14)
    rrect(d, [146, 140, 416, 400], 28, fill=C_MINT, outline=C_DARK, width=14)
    d.polygon([(235, 200), (235, 340), (355, 270)], fill=C_YELLOW, outline=C_DARK, width=14)
    return img
def icon_tug():
    img, d = new_canvas()
    circle(d, 155, 256, 68, fill=C_CORAL, outline=C_DARK, width=14)
    line_cap(d, (225, 256), (415, 256), fill=C_DARK, width=22)
    arrow_head(d, (440, 256), 0, size=56, fill=C_BLUE)
    return img
def icon_minimize():
    img, d = new_canvas()
    pts = []
    for x in range(86, 427, 12):
        t = (x - 256) / 155.0
        y = int(120 + 260 * (1.0 - t * t))
        pts.append((x, y))
    for i in range(len(pts) - 1):
        line_cap(d, pts[i], pts[i + 1], fill=C_DARK, width=20)
    circle(d, 256, 345, 56, fill=C_MINT, outline=C_DARK, width=14)
    return img
def icon_nextdocking():
    img, d = new_canvas()
    d.pieslice([76, 130, 356, 410], 45, 315, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 285, 270, 54, fill=C_CORAL, outline=C_DARK, width=14)
    arrow_head(d, (440, 270), 0, size=56, fill=C_MINT)
    return img
def icon_close_box():
    img, d = new_canvas()
    rrect(d, [92, 92, 420, 420], 68, fill=C_CORAL, outline=C_DARK, width=16)
    line_cap(d, (176, 176), (336, 336), fill=C_DARK, width=38)
    line_cap(d, (336, 176), (176, 336), fill=C_DARK, width=38)
    line_cap(d, (176, 176), (336, 336), fill=C_WHITE, width=20)
    line_cap(d, (336, 176), (176, 336), fill=C_WHITE, width=20)
    return img
def icon_content_save():
    img, d = new_canvas()
    d.polygon([(92, 92), (356, 92), (420, 156), (420, 420), (92, 420)], fill=C_BLUE, outline=C_DARK, width=16)
    rrect(d, [152, 92, 332, 212], 20, fill=C_WHITE, outline=C_DARK, width=14)
    rrect(d, [264, 114, 304, 190], 10, fill=C_CORAL, outline=C_DARK, width=10)
    rrect(d, [136, 268, 376, 420], 24, fill=C_YELLOW, outline=C_DARK, width=14)
    line_cap(d, (184, 320), (328, 320), fill=C_DARK, width=14)
    line_cap(d, (184, 366), (296, 366), fill=C_DARK, width=14)
    return img
def icon_undo_variant():
    img, d = new_canvas()
    d.arc([104, 148, 424, 428], start=215, end=45, fill=C_DARK, width=44)
    d.arc([104, 148, 424, 428], start=215, end=45, fill=C_BLUE, width=22)
    d.polygon([(96, 232), (208, 138), (222, 266)], fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_redo_variant():
    img, d = new_canvas()
    d.arc([88, 148, 408, 428], start=135, end=325, fill=C_DARK, width=44)
    d.arc([88, 148, 408, 428], start=135, end=325, fill=C_MINT, width=22)
    d.polygon([(416, 232), (304, 138), (290, 266)], fill=C_CORAL, outline=C_DARK, width=14)
    return img
def icon_crop():
    img, d = new_canvas()
    rrect(d, [148, 148, 364, 364], 20, fill=C_MINT, outline=C_DARK, width=14)
    line_cap(d, (156, 356), (356, 156), fill=C_WHITE, width=14)
    line_cap(d, (148, 76), (148, 364), fill=C_DARK, width=32)
    line_cap(d, (148, 364), (436, 364), fill=C_DARK, width=32)
    line_cap(d, (148, 76), (148, 364), fill=C_GOLD, width=16)
    line_cap(d, (148, 364), (436, 364), fill=C_GOLD, width=16)
    line_cap(d, (76, 148), (364, 148), fill=C_DARK, width=32)
    line_cap(d, (364, 148), (364, 436), fill=C_DARK, width=32)
    line_cap(d, (76, 148), (364, 148), fill=C_CORAL, width=16)
    line_cap(d, (364, 148), (364, 436), fill=C_CORAL, width=16)
    return img
def icon_zoom():
    img, d = new_canvas()
    line_cap(d, (295, 295), (426, 426), fill=C_DARK, width=48)
    line_cap(d, (295, 295), (426, 426), fill=C_CORAL, width=26)
    circle(d, 216, 216, 122, fill=C_CYAN, outline=C_DARK, width=16)
    circle(d, 216, 216, 92, fill=C_WHITE, outline=C_DARK, width=12)
    line_cap(d, (168, 216), (264, 216), fill=C_DARK, width=22)
    line_cap(d, (216, 168), (216, 264), fill=C_DARK, width=22)
    return img
def icon_outlinebox():
    img, d = new_canvas()
    top_pts = [(256, 76), (420, 162), (256, 248), (92, 162)]
    left_pts = [(92, 162), (256, 248), (256, 436), (92, 350)]
    right_pts = [(256, 248), (420, 162), (420, 350), (256, 436)]
    d.polygon(top_pts, fill=(160, 231, 229, 75), outline=C_DARK, width=14)
    d.polygon(left_pts, fill=(142, 197, 252, 75), outline=C_DARK, width=14)
    d.polygon(right_pts, fill=(226, 209, 249, 75), outline=C_DARK, width=14)
    for p1, p2 in [
        ((256, 76), (420, 162)),
        ((420, 162), (256, 248)),
        ((256, 248), (92, 162)),
        ((92, 162), (256, 76)),
        ((92, 162), (92, 350)),
        ((420, 162), (420, 350)),
        ((256, 248), (256, 436)),
        ((92, 350), (256, 436)),
        ((420, 350), (256, 436)),
    ]:
        line_cap(d, p1, p2, fill=C_DARK, width=20)
        line_cap(d, p1, p2, fill=C_CYAN, width=10)
    for vx, vy, vc in [
        (256, 76, C_YELLOW),
        (420, 162, C_CORAL),
        (92, 162, C_MINT),
        (256, 248, C_WHITE),
        (92, 350, C_BLUE),
        (420, 350, C_LAV),
        (256, 436, C_PEACH),
    ]:
        circle(d, vx, vy, 20, fill=vc, outline=C_DARK, width=10)
    return img
def icon_mouse():
    img, d = new_canvas()
    rrect(d, [136, 72, 376, 440], 120, fill=C_WHITE, outline=C_DARK, width=16)
    d.pieslice([136, 72, 376, 312], start=180, end=270, fill=C_BLUE, outline=C_DARK, width=14)
    d.pieslice([136, 72, 376, 312], start=270, end=360, fill=C_MINT, outline=C_DARK, width=14)
    line_cap(d, (136, 212), (376, 212), fill=C_DARK, width=14)
    rrect(d, [234, 128, 278, 204], 22, fill=C_CORAL, outline=C_DARK, width=12)
    return img
def icon_right_controller():
    img, d = new_canvas()
    circle(d, 256, 176, 98, fill=C_CYAN, outline=C_DARK, width=16)
    circle(d, 256, 176, 52, fill=(0, 0, 0, 0), outline=C_DARK, width=14)
    rrect(d, [206, 224, 306, 436], 48, fill=C_LAV, outline=C_DARK, width=16)
    circle(d, 256, 274, 28, fill=C_CORAL, outline=C_DARK, width=12)
    circle(d, 256, 344, 18, fill=C_YELLOW, outline=C_DARK, width=10)
    return img
def icon_eraser():
    img, d = new_canvas()
    line_cap(d, (120, 404), (408, 404), fill=C_DARK, width=26)
    line_cap(d, (120, 404), (408, 404), fill=C_MINT, width=14)
    pts_pink = [(116, 312), (232, 196), (332, 296), (216, 412)]
    pts_blue = [(232, 196), (324, 104), (424, 204), (332, 296)]
    d.polygon(pts_pink, fill=C_CORAL, outline=C_DARK, width=16)
    d.polygon(pts_blue, fill=C_BLUE, outline=C_DARK, width=16)
    return img
def icon_pickblobs():
    img, d = new_canvas()
    circle(d, 190, 250, 88, fill=C_MINT, outline=C_DARK, width=14)
    circle(d, 286, 290, 78, fill=C_BLUE, outline=C_DARK, width=14)
    circle(d, 266, 180, 74, fill=C_CORAL, outline=C_DARK, width=16)
    line_cap(d, (310, 148), (424, 76), fill=C_DARK, width=26)
    line_cap(d, (310, 148), (424, 76), fill=C_YELLOW, width=14)
    circle(d, 266, 180, 24, fill=C_WHITE, outline=C_DARK, width=10)
    return img
def icon_contour():
    img, d = new_canvas()
    d.ellipse([76, 96, 436, 416], fill=C_BLUE, outline=C_DARK, width=15)
    d.ellipse([122, 138, 390, 374], fill=C_MINT, outline=C_DARK, width=14)
    d.ellipse([168, 180, 344, 332], fill=C_YELLOW, outline=C_DARK, width=14)
    d.ellipse([214, 220, 298, 292], fill=C_CORAL, outline=C_DARK, width=12)
    return img
def icon_windowing():
    img, d = new_canvas()
    rrect(d, [84, 84, 428, 428], 48, fill=C_WHITE, outline=C_DARK, width=16)
    d.polygon([(100, 412), (256, 412), (256, 100), (100, 100)], fill=C_MUTED_BLUE)
    rrect(d, [84, 84, 428, 428], 48, fill=None, outline=C_DARK, width=16)
    pts = [(128, 372), (204, 364), (256, 256), (308, 148), (384, 140)]
    for i in range(len(pts) - 1):
        line_cap(d, pts[i], pts[i + 1], fill=C_DARK, width=28)
    for i in range(len(pts) - 1):
        line_cap(d, pts[i], pts[i + 1], fill=C_CORAL, width=14)
    circle(d, 128, 372, 22, fill=C_MINT, outline=C_DARK, width=10)
    circle(d, 384, 140, 22, fill=C_YELLOW, outline=C_DARK, width=10)
    return img
def icon_rotate_atoms():
    img, d = new_canvas()
    d.ellipse([84, 168, 428, 344], fill=None, outline=C_DARK, width=24)
    d.ellipse([84, 168, 428, 344], fill=None, outline=C_MINT, width=12)
    circle(d, 256, 256, 68, fill=C_BLUE, outline=C_DARK, width=15)
    circle(d, 104, 256, 36, fill=C_CORAL, outline=C_DARK, width=12)
    circle(d, 408, 256, 36, fill=C_YELLOW, outline=C_DARK, width=12)
    return img
def icon_swapaa():
    img, d = new_canvas()
    d.arc([120, 96, 392, 340], start=200, end=340, fill=C_DARK, width=28)
    d.arc([120, 96, 392, 340], start=200, end=340, fill=C_BLUE, width=14)
    d.arc([120, 172, 392, 416], start=20, end=160, fill=C_DARK, width=28)
    d.arc([120, 172, 392, 416], start=20, end=160, fill=C_GOLD, width=14)
    circle(d, 128, 256, 56, fill=C_MINT, outline=C_DARK, width=15)
    circle(d, 384, 256, 56, fill=C_CORAL, outline=C_DARK, width=15)
    return img
def icon_sequence():
    img, d = new_canvas()
    colors = [
        (92, 116, C_CORAL),
        (206, 116, C_MINT),
        (320, 116, C_BLUE),
        (92, 272, C_YELLOW),
        (206, 272, C_LAV),
        (320, 272, C_CYAN),
    ]
    for x, y, col in colors:
        rrect(d, [x, y, x + 100, y + 124], 22, fill=col, outline=C_DARK, width=14)
        line_cap(d, (x + 28, y + 62), (x + 72, y + 62), fill=C_DARK, width=16)
    return img
def icon_orthopick():
    img, d = new_canvas()
    top_pts = [(256, 80), (416, 166), (256, 252), (96, 166)]
    left_pts = [(96, 166), (256, 252), (256, 432), (96, 346)]
    right_pts = [(256, 252), (416, 166), (416, 346), (256, 432)]
    d.polygon(top_pts, fill=C_MINT, outline=C_DARK, width=14)
    d.polygon(left_pts, fill=C_BLUE, outline=C_DARK, width=14)
    d.polygon(right_pts, fill=C_LAV, outline=C_DARK, width=14)
    circle(d, 256, 252, 44, fill=C_CORAL, outline=C_DARK, width=14)
    circle(d, 256, 252, 16, fill=C_WHITE, outline=C_DARK, width=8)
    return img
def icon_whitebg():
    img, d = new_canvas()
    rrect(d, [88, 88, 424, 424], 56, fill=C_WHITE, outline=C_DARK, width=16)
    circle(d, 336, 176, 34, fill=C_YELLOW, outline=C_DARK, width=12)
    return img
def icon_graybg():
    img, d = new_canvas()
    rrect(d, [88, 88, 424, 424], 56, fill=(180, 190, 206, 255), outline=C_DARK, width=16)
    circle(d, 256, 256, 38, fill=C_BLUE, outline=C_DARK, width=12)
    return img
def icon_blackbg():
    img, d = new_canvas()
    rrect(d, [88, 88, 424, 424], 56, fill=(44, 46, 54, 255), outline=C_WHITE, width=14)
    rrect(d, [88, 88, 424, 424], 56, fill=None, outline=C_DARK, width=8)
    circle(d, 332, 180, 34, fill=C_LAV, outline=C_WHITE, width=10)
    return img
GENERATORS = {
    "open-in-app.png": icon_open_in_app,
    "video.png": icon_video,
    "atomhide.png": icon_atomhide,
    "ribshow.png": icon_ribshow,
    "ribhide.png": icon_ribhide,
    "surfhide.png": icon_surfhide,
    "stick.png": icon_stick,
    "simplelight.png": icon_simplelight,
    "softlight.png": icon_softlight,
    "fulllight.png": icon_fulllight,
    "flat.png": icon_flat,
    "silhouette.png": icon_silhouette,
    "colorbyelement.png": icon_colorbyelement,
    "colorbychain.png": icon_colorbychain,
    "rainbow.png": icon_rainbow,
    "hydrophobicity.png": icon_hydrophobicity,
    "bfactor.png": icon_bfactor,
    "hbonds.png": icon_hbonds,
    "hbondshide.png": icon_hbondshide,
    "nuc-slab.png": icon_nuc_slab,
    "nuc-box.png": icon_nuc_box,
    "nuc-elli.png": icon_nuc_elli,
    "nuc-muff.png": icon_nuc_muff,
    "sideview.png": icon_sideview,
    "viewsel.png": icon_viewsel,
    "viewall.png": icon_viewall,
    "orient.png": icon_orient,
    "mesh.png": icon_mesh,
    "orthoplanes.png": icon_orthoplanes,
    "fitmap.png": icon_fitmap,
    "smooth.png": icon_smooth,
    "airways.png": icon_airways,
    "chest.png": icon_chest,
    "brain.png": icon_brain,
    "initialcurve.png": icon_initialcurve,
    "moveplanes.png": icon_moveplanes,
    "rotateslab.png": icon_rotateslab,
    "tape.png": icon_tape,
    "mark_maximum.png": icon_mark_maximum,
    "mark_plane.png": icon_mark_plane,
    "mark_surface.png": icon_mark_surface,
    "mark_center.png": icon_mark_center,
    "mark_point.png": icon_mark_point,
    "mark_link.png": icon_mark_link,
    "mark_move.png": icon_mark_move,
    "mark_resize.png": icon_mark_resize,
    "mark_delete.png": icon_mark_delete,
    "select.png": icon_select,
    "rotate.png": icon_rotate,
    "translate.png": icon_translate,
    "move_picked_model.png": icon_move_picked_model,
    "rotatesel.png": icon_rotatesel,
    "drag_model.png": icon_drag_model,
    "move_atoms.png": icon_move_atoms,
    "pivot.png": icon_pivot,
    "distance.png": icon_distance,
    "label.png": icon_label,
    "movelabel.png": icon_movelabel,
    "ckicon.png": icon_ckicon,
    "zone.png": icon_zone,
    "vseries.png": icon_vseries,
    "bondrot.png": icon_bondrot,
    "coordset.png": icon_coordset,
    "tug.png": icon_tug,
    "minimize.png": icon_minimize,
    "nextdocking.png": icon_nextdocking,
    "close-box.png": icon_close_box,
    "content-save.png": icon_content_save,
    "undo-variant.png": icon_undo_variant,
    "redo-variant.png": icon_redo_variant,
    "crop.png": icon_crop,
    "zoom.png": icon_zoom,
    "outlinebox.png": icon_outlinebox,
    "mouse.png": icon_mouse,
    "right_controller.png": icon_right_controller,
    "eraser.png": icon_eraser,
    "pickblobs.png": icon_pickblobs,
    "contour.png": icon_contour,
    "windowing.png": icon_windowing,
    "rotate_atoms.png": icon_rotate_atoms,
    "swapaa.png": icon_swapaa,
    "sequence.png": icon_sequence,
    "orthopick.png": icon_orthopick,
    "whitebg.png": icon_whitebg,
    "graybg.png": icon_graybg,
    "blackbg.png": icon_blackbg,
}
ALIASES = {
    "ckiconvertical.png": "ckicon.png",
    "ckicon0.png": "ckicon.png",
    "maximum.png": "mark_maximum.png",
    "surface.png": "mark_surface.png",
    "center.png": "mark_center.png",
    "point.png": "mark_point.png",
    "link.png": "mark_link.png",
    "move.png": "mark_move.png",
    "resize.png": "mark_resize.png",
    "delete.png": "mark_delete.png",
    "marker.png": "mark_point.png",
    "marker2.png": "mark_surface.png",
    "move_h2o.png": "drag_model.png",
    "rotate_h2o.png": "rotatesel.png",
    "ball.png": "ball_stick.png",
    "hbondsflat.png": "hbonds.png",
    "hbondsflathide.png": "hbondshide.png",
    "mouse_small.png": "mouse.png",
    "right_controller_small.png": "right_controller.png",
    "atomhide-dark.png": "atomhide.png",
    "orient-dark.png": "orient.png",
    "recentfiles-dark.png": "recentfiles.png",
    "ribhide-dark.png": "ribhide.png",
    "silhouette-dark.png": "silhouette.png",
    "surfhide-dark.png": "surfhide.png",
    "viewall-dark.png": "viewall.png",
    "viewsel-dark.png": "viewsel.png",
    "clip_wht.png": "clip.png",
    "cliprot_wht.png": "cliprot.png",
    "undo.png": "undo-variant.png",
    "redo.png": "redo-variant.png",
    "save.png": "content-save.png",
    "open.png": "open-in-app.png",
    "recent.png": "recentfiles.png",
    "snapshot.png": "camera.png",
    "movie.png": "video.png",
    "surf.png": "surfshow.png",
    "zplane.png": "plane.png",
    "create_segmentation.png": "segger.png",
    "move_cursor.png": "translate.png",
    "resize_cursor.png": "mark_resize.png",
}
def main():
    dirs_to_update = [
        r"C:\Users\Parfion\Downloads\chimerax_mac_icons",
        r"C:\Users\Parfion\chimerax_start\icons",
        r"C:\Users\Parfion\Documents\GitHub\Chimera-X-\icons",
    ]
    svg_dirs = [
        r"C:\Users\Parfion\Downloads\chimerax_mac_icons",
        r"C:\Users\Parfion\chimerax_start\icons",
        r"C:\Users\Parfion\Documents\GitHub\Chimera-X-\svg",
    ]
    generated_png_bytes = {}
    generated_svg_text = {}
    for fname, fn in GENERATORS.items():
        hi_img = fn()
        out_img = hi_img.resize((OUT_S, OUT_S), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        out_img.save(buf, format="PNG")
        png_bytes = buf.getvalue()
        generated_png_bytes[fname] = png_bytes
        b64 = base64.b64encode(png_bytes).decode("ascii")
        svg_name = os.path.splitext(fname)[0] + ".svg"
        generated_svg_text[svg_name] = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">'
            f'<image width="128" height="128" href="data:image/png;base64,{b64}"/></svg>'
        )
        for d in dirs_to_update:
            if os.path.exists(d):
                with open(os.path.join(d, fname), "wb") as f:
                    f.write(png_bytes)
        for sd in svg_dirs:
            if os.path.exists(sd):
                with open(os.path.join(sd, svg_name), "w", encoding="utf-8") as f:
                    f.write(generated_svg_text[svg_name])
    src_icon_dir = r"C:\Users\Parfion\chimerax_start\icons"
    for alias_png, target_png in ALIASES.items():
        png_bytes = generated_png_bytes.get(target_png)
        if png_bytes is None:
            tp = os.path.join(src_icon_dir, target_png)
            if os.path.exists(tp):
                with open(tp, "rb") as fp:
                    png_bytes = fp.read()
        if png_bytes is not None:
            generated_png_bytes[alias_png] = png_bytes
            b64 = base64.b64encode(png_bytes).decode("ascii")
            svg_name = os.path.splitext(alias_png)[0] + ".svg"
            generated_svg_text[svg_name] = (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">'
                f'<image width="128" height="128" href="data:image/png;base64,{b64}"/></svg>'
            )
            for d in dirs_to_update:
                if os.path.exists(d):
                    with open(os.path.join(d, alias_png), "wb") as f:
                        f.write(png_bytes)
            for sd in svg_dirs:
                if os.path.exists(sd):
                    with open(os.path.join(sd, svg_name), "w", encoding="utf-8") as f:
                        f.write(generated_svg_text[svg_name])
    tree_roots = [
        r"C:\Users\Parfion\Documents\GitHub\Chimera-X-\packages\chimerax",
        r"C:\Users\Parfion\AppData\Local\UCSF\ChimeraX\1.12\Python311\site-packages\chimerax",
    ]
    replaced_in_trees = 0
    for tr in tree_roots:
        if not os.path.exists(tr):
            continue
        for root, _, files in os.walk(tr):
            for f in files:
                if f in generated_png_bytes:
                    with open(os.path.join(root, f), "wb") as fp:
                        fp.write(generated_png_bytes[f])
                    replaced_in_trees += 1
                elif f in generated_svg_text:
                    with open(os.path.join(root, f), "w", encoding="utf-8") as fp:
                        fp.write(generated_svg_text[f])
                    replaced_in_trees += 1
if __name__ == "__main__":
    main()
