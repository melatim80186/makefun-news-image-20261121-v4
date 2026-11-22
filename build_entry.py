# build_entry.py — draws news-image-20261121 v4 (fresh code, written 2026-11-22).
# 37 stories, all dated Saturday 21 November 2026 (see STORIES.md for the
# date-check method). Newspaper style: masthead, UTC timeline, numbers strip,
# region tabs, 13 pictured stories, world map, ALSO list, DATE CHECK box.
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1024, 1024
PAPER = (247, 242, 231); INK = (26, 26, 26); RED = (179, 32, 44)
BLUE = (31, 78, 121); TEAL = (0, 110, 110); GOLD = (176, 132, 30)
GREY = (110, 108, 100); LIGHT = (232, 226, 210); MID = (214, 206, 188)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
SERIF = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIFI = lambda s: F("DejaVuSerif.ttf", s)  # no italic file on this VM; plain serif
SANS = lambda s: F("DejaVuSans.ttf", s)
SANSB = lambda s: F("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(draw, text, font, width):
    out = []
    for line in text.split("\n"):
        words, cur = line.split(), ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if draw.textlength(t, font=font) <= width:
                cur = t
            else:
                if cur: out.append(cur)
                cur = w_
        if cur: out.append(cur)
    return out

def para(draw, x, y, text, font, width, fill=INK, leading=None):
    lh = leading or int(font.size * 1.25)
    for ln in wrap(draw, text, font, width):
        draw.text((x, y), ln, font=font, fill=fill); y += lh
    return y

def centre(draw, y, text, font, fill=INK, cx=512):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text, font=font, fill=fill)

def tagbar(draw, x, y, w, label, badge, bcol):
    draw.rectangle([x, y, x + w, y + 16], fill=INK)
    draw.text((x + 5, y + 2), label, font=SANSB(9), fill=(255, 255, 255))
    bw = draw.textlength(badge, font=SANSB(8)) + 10
    draw.rectangle([x + w - bw, y, x + w, y + 16], fill=bcol)
    draw.text((x + w - bw + 5, y + 3), badge, font=SANSB(8), fill=(255, 255, 255))

# ---------- masthead ----------
d.line([8, 6, 1016, 6], fill=INK, width=2)
centre(d, 8, "THE WORLD IN ONE DAY  ·  ALL TIMES UTC  ·  DAY 325 OF 2026",
       SANSB(11), GREY)
centre(d, 26, "Saturday 21 November 2026", SERIF(54), INK)
d.line([8, 88, 1016, 88], fill=RED, width=3)
centre(d, 94, "37 STORIES  ·  8 REGIONS  ·  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
       SANSB(13), RED)
centre(d, 112, "Iran strikes Bahrain  ·  Mexico captures \u201cEl Chapo Isidro\u201d  ·  COP31 talks run into overtime",
       SERIFI(13), INK)

# ---------- UTC timeline ----------
d.rectangle([8, 132, 1016, 154], fill=INK)
d.text((14, 138), "THE DAY IN UTC", font=SANSB(10), fill=(255, 255, 255))
tl = [("00:09", "Peru quake"), ("02:00", "Sinaloa raid"),
      ("06:50", "Sparta II hit"), ("09:42", "Timor quake"),
      ("12:12", "EU-Indonesia"), ("18:24", "Mercury burn"),
      ("19:44", "Bahrain blaze"), ("NIGHT", "COP31 talks")]
x = 120
for t, lbl in tl:
    d.text((x, 138), t, font=SANSB(10), fill=(255, 210, 90))
    tw = d.textlength(t, font=SANSB(10))
    d.text((x + tw + 4, 139), lbl, font=SANS(9), fill=(255, 255, 255))
    x += 110

# ---------- numbers strip ----------
nums = [("130+", "countries want fossil fuels\nnamed at COP31  ·  AFP"),
        ("3", "Houthi missiles downed\nover Riyadh  ·  AJ"),
        ("6.7", "magnitude of the Peru quake,\n108 km deep  ·  USGS"),
        ("146", "safe as Air Niugini jet lands\nin Davao  ·  CAAP"),
        ("$55,100", "Bitcoin's low, weakest\nsince Sept 2024  ·  Coinbase"),
        ("11", "dead as \u201cEl Chapo Isidro\u201d\nis caught  ·  Reuters")]
