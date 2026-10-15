"""Generate flat GPM pictures (same drawing as the hero in gpman-concept.svg).

    python3 scripts/make_gpm.py assets/gpm

PNG copies: for f in assets/gpm/*.svg; do rsvg-convert -w 800 "$f" -o "assets/gpm/png/$(basename "${f%.svg}").png"; done

Each SVG carries its own CSS animation (it plays wherever the SVG is shown as an
image, including GitHub READMEs) and stops for viewers who prefer reduced motion.
PNG renderers ignore the animation, so the PNGs are the still pose.
Animated parts are wrapped in their own <g class="..."> because a CSS transform
replaces an element's transform attribute.
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
  <g class="cape">
    <path d="M566 182 C528 236 510 330 482 400 Q540 382 600 392 Q660 382 718 400 C690 330 672 236 634 182 Z" fill="{CAPE}"/>
    <path d="M600 190 C596 270 596 330 600 392 Q660 382 718 400 C690 330 672 236 634 182 Z" fill="{CAPE_DARK}"/>
  </g>
  <path d="M572 286 L566 382 H594 L599 286 Z" fill="{SUIT_DARK}"/>
  <path d="M601 286 L606 382 H634 L628 286 Z" fill="{SUIT_DARK}"/>
  <path d="M567 352 H594 L594 384 Q580 392 560 386 Z" fill="{GOLD}"/>
  <path d="M606 352 H633 L640 386 Q620 392 606 384 Z" fill="{GOLD}"/>
  <g class="arm-r">{right}</g>
  <path d="M564 186 Q600 172 636 186 L630 292 H570 Z" fill="{SUIT}"/>
  <rect x="568" y="274" width="64" height="13" rx="4" fill="{GOLD}"/>
  <rect x="592" y="272" width="16" height="17" rx="3" fill="#fff3b0"/>
  <g class="arm-l">{left}</g>
  <circle cx="600" cy="224" r="24" fill="#ffcf6b" stroke="#fff3b0" stroke-width="3"/>
  <g stroke="#1a1f3d" stroke-width="3.5" fill="none" stroke-linecap="round"><path d="M592 210 V238"/><path d="M608 214 C608 226 592 222 592 232"/></g>
  <g fill="#1a1f3d"><circle cx="592" cy="210" r="4"/><circle cx="592" cy="238" r="4"/><circle cx="608" cy="214" r="4"/></g>
  <rect x="592" y="166" width="16" height="16" fill="#f2c39c"/>
  <circle cx="600" cy="142" r="30" fill="#ffd7b5"/>
  <path d="M570 140 C568 112 590 104 604 106 C624 106 634 120 631 138 C622 124 606 120 590 126 C582 130 576 134 570 140 Z" fill="#2b2d55"/>
  <path d="M572 140 Q600 130 628 140 L626 154 Q614 158 600 150 Q586 158 574 154 Z" fill="{SUIT}"/>
  <g class="eyes"><ellipse cx="587" cy="146" rx="6" ry="4" fill="#ffffff"/><ellipse cx="613" cy="146" rx="6" ry="4" fill="#ffffff"/></g>
  {face}'''


# ── motion (CSS) ─────────────────────────────────────────────────────────────
# Shared: glow breathes, eyes blink, figure bobs. Origins are in the local user
# space of each element (body parts: the 600-centred drawing above).
BASE_CSS = '''
    .glow { transform-origin: 200px 200px; animation: glow 2.4s ease-in-out infinite; }
    .eyes { transform-origin: 600px 146px; animation: blink 4s infinite; }
    .fig { animation: bob 2.4s ease-in-out infinite; }
    .tw { transform-box: fill-box; transform-origin: center; animation: twinkle 1.8s ease-in-out infinite; }
    .tw.b { animation-delay: -0.9s; }
    @keyframes glow { 0%, 100% { transform: scale(0.94); opacity: 0.85; } 50% { transform: scale(1.06); opacity: 1; } }
    @keyframes blink { 0%, 92%, 100% { transform: scaleY(1); } 95% { transform: scaleY(0.1); } }
    @keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
    @keyframes twinkle { 0%, 100% { transform: scale(0.6); opacity: 0.5; } 50% { transform: scale(1.2); opacity: 1; } }'''
REDUCED = '''
    @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }'''

MOTION = {
    "gpm-hero": '''
    .arm-l { transform-origin: 568px 194px; animation: pump 2.4s ease-in-out infinite; }
    @keyframes pump { 0%, 100% { transform: rotate(0); } 50% { transform: rotate(-7deg); } }''',
    "gpm-wave": '''
    .arm-r { transform-origin: 632px 194px; animation: wave 1s ease-in-out infinite alternate; }
    .wl { animation: fade 1s ease-in-out infinite alternate; }
    .wl.b { animation-delay: -0.5s; }
    @keyframes wave { from { transform: rotate(-12deg); } to { transform: rotate(10deg); } }
    @keyframes fade { from { opacity: 0.15; } to { opacity: 1; } }''',
    "gpm-flying": '''
    .fig { animation: fly 1.6s ease-in-out infinite; }
    .cape { transform-origin: 600px 186px; animation: flutter 0.4s ease-in-out infinite alternate; }
    .sp { animation: streak 0.8s linear infinite; }
    .sp.b { animation-delay: -0.27s; } .sp.c { animation-delay: -0.53s; }
    @keyframes fly { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(6px, -8px); } }
    @keyframes flutter { from { transform: scale(1, 1); } to { transform: scale(0.95, 1.03); } }
    @keyframes streak { 0% { transform: translate(18px, -13px); opacity: 0; } 30% { opacity: 1; } 100% { transform: translate(-30px, 21px); opacity: 0; } }''',
    "gpm-commit": '''
    .arm-r { transform-origin: 632px 194px; animation: lift 2.4s ease-in-out infinite; }
    .node { transform-origin: 267px 36px; animation: lift-node 2.4s ease-in-out infinite; }
    .halo { transform-box: fill-box; transform-origin: center; animation: halo 1.2s ease-out infinite; }
    .dot { animation: light 2.4s ease-in-out infinite; }
    .d2 { animation-delay: 0.2s; } .d3 { animation-delay: 0.4s; } .d4 { animation-delay: 0.6s; }
    @keyframes lift { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
    @keyframes lift-node { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-11px); } }  /* body bob + arm lift */
    @keyframes halo { 0% { transform: scale(0.7); opacity: 0.7; } 100% { transform: scale(1.5); opacity: 0; } }
    @keyframes light { 0%, 40%, 100% { fill: #2ecc9a; } 20% { fill: #dfffee; } }''',
    "gpm-review": '''
    .arm-r { transform-origin: 632px 194px; animation: scan 2.4s ease-in-out infinite; }
    .lens { transform-origin: 232px 146px; animation: scan-lens 2.4s ease-in-out infinite; }
    .code rect { animation: read 3s ease-in-out infinite; }
    .code rect:nth-child(2) { animation-delay: 0.3s; } .code rect:nth-child(3) { animation-delay: 0.6s; }
    .code rect:nth-child(4) { animation-delay: 0.9s; } .code rect:nth-child(5) { animation-delay: 1.2s; }
    @keyframes scan { 0%, 100% { transform: rotate(0); } 50% { transform: rotate(-22deg); } }
    @keyframes scan-lens { 0%, 100% { transform: translateY(0) rotate(0); } 50% { transform: translateY(-6px) rotate(-22deg); } }  /* follows the body bob */
    @keyframes read { 0%, 60%, 100% { opacity: 0.6; } 30% { opacity: 1; } }''',
    "gpm-celebrate": '''
    .fig { animation: jump 1.2s ease-in-out infinite; }
    .arm-l { transform-origin: 568px 194px; animation: cheer-l 0.6s ease-in-out infinite alternate; }
    .arm-r { transform-origin: 632px 194px; animation: cheer-r 0.6s ease-in-out infinite alternate; }
    .cf { animation: fall 2.4s linear infinite; }
    .cf:nth-child(2n) { animation-delay: -0.8s; } .cf:nth-child(3n) { animation-delay: -1.6s; }
    @keyframes jump { 0%, 100% { transform: translateY(0); } 40% { transform: translateY(-16px); } 60% { transform: translateY(-16px); } }
    @keyframes cheer-l { from { transform: rotate(4deg); } to { transform: rotate(-6deg); } }
    @keyframes cheer-r { from { transform: rotate(-4deg); } to { transform: rotate(6deg); } }
    @keyframes fall { 0% { transform: translateY(-30px); opacity: 0; } 15% { opacity: 1; } 85% { opacity: 1; } 100% { transform: translateY(70px); opacity: 0; } }''',
    "gpm-oops": '''
    .fig { animation: shake 2.4s ease-in-out infinite; }
    .drop { animation: drip 1.6s ease-in infinite; }
    .warn { animation: alarm 1.2s ease-in-out infinite; }
    @keyframes shake { 0%, 60%, 100% { transform: translateX(0); } 65%, 75%, 85% { transform: translateX(-3px); } 70%, 80%, 90% { transform: translateX(3px); } }
    @keyframes drip { 0% { transform: translateY(-6px); opacity: 0; } 20% { opacity: 1; } 100% { transform: translateY(26px); opacity: 0; } }
    @keyframes alarm { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }''',
    "gpm-avatar": '''
    .fig { animation: bob-s 2.4s ease-in-out infinite; }
    @keyframes bob-s { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-2.5px); } }  /* scaled 2.4x */''',
}


HEAD = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <style>{css}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#151b3a"/></linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#ffe680" stop-opacity="0.7"/><stop offset="0.45" stop-color="#ffb020" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#ff6a00" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="400" height="400" rx="28" fill="url(#bg)"/>'''


def head(name, title, desc):
    return HEAD.format(title=title, desc=desc, css=BASE_CSS + MOTION[name] + REDUCED)


def page(name, title, desc, caption, body, back="", front=""):
    return head(name, title, desc) + f'''
  <circle class="glow" cx="200" cy="200" r="150" fill="url(#glow)"/>
  {back}
  <g transform="translate(-400 -48)"><g class="fig">{body}
  </g></g>
  {front}
  <text x="200" y="378" fill="#ffcf6b" font-family="{FONT}" font-size="18" font-weight="800" text-anchor="middle" letter-spacing="1">{caption}</text>
</svg>
'''


def star(x, y, r, color, cls="tw"):
    return (f'<path class="{cls}" d="M{x} {y-r} Q{x} {y} {x+r} {y} Q{x} {y} {x} {y+r} Q{x} {y} {x-r} {y} '
            f'Q{x} {y} {x} {y-r} Z" fill="{color}"/>')


# ── scene props ──────────────────────────────────────────────────────────────
CONFETTI = '<g>' + "".join(
    f'<g class="cf"><rect x="{x}" y="{y}" width="8" height="14" rx="2" fill="{c}" transform="rotate({a} {x+4} {y+7})"/></g>'
    for x, y, a, c in [(60, 60, 20, "#2ecc9a"), (110, 40, -30, "#c77dff"), (300, 50, 35, "#4f8cff"),
                       (340, 100, -15, "#ff7a1a"), (50, 150, -40, "#ffcf6b"), (350, 180, 25, "#2ecc9a"),
                       (80, 250, 10, "#ff7a1a"), (330, 270, -25, "#c77dff")]
) + '</g>' + star(150, 70, 10, "#fff3b0") + star(270, 90, 8, "#ffffff", "tw b")

SPEED = "".join(
    f'<path class="sp {k}" d="M{x} {y} L{x+w} {y-w*0.7:.0f}" stroke="#8ea2d8" stroke-opacity="0.6" stroke-width="5" stroke-linecap="round"/>'
    for (x, y, w), k in zip([(40, 300, 60), (80, 340, 70), (30, 250, 40)], ["", "b", "c"])
)

COMMIT_CHAIN = ('<path d="M36 36 H247" stroke="#2ecc9a" stroke-width="5" stroke-linecap="round" opacity="0.7"/>'
                '<g stroke="#0b1020" stroke-width="3">'
                + "".join(f'<circle class="dot d{i}" cx="{x}" cy="36" r="8" fill="#2ecc9a"/>'
                          for i, x in enumerate((50, 100, 150, 200), 1)) + "</g>")
COMMIT_NODE = f'''<g class="node">
    <circle class="halo" cx="267" cy="36" r="24" fill="none" stroke="#2ecc9a" stroke-width="4"/>
    <circle cx="267" cy="36" r="30" fill="#2ecc9a" opacity="0.25"/>
    <circle cx="267" cy="36" r="18" fill="#2ecc9a" stroke="#dfffee" stroke-width="4"/>
    <text x="267" y="41" fill="#0b1020" font-family="{MONO}" font-size="13" font-weight="700" text-anchor="middle">+1</text>
  </g>'''

WAVE_LINES = ('<path class="wl" d="M300 70 Q312 84 304 100" fill="none" stroke="#ffcf6b" stroke-width="4" stroke-linecap="round"/>'
              '<path class="wl b" d="M314 60 Q332 82 318 108" fill="none" stroke="#ffcf6b" stroke-width="4" stroke-linecap="round" opacity="0.6"/>')

CODE = '<g class="code">' + "".join(
    f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="{c}" opacity="0.6"/>'
    for x, y, w, c in [(36, 100, 70, "#c77dff"), (52, 118, 90, "#4f8cff"), (52, 136, 60, "#2ecc9a"),
                       (36, 154, 80, "#ff7a1a"), (52, 172, 50, "#4f8cff")]) + '</g>'
LENS = '''<g class="lens">
    <line x1="254" y1="68" x2="275" y2="82" stroke="#8ea2d8" stroke-width="7" stroke-linecap="round"/>
    <circle cx="236" cy="48" r="24" fill="#9fd3ff" fill-opacity="0.25" stroke="#ffcf6b" stroke-width="6"/>
    <path d="M224 38 Q230 32 238 32" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>
  </g>'''

OOPS = '''<path class="drop" d="M286 66 C292 78 296 86 296 92 C296 100 290 104 284 104 C278 104 272 100 272 92 C272 86 278 78 286 66 Z" fill="#9fd3ff"/>
  <g class="warn"><g transform="translate(56 70)"><path d="M0 44 L26 0 L52 44 Z" fill="#ff5e3a" stroke="#ffcf6b" stroke-width="3" stroke-linejoin="round"/>
    <rect x="23" y="13" width="6" height="17" rx="3" fill="#ffffff"/><circle cx="26" cy="36" r="3.5" fill="#ffffff"/></g></g>'''

# ── pictures ─────────────────────────────────────────────────────────────────
PICTURES = {
    "gpm-hero": ("GPM hero", "GPM stands proud with one fist raised and the other hand on his hip.",
                   "GPM", hero(FIST_UP_L, HIP_R), star(80, 90, 10, "#fff3b0") + star(320, 120, 7, "#ffffff", "tw b"), ""),
    "gpm-wave": ("GPM waving", "GPM grins and waves hello.",
                   "Hello, developer!", hero(DOWN_L, WAVE_R, GRIN), WAVE_LINES, ""),
    "gpm-flying": ("GPM flying", "GPM flies up and to the right, fist forward, cape streaming behind him.",
                     "Push to main!", f'<g transform="translate(-10 -40) rotate(55 600 245)">{hero(FIST_UP_L, HIP_R, GRIN)}</g>', SPEED, ""),
    "gpm-commit": ("GPM commit", "GPM holds up a glowing green +1 commit at the end of a commit chain.",
                     "Commit power!", hero(HIP_L, HOLD_R, GRIN), COMMIT_CHAIN, COMMIT_NODE),
    "gpm-review": ("GPM code review", "GPM inspects lines of code with a big magnifying glass.",
                     "Code review!", hero(HIP_L, LENS_R), CODE, LENS),
    "gpm-celebrate": ("GPM celebrating", "GPM raises both fists and grins as confetti falls.",
                        "Level up!", hero(FIST_UP_L, FIST_UP_R, GRIN), CONFETTI, ""),
    "gpm-oops": ("GPM oops", "GPM looks worried next to a warning sign: something went wrong.",
                   "Oops! Merge conflict", hero(DOWN_L, DOWN_R, WORRY), "", OOPS),
}

for name, (title, desc, caption, body, back, front) in PICTURES.items():
    (OUT / f"{name}.svg").write_text(page(name, title, desc, caption, body, back, front))

# avatar: head-and-shoulders close-up, no caption
(OUT / "gpm-avatar.svg").write_text(head(
    "gpm-avatar", "GPM avatar",
    "Close-up of GPM's masked, grinning face above his gold git-branch emblem, for profile pictures.",
) + f'''
  <circle class="glow" cx="200" cy="190" r="190" fill="url(#glow)"/>
  <g transform="translate(200 215) scale(2.4) translate(-600 -190)"><g class="fig">{hero(HIP_L, HIP_R, GRIN)}
  </g></g>
</svg>
''')

# ── face cuts: head close-ups with expressions ───────────────────────────────
# Drawn in the same 600-centred space as hero() and scaled 4x, so 1 unit = 4 px.
# The mask hides real brows, so the eye holes, mask brows and mouth do the acting.
INK, MOUTH, TEAR = "#1a1f3d", "#7a3b2e", "#9fd3ff"


def eyes_open(cls="eyes"):
    return (f'<g class="{cls}"><ellipse cx="587" cy="146" rx="6" ry="4" fill="#fff"/>'
            '<ellipse cx="613" cy="146" rx="6" ry="4" fill="#fff"/></g>')


def arc_eye(x, up=True):  # closed eye: ^ (happy) or u (asleep)
    dy = -8 if up else 6
    return f'<path d="M{x-6} 148 Q{x} {148+dy} {x+6} 148" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'


def blush(color="#ff8a8a", op=0.55, cls=""):
    return (f'<g class="{cls}"><circle cx="579" cy="161" r="5" fill="{color}" opacity="{op}"/>'
            f'<circle cx="621" cy="161" r="5" fill="{color}" opacity="{op}"/></g>')


FACE_PARTS = {
    "smiling": eyes_open() + blush(op=0.4) + SMILE,
    "happy": arc_eye(587) + arc_eye(613) + blush(cls="bl")
             + f'<path d="M587 156 Q600 177 613 156 Z" fill="{MOUTH}"/>'
             + '<path d="M590 157 H610 L608 160 H592 Z" fill="#fff"/>'
             + '<ellipse cx="600" cy="168.5" rx="4.5" ry="2.4" fill="#ff8a8a"/>',
    "wink": '<ellipse class="eyes" cx="587" cy="146" rx="6" ry="4" fill="#fff"/>' + arc_eye(613) + blush(op=0.45)
            + f'<path d="M590 160 Q601 167 610 157" fill="none" stroke="{MOUTH}" stroke-width="2.5" stroke-linecap="round"/>'
            + '<ellipse cx="606" cy="163.5" rx="2.6" ry="2" fill="#ff8a8a"/>',
    # bored: lowered lids, eyes looking aside, flat tilted mouth
    "bored": '<path d="M581 146 H593 A6 4 0 0 1 581 146 Z" fill="#fff"/><path d="M607 146 H619 A6 4 0 0 1 607 146 Z" fill="#fff"/>'
             + f'<path d="M579.5 146 H594.5 M605.5 146 H620.5" stroke="#3b2aa0" stroke-width="2" stroke-linecap="round"/>'
             + f'<circle cx="591" cy="147.6" r="1.6" fill="{INK}"/><circle cx="617" cy="147.6" r="1.6" fill="{INK}"/>'
             + f'<path d="M592 162 L608 160" stroke="{MOUTH}" stroke-width="2.5" stroke-linecap="round"/>',
    "sleepy": arc_eye(587, up=False) + arc_eye(613, up=False) + blush(op=0.35)
              + f'<ellipse cx="600" cy="162" rx="2.6" ry="3" fill="{MOUTH}"/>',
    # angry: eye holes slant down toward the middle, mask brows fall toward the middle
    "angry": '<path d="M580 143 L594 148 Q591 152 586 151.5 Q580.5 150.5 580 146 Z" fill="#fff"/>'
             '<path d="M620 143 L606 148 Q609 152 614 151.5 Q619.5 150.5 620 146 Z" fill="#fff"/>'
             + f'<circle cx="588" cy="149" r="1.7" fill="{INK}"/><circle cx="612" cy="149" r="1.7" fill="{INK}"/>'
             + f'<path d="M578 137.5 L594 143 M622 137.5 L606 143" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
             + blush("#ff5e3a", 0.45)
             + f'<path d="M589 165 Q600 154 611 165 Z" fill="{MOUTH}"/>'
             + '<path d="M592.5 161 Q600 157.5 607.5 161 L607 162.6 Q600 159.6 593 162.6 Z" fill="#fff"/>',
    # crying: brows rise toward the middle, watery eyes, tear streams, wobbly mouth
    "crying": '<ellipse cx="587" cy="146" rx="6" ry="4.6" fill="#fff"/><ellipse cx="613" cy="146" rx="6" ry="4.6" fill="#fff"/>'
              + f'<path d="M581.2 147 Q587 152 592.8 147 Q587 149 581.2 147 Z" fill="{TEAR}"/>'
              + f'<path d="M607.2 147 Q613 152 618.8 147 Q613 149 607.2 147 Z" fill="{TEAR}"/>'
              + f'<circle cx="588.5" cy="145.5" r="2" fill="{INK}"/><circle cx="611.5" cy="145.5" r="2" fill="{INK}"/>'
              + '<circle cx="587.6" cy="144.6" r="0.8" fill="#fff"/><circle cx="610.6" cy="144.6" r="0.8" fill="#fff"/>'
              + f'<path d="M578 139 L593 135.5 M622 139 L607 135.5" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
              + f'<path d="M584 152 Q582 160 584 170 M616 152 Q618 160 616 170" fill="none" stroke="{TEAR}" stroke-width="3" stroke-linecap="round" opacity="0.9"/>'
              + f'<path class="mw" d="M590 166 Q600 156 610 166 Q600 162.5 590 166 Z" fill="{MOUTH}"/>'
              + f'<g class="drop"><path d="M584 171 C586 174 587 176 587 177.5 C587 179.3 585.7 180.4 584 180.4 C582.3 180.4 581 179.3 581 177.5 C581 176 582 174 584 171 Z" fill="{TEAR}"/></g>'
              + f'<g class="drop b"><path d="M616 171 C618 174 619 176 619 177.5 C619 179.3 617.7 180.4 616 180.4 C614.3 180.4 613 179.3 613 177.5 C613 176 614 174 616 171 Z" fill="{TEAR}"/></g>',
}


def zz(x, y, size, cls):
    return f'<text class="{cls}" x="{x}" y="{y}" fill="#c9d4f5" font-family="{FONT}" font-size="{size}" font-weight="800">Z</text>'


ANGER_MARK = '''<g class="mark"><g transform="translate(316 92)" stroke="#ff5e3a" stroke-width="7" stroke-linecap="round" fill="none">
    <path d="M-20 -6 Q-8 -6 -6 -20"/><path d="M6 -20 Q8 -6 20 -6"/><path d="M20 6 Q8 6 6 20"/><path d="M-6 20 Q-8 6 -20 6"/></g></g>'''
SIGH = '''<g class="puff"><circle cx="300" cy="300" r="14" fill="#c9d4f5" opacity="0.5"/><circle cx="322" cy="290" r="10" fill="#c9d4f5" opacity="0.4"/>
    <circle cx="338" cy="278" r="6" fill="#c9d4f5" opacity="0.3"/></g>'''

FACES = {
    "smiling": ("GPM smiling", "GPM smiles warmly.", "", '''
    .hd { transform-origin: 600px 178px; animation: tilt 3s ease-in-out infinite; }
    @keyframes tilt { 0%, 100% { transform: rotate(-2deg); } 50% { transform: rotate(2deg); } }'''),
    "happy": ("GPM happy", "GPM laughs with happy closed eyes and an open grin.",
              star(80, 100, 14, "#fff3b0") + star(330, 80, 10, "#ffffff", "tw b") + star(340, 230, 8, "#fff3b0", "tw"), '''
    .hd { animation: hop 0.8s ease-in-out infinite; }
    .bl { animation: glowy 0.8s ease-in-out infinite; }
    @keyframes hop { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
    @keyframes glowy { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }'''),
    "wink": ("GPM wink", "GPM winks and sticks out the tip of his tongue.", star(318, 96, 14, "#fff3b0"), '''
    .hd { transform-origin: 600px 178px; animation: lean 2.4s ease-in-out infinite; }
    @keyframes lean { 0%, 100% { transform: rotate(0); } 50% { transform: rotate(5deg); } }'''),
    "bored": ("GPM bored", "GPM looks bored, eyes half closed and glancing aside, sighing.", SIGH, '''
    .hd { transform-origin: 600px 178px; animation: sway 4s ease-in-out infinite; }
    .puff { animation: sigh 4s ease-out infinite; }
    @keyframes sway { 0%, 100% { transform: rotate(-3deg); } 50% { transform: rotate(1deg); } }
    @keyframes sigh { 0%, 30% { transform: translate(-16px, 10px); opacity: 0; } 50% { opacity: 1; } 100% { transform: translate(12px, -14px); opacity: 0; } }'''),
    "sleepy": ("GPM sleepy", "GPM dozes off with closed eyes as Z letters float up.",
               zz(286, 120, 40, "z1") + zz(322, 86, 30, "z2") + zz(348, 58, 22, "z3"), '''
    .hd { transform-origin: 600px 178px; animation: nod 3s ease-in-out infinite; }
    .z1, .z2, .z3 { animation: float 3s ease-out infinite; }
    .z2 { animation-delay: 1s; } .z3 { animation-delay: 2s; }
    @keyframes nod { 0%, 100% { transform: rotate(0); } 60% { transform: rotate(7deg); } }
    @keyframes float { 0% { transform: translate(0, 12px); opacity: 0; } 30% { opacity: 1; } 100% { transform: translate(14px, -18px); opacity: 0; } }'''),
    "angry": ("GPM angry", "GPM is angry: slanted eyes, brows down, clenched teeth, red cheeks and an anger mark.", ANGER_MARK, '''
    .hd { animation: rage 0.5s ease-in-out infinite; }
    .mark { transform-origin: 316px 92px; animation: throb 0.5s ease-in-out infinite; }
    @keyframes rage { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-1px); } 75% { transform: translateX(1px); } }
    @keyframes throb { 0%, 100% { transform: scale(0.85); } 50% { transform: scale(1.1); } }'''),
    "crying": ("GPM crying", "GPM cries, tears streaming from his eyes.", "", '''
    .hd { animation: sob 1.2s ease-in-out infinite; }
    .mw { transform-origin: 600px 163px; animation: wobble 0.6s ease-in-out infinite alternate; }
    .drop { animation: fall-tear 1.2s ease-in infinite; }
    .drop.b { animation-delay: -0.6s; }
    @keyframes sob { 0%, 100% { transform: translateY(0); } 30% { transform: translateY(-1.2px); } 60% { transform: translateY(0.4px); } }
    @keyframes wobble { from { transform: scaleX(1); } to { transform: scaleX(0.85); } }
    @keyframes fall-tear { 0% { transform: translateY(0); opacity: 1; } 100% { transform: translateY(14px); opacity: 0; } }'''),
}


def face_head(parts):
    return f'''
    <g class="cape"><path d="M566 182 C528 236 510 330 482 400 L718 400 C690 330 672 236 634 182 Z" fill="{CAPE}"/></g>
    <path d="M564 186 Q600 172 636 186 L640 230 H560 Z" fill="{SUIT}"/>
    <rect x="592" y="166" width="16" height="18" fill="#f2c39c"/>
    <g class="hd">
    <circle cx="600" cy="142" r="30" fill="#ffd7b5"/>
    <path d="M570 140 C568 112 590 104 604 106 C624 106 634 120 631 138 C622 124 606 120 590 126 C582 130 576 134 570 140 Z" fill="#2b2d55"/>
    <path d="M572 140 Q600 130 628 140 L626 154 Q614 158 600 150 Q586 158 574 154 Z" fill="{SUIT}"/>
    {parts}
    </g>'''


for key, (title, desc, fx, css) in FACES.items():
    name = f"gpm-face-{key}"
    MOTION[name] = css
    (OUT / f"{name}.svg").write_text(head(name, title, desc) + f'''
  <circle class="glow" cx="200" cy="190" r="170" fill="url(#glow)"/>
  <g transform="translate(200 210) scale(4) translate(-600 -150)">{face_head(FACE_PARTS[key])}
  </g>
  {fx}
</svg>
''')

for p in sorted(OUT.glob("*.svg")):
    print(p)
