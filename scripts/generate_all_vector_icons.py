import os
import math
from PIL import Image, ImageDraw, ImageFont
DIR_ICONS_FLAT = os.path.normpath(os.path.expanduser("~/Downloads/chimerax_mac_icons"))
DIR_USER_SITE = os.path.normpath(os.path.expanduser("~/AppData/Local/UCSF/ChimeraX/1.12/Python311/site-packages/chimerax"))
DIR_GITHUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in [DIR_ICONS_FLAT, DIR_USER_SITE, DIR_GITHUB]:
    os.makedirs(d, exist_ok=True)
PASTEL_BLUE = (142, 197, 252, 255)
PASTEL_CORAL = (255, 154, 162, 255)
PASTEL_MINT = (181, 234, 215, 255)
PASTEL_BUTTER = (255, 243, 176, 255)
PASTEL_PEACH = (255, 218, 193, 255)
PASTEL_LAVENDER = (226, 209, 249, 255)
PASTEL_CYAN = (160, 231, 229, 255)
PASTEL_ROSE = (255, 183, 178, 255)
PASTEL_GRAY = (176, 190, 197, 255)
GRAPHITE = (44, 44, 46, 255)
GRAPHITE_LIGHT = (44, 44, 46, 120)
GRAPHITE_TINT = (44, 44, 46, 30)
WHITE = (255, 255, 255, 255)
CANVAS_SIZE = 512
FINAL_SIZE = 128
def create_canvas():
    return Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
def save_image(im, filename, subdirs=None):
    res = im.resize((FINAL_SIZE, FINAL_SIZE), Image.Resampling.LANCZOS)
    p_flat = os.path.join(DIR_ICONS_FLAT, filename)
    res.save(p_flat, "PNG")
    gh_flat = os.path.join(DIR_GITHUB, "icons", filename)
    os.makedirs(os.path.dirname(gh_flat), exist_ok=True)
    res.save(gh_flat, "PNG")
    if subdirs:
        for s in subdirs:
            local_p = os.path.join(DIR_USER_SITE, s, filename)
            os.makedirs(os.path.dirname(local_p), exist_ok=True)
            res.save(local_p, "PNG")
            gh_mirror = os.path.join(DIR_GITHUB, "packages", s, filename)
            os.makedirs(os.path.dirname(gh_mirror), exist_ok=True)
            res.save(gh_mirror, "PNG")
def get_font(size):
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except Exception:
        return ImageFont.load_default()
def draw_atomshow():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([206, 206, 306, 306], fill=PASTEL_BLUE, outline=GRAPHITE, width=12)
    d.ellipse([70, 180, 442, 332], outline=GRAPHITE, width=18)
    im_rot = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
    d_rot = ImageDraw.Draw(im_rot)
    d_rot.ellipse([70, 180, 442, 332], outline=GRAPHITE, width=18)
    im.alpha_composite(im_rot.rotate(60, resample=Image.Resampling.BICUBIC))
    im.alpha_composite(im_rot.rotate(-60, resample=Image.Resampling.BICUBIC))
    d = ImageDraw.Draw(im)
    d.ellipse([75, 236, 115, 276], fill=PASTEL_MINT, outline=GRAPHITE, width=8)
    d.ellipse([397, 236, 437, 276], fill=PASTEL_MINT, outline=GRAPHITE, width=8)
    return im
def draw_atomhide():
    im = draw_atomshow()
    d = ImageDraw.Draw(im)
    d.line([80, 80, 432, 432], fill=WHITE, width=44)
    d.line([80, 80, 432, 432], fill=PASTEL_CORAL, width=28)
    d.line([80, 80, 432, 432], fill=GRAPHITE, width=6)
    return im
def draw_ribshow():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    pts_top = []
    pts_bot = []
    w = 44
    for x in range(60, 452, 6):
        t = (x - 60) / 392.0
        y = 256 + math.sin(t * math.pi * 2.5) * 110
        pts_top.append((x, y - w / 2))
        pts_bot.append((x, y + w / 2))
    pts = pts_top + pts_bot[::-1]
    d.polygon(pts, fill=PASTEL_BLUE)
    d.line(pts + [pts[0]], fill=GRAPHITE, width=14)
    d.polygon([(420, 195), (462, 256), (420, 317)], fill=PASTEL_BLUE)
    d.line([(420, 195), (462, 256), (420, 317)], fill=GRAPHITE, width=14)
    d.line(pts_top, fill=PASTEL_LAVENDER, width=12)
    return im
def draw_ribhide():
    im = draw_ribshow()
    d = ImageDraw.Draw(im)
    d.line([80, 80, 432, 432], fill=WHITE, width=44)
    d.line([80, 80, 432, 432], fill=PASTEL_CORAL, width=28)
    d.line([80, 80, 432, 432], fill=GRAPHITE, width=6)
    return im
def draw_surfshow():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    lobes = [
        (180, 220, 110),
        (300, 200, 120),
        (256, 310, 115),
        (340, 320, 95),
        (170, 320, 90)
    ]
    for x, y, r in lobes:
        d.ellipse([x - r, y - r, x + r, y + r], fill=PASTEL_LAVENDER)
    for x, y, r in lobes:
        d.ellipse([x - r, y - r, x + r, y + r], outline=GRAPHITE, width=16)
    d.arc([160, 190, 350, 330], start=30, end=150, fill=GRAPHITE, width=14)
    return im
