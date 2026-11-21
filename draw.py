#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261121.

Draws 'THE WORLD IN ONE DAY - Saturday 21 November 2026' with PIL only.
Build-time script: deterministic, stdlib + Pillow. Run twice -> same bytes.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SEED = 20261121
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

PAPER = (247, 241, 227)
PAPER_DK = (238, 229, 208)
INK = (26, 26, 26)
MUTED = (107, 98, 87)
RED = (176, 30, 30)
RED_DK = (140, 22, 22)
TEAL = (20, 86, 79)
TEAL_LT = (64, 128, 118)
GOLD = (201, 151, 28)
NAVY = (16, 28, 52)
CREAM = (250, 246, 236)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(text, fnt, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=None, spacing=0):
    lh = leading or int(fnt.size * 1.22)
    yy = y
    for ln in wrap(text, fnt, max_w, draw):
        draw.text((x, yy), ln, font=fnt, fill=fill)
        yy += lh + spacing
    return yy


def vgrad(img, box, c_top, c_bot):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    d = ImageDraw.Draw(img)
    for i in range(h):
        t = i / h
        c = tuple(int(c_top[k] + (c_bot[k] - c_top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def hgrad(img, box, c_l, c_r):
    x0, y0, x1, y1 = box
    w = max(1, x1 - x0)
    d = ImageDraw.Draw(img)
    for i in range(w):
        t = i / w
        c = tuple(int(c_l[k] + (c_r[k] - c_l[k]) * t) for k in range(3))
        d.line([(x0 + i, y0), (x0 + i, y1)], fill=c)


def soft_shadow(d, box, r=6):
    x0, y0, x1, y1 = box
    for i in range(3, 0, -1):
        d.rounded_rectangle([x0 + i, y0 + i, x1 + i, y1 + i], radius=r,
                            fill=(0, 0, 0, 26))


def paper_texture(img, rng):
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(95000):
        x = rng.randrange(W)
        y = rng.randrange(H)
        a = rng.randrange(5, 19)
        c = (120, 100, 60, a) if rng.random() < 0.5 else (255, 255, 255, a)
        d.point((x, y), fill=c)
    for yy in range(0, H, 5):
        d.line([(0, yy), (W, yy + 2)], fill=(150, 130, 90, 4))
    for _ in range(26):
        x = rng.randrange(W)
        y = rng.randrange(H)
        r = rng.randrange(18, 60)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(150, 130, 90, 10))


def vignette(img):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(4):
        a = 7 + i * 5
        d.rectangle([i * 7, i * 7, W - 1 - i * 7, H - 1 - i * 7],
                    outline=(60, 40, 10, a), width=7)
    img.alpha_composite(ov)


# ---------------------------------------------------------------- data
LEADS = [
    dict(pin=1, kick="CLIMATE  ·  ANTALYA, TURKIYE", scene="cop",
         head="COP31 spills into overtime",
         body=("Talks pass the Friday deadline into Saturday as nearly 200 nations "
               "deadlock over fossil fuels. The draft drops every mention of them "
               "- and the $120bn finance goal."),
         src="AP  ·  Reuters  ·  Guardian, 21 Nov"),
    dict(pin=2, kick="CONFLICT  ·  RIYADH", scene="riyadh",
         head="Missiles downed over Riyadh",
         body=("Saudi defences intercept three Houthi ballistic missiles in the "
               "early hours of Saturday - the third straight night of alerts "
               "over the capital."),
         src="Reuters  ·  AFP, 21 Nov"),
    dict(pin=3, kick="CRICKET  ·  WELLINGTON", scene="cricket",
         head="Rahul's ton puts India on top",
         body=("KL Rahul reaches 117* and Padikkal makes 80 on Day 3 as India "
               "reach 309/2, trailing New Zealand by 59 after lunch at 239/1."),
         src="Reuters  ·  Cricbuzz, 21 Nov"),
]

CARDS = [
    dict(pin=4, scene="cyclone", title="AKVAN AFTERMATH",
         body=("Heavy rain runs into Saturday; 372,000 evacuated, no deaths "
               "reported, 423 rescue teams out."),
         src="Sambad  ·  DotTimes"),
    dict(pin=5, scene="kyiv", title="KYIV COUNTS THE COST",
         body=("Overnight barrage toll: 9 killed, 28+ hurt; 110+ missiles, "
               "400+ drones; 3 Dnipro bridges shut."),
         src="CNN  ·  Kyiv Independent"),
    dict(pin=6, scene="poland", title="MISSILES LAND IN POLAND",
         body=("Two Russian missiles and a drone crash in the south-east; "
               "no one hurt. NATO: 'grave violation'."),
         src="AP"),
    dict(pin=7, scene="denmark", title="DENMARK EXPELS ATTACHE",
         body=("Russian defence attache ordered out over an alleged plot to "
               "kill rapper Kyivstoner in September."),
         src="Al Jazeera  ·  Reuters"),
    dict(pin=8, scene="trophy", title="ICC MAP TO 2035",
         body=("India to host the 2029 Champions Trophy and co-host the "
               "2031 ODI World Cup with Bangladesh."),
         src="Cricbuzz, 21 Nov"),
    dict(pin=9, scene="school", title="$52M FOR SCHOOLING",
         body=("UN fund backs 300,000 children in Lebanon, Myanmar and "
               "South Sudan on World Children's Day."),
         src="Education Cannot Wait"),
    dict(pin=10, scene="sco", title="SCO FORUM: DAY TWO",
         body=("Thematic sessions open in Delhi; Pakistan's minister speaks "
               "- first visit by a Pak minister in 3 years."),
         src="ANI  ·  IANS"),
    dict(pin=11, scene="whitehouse", title="TRUMP: PUTIN 'TIRED'",
         body=("Trump says Putin is 'ready for a deal'; no rush on Iran - "
               "a decision may wait until 2027."),
         src="Korea Times  ·  News89"),
    dict(pin=12, scene="court", title="PALISADES FIRE: GUILTY",
         body=("LA jury convicts Rinderknecht, 30, of arson in the 2025 fire "
               "that killed 12 and razed 6,845 structures."),
         src="Reuters  ·  AP"),
    dict(pin=13, scene="quake", title="PERU SHAKEN: M6.7",
         body=("Strong quake hits the central Andes at 00:09 UTC; felt in "
               "Lima. No damage or casualties reported."),
         src="USGS  ·  Reuters"),
]

BRIEFS = [
    (14, "COP31: 123 firms urge bold power deal", "Reuters"),
    (15, "COP31 draft first to admit 1.5C overshoot", "Reuters"),
    (16, "Next climate summit: Addis Ababa, Nov 2027", "AP"),
    (17, "Houthis threaten Jeddah, Shuqaiq, finance dist.", "AFP"),
    (18, "Denmark weighs curbs on Russian Schengen visas", "AJ"),
    (19, "Melania: Christmas wish is another ceasefire", "Daily Mail"),
    (20, "Trump defends calling Putin a 'friend'", "TOI"),
    (21, "Iran war nears its ninth month", "One Turn"),
    (22, "Hurricanes beat Thunder by 8 wickets", "CricTracker"),
    (23, "India 'takes note' of ICJ Rohingya ruling", "Logichub"),
    (24, "UK-EU sign food, carbon, youth deals", "One Turn"),
    (25, "Premier League MD11 kicks off: City v Fulham", "EPL"),
    (26, "Rahul 93*, Padikkal 53* at lunch, Day 3", "Reuters"),
    (27, "Padikkal: 4th fifty in five Tests", "Reuters"),
    (28, "Poland seeks more Eastern Sentry forces", "SOFX"),
    (29, "11-nation Koalicja drill runs in SE Poland", "Nexus"),
    (30, "Hosts blasted: 'worst COP ever'", "Guardian"),
    (31, "SpaceX launches classified USSF-317", "Space Launch Live"),
    (32, "Loss-and-damage fund to triple, sum blank", "AP"),
    (33, "ECW holds 10% of $52m for future shocks", "ECW"),
    (34, "SCO Delhi: 10 states, observers, partners", "ANI"),
    (35, "Korea dangers 'discussed' at 3-way summit", "Korea Times"),
    (36, "Zelensky: double-tap strikes are rising", "Kyiv Ind."),
]

PINS = [
    (1, 30.7, 36.9), (2, 46.7, 24.7), (3, 174.8, -41.3), (4, 85.0, 19.3),
    (5, 30.5, 50.5), (6, 22.0, 50.0), (7, 12.6, 55.7), (8, 72.9, 19.1),
    (9, 6.1, 46.2), (10, 77.2, 28.6), (11, -77.0, 38.9), (12, -118.2, 34.1),
    (13, -76.0, -10.9),
]


# ---------------------------------------------------------------- scenes
def scene_cop(d, x, y, w, h):
    vgrad_box = (x, y, x + w, y + h)
    img = d._image
    vgrad(img, vgrad_box, (178, 222, 208), (247, 241, 227))
    d.ellipse([x + w - 66, y + 10, x + w - 22, y + 54], fill=(240, 190, 60))
    d.ellipse([x + w - 60, y + 16, x + w - 28, y + 48], fill=(248, 210, 110))
    for i, mx in enumerate(range(x + 6, x + w - 6, 34)):
        d.polygon([(mx, y + h - 46), (mx + 17, y + h - 78 - (i % 3) * 8),
                   (mx + 34, y + h - 46)], fill=(96, 140, 110) if i % 2 else (74, 118, 92))
    d.rectangle([x + 14, y + h - 46, x + w - 14, y + h - 8], fill=(232, 222, 196))
    d.polygon([(x + 8, y + h - 46), (x + w // 2, y + h - 78),
               (x + w - 8, y + h - 46)], fill=(20, 86, 79))
    d.rectangle([x + w // 2 - 34, y + h - 34, x + w // 2 + 34, y + h - 8],
                fill=(247, 241, 227))
    for i, c in enumerate([(176, 30, 30), (20, 86, 79), (201, 151, 28),
                           (40, 90, 160), (120, 60, 140), (200, 120, 40)]):
        fx = x + 26 + i * 46
        d.line([(fx, y + h - 78), (fx, y + h - 52)], fill=(60, 60, 60), width=2)
        d.rectangle([fx, y + h - 78, fx + 26, y + h - 64], fill=c)
    for i in range(9):
        cx = x + 22 + i * 32
        d.ellipse([cx, y + h - 6, cx + 5, y + h - 1], fill=(90, 70, 50))


def scene_riyadh(d, x, y, w, h, rng):
    img = d._image
    vgrad(img, (x, y, x + w, y + h), (10, 16, 42), (52, 68, 110))
    for _ in range(26):
        sx, sy = x + rng.randrange(w), y + rng.randrange(h // 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 220))
    d.ellipse([x + w - 58, y + 12, x + w - 26, y + 44], fill=(235, 230, 200))
    base = y + h
    heights = [52, 78, 44, 96, 60, 120, 70, 88, 50, 66]
    bw = w // 10
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 2, base - hh, bx + bw - 2, base], fill=(12, 20, 44))
        for wy in range(base - hh + 8, base - 6, 12):
            for wx in range(bx + 6, bx + bw - 6, 10):
                if rng.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 110))
    d.polygon([(x + 4 * bw + 8, base - 120), (x + 5 * bw, base - 150),
               (x + 5 * bw + 16, base - 120)], fill=(12, 20, 44))
    trails = [(x + 30, y + 14, x + 150, y + 66), (x + 120, y + 6, x + 210, y + 58),
              (x + 210, y + 20, x + 280, y + 74)]
    for (x0, y0, x1, y1) in trails:
        for t in range(0, 21):
            tt = t / 20
            px = int(x0 + (x1 - x0) * tt)
            py = int(y0 + (y1 - y0) * tt + 14 * tt * (1 - tt) * -2)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 170, 60))
        d.ellipse([x1 - 4, y1 - 4, x1 + 4, y1 + 4], fill=(255, 220, 120))
    for (bx, by) in [(x + 150, y + 66), (x + 280, y + 74)]:
        for k in range(8):
            ang = k * 3.14159 / 4
            ex = int(bx + 13 * __import__("math").cos(ang))
            ey = int(by + 13 * __import__("math").sin(ang))
            d.line([(bx, by), (ex, ey)], fill=(255, 200, 80), width=2)
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 240, 160))