d.text((8, 160), "THE DAY IN NUMBERS", font=SANSB(10), fill=RED)
x = 8
for big, small in nums:
    d.rectangle([x, 176, x + 164, 222], outline=INK, width=1)
    d.text((x + 6, 178), big, font=SERIF(22), fill=RED)
    para(d, x + 6, 203, small, SANS(8), 152, leading=9)
    x += 168

# ---------- region tabs ----------
regs = [("EUROPE", 10, BLUE), ("ASIA", 9, (0, 128, 96)), ("MIDDLE EAST", 6, RED),
        ("N. AMERICA", 3, (120, 70, 140)), ("LATIN AM.", 2, (200, 110, 0)),
        ("AFRICA", 2, (140, 90, 20)), ("OCEANIA", 3, TEAL), ("GLOBAL", 3, GREY)]
d.text((8, 228), "STORIES BY REGION", font=SANSB(10), fill=RED)
x = 150
for name, n, col in regs:
    lab = f"{name} {n}"
    w_ = d.textlength(lab, font=SANSB(10)) + 12
    d.rectangle([x, 226, x + w_, 244], fill=col)
    d.text((x + 6, 230), lab, font=SANSB(10), fill=(255, 255, 255))
    x += w_ + 4

# ---------- flat illustrations (drawn in code, not photographs) ----------
def _scene(kind, box):
    x0, y0, x1, y1 = box
    w_, h_ = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "gulf":  # Bahrain / Hormuz
        d.rectangle(box, fill=(168, 208, 224))
        d.polygon([(x0, y0 + 30), (x0 + 120, y0), (x0 + 200, y0 + 20), (x0 + 190, y0 + 55),
                   (x0 + 90, y0 + 60), (x0, y0 + 75)], fill=(226, 205, 160))
        d.polygon([(x0 + 210, y0 + 55), (x1, y0 + 40), (x1, y1), (x0 + 230, y1)], fill=(226, 205, 160))
        d.ellipse([x0 + 60, y0 + 62, x0 + 92, y0 + 94], fill=(255, 120, 40))
        for a, b in [(76, 62), (76, 94), (60, 78), (92, 78)]:
            d.line([x0 + a, y0 + b - 12, x0 + a, y0 + b + 12], fill=(255, 80, 20), width=3)
            d.line([x0 + a - 12, y0 + b, x0 + a + 12, y0 + b], fill=(255, 80, 20), width=3)
        d.rectangle([x0 + 200, y0 + 70, x0 + 260, y0 + 84], fill=(60, 60, 60))
        d.polygon([(x0 + 210, y0 + 70), (x0 + 222, y0 + 58), (x0 + 228, y0 + 70)], fill=(60, 60, 60))
        d.text((x0 + 8, y1 - 18), "STRAIT OF HORMUZ", font=SANSB(9), fill=INK)
    elif kind == "cop":  # COP31 calendar, no deal yet
        d.rectangle(box, fill=(240, 236, 220))
        for i, day in enumerate(["16", "17", "18", "19", "20", "SAT 21"]):
            bx = x0 + 10 + i * 52
            d.rectangle([bx, y0 + 14, bx + 46, y0 + 58], outline=INK, width=2,
                        fill=RED if i == 5 else (255, 255, 255))
            d.text((bx + 6, y0 + 28), day, font=SANSB(10), fill=(255, 255, 255) if i == 5 else INK)
        d.text((x0 + 10, y0 + 66), "NO DEAL YET", font=SERIF(20), fill=RED)
        d.text((x0 + 10, y0 + 88), "3rd draft still missing", font=SANS(10), fill=INK)
    elif kind == "mexico":  # wanted poster
        d.rectangle(box, fill=(238, 226, 200))
        d.rectangle([x0 + 14, y0 + 8, x0 + 110, y0 + 96], outline=INK, width=2, fill=(255, 255, 255))
        d.ellipse([x0 + 46, y0 + 20, x0 + 78, y0 + 52], fill=(120, 120, 120))
        d.polygon([(x0 + 34, y0 + 88), (x0 + 46, y0 + 56), (x0 + 78, y0 + 56), (x0 + 90, y0 + 88)],
                  fill=(70, 70, 70))
        d.text((x0 + 126, y0 + 14), "FBI TOP 10", font=SANSB(12), fill=RED)
        d.text((x0 + 126, y0 + 34), "CAPTURED", font=SERIF(20), fill=INK)
        d.text((x0 + 126, y0 + 62), "11 DEAD", font=SERIF(16), fill=RED)
        d.text((x0 + 126, y0 + 84), "Guasave, Sinaloa", font=SANS(10), fill=INK)
    elif kind == "quake":  # Peru seismograph
        d.rectangle(box, fill=(222, 214, 196))
        d.polygon([(x0, y1), (x0 + 60, y0 + 55), (x0 + 110, y0 + 80), (x0 + 170, y0 + 30),
                   (x0 + 230, y0 + 85), (x0 + 290, y0 + 45), (x1, y1)], fill=(150, 120, 80))
        d.line([(x0, cy), (x0 + 40, cy), (x0 + 55, cy - 26), (x0 + 70, cy + 20),
                    (x0 + 85, cy - 34), (x0 + 100, cy + 26), (x0 + 130, cy),
                    (x0 + 200, cy), (x0 + 215, cy - 18), (x0 + 230, cy + 14), (x1, cy)],
                   fill=RED, width=3)
        d.text((x0 + 10, y0 + 8), "M6.7", font=SERIF(26), fill=INK)
        d.text((x0 + 120, y0 + 12), "108 KM DEEP", font=SANSB(11), fill=INK)
    elif kind == "ship":  # Sparta II ablaze
        d.rectangle(box, fill=(170, 205, 225))
        d.rectangle([x0 + 40, y0 + 58, x0 + 280, y0 + 82], fill=(40, 40, 40))
        d.rectangle([x0 + 90, y0 + 30, x0 + 130, y0 + 58], fill=(200, 200, 200))
        d.polygon([(x0 + 150, y0 + 58), (x0 + 165, y0 + 8), (x0 + 180, y0 + 58)], fill=(255, 140, 30))
        d.polygon([(x0 + 185, y0 + 58), (x0 + 200, y0 + 22), (x0 + 215, y0 + 58)], fill=(255, 90, 20))
        d.ellipse([x0 + 240, y0 + 10, x0 + 252, y0 + 22], fill=(60, 60, 60))
        d.text((x0 + 10, y0 + 84), "SPARTA II  ·  GULF OF FINLAND", font=SANSB(9), fill=INK)
    elif kind == "mercury":  # BepiColombo
        d.rectangle(box, fill=(18, 22, 40))
        for sx, sy in [(30, 20), (90, 14), (250, 18), (290, 40), (60, 90), (300, 85)]:
            d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 255))
        d.ellipse([x0 + 40, y0 + 30, x0 + 130, y0 + 120], fill=(180, 140, 100))
        d.ellipse([x0 + 62, y0 + 52, x0 + 100, y0 + 90], fill=(200, 165, 120))
        d.ellipse([x0 + 160, y0 + 30, x1 - 4, y0 + 90], outline=(255, 210, 90), width=2)
        d.rectangle([x0 + 210, y0 + 48, x0 + 226, y0 + 62], fill=(220, 220, 220))
        d.rectangle([x0 + 196, y0 + 54, x0 + 210, y0 + 58], fill=(150, 180, 255))
        d.text((x0 + 140, y0 + 84), "18:24 GMT", font=SANSB(11), fill=(255, 210, 90))
    elif kind == "flags":  # EU + Indonesia
        d.rectangle(box, fill=(240, 236, 220))
        d.rectangle([x0 + 20, y0 + 16, x0 + 140, y0 + 88], fill=(0, 51, 153))
        for k in range(12):
            import math
            a = k * math.pi / 6
            sx, sy = 80 + 34 * math.cos(a), 52 + 26 * math.sin(a)
            d.ellipse([x0 + sx - 3, y0 + sy - 3, x0 + sx + 3, y0 + sy + 3], fill=(255, 204, 0))
        d.rectangle([x0 + 180, y0 + 16, x0 + 300, y0 + 52], fill=(200, 30, 40))
        d.rectangle([x0 + 180, y0 + 52, x0 + 300, y0 + 88], fill=(255, 255, 255))
        d.text((x0 + 20, y0 + 92), "SIGNED  ·  98.5% OF TARIFFS GO", font=SANSB(9), fill=INK)
    elif kind == "bitcoin":  # chart dive + rebound
        d.rectangle(box, fill=(255, 248, 220))
        d.line([(x0 + 10, y0 + 30), (x0 + 80, y0 + 44), (x0 + 140, y0 + 38),
                    (x0 + 200, y0 + 78), (x0 + 250, y0 + 88), (x0 + 300, y0 + 62)],
                   fill=RED, width=4)
        d.text((x0 + 12, y0 + 8), "$55,100", font=SERIF(22), fill=INK)
        d.text((x0 + 180, y0 + 88), "LOWEST SINCE SEPT 2024", font=SANSB(9), fill=RED)
    elif kind == "fire":  # Basra power plant
        d.rectangle(box, fill=(235, 225, 205))
        d.rectangle([x0 + 30, y0 + 50, x0 + 150, y0 + 96], fill=(120, 120, 120))
        d.rectangle([x0 + 50, y0 + 20, x0 + 66, y0 + 50], fill=(90, 90, 90))
        d.rectangle([x0 + 90, y0 + 28, x0 + 104, y0 + 50], fill=(90, 90, 90))
        d.polygon([(x0 + 170, y0 + 96), (x0 + 190, y0 + 40), (x0 + 210, y0 + 96)], fill=(255, 140, 30))
        d.polygon([(x0 + 220, y0 + 96), (x0 + 240, y0 + 52), (x0 + 260, y0 + 96)], fill=(255, 90, 20))
        d.text((x0 + 160, y0 + 8), "4 DEAD", font=SERIF(18), fill=RED)
    elif kind == "expel":  # Denmark expulsion
        d.rectangle(box, fill=(238, 232, 214))
        d.rectangle([x0 + 90, y0 + 10, x0 + 230, y0 + 96], outline=INK, width=3, fill=(255, 255, 255))
        d.ellipse([x0 + 140, y0 + 26, x0 + 180, y0 + 66], fill=(120, 120, 120))
        d.polygon([(x0 + 128, y0 + 92), (x0 + 140, y0 + 68), (x0 + 180, y0 + 68), (x0 + 192, y0 + 92)],
                  fill=(70, 70, 70))
        d.text((x0 + 12, y0 + 30), "EXPELLED", font=SERIF(16), fill=RED)
        d.text((x0 + 12, y0 + 56), "7 DAYS\nTO LEAVE", font=SANSB(11), fill=INK)
    elif kind == "robot":  # Geneva killer robots
        d.rectangle(box, fill=(228, 232, 238))
        d.rectangle([x0 + 120, y0 + 18, x0 + 200, y0 + 70], fill=(150, 160, 170))
        d.ellipse([x0 + 140, y0 + 30, x0 + 152, y0 + 42], fill=RED)
        d.ellipse([x0 + 168, y0 + 30, x0 + 180, y0 + 42], fill=RED)
        d.rectangle([x0 + 140, y0 + 70, x0 + 180, y0 + 96], fill=(120, 130, 140))
        d.text((x0 + 10, y0 + 20), "DRAFT BY", font=SANSB(11), fill=INK)
        d.text((x0 + 10, y0 + 40), "2028", font=SERIF(26), fill=INK)
        d.text((x0 + 10, y0 + 72), "128 STATES AGREE", font=SANSB(9), fill=INK)
    elif kind == "plane":  # Davao emergency landing
        d.rectangle(box, fill=(180, 210, 230))
        d.ellipse([x0 + 90, y0 + 40, x0 + 240, y0 + 66], fill=(255, 255, 255))
        d.polygon([(x0 + 220, y0 + 40), (x0 + 290, y0 + 52), (x0 + 220, y0 + 60)], fill=(255, 255, 255))
        d.polygon([(x0 + 130, y0 + 66), (x0 + 160, y0 + 88), (x0 + 180, y0 + 66)], fill=(200, 200, 200))
        d.rectangle([x0, y0 + 88, x1, y1], fill=(90, 90, 90))
        d.text((x0 + 10, y0 + 6), "146 SAFE", font=SERIF(18), fill=INK)
    elif kind == "race":  # Las Vegas GP
        d.rectangle(box, fill=(20, 20, 30))
        for r in range(2):
            for c in range(8):
                if (r + c) % 2 == 0:
                    d.rectangle([x0 + 10 + c * 14, y0 + 10 + r * 14, x0 + 24 + c * 14, y0 + 24 + r * 14],
                                fill=(255, 255, 255))
        d.rectangle([x0 + 140, y0 + 44, x0 + 290, y0 + 66], fill=(200, 30, 40))
        d.ellipse([x0 + 160, y0 + 62, x0 + 182, y0 + 84], fill=INK)
        d.ellipse([x0 + 250, y0 + 62, x0 + 272, y0 + 84], fill=INK)
        d.text((x0 + 140, y0 + 86), "VERSTAPPEN WINS", font=SERIF(14), fill=(255, 210, 90))