def draw_surfhide():
    im = draw_surfshow()
    d = ImageDraw.Draw(im)
    d.line([80, 80, 432, 432], fill=WHITE, width=44)
    d.line([80, 80, 432, 432], fill=PASTEL_CORAL, width=28)
    d.line([80, 80, 432, 432], fill=GRAPHITE, width=6)
    return im
def draw_stick():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.line([130, 382, 382, 130], fill=GRAPHITE, width=54)
    d.ellipse([103, 355, 157, 409], fill=PASTEL_BLUE, outline=GRAPHITE, width=8)
    d.ellipse([355, 103, 409, 157], fill=PASTEL_CORAL, outline=GRAPHITE, width=8)
    d.line([150, 362, 362, 150], fill=(255, 255, 255, 180), width=12)
    return im
def draw_sphere():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([90, 90, 422, 422], fill=PASTEL_BLUE, outline=GRAPHITE, width=16)
    d.arc([140, 130, 320, 310], start=190, end=270, fill=WHITE, width=24)
    d.ellipse([170, 160, 205, 195], fill=WHITE)
    return im
def draw_ball():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([140, 140, 372, 372], fill=PASTEL_MINT, outline=GRAPHITE, width=14)
    d.arc([175, 170, 310, 305], start=190, end=270, fill=WHITE, width=16)
    d.ellipse([195, 190, 225, 220], fill=WHITE)
    return im
def draw_ball_stick():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.line([160, 352, 352, 160], fill=GRAPHITE, width=32)
    d.ellipse([90, 282, 230, 422], fill=PASTEL_BLUE, outline=GRAPHITE, width=12)
    d.ellipse([120, 312, 145, 337], fill=WHITE)
    d.ellipse([282, 90, 422, 230], fill=PASTEL_CORAL, outline=GRAPHITE, width=12)
    d.ellipse([312, 120, 337, 145], fill=WHITE)
    return im
def draw_hbonds():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([80, 206, 180, 306], fill=PASTEL_CORAL, outline=GRAPHITE, width=10)
    d.ellipse([332, 206, 432, 306], fill=PASTEL_BLUE, outline=GRAPHITE, width=10)
    for x in range(200, 315, 26):
        d.ellipse([x, 246, x + 16, 266], fill=PASTEL_CYAN, outline=GRAPHITE, width=4)
    return im
def draw_hbondshide():
    im = draw_hbonds()
    d = ImageDraw.Draw(im)
    d.line([80, 80, 432, 432], fill=WHITE, width=44)
    d.line([80, 80, 432, 432], fill=PASTEL_CORAL, width=28)
    d.line([80, 80, 432, 432], fill=GRAPHITE, width=6)
    return im
def draw_interfaces():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.arc([60, 120, 280, 392], start=-70, end=70, fill=PASTEL_BLUE, width=36)
    d.arc([232, 120, 452, 392], start=110, end=250, fill=PASTEL_MINT, width=36)
    for y in [180, 225, 256, 287, 332]:
        d.ellipse([244, y - 10, 268, y + 10], fill=PASTEL_BUTTER, outline=GRAPHITE, width=4)
    return im
def draw_sequence():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    pastels = [PASTEL_CORAL, PASTEL_BLUE, PASTEL_MINT, PASTEL_BUTTER, PASTEL_PEACH, PASTEL_LAVENDER]
    f = get_font(36)
    letters = ["M", "K", "L", "A", "V", "E", "D", "T", "Y", "G", "S", "R"]
    idx = 0
    for row in range(3):
        y = 100 + row * 110
        for col in range(4):
            x = 80 + col * 92
            c = pastels[idx % len(pastels)]
            d.rounded_rectangle([x, y, x + 76, y + 80], radius=16, fill=c, outline=GRAPHITE, width=6)
            letter = letters[idx % len(letters)]
            bbox = f.getbbox(letter)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            d.text((x + (76 - tw) / 2, y + (80 - th) / 2 - 4), letter, fill=GRAPHITE, font=f)
            idx += 1
    return im
def draw_nuc_ladder():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    for t_step in range(0, 100):
        t1 = t_step / 100.0
        t2 = (t_step + 1) / 100.0
        y1 = 80 + t1 * 352
        y2 = 80 + t2 * 352
        x1_left = 160 + math.sin(t1 * math.pi * 3) * 60
        x2_left = 160 + math.sin(t2 * math.pi * 3) * 60
        x1_right = 352 + math.sin(t1 * math.pi * 3 + math.pi) * 60
        x2_right = 352 + math.sin(t2 * math.pi * 3 + math.pi) * 60
        d.line([(x1_left, y1), (x2_left, y2)], fill=GRAPHITE, width=16)
        d.line([(x1_right, y1), (x2_right, y2)], fill=GRAPHITE, width=16)
    for i in range(7):
        t = i / 6.0
        y = 100 + t * 312
        x_left = 160 + math.sin(t * math.pi * 3) * 60
        x_right = 352 + math.sin(t * math.pi * 3 + math.pi) * 60
        col = PASTEL_BLUE if i % 2 == 0 else PASTEL_MINT
        d.line([(x_left, y), (x_right, y)], fill=col, width=18)
    return im
def draw_nuc_stubs():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    pts = []
    for y in range(80, 432, 8):
        x = 200 + math.sin((y - 80) / 352.0 * math.pi * 2) * 50
        pts.append((x, y))
    d.line(pts, fill=GRAPHITE, width=22)
    for y in range(110, 420, 50):
        x_base = 200 + math.sin((y - 80) / 352.0 * math.pi * 2) * 50
        d.line([(x_base, y), (x_base + 120, y)], fill=PASTEL_PEACH, width=20)
        d.ellipse([x_base + 110, y - 14, x_base + 138, y + 14], fill=PASTEL_PEACH, outline=GRAPHITE, width=6)
    return im
