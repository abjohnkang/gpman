# gpmeter — Git Power Meter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="assets/gpmeter-concept.svg" alt="gpmeter concept: your commit history powers up GPMan (Git-Power Man) and becomes a power score built from frequency, consistency and impact" width="100%">
</p>

gpmeter (Git Power Meter) is a tool designed to measure your software development activity and impact based on your Git commit history. By analyzing your repository data, it calculates an activity score that reflects your coding output, consistency, and overall development power.

## Features

* **Commit Analysis:** Tracks your commit frequency, consistency, and patterns over time.
* **Activity Scoring:** Calculates a unique "power" metric based on the volume and impact of your code changes.
* **Local Processing:** Analyzes your `.git` history directly on your local machine without exposing your source code.

## Meet GPMan

GPMan (Git-Power Man) is the gpmeter mascot. Feel free to use him in docs, slides, release notes and posts.

<table>
  <tr>
    <td align="center"><img src="assets/gpman/gpman-hero.svg" alt="GPMan standing proud with one fist raised" width="160"><br><sub>Hero</sub></td>
    <td align="center"><img src="assets/gpman/gpman-wave.svg" alt="GPMan waving hello" width="160"><br><sub>Hello</sub></td>
    <td align="center"><img src="assets/gpman/gpman-commit.svg" alt="GPMan holding up a glowing +1 commit" width="160"><br><sub>Commit</sub></td>
    <td align="center"><img src="assets/gpman/gpman-flying.svg" alt="GPMan flying with his cape streaming" width="160"><br><sub>Push</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/gpman/gpman-review.svg" alt="GPMan inspecting code with a magnifying glass" width="160"><br><sub>Code review</sub></td>
    <td align="center"><img src="assets/gpman/gpman-celebrate.svg" alt="GPMan celebrating with both fists up and confetti" width="160"><br><sub>Level up</sub></td>
    <td align="center"><img src="assets/gpman/gpman-oops.svg" alt="GPMan looking worried next to a warning sign" width="160"><br><sub>Oops</sub></td>
    <td align="center"><img src="assets/gpman/gpman-avatar.svg" alt="Close-up of GPMan's grinning masked face" width="160"><br><sub>Avatar</sub></td>
  </tr>
</table>

Face cuts for reactions, stickers and status messages:

<table>
  <tr>
    <td align="center"><img src="assets/gpman/gpman-face-smiling.svg" alt="GPMan smiling" width="100"><br><sub>Smiling</sub></td>
    <td align="center"><img src="assets/gpman/gpman-face-happy.svg" alt="GPMan laughing happily" width="100"><br><sub>Happy</sub></td>
    <td align="center"><img src="assets/gpman/gpman-face-wink.svg" alt="GPMan winking" width="100"><br><sub>Wink</sub></td>
    <td align="center"><img src="assets/gpman/gpman-face-bored.svg" alt="GPMan looking bored" width="100"><br><sub>Bored</sub></td>
    <td align="center"><img src="assets/gpman/gpman-face-sleepy.svg" alt="GPMan dozing off" width="100"><br><sub>Sleepy</sub></td>
    <td align="center"><img src="assets/gpman/gpman-face-angry.svg" alt="GPMan angry" width="100"><br><sub>Angry</sub></td>
    <td align="center"><img src="assets/gpman/gpman-face-crying.svg" alt="GPMan crying" width="100"><br><sub>Crying</sub></td>
  </tr>
</table>

The SVGs in [`assets/gpman/`](assets/gpman/) are animated (CSS, paused for viewers who prefer reduced motion); still 800×800 PNGs are in [`assets/gpman/png/`](assets/gpman/png/). To change or add a picture, edit [`scripts/make_gpman.py`](scripts/make_gpman.py) and run `python3 scripts/make_gpman.py assets/gpman`.

A GPMan favicon set for the website is in [`assets/favicon/`](assets/favicon/) (made by [`scripts/make_favicon.py`](scripts/make_favicon.py)). Copy it to the site root and add:

```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abjohnkang/gpmeter.git