def scene(kind, box):
    global d
    x0, y0, x1, y1 = box
    if y1 - y0 >= 100:
        _scene(kind, box)
        return
    tmp = Image.new("RGB", (320, 104), PAPER)
    saved = d
    d = ImageDraw.Draw(tmp)
    _scene(kind, (0, 0, 320, 104))
    d = saved
    img.paste(tmp.resize((x1 - x0, y1 - y0)), (x0, y0))

# ---------- heroes (3) ----------
HEROES = [
    ("MIDDLE EAST", "1", "CONFIRMED", RED, "gulf",
     "Iran strikes Bahrain as tanker is hit off Oman",
     "Bahrain says an Iranian attack set a civilian site ablaze. UKMTO: a tanker was struck off Khasab.",
     "AL JAZEERA · REUTERS · AFP"),
    ("GLOBAL", "2", "CONFIRMED", RED, "cop",
     "COP31 deadlocked over fossil fuels in overtime",
     "A day past its Friday deadline in Antalya, talks pause overnight. The EU rejects a draft omitting fossil fuels.",
     "BBC · AFP · IRISH TIMES"),
    ("N. AMERICA", "3", "CONFIRMED", RED, "mexico",
     "Mexico captures \u201cEl Chapo Isidro\u201d in army raid",
     "Troops seize FBI top-ten fugitive Fausto Isidro Meza Flores in Guasave; four soldiers and seven gunmen killed.",
     "REUTERS · AP · GUARDIAN"),
]
for i, (reg, num, badge, bc, kind, title, body, src) in enumerate(HEROES):
    x = 8 + i * 336
    d.rectangle([x, 250, x + 328, 448], outline=INK, width=1)
    scene(kind, (x + 1, 251, x + 327, 347))
    tagbar(d, x, 348, 328, f"{reg}  {num}", badge, bc)
    para(d, x + 6, 368, title, SERIF(17), 316, leading=19)
    para(d, x + 6, 406, body, SANS(10), 316, leading=12)
    d.text((x + 6, 434), src, font=SANSB(8), fill=GREY)