def draw_nuc_fill():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    hex_pts = [(180, 160), (280, 160), (330, 246), (280, 332), (180, 332), (130, 246)]
    d.polygon(hex_pts, fill=PASTEL_BLUE)
    d.line(hex_pts + [hex_pts[0]], fill=GRAPHITE, width=16)
    pent_pts = [(280, 160), (370, 190), (410, 260), (330, 332), (280, 332)]
    d.polygon(pent_pts, fill=PASTEL_MINT)
    d.line(pent_pts + [pent_pts[0]], fill=GRAPHITE, width=16)
    d.line([(190, 185), (270, 185)], fill=WHITE, width=8)
    d.line([(155, 250), (190, 310)], fill=WHITE, width=8)
    return im
def draw_nuc_slab():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    def draw_slab_block(bx, by, w, h, depth, col):
        top = [(bx, by), (bx + w, by), (bx + w + depth, by - depth * 0.6), (bx + depth, by - depth * 0.6)]
        d.polygon(top, fill=col)
        d.line(top + [top[0]], fill=GRAPHITE, width=10)
        front = [(bx, by), (bx + w, by), (bx + w, by + h), (bx, by + h)]
        d.polygon(front, fill=col)
        d.line(front + [front[0]], fill=GRAPHITE, width=10)
        side = [(bx + w, by), (bx + w + depth, by - depth * 0.6), (bx + w + depth, by + h - depth * 0.6), (bx + w, by + h)]
        d.polygon(side, fill=col)
        d.line(side + [side[0]], fill=GRAPHITE, width=10)
    draw_slab_block(110, 260, 220, 60, 60, PASTEL_BLUE)
    draw_slab_block(150, 160, 220, 60, 60, PASTEL_CORAL)
    return im
def draw_nuc_tube():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.arc([100, 100, 412, 412], start=45, end=270, fill=GRAPHITE, width=64)
    d.arc([100, 100, 412, 412], start=45, end=270, fill=PASTEL_LAVENDER, width=32)
    d.arc([100, 100, 412, 412], start=45, end=270, fill=WHITE, width=10)
    d.ellipse([270, 70, 330, 130], fill=PASTEL_LAVENDER, outline=GRAPHITE, width=8)
    d.ellipse([340, 320, 400, 380], fill=PASTEL_LAVENDER, outline=GRAPHITE, width=8)
    return im
def draw_nuc_elli():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    im_e = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
    de = ImageDraw.Draw(im_e)
    de.ellipse([90, 180, 422, 332], fill=PASTEL_MINT, outline=GRAPHITE, width=16)
    de.arc([140, 200, 372, 312], start=180, end=330, fill=WHITE, width=14)
    im.alpha_composite(im_e.rotate(-30, resample=Image.Resampling.BICUBIC))
    d.line([160, 420, 352, 92], fill=GRAPHITE, width=14)
    return im
def draw_nuc_muff():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([100, 186, 412, 326], radius=70, fill=PASTEL_CYAN, outline=GRAPHITE, width=16)
    d.line([200, 186, 200, 326], fill=GRAPHITE, width=10)
    d.line([312, 186, 312, 326], fill=GRAPHITE, width=10)
    d.line([170, 220, 342, 220], fill=WHITE, width=12)
    return im
def draw_nuc_box():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.rectangle([130, 200, 330, 400], outline=GRAPHITE, width=14)
    d.rectangle([182, 112, 382, 312], outline=GRAPHITE_LIGHT, width=10)
    d.line([(130, 200), (182, 112)], fill=GRAPHITE, width=12)
    d.line([(330, 200), (382, 112)], fill=GRAPHITE, width=12)
    d.line([(130, 400), (182, 312)], fill=GRAPHITE, width=12)
    d.line([(330, 400), (382, 312)], fill=GRAPHITE, width=12)
    d.ellipse([216, 216, 296, 296], fill=PASTEL_PEACH, outline=GRAPHITE, width=8)
    return im
def draw_nuc_color():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    f = get_font(52)
    tiles = [
        (100, 100, "A", PASTEL_CORAL),
        (266, 100, "T", PASTEL_MINT),
        (100, 266, "C", PASTEL_BLUE),
        (266, 266, "G", PASTEL_BUTTER)
    ]
    for x, y, letter, c in tiles:
        d.rounded_rectangle([x, y, x + 146, y + 146], radius=24, fill=c, outline=GRAPHITE, width=10)
        bbox = f.getbbox(letter)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        d.text((x + (146 - tw) / 2, y + (146 - th) / 2 - 8), letter, fill=GRAPHITE, font=f)
    return im
def draw_colorbyelement():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([186, 186, 326, 326], fill=PASTEL_GRAY, outline=GRAPHITE, width=12)
    d.ellipse([206, 70, 306, 170], fill=PASTEL_CORAL, outline=GRAPHITE, width=10)
    d.ellipse([342, 206, 442, 306], fill=PASTEL_BLUE, outline=GRAPHITE, width=10)
    d.ellipse([70, 206, 170, 306], fill=WHITE, outline=GRAPHITE, width=10)
    d.ellipse([206, 342, 306, 442], fill=PASTEL_BUTTER, outline=GRAPHITE, width=10)
    return im
