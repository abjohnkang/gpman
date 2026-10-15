"""Generate the gpman (power meter) favicon set for the website.

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

# A power meter: thick gradient dial and a needle near max, bold enough to read at 16 px.
FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <title>gpman</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b2350"/><stop offset="1" stop-color="#0b1020"/></linearGradient>
    <linearGradient id="dial" gradientUnits="userSpaceOnUse" x1="12" y1="0" x2="52" y2="0">
      <stop offset="0" stop-color="#4f8cff"/><stop offset="0.4" stop-color="#2ecc9a"/><stop offset="0.7" stop-color="#ffb020"/><stop offset="1" stop-color="#ff5e3a"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="url(#bg)"/>
  <path d="M17.9 50.1 A20 20 0 1 1 46.1 50.1" fill="none" stroke="url(#dial)" stroke-width="8" stroke-linecap="round"/>
  <path d="M30.5 33.4 L46.7 27.5 L33.5 38.6 Z" fill="#fff3b0" stroke="#fff3b0" stroke-width="1.5" stroke-linejoin="round"/>
  <circle cx="32" cy="36" r="5.5" fill="#ffcf6b" stroke="#0b1020" stroke-width="2"/>
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
    "name": "gpman",
    "short_name": "gpman",
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
