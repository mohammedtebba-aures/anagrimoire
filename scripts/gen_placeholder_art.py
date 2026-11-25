#!/usr/bin/env python3
"""Generate Anagrimoire placeholder art.

Writes PNGs into src/WordRoguelike.Game/art/. Every file has a fixed path and
size (see art/README.md) so a hand-drawn replacement can be dropped in under
the same name. Re-running this overwrites only the files still listed as
placeholders in PLACEHOLDER_FILES below; remove a file from that list once
you've replaced it so the script never clobbers your art.

Requires: rsvg-convert, Pillow.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "src" / "WordRoguelike.Game" / "art"

# Palette: ink on parchment.
PARCHMENT = "#F3E7CC"
PARCHMENT_DARK = "#E2D1AC"
INK = "#2B2118"
INK_SOFT = "#5C4A3A"
UPGRADE = "#3F6FB5"
UPGRADE_BG = "#D9E5F5"
INKED = "#B7791F"
INKED_BG = "#F6E3BF"
CURSE = "#A33A3A"
CURSE_BG = "#F2D3D3"
SEAL = "#6A4FB0"
DESK = "#2A1F1A"
DESK_LIGHT = "#3A2C24"

TILE_W, TILE_H = 192, 256


def render(svg: str, out: Path, w: int, h: int) -> None:
    if not should_write(out):
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["rsvg-convert", "-w", str(w), "-h", str(h), "-o", str(out)],
        input=svg.encode(),
        check=True,
    )
    print("wrote", out.relative_to(ROOT))


def should_write(out: Path) -> bool:
    rel = out.relative_to(ART).as_posix()
    if rel not in PLACEHOLDER_FILES:
        print("skip (replaced)", rel)
        return False
    return True


def svg(w: int, h: int, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'


# ---------- tile frames ----------
# The game draws the letter glyph (letters/X.png) in the centre box and the
# point value in the top-left slot. Frames only carry state.

def tile_frame(border: str, border_w: int, banner: str | None, dashed: bool, corner: str) -> str:
    dash = ' stroke-dasharray="14 8"' if dashed else ""
    body = (
        f'<rect x="{border_w/2+2}" y="{border_w/2+2}" width="{TILE_W-border_w-4}" height="{TILE_H-border_w-4}" '
        f'rx="18" fill="{PARCHMENT}" stroke="{border}" stroke-width="{border_w}"{dash}/>'
        # inner rule
        f'<rect x="16" y="16" width="{TILE_W-32}" height="{TILE_H-32}" rx="10" fill="none" '
        f'stroke="{PARCHMENT_DARK}" stroke-width="2"/>'
    )
    if banner:
        body += (
            f'<path d="M{border_w+2} 206 H{TILE_W-border_w-2} V{TILE_H-18-border_w/2} '
            f'Q{TILE_W-border_w-2} {TILE_H-border_w-2} {TILE_W-18-border_w/2} {TILE_H-border_w-2} '
            f'H{18+border_w/2} Q{border_w+2} {TILE_H-border_w-2} {border_w+2} {TILE_H-18-border_w/2} Z" '
            f'fill="{banner}"/>'
        )
    # corner flourish (top-right) hints at state
    body += f'<path d="M150 22 q18 0 20 20" fill="none" stroke="{corner}" stroke-width="4" stroke-linecap="round"/>'
    return svg(TILE_W, TILE_H, body)


TILES = {
    "tiles/tile_base.png": tile_frame(INK_SOFT, 3, None, False, PARCHMENT_DARK),
    "tiles/tile_upgraded.png": tile_frame(UPGRADE, 6, UPGRADE_BG, False, UPGRADE),
    "tiles/tile_inked.png": tile_frame(INKED, 6, INKED_BG, False, INKED),
    "tiles/tile_cursed.png": tile_frame(CURSE, 6, CURSE_BG, True, CURSE),
    "tiles/tile_back.png": svg(TILE_W, TILE_H,
        f'<rect x="3" y="3" width="{TILE_W-6}" height="{TILE_H-6}" rx="18" fill="{INK}" stroke="{INK_SOFT}" stroke-width="4"/>'
        f'<rect x="18" y="18" width="{TILE_W-36}" height="{TILE_H-36}" rx="10" fill="none" stroke="{INKED}" stroke-width="2"/>'
        f'<circle cx="96" cy="128" r="34" fill="none" stroke="{INKED}" stroke-width="3"/>'
        f'<path d="M96 100 L104 124 L128 128 L104 132 L96 156 L88 132 L64 128 L88 124 Z" fill="{INKED}"/>'),
    "tiles/tile_highlight.png": svg(TILE_W, TILE_H,
        f'<rect x="4" y="4" width="{TILE_W-8}" height="{TILE_H-8}" rx="18" fill="none" stroke="#FFFFFF" stroke-width="8" opacity="0.85"/>'),
}

# ---------- icons (64x64) ----------
ICONS = {
    "icons/icon_upgrade.png": svg(64, 64,
        f'<path d="M14 38 L32 20 L50 38" fill="none" stroke="{UPGRADE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M14 52 L32 34 L50 52" fill="none" stroke="{UPGRADE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'),
    "icons/icon_ink.png": svg(64, 64,
        f'<path d="M32 6 C32 6 12 32 12 42 a20 20 0 0 0 40 0 C52 32 32 6 32 6 Z" fill="{INKED}"/>'
        f'<circle cx="25" cy="42" r="5" fill="{INKED_BG}"/>'),
    "icons/icon_curse.png": svg(64, 64,
        f'<circle cx="32" cy="28" r="20" fill="{CURSE}"/>'
        f'<rect x="20" y="40" width="24" height="16" rx="4" fill="{CURSE}"/>'
        f'<circle cx="24" cy="28" r="6" fill="{CURSE_BG}"/><circle cx="40" cy="28" r="6" fill="{CURSE_BG}"/>'
        f'<rect x="27" y="46" width="3" height="10" fill="{CURSE_BG}"/><rect x="34" y="46" width="3" height="10" fill="{CURSE_BG}"/>'),
    "icons/icon_intent.png": svg(64, 64,
        f'<path d="M4 32 Q32 6 60 32 Q32 58 4 32 Z" fill="none" stroke="{INK}" stroke-width="5"/>'
        f'<circle cx="32" cy="32" r="10" fill="{SEAL}"/>'),
    "icons/icon_turns.png": svg(64, 64,
        f'<path d="M16 6 H48 M16 58 H48" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M20 8 Q20 26 32 32 Q20 38 20 56 H44 Q44 38 32 32 Q44 26 44 8 Z" fill="none" stroke="{INK}" stroke-width="4"/>'
        f'<path d="M24 50 Q32 40 40 50 Z" fill="{INKED}"/>'),
    "icons/icon_seal.png": svg(64, 64,
        f'<circle cx="32" cy="32" r="24" fill="{SEAL}"/>'
        f'<circle cx="32" cy="32" r="16" fill="none" stroke="#E6DDF7" stroke-width="3"/>'
        f'<path d="M32 22 L35 30 L43 32 L35 34 L32 42 L29 34 L21 32 L29 30 Z" fill="#E6DDF7"/>'),
}

# ---------- monsters (512x512, transparent, creature centred, feet at y~470) ----------

def eyes(cx, cy, gap, r, color="#F5EFE0"):
    return (f'<circle cx="{cx-gap}" cy="{cy}" r="{r}" fill="{color}"/><circle cx="{cx+gap}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<circle cx="{cx-gap}" cy="{cy}" r="{r*0.45}" fill="{INK}"/><circle cx="{cx+gap}" cy="{cy}" r="{r*0.45}" fill="{INK}"/>')


MONSTERS = {
    # A book whose pages are teeth.
    "monsters/page_eater.png": svg(512, 512,
        f'<ellipse cx="256" cy="478" rx="150" ry="16" fill="#000" opacity="0.25"/>'
        f'<path d="M86 150 L256 120 L426 150 L426 440 L256 410 L86 440 Z" fill="#6B3E2E" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        f'<path d="M110 250 L256 228 L402 250 L402 330 L256 352 L110 330 Z" fill="#1A0F0B"/>'
        + "".join(f'<path d="M{110+i*29} 250 l14 34 l15 -34 Z" fill="{PARCHMENT}"/>' for i in range(10))
        + "".join(f'<path d="M{110+i*29} 330 l14 -30 l15 30 Z" fill="{PARCHMENT}"/>' for i in range(10))
        + eyes(256, 185, 60, 22)
        + f'<path d="M256 120 L256 410" stroke="{INK}" stroke-width="6"/>'),
    # A dripping ink ghost.
    "monsters/ink_wraith.png": svg(512, 512,
        f'<ellipse cx="256" cy="478" rx="120" ry="14" fill="#000" opacity="0.25"/>'
        f'<path d="M136 440 L136 230 a120 120 0 0 1 240 0 L376 440 q-20 -30 -40 0 q-20 30 -40 0 q-20 -30 -40 0 q-20 30 -40 0 q-20 -30 -40 0 q-20 30 -40 0 Z" fill="#1F2140" stroke="{INK}" stroke-width="6"/>'
        f'<path d="M180 470 q6 -30 0 -40 M330 476 q6 -30 0 -36" stroke="#1F2140" stroke-width="10" stroke-linecap="round"/>'
        + eyes(256, 220, 44, 24, "#C9D4FF")
        + f'<path d="M216 310 q40 -26 80 0" fill="none" stroke="#C9D4FF" stroke-width="8" stroke-linecap="round"/>'),
    # A spider with quill legs.
    "monsters/quill_spider.png": svg(512, 512,
        f'<ellipse cx="256" cy="478" rx="170" ry="14" fill="#000" opacity="0.25"/>'
        + "".join(
            f'<path d="M256 300 L{256+s*dx} {y1} L{256+s*(dx+50)} 470" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
            for s in (-1, 1) for dx, y1 in ((70, 220), (110, 250), (150, 290), (180, 330)))
        + f'<ellipse cx="256" cy="300" rx="90" ry="70" fill="#3B2F4A" stroke="{INK}" stroke-width="6"/>'
        + f'<circle cx="256" cy="220" r="50" fill="#3B2F4A" stroke="{INK}" stroke-width="6"/>'
        + eyes(256, 212, 20, 10, "#F2B84B") + eyes(256, 238, 34, 7, "#F2B84B")),
    # Boss: an open tome with one great eye.
    "monsters/boss_unwritten.png": svg(512, 512,
        f'<ellipse cx="256" cy="482" rx="200" ry="16" fill="#000" opacity="0.3"/>'
        f'<path d="M40 180 Q150 140 256 190 Q362 140 472 180 L472 450 Q362 410 256 460 Q150 410 40 450 Z" fill="{PARCHMENT}" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
        f'<path d="M256 190 L256 460" stroke="{INK}" stroke-width="8"/>'
        + "".join(f'<path d="M{70+ (0 if i<5 else 250)} {230+(i%5)*40} h{120-(i%2)*30}" stroke="{INK_SOFT}" stroke-width="6" stroke-linecap="round" opacity="0.5"/>' for i in range(10))
        + f'<ellipse cx="256" cy="110" rx="120" ry="70" fill="#F5EFE0" stroke="{INK}" stroke-width="10"/>'
        f'<circle cx="256" cy="110" r="46" fill="{SEAL}"/><circle cx="256" cy="110" r="20" fill="{INK}"/>'
        f'<circle cx="272" cy="96" r="8" fill="#F5EFE0"/>'),
}

# ---------- backgrounds ----------
BACKGROUNDS = {
    "backgrounds/bg_desk.png": svg(1920, 1080,
        f'<rect width="1920" height="1080" fill="{DESK}"/>'
        + "".join(f'<rect y="{i*135}" width="1920" height="2" fill="{DESK_LIGHT}"/>' for i in range(1, 8))
        + f'<rect x="260" y="70" width="1400" height="940" rx="24" fill="{PARCHMENT_DARK}" opacity="0.10"/>'),
}

LETTERS = [f"letters/{c}.png" for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

PLACEHOLDER_FILES = set(TILES) | set(ICONS) | set(MONSTERS) | set(BACKGROUNDS) | set(LETTERS)


def letters() -> None:
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    font = ImageFont.truetype(font_path, 104)
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        out = ART / "letters" / f"{c}.png"
        if not should_write(out):
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((64, 66), c, font=font, fill=INK, anchor="mm")
        img.save(out)
        print("wrote", out.relative_to(ROOT))


def main() -> int:
    for group, (w, h) in ((TILES, (TILE_W, TILE_H)), (ICONS, (64, 64)), (MONSTERS, (512, 512)), (BACKGROUNDS, (1920, 1080))):
        for rel, s in group.items():
            render(s, ART / rel, w, h)
    letters()
    return 0


if __name__ == "__main__":
    sys.exit(main())
