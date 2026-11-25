#!/usr/bin/env python3
"""Draw "The World in One Day — 24 November 2026": a newspaper front page
summing up thirty verified news stories from Tuesday 24 November 2026.

Deterministic and offline: same input, same bytes, every run. Writes one
1024x1024 PNG to the path given as argv[1] (default: entry.png next to this
file). Uses only Pillow and the DejaVu fonts shipped with the system.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (251, 247, 236)
INK = (20, 24, 34)
NAVY = (18, 33, 61)
NAVY_DOT = (51, 80, 122)
GOLD = (197, 160, 72)
RULE = (180, 172, 150)
SOFT = (237, 241, 245)
GRID_LINE = (205, 198, 182)
MUTED = (96, 100, 112)
WHITE = (255, 255, 255)
RED = (178, 34, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)

# (number, headline, deck, category) — all thirty stories, each verified as
# having happened or first been reported on 24 November 2026.
STORIES = [
    (1, "Chess title match opens in a draw", "Sindarov\u2013Gukesh draw, Game 1", "sport"),
    (2, "Sanofi buys Insmed for $41bn", "Biggest biotech deal in years", "markets"),
    (3, "US measles-free status ends", "First loss in over 25 years", "health"),
    (4, "FDA clears first limb-girdle drug", "A first for the muscle disease", "health"),
    (5, "Most distant quasar ever found", "630m years after the Big Bang", "science"),
    (6, "5.6 quake shakes Nepal\u2019s Koshi", "Tremor near the China border", "disaster"),
    (7, "Tiangong opens to foreign astronaut", "Pakistan\u2019s Zeeshan Ali aboard", "science"),
    (8, "Candy-factory fire kills 3", "34\u201337 missing in Indonesia", "disaster"),
    (9, "Malaysia to repatriate 6,803", "Myanmar nationals, next month", "politics"),
    (10, "Hasina plans return from exile", "Ousted leader eyes Dec 16", "politics"),
    (11, "Pentagon rebukes Canada", "Defence spending, F-35 review", "politics"),
    (12, "China sentences spy to death", "Official leaked state secrets", "politics"),
    (13, "US drone aided Mexico drug bust", "Sinaloa lord caught with help", "politics"),
    (14, "3 Salvadoran soldiers die in Haiti", "Died fighting gangs in Haiti", "politics"),
    (15, "WHO chief visits ailing Cuba", "Health system breaking down", "health"),
    (16, "Pope\u2019s diary reveals dark crisis", "Writings tell of the devil", "culture"),
    (17, "N. Korea reviews Swiss ties", "Sanctions over youth camp", "politics"),
    (18, "Solomons to end China pact", "Australia treaty comes next", "politics"),
    (19, "Seoul +6%, Nikkei +3.9% Tuesday", "Chip rally after Huang return", "markets"),
    (20, "Car bomb rocks Villavicencio", "Blast wrecks buildings", "disaster"),
    (21, "11 die in UAE coach crash", "Coach\u2013truck crash, RAK", "disaster"),
    (22, "Supermoon lights the night sky", "November\u2019s closest full moon", "science"),
    (23, "Commanders stun Bengals 22\u201320", "Walk-off field goal wins it", "sport"),
    (24, "Dow tops 50,000 for first time", "Up 0.85% as S&P, Nasdaq fall", "markets"),
    (25, "Hamas security chief killed", "Naeem Abu Nahel among 7 dead", "politics"),
    (26, "2 killed in Zaporizhzhia strike", "40 wounded as flats are hit", "politics"),
    (27, "Houthi strike hits Riyadh tower", "PIF Tower hit again, 11 hurt", "politics"),
    (28, "Senegal reinstated as AFCON champs", "CAS overturns the forfeit", "sport"),
    (29, "Germany first into Delta system", "Ukraine battlefield software", "politics"),
    (30, "Iraq takes over Kurdish oilfields", "PM acts after smuggling probe", "politics"),
]

CAT_COLORS = {
    "politics": (27, 58, 107),
    "markets": (30, 122, 52),
    "sport": (194, 65, 12),
    "science": (14, 116, 144),
    "disaster": (185, 28, 28),
    "health": (109, 40, 217),
    "culture": (157, 23, 77),
}


def wrap(draw, text, fnt, width, max_lines):
    """Split text into at most max_lines lines fitting width.

    Words fill each line before moving on; if words are left over once the
    last line is full, the last line ends with an ellipsis.
    """
    words = text.split()
    lines, cur = [], ""
    truncated = False
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        elif len(lines) < max_lines - 1:
            lines.append(cur)
            cur = word
        else:
            truncated = True
            break
    if cur:
        lines.append(cur)
    if truncated and lines:
        last = lines[-1]
        while last and draw.textlength(last + "\u2026", font=fnt) > width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last + "\u2026"
    return lines[:max_lines]


# Stylised continent outlines in (longitude, latitude). Coarse but recognisable:
# the map is drawn as dots, so small wobbles vanish into the stipple.
CONTINENTS = [
    # North America, from Alaska around to Central America.
    [(-168, 66), (-162, 60), (-155, 58), (-145, 60), (-135, 58), (-130, 54),
     (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-108, 24), (-105, 20),
     (-97, 19), (-92, 15), (-86, 13), (-83, 9), (-79, 9), (-81, 13), (-86, 16),
     (-90, 21), (-91, 19), (-97, 22), (-97, 26), (-93, 30), (-89, 30), (-84, 30),
     (-81, 26), (-80, 32), (-76, 35), (-74, 39), (-70, 42), (-68, 44), (-65, 44),
     (-60, 46), (-55, 52), (-60, 55), (-65, 58), (-68, 58), (-72, 62), (-78, 62),
     (-85, 66), (-92, 66), (-95, 69), (-105, 68), (-115, 69), (-125, 70),
     (-135, 68), (-145, 70), (-155, 71), (-162, 70), (-168, 66)],
    # Greenland.
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70), (-20, 74),
     (-25, 76), (-32, 80), (-45, 80), (-58, 76), (-60, 70), (-58, 64)],
    # South America.
    [(-77, 7), (-72, 11), (-64, 10), (-58, 6), (-52, 4), (-50, 0), (-44, -3),
     (-38, -5), (-35, -8), (-38, -15), (-40, -22), (-48, -27), (-52, -33),
     (-57, -38), (-65, -41), (-68, -47), (-70, -52), (-73, -54), (-70, -50),
     (-70, -40), (-72, -30), (-70, -20), (-75, -15), (-80, -10), (-81, -5),
     (-80, 0), (-77, 7)],
    # Europe, with the British Isles as a separate blob.
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (-1, 51), (2, 51), (5, 53),
     (8, 55), (10, 58), (12, 56), (18, 56), (21, 55), (24, 58), (28, 59),
     (30, 60), (25, 62), (20, 65), (18, 69), (25, 71), (30, 70), (35, 68),
     (40, 66), (40, 60), (32, 58), (28, 55), (24, 52), (22, 48), (20, 45),
     (18, 42), (15, 40), (12, 44), (8, 44), (3, 43), (0, 39), (-2, 37),
     (-6, 36), (-10, 36)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51)],
    # Africa.
    [(-17, 15), (-10, 30), (-5, 35), (0, 36), (10, 37), (20, 32), (30, 31),
     (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10),
     (44, 5), (41, 0), (40, -5), (38, -12), (35, -18), (32, -25), (28, -32),
     (20, -35), (17, -32), (15, -27), (12, -18), (12, -10), (9, -1), (9, 4),
     (4, 6), (-8, 5), (-13, 8), (-17, 15)],
    # Eurasia, one big outline from Iberia to the Pacific.
    [(40, 68), (50, 70), (60, 72), (70, 73), (80, 73), (90, 75), (100, 76),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (155, 48),
     (150, 45), (142, 45), (140, 40), (135, 38), (130, 35), (127, 33),
     (122, 32), (120, 28), (115, 23), (110, 20), (108, 15), (105, 10),
     (103, 7), (100, 8), (98, 12), (95, 16), (92, 20), (89, 22), (86, 20),
     (82, 17), (80, 13), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25),
     (62, 25), (58, 26), (54, 26), (50, 29), (48, 30), (44, 29), (40, 28),
     (38, 22), (36, 18), (35, 15), (39, 12), (43, 12), (48, 14), (52, 15),
     (56, 17), (58, 22), (56, 26), (52, 28), (48, 30), (44, 32), (40, 36),
     (38, 40), (36, 42), (32, 45), (30, 48), (28, 52), (26, 56), (24, 60),
     (22, 64), (25, 68), (30, 70), (35, 68), (40, 68)],
    # Japan.
    [(130, 31), (132, 33), (135, 34), (137, 36), (139, 38), (141, 40),
     (142, 42), (143, 44), (141, 45), (140, 42), (138, 39), (136, 36),
     (133, 34), (130, 31)],
    # South-East Asia islands, drawn as one thin chain.
    [(95, 16), (98, 12), (100, 8), (103, 5), (105, 2), (108, -2), (110, -5),
     (113, -8), (118, -9), (122, -8), (125, -6), (128, -4), (130, -2),
     (132, 0), (135, -2), (138, -4), (140, -6), (141, -8), (138, -9),
     (132, -6), (126, -4), (120, -2), (114, 0), (108, 2), (104, 5), (100, 8),
     (97, 12), (95, 16)],
    # New Guinea.
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9),
     (142, -8), (137, -6), (132, -4), (131, -1)],
    # Australia.
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (113, -22)],
    # New Zealand.
    [(167, -35), (170, -38), (172, -41), (174, -41), (176, -38), (174, -36),
     (170, -35), (167, -35)],
    [(167, -42), (169, -44), (171, -46), (168, -46), (166, -44)],
]

# Story number -> (longitude, latitude) of the hotspot dot on the map.
MARKERS = {
    1: (6.1, 46.2),    # Geneva — chess
    6: (85.3, 27.7),   # Kathmandu — Nepal quake
    8: (106.8, -6.2),  # Jakarta — factory fire
    23: (-84.0, 35.0), # Washington — MNF (nudged so it clears New York)
    24: (-70.0, 43.0), # New York — Dow (nudged so it clears Washington)
    25: (34.5, 31.5),  # Gaza
    27: (46.7, 24.7),  # Riyadh — PIF Tower
    28: (-17.4, 14.7), # Dakar — Senegal
}


def lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (82.0 - lat) / 140.0 * (y1 - y0)
    return x, y


def draw_map(img, box):
    """Dotted world map with red numbered hotspots for eight of the stories."""
    x0, y0, x1, y1 = box
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, fill=SOFT)
    # faint graticule every 30 degrees
    for lon in range(-180, 181, 30):
        x, _ = lonlat_to_xy(lon, 0, box)
        draw.line([(x, y0), (x, y1)], fill=(214, 220, 228), width=1)
    for lat in range(-60, 83, 30):
        _, y = lonlat_to_xy(0, lat, box)
        draw.line([(x0, y), (x1, y)], fill=(214, 220, 228), width=1)
    # land mask from the continent polygons
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    mdraw = ImageDraw.Draw(mask)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, (0, 0, x1 - x0, y1 - y0)) for lon, lat in poly]
        mdraw.polygon(pts, fill=255)
    step = 8
    r = 2.1
    for gy in range(y0 + 4, y1 - 2, step):
        for gx in range(x0 + 4, x1 - 2, step):
            if mask.getpixel((gx - x0, gy - y0)):
                draw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=NAVY_DOT)
    # hotspot markers
    fnt = SANS_BOLD(12)
    for num, (lon, lat) in sorted(MARKERS.items()):
        x, y = lonlat_to_xy(lon, lat, box)
        draw.ellipse([x - 10, y - 10, x + 10, y + 10], fill=RED,
                     outline=WHITE, width=2)
        tw = draw.textlength(str(num), font=fnt)
        draw.text((x - tw / 2, y - 8), str(num), font=fnt, fill=WHITE)
    draw.rectangle(box, outline=GRID_LINE, width=1)


def draw_masthead(img, draw):
    draw.rectangle([24, 20, 1000, 138], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_BOLD(58)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 34), title, font=tf, fill=WHITE)
    draw.line([(120, 112), (904, 112)], fill=GOLD, width=2)
    sub = "TUESDAY, 24 NOVEMBER 2026   \u00b7   30 STORIES FROM EVERY TIME ZONE"
    sf = SANS_BOLD(17)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 118), sub, font=sf, fill=(232, 205, 130))


def draw_chessboard(draw, x, y, size):
    """A tiny 8x8 board, Game 1's Berlin Defence after 38 moves: drawn pieces
    are schematic — white king e1, black king g8, the rest as dots."""
    sq = size / 8.0
    for r in range(8):
        for c in range(8):
            light = (r + c) % 2 == 0
            col = (240, 230, 205) if light else (120, 110, 90)
            draw.rectangle([x + c * sq, y + r * sq,
                            x + (c + 1) * sq, y + (r + 1) * sq], fill=col)
    draw.rectangle([x, y, x + size, y + size], outline=INK, width=2)
    # a few pieces as simple discs: white king e1, black king g8, rooks a1/h1
    def piece(col, row, color):
        cx = x + (col + 0.5) * sq
        cy = y + (row + 0.5) * sq
        draw.ellipse([cx - sq * 0.32, cy - sq * 0.32,
                      cx + sq * 0.32, cy + sq * 0.32], fill=color,
                     outline=INK, width=1)
    piece(4, 7, WHITE)   # white king, e1
    piece(6, 0, INK)     # black king, g8
    piece(0, 7, WHITE)   # white rook, a1
    piece(7, 7, WHITE)   # white rook, h1
    piece(0, 0, INK)     # black rook, a8
    piece(7, 0, INK)     # black rook, h8


def draw_lead(img, draw):
    y0, y1 = 150, 252
    draw.rectangle([24, y0, 1000, y1], fill=(255, 255, 255),
                   outline=GRID_LINE, width=1)
    draw.rectangle([24, y0, 1000, y0 + 3], fill=RED)
    tag = "LEAD STORY  \u00b7  CHESS"
    tf = SANS_BOLD(13)
    draw.text((40, y0 + 12), tag, font=tf, fill=RED)
    head = "World chess title match opens with a draw"
    hf = SANS_BOLD(27)
    draw.text((40, y0 + 34), head, font=hf, fill=INK)
    deck = ("Sindarov and Gukesh split Game 1 in 38 moves \u2014 the youngest "
            "title match in history.")
    df = SANS(16)
    draw.text((40, y0 + 70), deck, font=df, fill=MUTED)
    draw_chessboard(draw, 888, y0 + 10, 84)


def draw_grid(img, draw):
    x0, y0 = 24, 536
    cw, ch, gap = 188, 66, 8
    hf = SANS_BOLD(14)
    df = SANS(11)
    cf = SANS_BOLD(13)
    nf = SANS_BOLD(12)
    for idx, (num, head, deck, cat) in enumerate(STORIES):
        col, row = idx % 5, idx // 5
        x = x0 + col * (cw + gap)
        y = y0 + row * (ch + 6)
        color = CAT_COLORS[cat]
        # number disc
        draw.ellipse([x, y + 3, x + 24, y + 27], fill=color)
        label = str(num)
        tw = draw.textlength(label, font=nf)
        draw.text((x + 12 - tw / 2, y + 7), label, font=nf, fill=WHITE)
        tx = x + 32
        twidth = cw - 32
        lines = wrap(draw, head, hf, twidth, 2)
        for i, line in enumerate(lines):
            draw.text((tx, y + 2 + i * 17), line, font=hf, fill=INK)
        dy = y + 2 + len(lines) * 17 + 3
        draw.text((tx, dy), deck, font=df, fill=MUTED)
        # hairline under each card except the last row
        if row < 5:
            draw.line([(x, y + ch + 2), (x + cw, y + ch + 2)],
                      fill=GRID_LINE, width=1)


def draw_footer(img, draw):
    ff = SANS(13)
    line = ("THE WORLD IN ONE DAY \u2014 24 NOVEMBER 2026  \u00b7  Every event above "
            "happened, or was first reported, on 24 November 2026")
    tw = draw.textlength(line, font=ff)
    draw.text(((W - tw) / 2, 972), line, font=ff, fill=MUTED)
    draw.line([(24, 966), (1000, 966)], fill=RULE, width=1)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(img, draw)
    draw_lead(img, draw)
    draw_map(img, (24, 264, 1000, 500))
    cap = "THE DAY ON THE MAP \u2014 GENEVA TO RIYADH, WASHINGTON TO JAKARTA"
    cf = SANS_BOLD(13)
    cw = draw.textlength(cap, font=cf)
    draw.text(((W - cw) / 2, 508), cap, font=cf, fill=MUTED)
    draw_grid(img, draw)
    draw_footer(img, draw)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
