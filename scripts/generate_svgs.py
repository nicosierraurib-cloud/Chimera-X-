# -*- coding: utf-8 -*-
"""
Generador de archivos vectoriales SVG puros con colores pasteles
para el repositorio Chimera-X-
"""

import os

SVG_DIR = r"C:\Users\Parfion\Documents\GitHub\Chimera-X-\svg"
os.makedirs(SVG_DIR, exist_ok=True)

# Paleta Pastel en formato HEX
P_BLUE = "#8EC5FC"
P_CORAL = "#FF9AA2"
P_MINT = "#B5EAD7"
P_BUTTER = "#FFF3B0"
P_PEACH = "#FFDAC1"
P_LAVENDER = "#E2D1F9"
P_CYAN = "#A0E7E5"
P_GRAY = "#B0BEC5"
GRAPHITE = "#2C2C2E"
WHITE = "#FFFFFF"

SVG_TEMPLATES = {
    "atomshow.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <circle cx="256" cy="256" r="50" fill="{P_BLUE}" stroke="{GRAPHITE}" stroke-width="12"/>
  <ellipse cx="256" cy="256" rx="186" ry="76" fill="none" stroke="{GRAPHITE}" stroke-width="16"/>
  <ellipse cx="256" cy="256" rx="186" ry="76" fill="none" stroke="{GRAPHITE}" stroke-width="16" transform="rotate(60 256 256)"/>
  <ellipse cx="256" cy="256" rx="186" ry="76" fill="none" stroke="{GRAPHITE}" stroke-width="16" transform="rotate(-60 256 256)"/>
  <circle cx="95" cy="256" r="20" fill="{P_MINT}" stroke="{GRAPHITE}" stroke-width="8"/>
  <circle cx="417" cy="256" r="20" fill="{P_MINT}" stroke="{GRAPHITE}" stroke-width="8"/>
</svg>''',

    "atomhide.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <circle cx="256" cy="256" r="50" fill="{P_BLUE}" stroke="{GRAPHITE}" stroke-width="12"/>
  <ellipse cx="256" cy="256" rx="186" ry="76" fill="none" stroke="{GRAPHITE}" stroke-width="16"/>
  <line x1="80" y1="80" x2="432" y2="432" stroke="{WHITE}" stroke-width="44" stroke-linecap="round"/>
  <line x1="80" y1="80" x2="432" y2="432" stroke="{P_CORAL}" stroke-width="28" stroke-linecap="round"/>
  <line x1="80" y1="80" x2="432" y2="432" stroke="{GRAPHITE}" stroke-width="6" stroke-linecap="round"/>
</svg>''',

    "ribshow.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <path d="M 60,256 C 140,140 220,370 300,256 C 360,170 410,230 440,256 L 420,200 L 460,256 L 420,312 Z" fill="{P_BLUE}" stroke="{GRAPHITE}" stroke-width="16" stroke-linejoin="round"/>
  <path d="M 60,236 C 140,120 220,350 300,236 C 360,150 410,210 440,236" fill="none" stroke="{P_LAVENDER}" stroke-width="12" stroke-linecap="round"/>
</svg>''',

    "nuc-ladder.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <path d="M 160,80 Q 220,168 160,256 T 160,432" fill="none" stroke="{GRAPHITE}" stroke-width="18" stroke-linecap="round"/>
  <path d="M 352,80 Q 292,168 352,256 T 352,432" fill="none" stroke="{GRAPHITE}" stroke-width="18" stroke-linecap="round"/>
  <line x1="170" y1="120" x2="342" y2="120" stroke="{P_BLUE}" stroke-width="18" stroke-linecap="round"/>
  <line x1="200" y1="180" x2="312" y2="180" stroke="{P_MINT}" stroke-width="18" stroke-linecap="round"/>
  <line x1="210" y1="256" x2="302" y2="256" stroke="{P_BLUE}" stroke-width="18" stroke-linecap="round"/>
  <line x1="200" y1="332" x2="312" y2="332" stroke="{P_MINT}" stroke-width="18" stroke-linecap="round"/>
  <line x1="170" y1="392" x2="342" y2="392" stroke="{P_BLUE}" stroke-width="18" stroke-linecap="round"/>
</svg>''',

    "nuc-fill.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <polygon points="180,160 280,160 330,246 280,332 180,332 130,246" fill="{P_BLUE}" stroke="{GRAPHITE}" stroke-width="16"/>
  <polygon points="280,160 370,190 410,260 330,332 280,332" fill="{P_MINT}" stroke="{GRAPHITE}" stroke-width="16"/>
  <line x1="190" y1="185" x2="270" y2="185" stroke="{WHITE}" stroke-width="8"/>
</svg>''',

    "nuc-slab.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <polygon points="110,260 330,260 390,224 170,224" fill="{P_BLUE}" stroke="{GRAPHITE}" stroke-width="12"/>
  <polygon points="110,260 330,260 330,320 110,320" fill="{P_BLUE}" stroke="{GRAPHITE}" stroke-width="12"/>
  <polygon points="150,160 370,160 430,124 210,124" fill="{P_CORAL}" stroke="{GRAPHITE}" stroke-width="12"/>
  <polygon points="150,160 370,160 370,220 150,220" fill="{P_CORAL}" stroke="{GRAPHITE}" stroke-width="12"/>
</svg>''',

    "colorbychain.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <path d="M 120,80 Q 84,168 120,256 T 120,432" fill="none" stroke="{P_BLUE}" stroke-width="32" stroke-linecap="round"/>
  <path d="M 256,80 Q 220,168 256,256 T 256,432" fill="none" stroke="{P_CORAL}" stroke-width="32" stroke-linecap="round"/>
  <path d="M 392,80 Q 356,168 392,256 T 392,432" fill="none" stroke="{P_MINT}" stroke-width="32" stroke-linecap="round"/>
  <path d="M 120,80 Q 84,168 120,256 T 120,432" fill="none" stroke="{GRAPHITE}" stroke-width="6" stroke-linecap="round"/>
  <path d="M 256,80 Q 220,168 256,256 T 256,432" fill="none" stroke="{GRAPHITE}" stroke-width="6" stroke-linecap="round"/>
  <path d="M 392,80 Q 356,168 392,256 T 392,432" fill="none" stroke="{GRAPHITE}" stroke-width="6" stroke-linecap="round"/>
</svg>''',

    "rainbow.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <path d="M 56,340 A 200,200 0 0,1 456,340" fill="none" stroke="{P_CORAL}" stroke-width="24"/>
  <path d="M 86,340 A 170,170 0 0,1 426,340" fill="none" stroke="{P_PEACH}" stroke-width="24"/>
  <path d="M 116,340 A 140,140 0 0,1 396,340" fill="none" stroke="{P_BUTTER}" stroke-width="24"/>
  <path d="M 146,340 A 110,110 0 0,1 366,340" fill="none" stroke="{P_MINT}" stroke-width="24"/>
  <path d="M 176,340 A 80,80 0 0,1 336,340" fill="none" stroke="{P_BLUE}" stroke-width="24"/>
</svg>''',

    "esp.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <ellipse cx="256" cy="256" rx="156" ry="136" fill="none" stroke="{P_GRAY}" stroke-width="10"/>
  <circle cx="140" cy="256" r="50" fill="{P_BLUE}" stroke="{GRAPHITE}" stroke-width="10"/>
  <line x1="115" y1="256" x2="165" y2="256" stroke="{GRAPHITE}" stroke-width="12" stroke-linecap="round"/>
  <line x1="140" y1="231" x2="140" y2="281" stroke="{GRAPHITE}" stroke-width="12" stroke-linecap="round"/>
  <circle cx="372" cy="256" r="50" fill="{P_CORAL}" stroke="{GRAPHITE}" stroke-width="10"/>
  <line x1="347" y1="256" x2="397" y2="256" stroke="{GRAPHITE}" stroke-width="12" stroke-linecap="round"/>
</svg>''',

    "mesh.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect x="110" y="140" width="292" height="250" rx="30" fill="none" stroke="{P_BLUE}" stroke-width="16"/>
  <line x1="160" y1="140" x2="160" y2="390" stroke="{GRAPHITE}" stroke-width="10"/>
  <line x1="220" y1="140" x2="220" y2="390" stroke="{GRAPHITE}" stroke-width="10"/>
  <line x1="280" y1="140" x2="280" y2="390" stroke="{GRAPHITE}" stroke-width="10"/>
  <line x1="340" y1="140" x2="340" y2="390" stroke="{GRAPHITE}" stroke-width="10"/>
  <line x1="110" y1="200" x2="402" y2="200" stroke="{GRAPHITE}" stroke-width="10"/>
  <line x1="110" y1="260" x2="402" y2="260" stroke="{GRAPHITE}" stroke-width="10"/>
  <line x1="110" y1="320" x2="402" y2="320" stroke="{GRAPHITE}" stroke-width="10"/>
</svg>''',

    "contour.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <ellipse cx="256" cy="256" rx="176" ry="176" fill="none" stroke="{GRAPHITE}" stroke-width="12"/>
  <ellipse cx="256" cy="256" rx="126" ry="136" fill="none" stroke="{GRAPHITE}" stroke-width="14"/>
  <ellipse cx="256" cy="256" rx="76" ry="86" fill="none" stroke="{GRAPHITE}" stroke-width="16"/>
  <circle cx="256" cy="251" r="16" fill="{P_MINT}" stroke="{GRAPHITE}" stroke-width="8"/>
</svg>''',

    "mac_traffic_lights.svg": f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 50">
  <circle cx="25" cy="25" r="15" fill="{P_CORAL}" stroke="{GRAPHITE}" stroke-width="2"/>
  <circle cx="75" cy="25" r="15" fill="{P_BUTTER}" stroke="{GRAPHITE}" stroke-width="2"/>
  <circle cx="125" cy="25" r="15" fill="{P_MINT}" stroke="{GRAPHITE}" stroke-width="2"/>
</svg>'''
}

for name, svg_text in SVG_TEMPLATES.items():
    p = os.path.join(SVG_DIR, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(svg_text)

print(f"Generados {len(SVG_TEMPLATES)} archivos SVG vectoriales puros en {SVG_DIR}.")
