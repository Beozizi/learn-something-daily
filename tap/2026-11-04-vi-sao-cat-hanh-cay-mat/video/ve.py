"""Hàm vẽ SVG dùng chung cho các cảnh: đồ vật trong bếp, sơ đồ trên bảng, nhân vật Tò.

Quy ước: mỗi hàm trả về chuỗi SVG. Vị trí đặt bằng thuộc tính transform ở nhóm ngoài,
nhóm trong mang id để GSAP diễn hoạt (không để GSAP đè lên transform đặt vị trí).
"""
import re
from pathlib import Path

INK = "#081420"
SW = 6
WALL = "#1E4A63"
TILE = "#245A78"
TILE_LINE = "#2C6788"
SKY = "#FF9F5A"
WOOD_TOP = "#B7834F"
WOOD = "#7A5233"
WOOD_DARK = "#5E3E26"
SLATE = "#13304A"
PAPER = "#F5F1E8"
TEAL = "#19C3B1"
GREY = "#9FB3C8"
YELLOW = "#FFC145"
GAS = "#CDEB6E"
TEAR = "#9FD8F5"
CORAL = "#FF6B5A"
WHITE = "#F5F7FA"
ONION = "#E8B36A"
ONION_LINE = "#C98A3E"
CELL = "#EEF3D2"
PINK = "#F7A8B8"

TO_DIR = Path(r"E:\science and technology\assets\nhan-vat\to")


def place(x, y, inner, s=1.0, r=0.0, extra=""):
    t = f"translate({x} {y})"
    if r:
        t += f" rotate({r})"
    if s != 1:
        t += f" scale({s})"
    return f'<g transform="{t}"{extra}>{inner}</g>'


def g(id_, inner, extra=""):
    return f'<g id="{id_}"{extra}>{inner}</g>'


def text(x, y, s, size=52, weight=800, fill=WHITE, anchor="start", id_=None, extra=""):
    i = f' id="{id_}"' if id_ else ""
    return (f'<text{i} x="{x}" y="{y}" font-family="Be Vietnam Pro" font-weight="{weight}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}"{extra}>{s}</text>')


# ---------- nhân vật ----------