# ---------- secondary pictured (10) ----------
SEC = [
    ("PERU · QUAKE", "4", "OFFICIAL", BLUE, "quake", "Deep 6.7 quake shakes Peru", "Jun\u00edn, 108 km deep · USGS"),
    ("GULF OF FINLAND", "5", "CONFIRMED", RED, "ship", "Drones set Russian cargo ship ablaze", "Sparta II, crew taken off · BBC"),
    ("MERCURY · SCIENCE", "6", "OFFICIAL", BLUE, "mercury", "BepiColombo fires its Mercury orbit burn", "18:24 GMT burn, 8 yrs out · ESA"),
    ("BRUSSELS · TRADE", "7", "OFFICIAL", BLUE, "flags", "EU and Indonesia sign trade pact", "98.5% of tariffs go · EURONEWS"),
    ("CRYPTO", "8", "CONFIRMED", RED, "bitcoin", "Bitcoin dives, then rebounds", "$55,100 low since Sept 2024"),
    ("IRAQ · DISASTER", "9", "CONFIRMED", RED, "fire", "Power-plant fire kills 4 in Basra", "35 hurt, houses ablaze · REUTERS"),
    ("DENMARK · DIPLOMACY", "10", "CONFIRMED", RED, "expel", "Denmark expels Russian attach\u00e9", "Over Kyivstoner murder plot"),
    ("GENEVA · ARMS", "11", "REPORTED", TEAL, "robot", "UN \u2018killer robot\u2019 talks end", "Draft rules by 2028, 128 states"),
    ("DAVAO · AVIATION", "12", "OFFICIAL", BLUE, "plane", "Air Niugini jet lands safe, 146 aboard", "Engine-fire warning · CAAP"),
    ("LAS VEGAS · SPORT", "13", "CONFIRMED", RED, "race", "Verstappen wins wild Las Vegas GP", "Antonelli fastest, penalised"),
]
for i, (reg, num, badge, bc, kind, title, src) in enumerate(SEC):
    col, row = i % 5, i // 5
    x = 8 + col * 204
    y = 454 + row * 104
    d.rectangle([x, y, x + 196, y + 98], outline=INK, width=1)
    scene(kind, (x + 1, y + 1, x + 195, y + 45))
    d.text((x + 5, y + 48), f"{num}  {reg}", font=SANSB(8), fill=RED)
    bw = d.textlength(badge, font=SANSB(7)) + 8
    d.rectangle([x + 196 - bw, y + 46, x + 196, y + 60], fill=bc)
    d.text((x + 196 - bw + 4, y + 48), badge, font=SANSB(7), fill=(255, 255, 255))
    para(d, x + 5, y + 62, title, SANSB(9), 186, leading=11)
    d.text((x + 5, y + 88), src, font=SANS(8), fill=GREY)