def draw_colorbychain():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    chains = [(120, PASTEL_BLUE), (256, PASTEL_CORAL), (392, PASTEL_MINT)]
    for x_center, color in chains:
        pts = []
        for y in range(80, 432, 10):
            t = (y - 80) / 352.0
            x = x_center + math.sin(t * math.pi * 3) * 36
            pts.append((x, y))
        d.line(pts, fill=color, width=32)
        d.line(pts, fill=GRAPHITE, width=6)
    return im
def draw_polymer():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(11):
        t = i / 10.0
        x = 90 + t * 332
        y = 256 + math.sin(t * math.pi * 2.5) * 110
        pts.append((x, y))
    d.line(pts, fill=GRAPHITE, width=14)
    pastels = [PASTEL_BLUE, PASTEL_CYAN, PASTEL_MINT, PASTEL_BUTTER, PASTEL_PEACH, PASTEL_CORAL, PASTEL_LAVENDER]
    for i, (x, y) in enumerate(pts):
        c = pastels[i % len(pastels)]
        d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=c, outline=GRAPHITE, width=8)
        d.ellipse([x - 8, y - 8, x - 2, y - 2], fill=WHITE)
    return im
def draw_rainbow():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    bands = [
        (200, PASTEL_CORAL),
        (170, PASTEL_PEACH),
        (140, PASTEL_BUTTER),
        (110, PASTEL_MINT),
        (80, PASTEL_BLUE),
        (50, PASTEL_LAVENDER)
    ]
    for r, col in bands:
        d.arc([256 - r, 340 - r, 256 + r, 340 + r], start=180, end=0, fill=col, width=24)
        d.arc([256 - r, 340 - r, 256 + r, 340 + r], start=180, end=0, fill=GRAPHITE, width=4)
    return im
def draw_esp():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.arc([100, 120, 412, 392], start=180, end=0, fill=GRAPHITE_LIGHT, width=10)
    d.arc([100, 120, 412, 392], start=0, end=180, fill=GRAPHITE_LIGHT, width=10)
    d.arc([140, 160, 372, 352], start=180, end=0, fill=GRAPHITE_LIGHT, width=8)
    d.arc([140, 160, 372, 352], start=0, end=180, fill=GRAPHITE_LIGHT, width=8)
    d.ellipse([90, 206, 190, 306], fill=PASTEL_BLUE, outline=GRAPHITE, width=10)
    d.line([115, 256, 165, 256], fill=GRAPHITE, width=12)
    d.line([140, 231, 140, 281], fill=GRAPHITE, width=12)
    d.ellipse([322, 206, 422, 306], fill=PASTEL_CORAL, outline=GRAPHITE, width=10)
    d.line([347, 256, 397, 256], fill=GRAPHITE, width=12)
    return im
def draw_hydrophobicity():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.line([70, 380, 442, 380], fill=GRAPHITE, width=18)
    for x in range(80, 440, 30):
        d.line([x, 380, x - 10, 415], fill=GRAPHITE_LIGHT, width=8)
    pts = [(256, 110), (330, 240), (360, 310), (330, 376), (182, 376), (152, 310), (182, 240)]
    d.polygon(pts, fill=PASTEL_CYAN)
    d.line(pts + [pts[0]], fill=GRAPHITE, width=16)
    d.arc([180, 200, 300, 340], start=160, end=240, fill=WHITE, width=16)
    return im
def draw_bfactor():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([226, 100, 286, 320], radius=30, fill=WHITE, outline=GRAPHITE, width=14)
    d.ellipse([196, 290, 316, 410], fill=PASTEL_CORAL, outline=GRAPHITE, width=14)
    d.rounded_rectangle([236, 180, 276, 320], radius=16, fill=PASTEL_CORAL)
    for y, w in [(140, 40), (200, 60), (260, 75)]:
        d.arc([296, y - 20, 296 + w * 2, y + 20], start=-60, end=60, fill=PASTEL_BUTTER, width=12)
        d.arc([216 - w * 2, y - 20, 216, y + 20], start=120, end=240, fill=PASTEL_BUTTER, width=12)
    return im
def draw_colorrandom():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([130, 180, 330, 380], radius=24, fill=WHITE, outline=GRAPHITE, width=14)
    top = [(130, 180), (330, 180), (382, 130), (182, 130)]
    d.polygon(top, fill=(245, 245, 250, 255))
    d.line(top + [top[0]], fill=GRAPHITE, width=14)
    side = [(330, 180), (382, 130), (382, 330), (330, 380)]
    d.polygon(side, fill=(225, 225, 235, 255))
    d.line(side + [side[0]], fill=GRAPHITE, width=14)
    pips = [(180, 230, PASTEL_CORAL), (280, 230, PASTEL_MINT), (230, 280, PASTEL_BLUE), (180, 330, PASTEL_BUTTER), (280, 330, PASTEL_LAVENDER)]
    for px, py, c in pips:
        d.ellipse([px - 14, py - 14, px + 14, py + 14], fill=c, outline=GRAPHITE, width=4)
    return im
def draw_colorzone():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    for angle in range(0, 360, 18):
        rad = math.radians(angle)
        x1 = 256 + math.cos(rad) * 160
        y1 = 256 + math.sin(rad) * 160
        x2 = 256 + math.cos(rad) * 174
        y2 = 256 + math.sin(rad) * 174
        d.line([(x1, y1), (x2, y2)], fill=PASTEL_BLUE, width=10)
    d.line([256, 256, 386, 170], fill=PASTEL_BLUE, width=10)
    d.ellipse([206, 206, 306, 306], fill=PASTEL_LAVENDER, outline=GRAPHITE, width=12)
    return im