def to(uid, pose, x, y, h):
    """Tò ở tư thế `pose`, góc trên trái (x, y), cao h px. Bọc trong nhóm id `<uid>-w` để bật/tắt."""
    src = (TO_DIR / f"{pose}.svg").read_text(encoding="utf-8")
    inner = re.search(r"<svg[^>]*>(.*)</svg>", src, re.S).group(1)
    inner = re.sub(r"<title>.*?</title>", "", inner)
    inner = inner.replace(f'id="to-{pose}"', f'id="{uid}"')
    w = h * 440 / 540
    return (f'<g id="{uid}-w"><svg x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'viewBox="0 0 440 540" overflow="visible">{inner}</svg></g>')


def to_point(x, y, h, px, py):
    """Đổi tọa độ trong SVG của Tò (viewBox 440×540) sang tọa độ khung hình."""
    k = h / 540
    return x + px * k, y + py * k


# ---------- đồ vật ----------

def onion(id_, cx, cy, s=1.0):
    body = f"""
<path d="M-22 84 q-6 18 -18 24 M0 88 q0 18 -6 28 M20 84 q8 16 18 20" fill="none" stroke="{ONION_LINE}" stroke-width="5" stroke-linecap="round"/>
<path d="M0 -96 C22 -62 82 -42 82 20 C82 70 46 92 0 92 C-46 92 -82 70 -82 20 C-82 -42 -22 -62 0 -96 Z" fill="{ONION}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
<path d="M0 -84 C-30 -44 -52 8 -32 86 M0 -84 C30 -44 52 8 32 86 M0 -88 V90" fill="none" stroke="{ONION_LINE}" stroke-width="4"/>
<path d="M-50 -2 C-52 26 -42 50 -26 62" fill="none" stroke="#F6D49A" stroke-width="9" stroke-linecap="round"/>
<path d="M-4 -92 q2 -20 -10 -36 M4 -92 q8 -16 4 -32" fill="none" stroke="#A0703A" stroke-width="7" stroke-linecap="round"/>"""
    return place(cx, cy, g(id_, body), s)


def knife(id_, x, y, s=1.0, r=0.0, sharp=True, flip=False):
    """Dao: cán ở gốc tọa độ, lưỡi chạy theo +x. flip lật ngang."""
    blade = "#DDE6EE" if sharp else "#A7B2BC"
    parts = f"""
<rect x="-170" y="-22" width="170" height="44" rx="16" fill="#6B4529" stroke="{INK}" stroke-width="{SW}"/>
<circle cx="-130" cy="0" r="6" fill="#D9C3A0" stroke="{INK}" stroke-width="3"/>
<circle cx="-82" cy="0" r="6" fill="#D9C3A0" stroke="{INK}" stroke-width="3"/>
<circle cx="-34" cy="0" r="6" fill="#D9C3A0" stroke="{INK}" stroke-width="3"/>
<path d="M10 -24 L250 -24 Q302 -20 322 8 L10 26 Z" fill="{blade}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
<rect x="-6" y="-28" width="18" height="56" rx="4" fill="{GREY}" stroke="{INK}" stroke-width="{SW}"/>"""
    if sharp:
        parts += f"""<path d="M24 18 L300 9" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
<g id="{id_}-spark"><path transform="translate(236 -6)" d="M0 -20 L5 -5 L20 0 L5 5 L0 20 L-5 5 L-20 0 L-5 -5 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/></g>"""
    else:
        parts += f"""<path d="M70 24 l9 -10 l9 9 Z M150 21 l8 -9 l8 8 Z M230 16 l7 -9 l8 8 Z" fill="{INK}"/>
<path d="M40 -8 L200 -10 M60 6 L180 4" stroke="#8D98A2" stroke-width="4" stroke-linecap="round"/>"""
    sc = f"scale({-s} {s})" if flip else (f"scale({s})" if s != 1 else "")
    t = f"translate({x} {y})" + (f" rotate({r})" if r else "") + (f" {sc}" if sc else "")
    return f'<g transform="{t}">{g(id_, parts)}</g>'


def clock(id_, cx, cy, r, hour=6.0, minute=0.0):
    """Đồng hồ vẽ ở tọa độ tuyệt đối để kim xoay quanh (cx, cy)."""
    ticks = "".join(
        f'<line x1="{cx}" y1="{cy - r + 14}" x2="{cx}" y2="{cy - r + (34 if k % 3 == 0 else 24)}" '
        f'stroke="{INK}" stroke-width="{6 if k % 3 == 0 else 4}" transform="rotate({k * 30} {cx} {cy})"/>'
        for k in range(12))
    ha = (hour % 12) * 30 + minute * 0.5
    ma = minute * 6
    return f"""<g id="{id_}">
<circle cx="{cx}" cy="{cy}" r="{r + 10}" fill="{WOOD}" stroke="{INK}" stroke-width="{SW}"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>
{ticks}
<g id="{id_}-h" transform="rotate({ha} {cx} {cy})"><line x1="{cx}" y1="{cy + 10}" x2="{cx}" y2="{cy - r * 0.5}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></g>
<g id="{id_}-m" transform="rotate({ma} {cx} {cy})"><line x1="{cx}" y1="{cy + 14}" x2="{cx}" y2="{cy - r * 0.78}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>
<circle cx="{cx}" cy="{cy}" r="9" fill="{CORAL}" stroke="{INK}" stroke-width="4"/>
</g>"""


def basket(id_, cx, cy, n=4, s=1.0):
    """Rổ hành: n củ hành ló lên trên miệng rổ, mỗi củ có id `<id>-o<k>`."""
    onions = "".join(onion(f"{id_}-o{k}", -105 + k * (210 / max(n - 1, 1)), -40 - (18 if k % 2 else 0), 0.55)
                     for k in range(n))
    weave = "".join(f'<path d="M{-150 + k * 50} -10 L{-120 + k * 40} 110" stroke="{ONION_LINE}" stroke-width="5"/>'
                    for k in range(7))
    body = f"""{onions}
<path d="M-170 -14 L170 -14 L130 112 Q0 130 -130 112 Z" fill="#C98A3E" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
{weave}
<path d="M-160 30 Q0 46 160 30 M-148 70 Q0 86 148 70" fill="none" stroke="#A86F2E" stroke-width="5"/>
<rect x="-182" y="-30" width="364" height="30" rx="15" fill="#D9A066" stroke="{INK}" stroke-width="{SW}"/>"""
    return place(cx, cy, g(id_, body), s)


def cutting_board(x, y, w=420, h=34):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#D9A066" stroke="{INK}" stroke-width="{SW}"/>'
            f'<circle cx="{x + w - 30}" cy="{y + h / 2}" r="8" fill="#A86F2E" stroke="{INK}" stroke-width="3"/>')


