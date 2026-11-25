# Art

Every file here has a **fixed path, size, and role**. To replace a placeholder,
draw it at the size below, export as PNG with transparency, and save it over
the old file under the same name. No code changes needed.

Then remove that path from `PLACEHOLDER_FILES` in
`scripts/gen_placeholder_art.py` so re-running the generator never overwrites
your drawing, and flip its status below to `final`.

Drawing at 2x the listed size is fine; set the texture's import scale or the
node's scale in Godot accordingly. Keep the aspect ratio.

## Tiles — 192 × 256

The game composes a tile from three layers: **frame** (state) → **letter glyph**
(centred) → **point value** (text, top-left). So frames must leave room:

| Region | Box (x, y, w, h) | Keep clear? |
|---|---|---|
| Point value | 16, 14, 44, 36 | yes, game draws text here |
| Letter glyph | 32, 56, 128, 128 | yes, game draws `letters/X.png` here |
| Status icon | 136, 14, 40, 40 | decorate freely, or leave for an icon |
| Banner | 0, 206, 192, 50 | modifier text is drawn on top, keep it calm |

| File | Role | Status |
|---|---|---|
| `tiles/tile_base.png` | plain tile | placeholder |
| `tiles/tile_upgraded.png` | upgraded tile | placeholder |
| `tiles/tile_inked.png` | tile with a modifier ("ink") | placeholder |
| `tiles/tile_cursed.png` | curse tile added by enemies | placeholder |
| `tiles/tile_back.png` | face-down tile (bag/draw pile) | placeholder |
| `tiles/tile_highlight.png` | selection overlay, drawn on top | placeholder |

## Letters — 128 × 128

`letters/A.png` … `letters/Z.png`. One glyph each, centred, transparent
background, ink colour. Hand-lettered glyphs here are the cheapest way to make
the whole game look like yours.

All 26: placeholder.

## Icons — 64 × 64

| File | Role | Status |
|---|---|---|
| `icons/icon_upgrade.png` | upgraded marker | placeholder |
| `icons/icon_ink.png` | modifier marker | placeholder |
| `icons/icon_curse.png` | curse marker | placeholder |
| `icons/icon_intent.png` | enemy's next twist | placeholder |
| `icons/icon_turns.png` | turns remaining | placeholder |
| `icons/icon_seal.png` | seal / target score | placeholder |

## Monsters — 512 × 512

Transparent background, creature centred, feet/base around y = 470 so they all
stand on the same line. One still image each; the game handles hit flashes and
shakes.

| File | Role | Status |
|---|---|---|
| `monsters/page_eater.png` | act 1 enemy | placeholder |
| `monsters/ink_wraith.png` | act 1 enemy | placeholder |
| `monsters/quill_spider.png` | act 1 elite | placeholder |
| `monsters/boss_unwritten.png` | act 1 boss | placeholder |

New monster: add `monsters/<snake_name>.png` at the same size and reference it
from the encounter's data.

## Backgrounds — 1920 × 1080

| File | Role | Status |
|---|---|---|
| `backgrounds/bg_desk.png` | main play screen | placeholder |

## Before release

Every placeholder here was made by Claude (programmatic vector shapes and a
system font, not an image model). If any of them ship, Steam's AI content
disclosure applies. Check that nothing in this file still says `placeholder`
before you build a release.