# ---------- world map (coarse land mask, drawn in code) ----------
MAP = [
    ".....##########..............#########################.......",
    "....############.............##########################.....",
    "....#############............###########################....",
    ".....############............#############..############....",
    "......###########............###########################....",
    ".......##########............###########################....",
    "........#########.............################.#########...",
    ".........#########............###########..###########......",
    "..........########............##########...##########......",
    "...........######..............########.....#########......",
    "............#####..............######.......########.......",
    ".............####..............#####.........#######........",
    ".............#####.............#####..........######........",
    ".............######............####...........#####.........",
    "..............#####............###............####..........",
    "..............#####............####...........###..####.....",
    "..............#####............####...........##...#####....",
    "...............####............###............#....#####....",
    "...............####............###................####.....",
    "...............####............##.................####.....",
    "................###............##.................####.....",
    "................###............#..................###......",
    "................##................................##......",
    "................##................................##......",
    "................#..................................#......",
    "................#.........................................",
]
MX, MY, MW, MH = 8, 680, 328, 188
d.rectangle([8, 662, 336, 872], outline=INK, width=1)
d.rectangle([8, 662, 336, 680], fill=INK)
d.text((14, 666), "WHERE IT HAPPENED", font=SANSB(10), fill=(255, 255, 255))
d.text((200, 666), "pins 1\u201313 = pictured", font=SANS(9), fill=(200, 200, 200))
cw, ch = MW / 60, MH / 26
for r, row in enumerate(MAP):
    for c, ch_ in enumerate(row):
        if ch_ == "#":
            d.rectangle([MX + c * cw, MY + r * ch, MX + (c + 1) * cw, MY + (r + 1) * ch],
                        fill=(214, 196, 150))