def draw_bondrot():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.line([256, 80, 256, 432], fill=GRAPHITE, width=36)
    d.ellipse([231, 65, 281, 115], fill=PASTEL_BLUE, outline=GRAPHITE, width=8)
    d.ellipse([231, 397, 281, 447], fill=PASTEL_CORAL, outline=GRAPHITE, width=8)
    d.arc([110, 180, 402, 332], start=20, end=200, fill=PASTEL_PEACH, width=22)
    d.polygon([(360, 270), (410, 250), (390, 310)], fill=PASTEL_PEACH)
    return im
def draw_distance():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([90, 216, 170, 296], fill=PASTEL_BLUE, outline=GRAPHITE, width=10)
    d.ellipse([342, 216, 422, 296], fill=PASTEL_MINT, outline=GRAPHITE, width=10)
    d.line([180, 256, 332, 256], fill=PASTEL_CORAL, width=16)
    d.polygon([(180, 256), (210, 240), (210, 272)], fill=PASTEL_CORAL)
    d.polygon([(332, 256), (302, 240), (302, 272)], fill=PASTEL_CORAL)
    return im
def draw_swapaa():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([100, 186, 220, 306], fill=PASTEL_BLUE, outline=GRAPHITE, width=10)
    d.ellipse([292, 186, 412, 306], fill=PASTEL_CORAL, outline=GRAPHITE, width=10)
    d.arc([140, 110, 372, 250], start=190, end=350, fill=PASTEL_MINT, width=18)
    d.polygon([(360, 190), (390, 160), (360, 130)], fill=PASTEL_MINT)
    d.arc([140, 240, 372, 380], start=10, end=170, fill=PASTEL_MINT, width=18)
    d.polygon([(152, 290), (122, 320), (152, 350)], fill=PASTEL_MINT)
    return im
def draw_tape():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    tape = [(90, 190), (422, 190), (422, 322), (90, 322)]
    d.polygon(tape, fill=PASTEL_BUTTER)
    d.line(tape + [tape[0]], fill=GRAPHITE, width=14)
    for i in range(11):
        x = 115 + i * 28
        h = 45 if i % 5 == 0 else 25
        d.line([x, 190, x, 190 + h], fill=GRAPHITE, width=8)
    return im
def draw_tug():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([120, 206, 220, 306], fill=PASTEL_BLUE, outline=GRAPHITE, width=12)
    d.line([220, 256, 390, 256], fill=PASTEL_CORAL, width=20)
    d.polygon([(360, 226), (410, 256), (360, 286)], fill=PASTEL_CORAL)
    return im
def draw_minimize():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    pts = []
    for x in range(90, 423, 8):
        t = (x - 256) / 100.0
        y = 380 - 240 * math.exp(-0.5 * t * t)
        pts.append((x, 480 - y))
    d.line(pts, fill=GRAPHITE, width=18)
    d.ellipse([216, 290, 296, 370], fill=PASTEL_MINT, outline=GRAPHITE, width=10)
    return im
def draw_label():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([90, 110, 422, 402], radius=40, fill=PASTEL_LAVENDER, outline=GRAPHITE, width=16)
    f = get_font(180)
    bbox = f.getbbox("A")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text(((CANVAS_SIZE - tw) / 2, (CANVAS_SIZE - th) / 2 - 24), "A", fill=GRAPHITE, font=f)
    return im
def draw_movelabel():
    im = draw_label()
    d = ImageDraw.Draw(im)
    cx, cy = 380, 130
    d.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], fill=PASTEL_BLUE, outline=GRAPHITE, width=8)
    d.line([cx - 30, cy, cx + 30, cy], fill=WHITE, width=8)
    d.line([cx, cy - 30, cx, cy + 30], fill=WHITE, width=8)
    return im
def draw_eraser():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([100, 180, 240, 320], fill=PASTEL_GRAY, outline=GRAPHITE, width=10)
    eraser = [(220, 140), (340, 240), (280, 320), (160, 220)]
    d.polygon(eraser, fill=PASTEL_CORAL)
    d.line(eraser + [eraser[0]], fill=GRAPHITE, width=14)
    return im
def draw_vseries():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    for offset in [0, 40, 80]:
        d.rounded_rectangle([100 + offset, 100 + offset, 332 + offset, 332 + offset], radius=20, fill=PASTEL_BLUE, outline=GRAPHITE, width=12)
    d.polygon([(220, 200), (270, 240), (220, 280)], fill=GRAPHITE)
    return im
def draw_pickblobs():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.ellipse([110, 140, 360, 380], fill=PASTEL_LAVENDER, outline=GRAPHITE, width=16)
    cursor = [(250, 190), (370, 310), (320, 315), (355, 395), (325, 410), (290, 330), (250, 370)]
    d.polygon(cursor, fill=PASTEL_BLUE, outline=GRAPHITE)
    d.line(cursor + [cursor[0]], fill=GRAPHITE, width=8)
    return im
def draw_volseg():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([100, 100, 246, 246], radius=20, fill=PASTEL_MINT, outline=GRAPHITE, width=10)
    d.rounded_rectangle([266, 100, 412, 246], radius=20, fill=PASTEL_CORAL, outline=GRAPHITE, width=10)
    d.rounded_rectangle([100, 266, 246, 412], radius=20, fill=PASTEL_BLUE, outline=GRAPHITE, width=10)
    d.rounded_rectangle([266, 266, 412, 412], radius=20, fill=PASTEL_BUTTER, outline=GRAPHITE, width=10)
    return im