def gas_wisps(id_, pts, width=14):
    """Làn khí cay: các đường cong màu GAS, vẽ dần bằng stroke-dashoffset (pathLength = 1)."""
    paths = "".join(
        f'<path id="{id_}-{k}" d="{d}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" fill="none" '
        f'stroke="{GAS}" stroke-width="{width}" stroke-linecap="round"/>'
        for k, d in enumerate(pts))
    return g(id_, paths)


def gas_cloud(id_, cx, cy, s=1.0, label=None):
    body = f"""<path d="M-120 30 C-150 30 -158 -14 -122 -24 C-128 -66 -70 -82 -48 -52 C-34 -92 34 -92 46 -54 C74 -82 128 -62 118 -20 C156 -14 150 32 116 32 Z"
 fill="{GAS}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
<path d="M-80 -6 q10 -14 24 -8 M20 -30 q14 -10 26 0" fill="none" stroke="#A9C94A" stroke-width="5" stroke-linecap="round"/>"""
    if label:
        body += text(0, 14, label, 34, 800, INK, "middle")
    return place(cx, cy, g(id_, body), s)


def tear(id_, x, y, s=1.0):
    return place(x, y, g(id_, f'<path d="M0 -26 C10 -10 18 2 18 12 A18 18 0 0 1 -18 12 C-18 2 -10 -10 0 -26 Z" '
                              f'fill="{TEAR}" stroke="{INK}" stroke-width="4"/>'), s)


def sparkle(id_, x, y, s=1.0):
    return place(x, y, g(id_, f'<path d="M0 -24 L6 -6 L24 0 L6 6 L0 24 L-6 6 L-24 0 L-6 -6 Z" fill="#FFFFFF" '
                              f'stroke="{INK}" stroke-width="3"/>'), s)


def scissors(id_, x, y, s=1.0):
    body = f"""<path d="M-6 -6 L46 -34 M-6 6 L46 34" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
<path d="M-6 -6 L46 -34 M-6 6 L46 34" stroke="{GREY}" stroke-width="8" stroke-linecap="round"/>
<circle cx="-24" cy="-16" r="14" fill="none" stroke="{INK}" stroke-width="7"/>
<circle cx="-24" cy="16" r="14" fill="none" stroke="{INK}" stroke-width="7"/>
<circle cx="0" cy="0" r="5" fill="{INK}"/>"""
    return place(x, y, g(id_, body), s)


def molecule(id_, x, y, r=27):
    return place(x, y, g(id_, f'<circle r="{r}" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
                              + text(0, r * 0.42, "S", r * 1.1, 900, INK, "middle")))


def enzyme2(id_, x, y, s=1.0):
    body = (f'<path d="M0 -30 L26 -15 L26 15 L0 30 L-26 15 L-26 -15 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="5" '
            f'stroke-linejoin="round"/><path d="M-10 -4 L0 6 L12 -8" fill="none" stroke="{INK}" stroke-width="5" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')
    return place(x, y, g(id_, body), s)


def eye_side(id_, cx, cy, r=120):
    """Nhãn cầu nhìn nghiêng, giác mạc lồi về bên trái."""
    body = f"""<circle cx="0" cy="0" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="{SW}"/>
<path d="M{-r * 0.82} {-r * 0.55} Q{-r * 1.28} 0 {-r * 0.82} {r * 0.55}" fill="#DDF3FB" stroke="{INK}" stroke-width="{SW}"/>
<rect x="{-r * 0.86}" y="{-r * 0.42}" width="{r * 0.22}" height="{r * 0.84}" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>
<path d="M{r * 0.95} -10 C{r * 1.3} -14 {r * 1.5} 10 {r * 1.8} 6" fill="none" stroke="{PINK}" stroke-width="22" stroke-linecap="round"/>
<path d="M{-r * 0.2} {-r * 0.98} Q{r * 0.3} {-r * 1.12} {r * 0.7} {-r * 0.72}" fill="none" stroke="#F2C29B" stroke-width="26" stroke-linecap="round"/>
<path d="M{-r * 0.2} {-r * 0.98} Q{r * 0.3} {-r * 1.12} {r * 0.7} {-r * 0.72}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-dasharray="0"/>"""
    return place(cx, cy, g(id_, body))