PINS = {1: (50.6, 26.2), 2: (30.7, 36.9), 3: (-107.4, 25.0), 4: (-75.0, -11.0),
        5: (24.0, 59.8), 7: (4.4, 50.8), 9: (47.8, 30.5), 10: (12.6, 55.7),
        11: (6.1, 46.2), 12: (125.6, 7.1), 13: (-115.1, 36.1)}
NUDGE = {1: (-11, 9), 9: (11, -7), 7: (-12, 3), 11: (12, 7), 10: (2, -12), 5: (9, -5)}
for n, (lon, lat) in PINS.items():
    px = MX + (lon + 180) / 360 * MW
    py = MY + (75 - lat) / 130 * MH
    dx, dy = NUDGE.get(n, (0, 0))
    if (dx, dy) != (0, 0):
        d.line([px, py, px + dx, py + dy], fill=RED, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        px, py = px + dx, py + dy
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px - 3, py - 5), str(n), font=SANSB(7), fill=(255, 255, 255))
d.text((14, 856), "6 Mercury & 8 Bitcoin: off-map (space / global).",
       font=SANS(8), fill=GREY)

# ---------- ALSO list 14-37 ----------
ALSO = [
    (14, "Kyiv: Zelensky calls bridge strike \u2018a fair response\u2019", "BBC"),
    (15, "Riyadh: coalition downs 3 Houthi missiles", "AJ"),
    (16, "Gaza City: Israeli strike kills 4, rescuers say", "REUTERS"),
    (17, "Beirut: Aoun demands Israeli pull-out", "AJ"),
    (18, "Brussels: Costa proposes \u20ac204bn cut to EU budget", "DW"),
    (19, "Bras\u00edlia: Bolsonaro moved to intensive care", "REUTERS"),
    (20, "Washington: FBI probes crime-database breach", "BBC"),
    (21, "Serang, Java: sweet-factory fire, 3 dead, 36 missing", "BBC"),
    (22, "Hanoi: law to speed land expropriation passes", "REUTERS"),
    (23, "Savar: 80 garment factories shut in wage protests", "TBS"),
    (24, "Mastung: Pakistan forces kill 15 militants", "DAWN"),
    (25, "Beijing: Singapore\u2019s Wong meets Li Qiang, 20+ deals", "ST"),
    (26, "Qinghai: M5.9 quake, 10:45 UTC", "USGS"),
    (27, "Dublin: Ireland beat South Africa 20\u201317", "BBC"),
    (28, "Turin: Alcaraz beats Shelton, faces Zverev", "ATP"),
    (29, "Melbourne: Australia beat England by 3 wickets", "BBC"),
    (30, "Wellington: India 486/4, lead New Zealand by 118", "AFP"),
    (31, "Abuja: CAF makes Kiswahili a 5th official language", "CAF"),
    (32, "Niger State: gunmen kill 5 in village raid", "TRUST"),
    (33, "Paris: 144 held at cost-of-living marches", "AFP"),
    (34, "London: England beat All Blacks 37\u201312", "BBC"),
    (35, "Taiwan: 15 Chinese jets cross the median line", "MND"),
    (36, "Darwin: M6.8 Timor quake felt across the north", "USGS"),
    (37, "Warsaw: Rutte \u2014 NATO will defend every inch", "GUARDIAN"),
]
d.rectangle([344, 662, 1016, 872], outline=INK, width=1)
d.rectangle([344, 662, 1016, 680], fill=INK)
d.text((350, 666), "ALSO ON SATURDAY 21 NOVEMBER \u2014 24 MORE STORIES", font=SANSB(10),
       fill=(255, 255, 255))