def scene_cricket(d, x, y, w, h):
    img = d._image
    vgrad(img, (x, y, x + w, y + h), (146, 196, 120), (86, 148, 74))
    d.ellipse([x + w - 62, y + 10, x + w - 24, y + 48], fill=(250, 220, 130))
    d.rectangle([x + w // 2 - 26, y + 18, x + w - 14, y + 52], fill=(24, 40, 24))
    d.rectangle([x + w // 2 - 26, y + 18, x + w - 14, y + 52],
                outline=(250, 220, 130), width=2)
    d.text((x + w // 2 - 18, y + 24), "IND 309/2", font=F_SANS_B(13),
           fill=(250, 240, 200))
    d.text((x + w // 2 - 18, y + 40), "RAHUL 117*", font=F_SANS_B(9),
           fill=(255, 220, 120))
    d.rectangle([x + 28, y + 58, x + w - 28, y + h - 6], fill=(196, 164, 110))
    d.rectangle([x + 28, y + 58, x + w - 28, y + h - 6],
                outline=(140, 110, 60), width=2)
    d.line([(x + 60, y + 58), (x + 60, y + h - 6)], fill=(255, 255, 255), width=2)
    d.line([(x + w - 60, y + 58), (x + w - 60, y + h - 6)], fill=(255, 255, 255),
           width=2)
    for sx in (x + 66, x + 72, x + 78):
        d.line([(sx, y + 66), (sx, y + 80)], fill=(255, 220, 60), width=3)
    d.ellipse([x + 148, y + 82, x + 162, y + 96], fill=(52, 36, 22))
    d.line([(x + 155, y + 96), (x + 155, y + 116)], fill=(52, 36, 22), width=6)
    d.line([(x + 155, y + 116), (x + 146, y + h - 8)], fill=(52, 36, 22), width=4)
    d.line([(x + 155, y + 116), (x + 166, y + h - 8)], fill=(52, 36, 22), width=4)
    d.line([(x + 155, y + 102), (x + 140, y + 112)], fill=(52, 36, 22), width=4)
    d.line([(x + 140, y + 112), (x + 128, y + 96)], fill=(160, 110, 60), width=5)
    d.ellipse([x + 96, y + 76, x + 106, y + 86], fill=(178, 32, 32))
    d.ellipse([x + 96, y + 76, x + 106, y + 86], outline=(255, 255, 255))


def mini_scene(d, kind, x, y, w, h, rng):
    import math
    if kind == "cyclone":
        vgrad(d._image, (x, y, x + w, y + h), (70, 110, 150), (220, 235, 240))
        cx, cy = x + w // 2, y + h // 2 + 4
        for r in range(20, 4, -4):
            d.arc([cx - r, cy - r, cx + r, cy + r], start=20 + r * 9,
                  end=300 + r * 9, fill=(255, 255, 255), width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(176, 30, 30))
        d.polygon([(x + 6, y + h - 8), (x + 60, y + h - 20), (x + 120, y + h - 10),
                   (x + w - 6, y + h - 6)], fill=(40, 90, 70))
    elif kind == "kyiv":
        vgrad(d._image, (x, y, x + w, y + h), (14, 20, 46), (60, 70, 110))
        for i, hh in enumerate([22, 34, 26, 40, 30]):
            bx = x + 8 + i * 36
            d.rectangle([bx, y + h - hh, bx + 28, y + h], fill=(10, 14, 34))
            d.rectangle([bx + 6, y + h - hh + 6, bx + 10, y + h - hh + 10],
                        fill=(255, 214, 110))
        for (x0, y0, x1, y1) in [(x + 20, y + 4, x + 80, y + 22),
                                 (x + 90, y + 2, x + 150, y + 18)]:
            for t in range(11):
                tt = t / 10
                d.ellipse([int(x0 + (x1 - x0) * tt) - 1, int(y0 + (y1 - y0) * tt) - 1,
                           int(x0 + (x1 - x0) * tt) + 1, int(y0 + (y1 - y0) * tt) + 1],
                          fill=(255, 170, 60))
    elif kind == "poland":
        vgrad(d._image, (x, y, x + w, y + h), (210, 220, 230), (240, 238, 228))
        d.ellipse([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + h - 8],
                  outline=(20, 86, 79), width=2)
        d.line([(x + 14, y + 12), (x + w - 30, y + 30)], fill=(176, 30, 30), width=2)
        d.ellipse([x + w - 34, y + 26, x + w - 26, y + 34], fill=(176, 30, 30))
        d.ellipse([x + w // 2 - 5, y + h // 2 - 12, x + w // 2 + 5, y + h // 2 - 2],
                  fill=(176, 30, 30))
        d.polygon([(x + w // 2 - 7, y + h // 2 - 2), (x + w // 2 + 7, y + h // 2 - 2),
                   (x + w // 2, y + h // 2 + 12)], fill=(176, 30, 30))
    elif kind == "denmark":
        vgrad(d._image, (x, y, x + w, y + h), (200, 60, 60), (150, 30, 30))
        d.rectangle([x + 52, y + 6, x + 66, y + h - 6], fill=(255, 255, 255))
        d.rectangle([x + 8, y + 16, x + w - 8, y + 28], fill=(255, 255, 255))
        d.rectangle([x + 120, y + 26, x + w - 10, y + h - 4], fill=(60, 60, 70))
        d.polygon([(x + 120, y + 26), (x + 150, y + 12), (x + w - 10, y + 26)],
                  fill=(90, 90, 100))
        d.rectangle([x + 132, y + 32, x + 138, y + 38], fill=(255, 214, 110))
    elif kind == "trophy":
        vgrad(d._image, (x, y, x + w, y + h), (250, 230, 170), (220, 190, 110))
        cx = x + w // 2
        d.polygon([(cx - 26, y + 8), (cx + 26, y + 8), (cx + 18, y + 28),
                   (cx - 18, y + 28)], fill=(201, 151, 28))
        d.arc([cx - 36, y + 6, cx - 14, y + 26], 90, 270, fill=(160, 110, 20), width=3)
        d.arc([cx + 14, y + 6, cx + 36, y + 26], -90, 90, fill=(160, 110, 20), width=3)
        d.rectangle([cx - 4, y + 28, cx + 4, y + 36], fill=(160, 110, 20))
        d.rectangle([cx - 16, y + 36, cx + 16, y + 42], fill=(120, 80, 10))
        for sx in (x + 20, x + w - 34):
            d.ellipse([sx, y + 10, sx + 12, y + 22], fill=(255, 255, 255))
    elif kind == "school":
        vgrad(d._image, (x, y, x + w, y + h), (240, 235, 215), (210, 195, 160))
        for i, c in enumerate([(176, 30, 30), (20, 86, 79), (201, 151, 28)]):
            by = y + h - 10 - i * 9
            d.rectangle([x + 30, by - 7, x + 130, by], fill=c)
        d.rectangle([x + 140, y + 8, x + w - 14, y + h - 8], fill=(255, 255, 255),
                    outline=(120, 110, 90))
        d.line([(x + 148, y + 18), (x + w - 22, y + 18)], fill=(40, 90, 160), width=2)
        d.line([(x + 148, y + 26, ), (x + w - 22, y + 26)], fill=(40, 90, 160), width=2)
        d.ellipse([x + 150, y + 32, x + 162, y + 44], fill=(255, 214, 110))
    elif kind == "sco":
        vgrad(d._image, (x, y, x + w, y + h), (230, 225, 205), (200, 190, 160))
        for i, c in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8),
                               (200, 40, 40), (20, 86, 79), (40, 90, 160)]):
            fx = x + 14 + i * 28
            d.line([(fx, y + 8), (fx, y + 34)], fill=(60, 60, 60), width=2)
            d.rectangle([fx, y + 8, fx + 20, y + 20], fill=c)
        d.rectangle([x + 20, y + 34, x + w - 20, y + h - 6], fill=(150, 60, 40))
        d.polygon([(x + 20, y + 34), (x + w // 2, y + 22), (x + w - 20, y + 34)],
                  fill=(120, 45, 30))
    elif kind == "whitehouse":
        vgrad(d._image, (x, y, x + w, y + h), (200, 215, 235), (240, 238, 228))
        d.rectangle([x + 40, y + 22, x + w - 40, y + h - 6], fill=(245, 245, 240),
                    outline=(120, 120, 110))
        d.polygon([(x + 34, y + 22), (x + w // 2, y + 8), (x + w - 34, y + 22)],
                  fill=(200, 200, 190))
        for i in range(4):
            cx0 = x + 52 + i * 30
            d.rectangle([cx0, y + 26, cx0 + 8, y + h - 8], fill=(210, 210, 200))
        d.ellipse([x + w - 30, y + 6, x + w - 14, y + 22], fill=(255, 214, 110))
    elif kind == "court":
        vgrad(d._image, (x, y, x + w, y + h), (235, 225, 205), (200, 170, 130))
        d.rectangle([x + 30, y + 20, x + 110, y + h - 6], fill=(240, 235, 220),
                    outline=(120, 110, 90))
        d.polygon([(x + 24, y + 20), (x + 70, y + 8), (x + 116, y + 20)],
                  fill=(160, 130, 100))
        for i in range(3):
            cx0 = x + 38 + i * 22
            d.rectangle([cx0, y + 26, cx0 + 8, y + h - 8], fill=(140, 120, 95))
        cx = x + w - 34
        d.polygon([(cx - 10, y + h - 6), (cx, y + 12), (cx + 10, y + h - 6)],
                  fill=(220, 90, 20))
        d.ellipse([cx - 4, y + 8, cx + 4, y + 16], fill=(255, 200, 60))
    elif kind == "quake":
        vgrad(d._image, (x, y, x + w, y + h), (210, 200, 180), (150, 130, 105))
        for i, mh in enumerate([18, 30, 24, 38]):
            mx = x + 8 + i * 44
            d.polygon([(mx, y + h - 8), (mx + 22, y + h - 8 - mh),
                       (mx + 44, y + h - 8)], fill=(110, 90, 70) if i % 2 else (90, 75, 58))
        pts = [(x + 8, y + 30), (x + 40, y + 22), (x + 60, y + 34),
               (x + 90, y + 20), (x + 120, y + 32), (x + 150, y + 22),
               (x + w - 8, y + 30)]
        d.line(pts, fill=(176, 30, 30), width=3, joint="curve")


# ---------------------------------------------------------------- map
LAND = {
    "namerica": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
                 (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 39),
                 (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
                 (-110, 23), (-115, 29), (-120, 34), (-125, 40), (-125, 48),
                 (-135, 58), (-155, 58), (-165, 60)],
    "greenland": [(-58, 64), (-45, 60), (-40, 64), (-30, 68), (-20, 70), (-25, 76),
                  (-40, 80), (-55, 78), (-60, 74)],
    "samerica": [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
                 (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -41),
                 (-70, -50), (-74, -54), (-73, -44), (-72, -30), (-70, -18),
                 (-77, -12), (-81, -5), (-80, 1)],
    "africa": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
               (30, -30), (20, -35), (15, -27), (12, -18), (9, -1), (9, 4),
               (-8, 5), (-15, 12)],
    "eurasia": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
                (10, 59), (18, 56), (21, 55), (24, 59), (30, 60), (30, 70),
                (40, 68), (55, 69), (70, 72), (90, 75), (110, 74), (130, 72),
                (150, 70), (170, 67), (178, 65), (170, 60), (162, 56), (156, 51),
                (142, 50), (140, 40), (135, 35), (130, 33), (122, 30), (120, 22),
                (110, 20), (105, 10), (100, 8), (97, 16), (92, 21), (88, 22),
                (80, 15), (77, 8), (73, 20), (66, 25), (60, 25), (57, 27),
                (52, 29), (48, 30), (43, 29), (39, 21), (35, 28), (33, 31),
                (30, 36), (26, 38), (23, 36), (19, 40), (15, 44), (12, 44),
                (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36)],
    "australia": [(114, -22), (114, -32), (120, -34), (130, -32), (137, -35),
                  (142, -38), (147, -39), (150, -37), (153, -32), (153, -27),
                  (146, -19), (142, -11), (136, -12), (132, -12), (126, -14),
                  (122, -17), (118, -20)],
    "uk": [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53)],
    "japan": [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
              (143, 43), (145, 44), (142, 42), (140, 39), (137, 37), (133, 35),
              (131, 33)],
    "seasia": [(95, 5), (100, 6), (104, 2), (105, -5), (110, -7), (115, -8),
               (120, -10), (125, -9), (130, -3), (135, -4), (140, -8), (138, -2),
               (132, 0), (128, 2), (122, 1), (118, 3), (112, 4), (105, 6)],
}


def inside_poly(lon, lat, poly):
    ins = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xint:
                ins = not ins
        j = i
    return ins


def on_land(lon, lat):
    return any(inside_poly(lon, lat, p) for p in LAND.values())


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 238),
                outline=(20, 86, 79), width=2)
    for k in range(1, 12):
        gx = x + k * w // 12
        d.line([(gx, y), (gx, y + h)], fill=(190, 205, 208), width=1)
    for k in range(1, 5):
        gy = y + k * h // 5
        d.line([(x, gy), (x + w, gy)], fill=(190, 205, 208), width=1)
    lon, lat = -180, 84
    while lon < 180:
        lat = 84
        while lat > -58:
            if on_land(lon, lat):
                px = x + int((lon + 180) / 360 * w)
                py = y + int((84 - lat) / 142 * h)
                d.ellipse([px - 1, py - 1, px + 2, py + 2], fill=(52, 96, 88))
            lat -= 3
        lon += 2
    d.rectangle([x + 4, y + 2, x + 300, y + 18], fill=(226, 236, 238))
    d.text((x + 8, y + 4), "THE WORLD ON SATURDAY — 13 PINS",
           font=F_SANS_B(11), fill=TEAL)
    for (num, lo, la) in PINS:
        px = x + int((lo + 180) / 360 * w)
        py = y + int((84 - la) / 142 * h)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        t = str(num)
        tw = d.textlength(t, font=F_SANS_B(10))
        d.text((px - tw / 2, py - 7), t, font=F_SANS_B(10), fill=(255, 255, 255))


# ---------------------------------------------------------------- build
def build():
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # masthead
    d.text((20, 12), "SATURDAY EDITION  ·  36 STORIES  ·  6 CONTINENTS  ·  EVERY ITEM DATED",
           font=F_SANS_B(11), fill=RED)
    d.text((20, 30), "THE WORLD IN ONE DAY", font=F_SERIF_B(46), fill=INK)
    d.text((20, 76), "Saturday 21 November 2026",
           font=F_SERIF_B(20), fill=RED)
    d.line([(20, 100), (1004, 100)], fill=INK, width=2)
    d.line([(20, 104), (1004, 104)], fill=RED, width=1)

    # stats strip
    d.rectangle([16, 110, 1008, 140], fill=RED)
    stats = [("3", "MISSILES DOWNED OVER RIYADH"),
             ("372,000", "EVACUATED AS AKVAN PASSED"),
             ("M6.7", "QUAKE SHAKES PERU, FELT IN LIMA"),
             ("117*", "RAHUL'S CENTURY IN WELLINGTON")]
    sx = 30
    for val, lab in stats:
        d.text((sx, 114), val, font=F_SANS_B(17), fill=(255, 255, 255))
        d.text((sx, 131), lab, font=F_SANS(8), fill=(255, 225, 200))
        sx += 248

    # continent chips
    chips = ["ASIA", "EUROPE", "AFRICA", "N. AMERICA", "S. AMERICA", "OCEANIA"]
    cx = 20
    for c in chips:
        tw = d.textlength(c, font=F_SANS_B(11))
        d.rounded_rectangle([cx, 146, cx + tw + 18, 168], radius=10,
                            fill=TEAL, outline=(255, 255, 255), width=1)
        d.text((cx + 9, 151), c, font=F_SANS_B(11), fill=(255, 255, 255))
        cx += tw + 26
    d.text((712, 151), "All 36 happened or first reported Sat 21 Nov 2026",
           font=F_SANS(11), fill=MUTED)

    # leads
    lx = [20, 352, 684]
    for i, lead in enumerate(LEADS):
        x = lx[i]
        y = 176
        w = 320
        soft_shadow(d, (x, y, x + w, y + 210))
        d.rectangle([x, y, x + w, y + 210], fill=CREAM, outline=(180, 165, 135))
        d.rectangle([x, y, x + w, y + 104], outline=(180, 165, 135))
        if lead["scene"] == "cop":
            scene_cop(d, x, y, w, 104)
        elif lead["scene"] == "riyadh":
            scene_riyadh(d, x, y, w, 104, rng)
        else:
            scene_cricket(d, x, y, w, 104)
        d.ellipse([x + 8, y + 112, x + 30, y + 134], fill=RED)
        t = str(lead["pin"])
        tw = d.textlength(t, font=F_SANS_B(13))
        d.text((x + 19 - tw / 2, y + 114), t, font=F_SANS_B(13),
               fill=(255, 255, 255))
        d.text((x + 36, y + 113), lead["kick"], font=F_SANS_B(10), fill=RED)
        yy = text_block(d, x + 10, y + 136, lead["head"], F_SERIF_B(15), w - 20,
                        leading=18)
        yy = text_block(d, x + 10, yy + 2, lead["body"], F_SANS(10), w - 20,
                        leading=13)
        d.text((x + 10, y + 196), "SRC: " + lead["src"], font=F_SANS(8), fill=MUTED)

    # feature cards 5 x 2
    for i, card in enumerate(CARDS):
        col, row = i % 5, i // 5
        x = 16 + col * 200
        y = 398 + row * 124
        w, h = 192, 118
        soft_shadow(d, (x, y, x + w, y + h))
        d.rectangle([x, y, x + w, y + h], fill=CREAM, outline=(180, 165, 135))
        mini_scene(d, card["scene"], x + 1, y + 1, w - 2, 46, rng)
        d.ellipse([x + 6, y + 52, x + 24, y + 70], fill=RED)
        t = str(card["pin"])
        tw = d.textlength(t, font=F_SANS_B(11))
        d.text((x + 15 - tw / 2, y + 54), t, font=F_SANS_B(11),
               fill=(255, 255, 255))
        d.text((x + 28, y + 54), card["title"], font=F_SANS_B(10), fill=INK)
        text_block(d, x + 8, y + 72, card["body"], F_SANS(9), w - 16, leading=11)
        d.text((x + 8, y + 104), "SRC: " + card["src"], font=F_SANS(7), fill=MUTED)

    # map
    draw_map(d, 16, 652, 992, 138)

    # briefs
    d.text((16, 796), "THE DAY IN BRIEF  ·  14-36", font=F_SANS_B(11), fill=RED)
    d.line([(16, 812), (1008, 812)], fill=RED, width=1)
    for i, (num, txt, src) in enumerate(BRIEFS):
        col = i // 8
        row = i % 8
        x = 16 + col * 336
        y = 818 + row * 18
        d.text((x, y), str(num), font=F_SANS_B(10), fill=RED)
        d.text((x + 22, y), txt, font=F_SANS(10), fill=INK)
        tw = d.textlength(txt, font=F_SANS(10))
        d.text((x + 22 + tw + 4, y), "— " + src, font=F_SANS(9), fill=MUTED)

    # date check
    d.rectangle([16, 964, 1008, 986], fill=(232, 222, 196), outline=(176, 30, 30))
    d.text((24, 969),
           "DATE CHECK — NOT 21 NOV, EXCLUDED: Akvan landfall 20 Nov  ·  ICJ Myanmar 19 Nov  ·  Pete Rose pardon 20 Nov  ·  Sensex +898 20 Nov  ·  JPMorgan/Visa/MC 19 Nov  ·  Elantra 19 Nov",
           font=F_SANS_B(9), fill=RED_DK)

    # footer
    d.text((16, 992),
           "METHOD: every story happened, or was first reported, on Sat 21 Nov 2026 in some time zone; late-Friday events count only where first reported Saturday. Sources named on each item.",
           font=F_SANS(8), fill=MUTED)
    d.text((16, 1004),
           "THE WORLD IN ONE DAY  ·  Saturday 21 November 2026  ·  36 verified stories  ·  make.fun news-image-20261121  ·  drawn by code, no photos",
           font=F_SANS_B(8), fill=INK)

    paper_texture(img, rng)
    img2 = img.convert("RGBA")
    vignette(img2)
    img2.convert("RGB").save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