def brain(id_, cx, cy, s=1.0):
    body = f"""<path d="M-100 20 C-120 -30 -80 -70 -40 -64 C-30 -96 30 -96 44 -64 C90 -76 122 -30 104 12 C120 50 70 80 30 66 C10 84 -40 84 -56 62 C-96 70 -120 50 -100 20 Z"
 fill="{PINK}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
<path d="M-60 -20 q20 -20 40 0 q20 20 40 0 M-70 22 q24 -16 48 4 q24 16 50 -6 M0 -60 q-10 30 6 60" fill="none" stroke="#D97F94" stroke-width="5" stroke-linecap="round"/>"""
    return place(cx, cy, g(id_, body), s)


def gland(id_, cx, cy, s=1.0):
    return place(cx, cy, g(id_, f'<ellipse rx="44" ry="24" fill="{PINK}" stroke="{INK}" stroke-width="5" transform="rotate(-20)"/>'
                                f'<path d="M-20 0 q10 -10 20 0 q10 10 20 0" fill="none" stroke="#D97F94" stroke-width="4"/>'), s)


def blade_tip(id_, cx, tip_y, sharp=True, h=420):
    """Mũi dao phóng đại nhìn ngang, mũi hướng xuống ở (cx, tip_y)."""
    if sharp:
        d = f"M{-26} {-h} L{26} {-h} L4 -4 Q0 2 -4 -4 Z"
        edge = f'<path d="M14 {-h} L2 -10" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
        fill = "#DDE6EE"
    else:
        d = f"M-150 {-h} L150 {-h} L44 -30 Q0 18 -44 -30 Z"
        edge = f'<path d="M-60 {-h * 0.6} L-20 -60" stroke="#8D98A2" stroke-width="5" stroke-linecap="round"/>'
        fill = "#A7B2BC"
    return place(cx, tip_y, g(id_, f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>{edge}'))


def cell_row(prefix, x, y, n=6, w=86, h=120, gap=6, skin=True):
    """Một hàng tế bào hành, mỗi tế bào id `<prefix>-<k>` (lớp phủ vỡ: `<prefix>-<k>-b`)."""
    out = []
    for k in range(n):
        cx = x + k * (w + gap)
        out.append(
            f'<g id="{prefix}-{k}"><rect x="{cx}" y="{y}" width="{w}" height="{h}" rx="22" fill="{CELL}" stroke="{INK}" stroke-width="5"/>'
            f'<rect id="{prefix}-{k}-b" x="{cx}" y="{y}" width="{w}" height="{h}" rx="22" fill="{CORAL}" stroke="{INK}" stroke-width="5" opacity="0"/>'
            f'<circle cx="{cx + w / 2}" cy="{y + h / 2}" r="12" fill="#D6DFA8"/></g>')
    if skin:
        out.append(f'<rect id="{prefix}-skin" x="{x - 10}" y="{y - 30}" width="{n * (w + gap) + 14}" height="30" rx="10" '
                   f'fill="{ONION}" stroke="{INK}" stroke-width="5"/>')
    return "".join(out)


def droplets(prefix, x, y, n=8, r=12):
    return "".join(f'<circle id="{prefix}-{k}" cx="{x}" cy="{y}" r="{r - (k % 3) * 3}" fill="{CELL}" stroke="{INK}" stroke-width="4" opacity="0"/>'
                   for k in range(n))


def option_row(prefix, x, y, letter, sharp, label):
    """Một phương án A/B/C: chữ cái lớn, con dao, nhãn cách cắt."""
    return g(prefix, f"""<rect id="{prefix}-box" x="{x - 30}" y="{y - 86}" width="1130" height="172" rx="28" fill="none" stroke="{YELLOW}" stroke-width="8" opacity="0"/>
{text(x + 50, y + 44, letter, 128, 900, YELLOW, "middle")}
{knife(prefix + "-k", x + 330, y, 0.8, 0, sharp)}
{text(x + 640, y + 18, label, 54, 800, WHITE)}
<line id="{prefix}-strike" x1="{x - 20}" y1="{y}" x2="{x + 1090}" y2="{y}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>""")


# ---------- khung cảnh ----------

def kitchen_back(p, hour=6.0, minute=0.0):
    tiles = "".join(f'<line x1="0" y1="{y}" x2="1920" y2="{y}" stroke="{TILE_LINE}" stroke-width="4"/>' for y in (560, 610, 660))
    tiles += "".join(f'<line x1="{x + (60 if row % 2 else 0)}" y1="{510 + row * 50}" x2="{x + (60 if row % 2 else 0)}" y2="{560 + row * 50}" '
                     f'stroke="{TILE_LINE}" stroke-width="4"/>' for row in range(4) for x in range(0, 1920, 120))
    jars = "".join(
        f'<rect x="{x}" y="{238 - hh}" width="70" height="{hh}" rx="12" fill="{c}" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="{x - 6}" y="{226 - hh}" width="82" height="18" rx="6" fill="{WOOD}" stroke="{INK}" stroke-width="5"/>'
        for x, hh, c in ((760, 90, "#F5F1E8"), (870, 120, "#E86A6A"), (980, 80, "#FFC145"), (1090, 104, TEAL)))
    return f"""<rect x="0" y="0" width="1920" height="1080" fill="{WALL}"/>
<rect x="0" y="510" width="1920" height="200" fill="{TILE}"/>{tiles}
<rect x="120" y="110" width="440" height="330" fill="{SKY}" stroke="{INK}" stroke-width="10"/>
<circle cx="440" cy="360" r="70" fill="#FFD27A"/>
<rect x="120" y="330" width="440" height="110" fill="#E9785A"/>
<path d="M340 110 V440 M120 270 H560" stroke="{INK}" stroke-width="12"/>
<rect x="100" y="436" width="480" height="26" rx="8" fill="{WOOD}" stroke="{INK}" stroke-width="{SW}"/>
<rect x="720" y="238" width="520" height="24" rx="8" fill="{WOOD}" stroke="{INK}" stroke-width="{SW}"/>{jars}
{clock(p + "-clock", 1620, 250, 110, hour, minute)}"""


def kitchen_front():
    drawers = "".join(f'<rect x="{x}" y="790" width="380" height="120" rx="14" fill="{WOOD_DARK}" stroke="{INK}" stroke-width="{SW}"/>'
                      f'<rect x="{x + 150}" y="836" width="80" height="20" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="4"/>'
                      for x in (80, 540, 1000, 1460))
    doors = "".join(f'<rect x="{x}" y="950" width="380" height="160" rx="14" fill="{WOOD_DARK}" stroke="{INK}" stroke-width="{SW}"/>'
                    for x in (80, 540, 1000, 1460))
    return f"""<rect x="-20" y="744" width="1960" height="360" fill="{WOOD}" stroke="{INK}" stroke-width="{SW}"/>{drawers}{doors}
<rect x="-20" y="700" width="1960" height="48" rx="6" fill="{WOOD_TOP}" stroke="{INK}" stroke-width="{SW}"/>"""


def slate_frame():
    return (f'<rect x="0" y="0" width="1920" height="1080" fill="{SLATE}"/>'
            f'<path d="M140 980 q30 -6 60 0 M1700 120 q40 -8 80 2 M1500 1000 q50 -6 90 0" stroke="#1D4262" stroke-width="10" stroke-linecap="round"/>')


def slate_border():
    return (f'<rect x="14" y="14" width="1892" height="1052" rx="20" fill="none" stroke="{WOOD}" stroke-width="28"/>'
            f'<rect x="28" y="28" width="1864" height="1024" rx="10" fill="none" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="0" y="0" width="1920" height="1080" fill="none" stroke="{INK}" stroke-width="6"/>')


def rice_cooker(id_, cx, cy, s=1.0):
    body = f"""<rect x="-120" y="-60" width="240" height="150" rx="50" fill="#F5F7FA" stroke="{INK}" stroke-width="{SW}"/>
<path d="M-110 -40 Q0 -120 110 -40 Z" fill="#DDE6EE" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
<rect x="-30" y="-100" width="60" height="22" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="5"/>
<rect x="-70" y="20" width="140" height="44" rx="12" fill="#C9D3DB" stroke="{INK}" stroke-width="5"/>
<circle id="{id_}-led" cx="-36" cy="42" r="10" fill="#6B7780" stroke="{INK}" stroke-width="4"/>
<rect x="-10" y="34" width="60" height="16" rx="6" fill="#6B7780"/>"""
    return place(cx, cy, g(id_, body), s)


def plate(id_, cx, cy, s=1.0):
    rings = "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="26" ry="12" fill="none" stroke="#F1E3C2" stroke-width="7"/>'
                    f'<ellipse cx="{dx}" cy="{dy}" rx="26" ry="12" fill="none" stroke="{INK}" stroke-width="2"/>'
                    for dx, dy in ((-40, -16), (6, -22), (44, -12), (-14, -6), (24, -4)))
    body = f'<ellipse cx="0" cy="0" rx="120" ry="34" fill="#FFFFFF" stroke="{INK}" stroke-width="{SW}"/>' \
           f'<ellipse cx="0" cy="-4" rx="84" ry="20" fill="#EEF2F5"/>{rings}'
    return place(cx, cy, g(id_, body), s)


def bell(id_, cx, cy, s=1.0):
    body = f"""<path d="M-50 40 C-50 -10 -40 -50 0 -54 C40 -50 50 -10 50 40 L62 56 L-62 56 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
<circle cx="0" cy="66" r="14" fill="{YELLOW}" stroke="{INK}" stroke-width="5"/>
<rect x="-8" y="-72" width="16" height="20" rx="6" fill="{YELLOW}" stroke="{INK}" stroke-width="5"/>"""
    return place(cx, cy, g(id_, body), s)


def fridge(id_, x, y, w=420, h=700):
    door_h = h * 0.36
    return g(id_, f"""<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="#E6EEF3" stroke="{INK}" stroke-width="{SW}"/>
<rect x="{x + 18}" y="{y + door_h + 18}" width="{w - 36}" height="{h - door_h - 36}" rx="16" fill="#CFE3EA" stroke="{INK}" stroke-width="5"/>
<line x1="{x + 18}" y1="{y + door_h + 170}" x2="{x + w - 18}" y2="{y + door_h + 170}" stroke="{INK}" stroke-width="6"/>
<line x1="{x + 18}" y1="{y + door_h + 320}" x2="{x + w - 18}" y2="{y + door_h + 320}" stroke="{INK}" stroke-width="6"/>
<path d="M{x + 60} {y + door_h + 60} l20 20 m0 -20 l-20 20 M{x + w - 80} {y + door_h + 250} l18 18 m0 -18 l-18 18" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
{onion(id_ + "-onion", x + w / 2, y + door_h + 250, 0.7)}
<rect x="{x}" y="{y}" width="{w}" height="{door_h}" rx="34" fill="#E6EEF3" stroke="{INK}" stroke-width="{SW}"/>
<rect x="{x + w - 70}" y="{y + 40}" width="22" height="{door_h - 80}" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="5"/>
<g id="{id_}-door"><rect x="{x}" y="{y + door_h}" width="{w}" height="{h - door_h}" rx="34" fill="#E6EEF3" stroke="{INK}" stroke-width="{SW}"/>
<rect x="{x + w - 70}" y="{y + door_h + 40}" width="22" height="160" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="5"/></g>""")


def medal(id_, cx, cy, s=1.0):
    body = f"""<path d="M-60 -220 L-14 -40 L14 -40 L60 -220 Z" fill="{CORAL}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
<path d="M-20 -220 L0 -60 L20 -220" fill="none" stroke="#FFFFFF" stroke-width="8"/>
<circle cx="0" cy="40" r="96" fill="{YELLOW}" stroke="{INK}" stroke-width="{SW}"/>
<circle cx="0" cy="40" r="70" fill="none" stroke="#E5A024" stroke-width="8"/>
{text(0, 28, "IG NOBEL", 30, 900, INK, "middle")}
{text(0, 74, "2013", 44, 900, INK, "middle")}"""
    return place(cx, cy, g(id_, body), s)


def switch(id_, cx, cy, s=1.0):
    body = f"""<rect x="-70" y="-110" width="140" height="220" rx="30" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>
<rect x="-34" y="-74" width="68" height="148" rx="20" fill="#C9D3DB" stroke="{INK}" stroke-width="5"/>
<g id="{id_}-lever"><rect x="-26" y="-68" width="52" height="66" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="5"/></g>
{text(0, -124, "GEN", 36, 900, WHITE, "middle")}"""
    return place(cx, cy, g(id_, body), s)