for i, (n, txt, src) in enumerate(ALSO):
    col, row = i // 12, i % 12
    x = 350 + col * 336
    y = 686 + row * 16
    d.text((x, y), str(n), font=SANSB(10), fill=RED)
    d.text((x + 20, y), txt, font=SANS(10), fill=INK)
    sw = d.textlength(src, font=SANSB(8))
    d.text((x + 330 - sw, y + 1), src, font=SANSB(8), fill=GREY)

# ---------- DATE CHECK ----------
d.rectangle([8, 880, 1016, 968], outline=RED, width=2)
d.text((14, 886), "DATE CHECK \u2014 WHAT WE LEFT OUT", font=SANSB(11), fill=RED)
para(d, 14, 900,
     "Friday 20 Nov, not shown: Wall Street\u2019s AI rout  ·  Russian missiles landing in Poland  ·  Kyiv\u2019s bridges barrage  ·  Cyclone Akvan\u2019s landfall  ·  US Treasury\u2019s Iran oil-trustee sanctions.",
     SANS(10), 996, leading=13)
para(d, 14, 926,
     "Thursday 19 Nov, not shown: the Shenzhen Trump\u2013Xi\u2013Putin summit  ·  the ICJ Myanmar ruling  ·  the Anthropic IPO.  Wednesday 18 Nov: Voyager 1\u2019s light-day.  Not yet: COP31\u2019s closing session (Sunday 22) and BepiColombo\u2019s first Mercury science.",
     SANS(10), 996, leading=13)
d.text((14, 954), "Every story above happened, or was first reported, on Saturday 21 November 2026.",
       font=SANSB(10), fill=INK)

# ---------- footer ----------
d.line([8, 976, 1016, 976], fill=INK, width=1)
d.text((8, 982), "HOW SURE:  ", font=SANSB(9), fill=INK)
fx = 8 + d.textlength("HOW SURE:  ", font=SANSB(9))
for lab, col in [("CONFIRMED  2+ outlets", RED), ("  OFFICIAL  on the record", BLUE),
                 ("  REPORTED  one outlet", TEAL), ("  CLAIM  one side says", GREY)]:
    d.rectangle([fx, 983, fx + 10, 993], fill=col)
    d.text((fx + 13, 982), lab, font=SANS(9), fill=INK)
    fx += 13 + d.textlength(lab, font=SANS(9)) + 6
centre(d, 998, "Sources named beside each story. All maps and drawings are original vector work, drawn in code \u2014 not photographs.",
       SANS(9), GREY)
centre(d, 1012, "Saturday 21 November 2026  ·  37 stories  ·  8 regions  ·  The World in One Day",
       SANSB(9), INK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
