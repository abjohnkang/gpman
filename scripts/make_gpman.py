"""Generate flat GPMan pictures (same drawing as the hero in git-power-concept.svg).

    python3 scripts/make_gpman.py assets/gpman

PNG copies: for f in assets/gpman/*.svg; do rsvg-convert -w 800 "$f" -o "assets/gpman/png/$(basename "${f%.svg}").png"; done
"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

SUIT, SUIT_DARK, CAPE, CAPE_DARK, GOLD = "#6c4cff", "#5a3fd6", "#ff7a1a", "#e8590c", "#ffb020"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"


# ── body parts ───────────────────────────────────────────────────────────────
def arm(points, end, end_r=11, hand="fist"):
    d = "M" + " L".join(f"{x} {y}" for x, y in points)
    s = f'<path d="{d}" fill="none" stroke="{SUIT}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
    x, y = end
    s += f'<circle cx="{x}" cy="{y}" r="{end_r}" fill="{GOLD}"/>'
    if hand == "open":  # waving hand: three raised fingers
        for dx in (-7, 0, 7):
            s += f'<rect x="{x + dx - 3}" y="{y - end_r - 9}" width="6" height="14" rx="3" fill="{GOLD}"/>'
    return s


HIP_L = arm([(568, 194), (538, 238), (566, 266)], (566, 266))
HIP_R = arm([(632, 194), (662, 238), (634, 266)], (634, 266))
DOWN_L = arm([(568, 194), (556, 236), (560, 270)], (560, 274))
DOWN_R = arm([(632, 194), (644, 236), (640, 270)], (640, 274))
FIST_UP_L = arm([(568, 194), (540, 148), (532, 108)], (531, 100), 14)
FIST_UP_R = arm([(632, 194), (660, 148), (668, 108)], (669, 100), 14)
WAVE_R = arm([(632, 194), (664, 158), (672, 118)], (674, 110), 13, "open")
HOLD_R = arm([(632, 194), (660, 150), (666, 118)], (667, 112), 12)
LENS_R = arm([(632, 194), (664, 170), (676, 136)], (677, 128), 12)

SMILE = '<path d="M591 160 Q600 167 609 160" fill="none" stroke="#7a3b2e" stroke-width="2.5" stroke-linecap="round"/>'
GRIN = ('<path d="M588 157 Q600 174 612 157 Z" fill="#7a3b2e"/>'
        '<path d="M591 158 H609 L607 162 H593 Z" fill="#ffffff"/>')
# worried: brows rise toward the middle, small frown
WORRY = ('<path d="M574 130 Q583 126 592 122" fill="none" stroke="#2b2d55" stroke-width="3" stroke-linecap="round"/>'
         '<path d="M626 130 Q617 126 608 122" fill="none" stroke="#2b2d55" stroke-width="3" stroke-linecap="round"/>'
         '<path d="M591 165 Q600 157 609 165" fill="none" stroke="#7a3b2e" stroke-width="2.5" stroke-linecap="round"/>')


def hero(left, right, face=SMILE):
    return f'''
  <path d="M566 182 C528 236 510 330 482 400 Q540 382 600 392 Q660 382 718 400 C690 330 672 236 634 182 Z" fill="{CAPE}"/>
  <path d="M600 190 C596 270 596 330 600 392 Q660 382 718 400 C690 330 672 236 634 182 Z" fill="{CAPE_DARK}"/>
  <path d="M572 286 L566 382 H594 L599 286 Z" fill="{SUIT_DARK}"/>
  <path d="M601 286 L606 382 H634 L628 286 Z" fill="{SUIT_DARK}"/>
  <path d="M567 352 H594 L594 384 Q580 392 560 386 Z" fill="{GOLD}"/>
  <path d="M606 352 H633 L640 386 Q620 392 606 384 Z" fill="{GOLD}"/>
  {right}
  <path d="M564 186 Q600 172 636 186 L630 292 H570 Z" fill="{SUIT}"/>
  <rect x="568" y="274" width="64" height="13" rx="4" fill="{GOLD}"/>
  <rect x="592" y="272" width="16" height="17" rx="3" fill="#fff3b0"/>
  {left}
  <circle cx="600" cy="224" r="24" fill="#ffcf6b" stroke="#fff3b0" stroke-width="3"/>
  <g stroke="#1a1f3d" stroke-width="3.5" fill="none" stroke-linecap="round"><path d="M592 210 V238"/><path d="M608 214 C608 226 592 222 592 232"/></g>
  <g fill="#1a1f3d"><circle cx="592" cy="210" r="4"/><circle cx="592" cy="238" r="4"/><circle cx="608" cy="214" r="4"/></g>
  <rect x="592" y="166" width="16" height="16" fill="#f2c39c"/>
  <circle cx="600" cy="142" r="30" fill="#ffd7b5"/>
  <path d="M570 140 C568 112 590 104 604 106 C624 106 634 120 631 138 C622 124 606 120 590 126 C582 130 576 134 570 140 Z" fill="#2b2d55"/>
  <path d="M572 140 Q600 130 628 140 L626 154 Q614 158 600 150 Q586 158 574 154 Z" fill="{SUIT}"/>
  <ellipse cx="587" cy="146" rx="6" ry="4" fill="#ffffff"/>
  <ellipse cx="613" cy="146" rx="6" ry="4" fill="#ffffff"/>
  {face}'''


HEAD = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#151b3a"/></linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#ffe680" stop-opacity="0.7"/><stop offset="0.45" stop-color="#ffb020" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#ff6a00" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="400" height="400" rx="28" fill="url(#bg)"/>'''


def page(title, desc, caption, body, back="", front=""):
    return HEAD.format(title=title, desc=desc) + f'''
  <circle cx="200" cy="200" r="150" fill="url(#glow)"/>
  {back}
  <g transform="translate(-400 -48)">{body}
  </g>
  {front}
  <text x="200" y="378" fill="#ffcf6b" font-family="{FONT}" font-size="18" font-weight="800" text-anchor="middle" letter-spacing="1">{caption}</text>
</svg>
'''


def star(x, y, r, color):
    return (f'<path d="M{x} {y-r} Q{x} {y} {x+r} {y} Q{x} {y} {x} {y+r} Q{x} {y} {x-r} {y} '
            f'Q{x} {y} {x} {y-r} Z" fill="{color}"/>')


# ── scene props ──────────────────────────────────────────────────────────────
CONFETTI = "".join(
    f'<rect x="{x}" y="{y}" width="8" height="14" rx="2" fill="{c}" transform="rotate({a} {x+4} {y+7})"/>'
    for x, y, a, c in [(60, 60, 20, "#2ecc9a"), (110, 40, -30, "#c77dff"), (300, 50, 35, "#4f8cff"),
                       (340, 100, -15, "#ff7a1a"), (50, 150, -40, "#ffcf6b"), (350, 180, 25, "#2ecc9a"),
                       (80, 250, 10, "#ff7a1a"), (330, 270, -25, "#c77dff")]
) + star(150, 70, 10, "#fff3b0") + star(270, 90, 8, "#ffffff")

SPEED = "".join(
    f'<path d="M{x} {y} L{x+w} {y-w*0.7:.0f}" stroke="#8ea2d8" stroke-opacity="0.6" stroke-width="5" stroke-linecap="round"/>'
    for x, y, w in [(40, 300, 60), (80, 340, 70), (30, 250, 40)]
)

COMMIT_CHAIN = ('<path d="M36 36 H247" stroke="#2ecc9a" stroke-width="5" stroke-linecap="round" opacity="0.7"/>'
                '<g stroke="#0b1020" stroke-width="3" fill="#2ecc9a">'
                + "".join(f'<circle cx="{x}" cy="36" r="8"/>' for x in (50, 100, 150, 200)) + "</g>")
COMMIT_NODE = f'''<circle cx="267" cy="36" r="30" fill="#2ecc9a" opacity="0.25"/>
  <circle cx="267" cy="36" r="18" fill="#2ecc9a" stroke="#dfffee" stroke-width="4"/>
  <text x="267" y="41" fill="#0b1020" font-family="{MONO}" font-size="13" font-weight="700" text-anchor="middle">+1</text>'''

WAVE_LINES = ('<path d="M300 70 Q312 84 304 100" fill="none" stroke="#ffcf6b" stroke-width="4" stroke-linecap="round"/>'
              '<path d="M314 60 Q332 82 318 108" fill="none" stroke="#ffcf6b" stroke-width="4" stroke-linecap="round" opacity="0.6"/>')

CODE = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="{c}" opacity="0.6"/>'
               for x, y, w, c in [(36, 100, 70, "#c77dff"), (52, 118, 90, "#4f8cff"), (52, 136, 60, "#2ecc9a"),
                                  (36, 154, 80, "#ff7a1a"), (52, 172, 50, "#4f8cff")])
LENS = '''<line x1="254" y1="68" x2="275" y2="82" stroke="#8ea2d8" stroke-width="7" stroke-linecap="round"/>
  <circle cx="236" cy="48" r="24" fill="#9fd3ff" fill-opacity="0.25" stroke="#ffcf6b" stroke-width="6"/>
  <path d="M224 38 Q230 32 238 32" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>'''

OOPS = '''<path d="M286 66 C292 78 296 86 296 92 C296 100 290 104 284 104 C278 104 272 100 272 92 C272 86 278 78 286 66 Z" fill="#9fd3ff"/>
  <g transform="translate(56 70)"><path d="M0 44 L26 0 L52 44 Z" fill="#ff5e3a" stroke="#ffcf6b" stroke-width="3" stroke-linejoin="round"/>
    <rect x="23" y="13" width="6" height="17" rx="3" fill="#ffffff"/><circle cx="26" cy="36" r="3.5" fill="#ffffff"/></g>'''

# ── pictures ─────────────────────────────────────────────────────────────────
PICTURES = {
    "gpman-hero": ("GPMan hero", "GPMan stands proud with one fist raised and the other hand on his hip.",
                   "GPMan", hero(FIST_UP_L, HIP_R), star(80, 90, 10, "#fff3b0") + star(320, 120, 7, "#ffffff"), ""),
    "gpman-wave": ("GPMan waving", "GPMan grins and waves hello.",
                   "Hello, developer!", hero(DOWN_L, WAVE_R, GRIN), WAVE_LINES, ""),
    "gpman-flying": ("GPMan flying", "GPMan flies up and to the right, fist forward, cape streaming behind him.",
                     "Push to main!", f'<g transform="translate(-10 -40) rotate(55 600 245)">{hero(FIST_UP_L, HIP_R, GRIN)}</g>', SPEED, ""),
    "gpman-commit": ("GPMan commit", "GPMan holds up a glowing green +1 commit at the end of a commit chain.",
                     "Commit power!", hero(HIP_L, HOLD_R, GRIN), COMMIT_CHAIN, COMMIT_NODE),
    "gpman-review": ("GPMan code review", "GPMan inspects lines of code with a big magnifying glass.",
                     "Code review!", hero(HIP_L, LENS_R), CODE, LENS),
    "gpman-celebrate": ("GPMan celebrating", "GPMan raises both fists and grins as confetti falls.",
                        "Level up!", hero(FIST_UP_L, FIST_UP_R, GRIN), CONFETTI, ""),
    "gpman-oops": ("GPMan oops", "GPMan looks worried next to a warning sign: something went wrong.",
                   "Oops! Merge conflict", hero(DOWN_L, DOWN_R, WORRY), "", OOPS),
}

for name, (title, desc, caption, body, back, front) in PICTURES.items():
    (OUT / f"{name}.svg").write_text(page(title, desc, caption, body, back, front))

# avatar: head-and-shoulders close-up, no caption
(OUT / "gpman-avatar.svg").write_text(HEAD.format(
    title="GPMan avatar",
    desc="Close-up of GPMan's masked, grinning face above his gold git-branch emblem, for profile pictures.",
) + f'''
  <circle cx="200" cy="190" r="190" fill="url(#glow)"/>
  <g transform="translate(200 215) scale(2.4) translate(-600 -190)">{hero(HIP_L, HIP_R, GRIN)}
  </g>
</svg>
''')

for p in sorted(OUT.glob("*.svg")):
    print(p)
