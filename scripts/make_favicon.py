"""Generate the GPMan favicon set for the website.

    python3 scripts/make_favicon.py assets/favicon

Writes favicon.svg (64x64 design, modern browsers), favicon.ico (16/32/48),
apple-touch-icon.png (180), icon-192.png and icon-512.png (web app manifest)
and site.webmanifest. Needs rsvg-convert and Pillow.
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

# GPMan's face, simplified so the purple mask and white eyes still read at 16 px.
FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <title>GPMan</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b2350"/><stop offset="1" stop-color="#0b1020"/></linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="url(#bg)"/>
  <path d="M10 64 Q14 50 32 50 Q50 50 54 64 Z" fill="#ff7a1a"/>
  <path d="M18 64 Q20 54 32 54 Q44 54 46 64 Z" fill="#6c4cff"/>
  <circle cx="32" cy="32" r="19" fill="#ffd7b5"/>
  <path d="M13 31 C11 15 22 8 33 8 C46 8 54 17 51 31 C46 22 38 19 31 21 C24 20 17 24 13 31 Z" fill="#2b2d55"/>
  <path d="M12 30 Q32 23 52 30 L51 40 Q42 43 32 37 Q22 43 13 40 Z" fill="#6c4cff"/>
  <ellipse cx="23.5" cy="33" rx="4.2" ry="3" fill="#ffffff"/>
  <ellipse cx="40.5" cy="33" rx="4.2" ry="3" fill="#ffffff"/>
  <path d="M26 42 Q32 49 38 42 Z" fill="#7a3b2e"/>
</svg>
'''

svg = OUT / "favicon.svg"
svg.write_text(FAVICON)


def png(size, name):
    out = OUT / name
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(svg), "-o", str(out)], check=True)
    return out


big = png(512, "icon-512.png")
png(192, "icon-192.png")
png(180, "apple-touch-icon.png")
Image.open(big).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

(OUT / "site.webmanifest").write_text(json.dumps({
    "name": "Git Power",
    "short_name": "Git Power",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
    ],
    "theme_color": "#151b3a",
    "background_color": "#0b1020",
    "display": "standalone",
}, indent=2) + "\n")

for p in sorted(OUT.iterdir()):
    print(p)