def draw_coordset():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([90, 120, 422, 392], radius=32, fill=WHITE, outline=GRAPHITE, width=16)
    d.polygon([(190, 180), (340, 256), (190, 332)], fill=PASTEL_BLUE)
    d.line([(190, 180), (340, 256), (190, 332), (190, 180)], fill=GRAPHITE, width=12)
    return im
import generate_all_mac_icons as base_gen
import append_remaining_icons as ext_gen
ICON_BUILDERS = {
    "atomshow.png": (draw_atomshow, ["shortcuts/icons", "basic_actions/lib"]),
    "atomhide.png": (draw_atomhide, ["shortcuts/icons", "basic_actions/lib"]),
    "atomhide-dark.png": (draw_atomhide, ["shortcuts/icons"]),
    "ribshow.png": (draw_ribshow, ["shortcuts/icons", "basic_actions/lib"]),
    "ribhide.png": (draw_ribhide, ["shortcuts/icons", "basic_actions/lib"]),
    "ribhide-dark.png": (draw_ribhide, ["shortcuts/icons"]),
    "ribbon.png": (draw_ribshow, ["shortcuts/icons"]),
    "surfshow.png": (draw_surfshow, ["shortcuts/icons", "basic_actions/lib"]),
    "surf.png": (draw_surfshow, ["shortcuts/icons"]),
    "mapsurf.png": (draw_surfshow, ["shortcuts/icons"]),
    "surfhide.png": (draw_surfhide, ["shortcuts/icons", "basic_actions/lib"]),
    "surfhide-dark.png": (draw_surfhide, ["shortcuts/icons"]),
    "stick.png": (draw_stick, ["shortcuts/icons"]),
    "sphere.png": (draw_sphere, ["shortcuts/icons"]),
    "ball.png": (draw_ball, ["shortcuts/icons", "markers/icons"]),
    "ball_stick.png": (draw_ball_stick, ["shortcuts/icons"]),
    "hbonds.png": (draw_hbonds, ["shortcuts/icons"]),
    "hbondsflat.png": (draw_hbonds, ["shortcuts/icons"]),
    "hbondshide.png": (draw_hbondshide, ["shortcuts/icons"]),
    "hbondsflathide.png": (draw_hbondshide, ["shortcuts/icons"]),
    "interfaces.png": (draw_interfaces, ["shortcuts/icons"]),
    "sequence.png": (draw_sequence, ["shortcuts/icons"]),
    "nuc-ladder.png": (draw_nuc_ladder, ["nucleotides/icons"]),
    "nuc-stubs.png": (draw_nuc_stubs, ["nucleotides/icons"]),
    "nuc-fill.png": (draw_nuc_fill, ["nucleotides/icons"]),
    "nuc-slab.png": (draw_nuc_slab, ["nucleotides/icons"]),
    "nuc-tube.png": (draw_nuc_tube, ["nucleotides/icons"]),
    "nuc-elli.png": (draw_nuc_elli, ["nucleotides/icons"]),
    "nuc-muff.png": (draw_nuc_muff, ["nucleotides/icons"]),
    "nuc-box.png": (draw_nuc_box, ["nucleotides/icons"]),
    "nuc-atoms.png": (draw_ball_stick, ["nucleotides/icons"]),
    "nuc-color.png": (draw_nuc_color, ["nucleotides/icons"]),
    "plain.png": (draw_atomshow, ["shortcuts/icons", "nucleotides/icons"]),
    "colorbyelement.png": (draw_colorbyelement, ["shortcuts/icons"]),
    "colorbychain.png": (draw_colorbychain, ["shortcuts/icons"]),
    "polymer.png": (draw_polymer, ["shortcuts/icons"]),
    "rainbow.png": (draw_rainbow, ["shortcuts/icons"]),
    "esp.png": (draw_esp, ["shortcuts/icons"]),
    "hydrophobicity.png": (draw_hydrophobicity, ["shortcuts/icons"]),
    "bfactor.png": (draw_bfactor, ["shortcuts/icons"]),
    "colorrandom.png": (draw_colorrandom, ["shortcuts/icons"]),
    "colorzone.png": (draw_colorzone, ["shortcuts/icons"]),
    "bondrot.png": (draw_bondrot, ["bond_rot"]),
    "distance.png": (draw_distance, ["struct_measure"]),
    "swapaa.png": (draw_swapaa, ["swapaa"]),
    "tape.png": (draw_tape, ["tape_measure"]),
    "tug.png": (draw_tug, ["tug"]),
    "minimize.png": (draw_minimize, ["tug"]),
    "label.png": (draw_label, ["label"]),
    "movelabel.png": (draw_movelabel, ["label"]),
    "eraser.png": (draw_eraser, ["map_eraser"]),
    "vseries.png": (draw_vseries, ["map_series"]),
    "pickblobs.png": (draw_pickblobs, ["pick_blobs"]),
    "volseg.png": (draw_volseg, ["segger"]),
    "coordset.png": (draw_coordset, ["std_commands"]),
    "zone.png": (draw_colorzone, ["zone"]),
    "contour.png": (base_gen.draw_contour, ["map/icons", "shortcuts/icons"]),
    "mesh.png": (base_gen.draw_mesh, ["shortcuts/icons"]),
    "mapimage.png": (base_gen.draw_mapimage, ["shortcuts/icons"]),
    "outlinebox.png": (base_gen.draw_outlinebox, ["shortcuts/icons"]),
    "cubeoutline.png": (base_gen.draw_outlinebox, ["shortcuts/icons"]),
    "step1.png": (lambda: base_gen.draw_step_badge("1"), ["shortcuts/icons"]),
    "step2.png": (lambda: base_gen.draw_step_badge("2"), ["shortcuts/icons"]),
    "step4.png": (lambda: base_gen.draw_step_badge("4"), ["shortcuts/icons"]),
    "plane.png": (base_gen.draw_zplane, ["shortcuts/icons", "markers/icons"]),
    "zplane.png": (base_gen.draw_zplane, ["shortcuts/icons"]),
    "slab.png": (base_gen.draw_slab, ["shortcuts/icons"]),
    "orthoplanes.png": (base_gen.draw_orthoplanes, ["shortcuts/icons"]),
    "fullvolume.png": (base_gen.draw_fullvolume, ["shortcuts/icons"]),
    "volzone.png": (base_gen.draw_volzone, ["shortcuts/icons"]),
    "fitmap.png": (base_gen.draw_fitmap, ["shortcuts/icons"]),
    "diffmap.png": (base_gen.draw_diffmap, ["shortcuts/icons"]),
    "smooth.png": (base_gen.draw_smooth, ["shortcuts/icons"]),
    "dust.png": (base_gen.draw_dust, ["shortcuts/icons"]),
    "rotateslab.png": (base_gen.draw_rotateslab, ["map/icons"]),
    "moveplanes.png": (base_gen.draw_moveplanes, ["map/icons"]),
    "crop.png": (base_gen.draw_crop, ["map/icons"]),
    "windowing.png": (base_gen.draw_windowing, ["map/icons"]),
    "showmap.png": (base_gen.draw_fullvolume, ["shortcuts/icons"]),
    "hidemap.png": (draw_surfhide, ["shortcuts/icons"]),
    "xyzslice.png": (base_gen.draw_orthoplanes, ["shortcuts/icons"]),
    "perpslice.png": (base_gen.draw_zplane, ["shortcuts/icons"]),
    "airways.png": (base_gen.draw_airways, ["shortcuts/icons"]),
    "chest.png": (base_gen.draw_chest, ["shortcuts/icons"]),
    "brain.png": (base_gen.draw_brain, ["shortcuts/icons"]),
    "ear.png": (ext_gen.draw_ear, ["shortcuts/icons"]),
    "opendicom.png": (base_gen.draw_opendicom, ["medical_toolbar/icons"]),
    "maximum.png": (ext_gen.draw_maximum, ["markers/icons"]),
    "center.png": (base_gen.draw_center, ["markers/icons"]),
    "point.png": (base_gen.draw_point, ["markers/icons"]),
    "link.png": (base_gen.draw_link, ["markers/icons"]),
    "delete.png": (base_gen.draw_delete, ["markers/icons"]),
    "resize.png": (base_gen.draw_resize, ["markers/icons"]),
    "marker.png": (base_gen.draw_marker, ["markers/icons"]),
    "marker2.png": (base_gen.draw_marker, ["markers/icons"]),
    "surface.png": (draw_surfshow, ["markers/icons"]),
    "select.png": (base_gen.draw_select, ["mouse_modes/icons", "ui/icons"]),
    "rotate.png": (base_gen.draw_rotate, ["mouse_modes/icons"]),
    "translate.png": (base_gen.draw_translate, ["mouse_modes/icons"]),
    "zoom.png": (base_gen.draw_zoom, ["mouse_modes/icons"]),
    "pivot.png": (base_gen.draw_center, ["mouse_modes/icons"]),
    "move_atoms.png": (base_gen.draw_select, ["mouse_modes/icons"]),
    "move_picked_model.png": (base_gen.draw_select, ["mouse_modes/icons"]),
    "move_h2o.png": (lambda: ext_gen.draw_h2o(move=True), ["mouse_modes/icons"]),
    "rotate_h2o.png": (lambda: ext_gen.draw_h2o(rotate=True), ["mouse_modes/icons"]),
    "rotate_atoms.png": (lambda: ext_gen.draw_h2o(rotate=True), ["mouse_modes/icons"]),
    "rotatesel.png": (base_gen.draw_rotate, ["mouse_modes/icons"]),
    "clip.png": (lambda: ext_gen.draw_clip(False), ["mouse_modes/icons"]),
    "clip_wht.png": (lambda: ext_gen.draw_clip(False), ["mouse_modes/icons"]),
    "cliprot.png": (lambda: ext_gen.draw_clip(True), ["mouse_modes/icons"]),
    "cliprot_wht.png": (lambda: ext_gen.draw_clip(True), ["mouse_modes/icons"]),
    "whitebg.png": (base_gen.draw_whitebg, ["shortcuts/icons"]),
    "graybg.png": (base_gen.draw_graybg, ["shortcuts/icons"]),
    "blackbg.png": (base_gen.draw_blackbg, ["shortcuts/icons"]),
    "simplelight.png": (base_gen.draw_simplelight, ["shortcuts/icons"]),
    "softlight.png": (base_gen.draw_softlight, ["shortcuts/icons"]),
    "fulllight.png": (base_gen.draw_fulllight, ["shortcuts/icons"]),
    "flat.png": (ext_gen.draw_flat, ["shortcuts/icons"]),
    "shadow.png": (ext_gen.draw_shadow, ["shortcuts/icons"]),
    "silhouette.png": (ext_gen.draw_silhouette, ["shortcuts/icons"]),
    "silhouette-dark.png": (ext_gen.draw_silhouette, ["shortcuts/icons"]),
    "sideview.png": (base_gen.draw_sideview, ["toolbar/icons"]),
    "viewall.png": (base_gen.draw_viewall, ["shortcuts/icons"]),
    "viewall-dark.png": (base_gen.draw_viewall, ["shortcuts/icons"]),
    "viewsel.png": (base_gen.draw_viewsel, ["shortcuts/icons"]),
    "viewsel-dark.png": (base_gen.draw_viewsel, ["shortcuts/icons"]),
    "orient.png": (base_gen.draw_orient, ["shortcuts/icons"]),
    "orient-dark.png": (base_gen.draw_orient, ["shortcuts/icons"]),
    "camera.png": (base_gen.draw_camera, ["shortcuts/icons"]),
    "snapshot.png": (base_gen.draw_camera, ["shortcuts/icons"]),
    "video.png": (base_gen.draw_video, ["shortcuts/icons"]),
    "movie.png": (base_gen.draw_video, ["shortcuts/icons"]),
    "open-in-app.png": (base_gen.draw_open, ["toolbar/icons"]),
    "open.png": (base_gen.draw_open, ["toolbar/icons"]),
    "content-save.png": (base_gen.draw_save, ["toolbar/icons"]),
    "save.png": (base_gen.draw_save, ["toolbar/icons"]),
    "recentfiles.png": (base_gen.draw_recent, ["toolbar/icons"]),
    "recentfiles-dark.png": (base_gen.draw_recent, ["toolbar/icons"]),
    "recent.png": (base_gen.draw_recent, ["toolbar/icons"]),
    "undo-variant.png": (base_gen.draw_undo, ["toolbar/icons"]),
    "undo.png": (base_gen.draw_undo, ["toolbar/icons"]),
    "redo-variant.png": (base_gen.draw_redo, ["toolbar/icons"]),
    "redo.png": (base_gen.draw_redo, ["toolbar/icons"]),
    "exit.png": (ext_gen.draw_exit, ["toolbar/icons"]),
    "close-box.png": (ext_gen.draw_close_box, ["toolbar/icons"]),
    "file-image.png": (ext_gen.draw_file_image, ["toolbar/icons"]),
    "gear.png": (ext_gen.draw_gear, ["ui/icons"]),
    "shown.png": (lambda: ext_gen.draw_eye(True), ["ui/icons"]),
    "hidden.png": (lambda: ext_gen.draw_eye(False), ["ui/icons"]),
    "play.png": (lambda: ext_gen.draw_media_btn("play"), ["ui/icons"]),
    "play256.png": (lambda: ext_gen.draw_media_btn("play"), ["ui/icons"]),
    "pause.png": (lambda: ext_gen.draw_media_btn("pause"), ["ui/icons"]),
    "pause128.png": (lambda: ext_gen.draw_media_btn("pause"), ["ui/icons"]),
    "stop.png": (lambda: ext_gen.draw_media_btn("stop"), ["ui/icons"]),
    "stop128.png": (lambda: ext_gen.draw_media_btn("stop"), ["ui/icons"]),
    "record.png": (lambda: ext_gen.draw_media_btn("record"), ["ui/icons"]),
    "record128.png": (lambda: ext_gen.draw_media_btn("record"), ["ui/icons"]),
    "magnifying-glass.png": (lambda: ext_gen.draw_magnifier(""), ["sel_inspector/icons"]),
    "magnifying-glass-thin.png": (lambda: ext_gen.draw_magnifier("thin"), ["sel_inspector/icons"]),
    "magnifying-glass+water.png": (lambda: ext_gen.draw_magnifier("water"), ["sel_inspector/icons"]),
    "ckicon.png": (lambda: ext_gen.draw_color_key(False), ["color_key/icons"]),
    "ckicon0.png": (lambda: ext_gen.draw_color_key(False), ["color_key/icons"]),
    "ckiconvertical.png": (lambda: ext_gen.draw_color_key(True), ["color_key/icons"]),
    "lock.png": (ext_gen.draw_lock, ["shortcuts/icons"]),
    "icecube.png": (ext_gen.draw_icecube, ["shortcuts/icons"]),
    "vr.png": (lambda: ext_gen.draw_headset(False), ["shortcuts/icons"]),
    "xr.png": (lambda: ext_gen.draw_headset(True), ["shortcuts/icons"]),
    "nextdocking.png": (draw_stick, ["viewdock/icons"]),
    "orthopick.png": (base_gen.draw_orient, ["orthopick/icons"]),
    "create_segmentation.png": (draw_volseg, ["segmentations/icons"]),
    "segmentation.png": (draw_volseg, ["segmentations/icons"]),
    "mouse.png": (base_gen.draw_select, ["segmentations/icons"]),
    "move_cursor.png": (base_gen.draw_center, ["segmentations/icons"]),
    "resize_cursor.png": (base_gen.draw_resize, ["segmentations/icons"]),
    "right_controller.png": (base_gen.draw_select, ["segmentations/icons"]),
    "mac_close.png": (lambda: base_gen.draw_traffic_light(PASTEL_CORAL), []),
    "mac_close_hover.png": (lambda: base_gen.draw_traffic_light((255, 95, 86, 255), "x"), []),
    "mac_minimize.png": (lambda: base_gen.draw_traffic_light(PASTEL_BUTTER), []),
    "mac_minimize_hover.png": (lambda: base_gen.draw_traffic_light((255, 189, 46, 255), "-"), []),
    "mac_zoom.png": (lambda: base_gen.draw_traffic_light(PASTEL_MINT), []),
    "mac_zoom_hover.png": (lambda: base_gen.draw_traffic_light((52, 199, 89, 255), "+"), []),
}
count = 0
for fname, (fn, subdirs) in ICON_BUILDERS.items():
    im = fn()
    save_image(im, fname, subdirs)
    count += 1
