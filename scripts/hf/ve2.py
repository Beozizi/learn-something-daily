"""Đồ vật bổ sung (tập 2 — nước): văn phòng, ly, chai, cơ thể, thận, cân, thang màu nước tiểu…

Cùng quy ước với ve.py: nhóm ngoài đặt vị trí, nhóm trong mang id để GSAP diễn hoạt.
"""
import math

from .ve import (INK, SW, PAPER, TEAL, GREY, YELLOW, GAS, CORAL, WHITE, WOOD, WOOD_TOP, place, g, text, clock)

WATER = "#4FB3E8"
WATER_DARK = "#2E86C1"
WATER_LIGHT = "#CDEEFC"
RED = "#E5484D"
DESK_FRONT = "#3B5C78"
URINE = ["#FBF6D6", "#F6EC9E", "#F0D76A", "#E2B53C", "#C4871E"]


def office_back(p, hour=7.0, minute=0.0):
    sky = (f'<rect x="120" y="100" width="560" height="360" fill="#8FD3F4" stroke="{INK}" stroke-width="10"/>'
           + "".join(f'<rect x="{x}" y="{460 - h}" width="{w}" height="{h}" fill="#5B7C99"/>'
                     for x, w, h in ((130, 90, 180), (230, 70, 250), (310, 110, 150), (430, 80, 220), (520, 150, 120)))
           + "".join(f'<rect x="{x}" y="{y}" width="14" height="18" fill="#FFE59A"/>'
                     for x, y in ((150, 320), (180, 360), (250, 260), (270, 330), (450, 280), (470, 340), (560, 380)))
           + f'<path d="M400 100 V460 M120 280 H680" stroke="{INK}" stroke-width="12"/>')
    board = (f'<rect x="1000" y="150" width="380" height="250" rx="12" fill="#F5F7FA" stroke="{INK}" stroke-width="{SW}"/>'
             f'<path d="M1040 340 L1110 280 L1170 310 L1240 220 L1330 250" fill="none" stroke="{TEAL}" stroke-width="10" '
             f'stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M1040 200 H1200 M1040 235 H1150" stroke="{GREY}" stroke-width="8" stroke-linecap="round"/>')
    plant = (f'<path d="M820 470 C780 400 760 360 800 330 M830 470 C840 390 880 360 900 340 M825 470 C810 420 830 380 850 360" '
             f'stroke="#2F9E6E" stroke-width="18" stroke-linecap="round" fill="none"/>'
             f'<path d="M790 470 H870 L858 540 H802 Z" fill="#E86A6A" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    return (f'<rect width="1920" height="1080" fill="#2A5674"/>'
            f'<rect x="0" y="540" width="1920" height="12" fill="#244B66"/>{sky}{board}{plant}'
            + clock(p + "-clock", 1620, 250, 110, hour, minute))


def office_front():
    return (f'<rect x="-20" y="744" width="1960" height="360" fill="{DESK_FRONT}" stroke="{INK}" stroke-width="{SW}"/>'
            + "".join(f'<rect x="{x}" y="800" width="500" height="230" rx="16" fill="#335270" stroke="{INK}" stroke-width="{SW}"/>'
                      for x in (120, 1300))
            + f'<rect x="-20" y="700" width="1960" height="48" rx="6" fill="#D8C3A5" stroke="{INK}" stroke-width="{SW}"/>')


def laptop(id_, cx, cy, s=1.0):
    body = (f'<rect x="-170" y="-230" width="340" height="230" rx="16" fill="#C9D3DB" stroke="{INK}" stroke-width="{SW}"/>'
            f'<circle cx="0" cy="-118" r="22" fill="#F5F7FA" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-200 0 H200 L180 22 H-180 Z" fill="#9FB3C8" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    return place(cx, cy, g(id_, body), s)


def coffee_cup(id_, cx, cy, s=1.0):
    body = (f'<path d="M58 -40 C96 -40 96 20 52 18" fill="none" stroke="{INK}" stroke-width="14"/>'
            f'<path d="M58 -40 C96 -40 96 20 52 18" fill="none" stroke="#F5F7FA" stroke-width="6"/>'
            f'<path d="M-62 -66 H62 L50 40 Q0 56 -50 40 Z" fill="#F5F7FA" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<ellipse cx="0" cy="-64" rx="58" ry="12" fill="#7A4A2A" stroke="{INK}" stroke-width="4"/>'
            f'<g id="{id_}-steam"><path d="M-20 -90 q-14 -20 0 -40 q14 -20 0 -40 M20 -90 q-14 -20 0 -40" fill="none" '
            f'stroke="#DDE6EE" stroke-width="8" stroke-linecap="round"/></g>')
    return place(cx, cy, g(id_, body), s)


def bottle(id_, cx, cy, s=1.0, level=0.85):
    shape = "M-55 -150 C-55 -190 -30 -200 -30 -230 H30 C30 -200 55 -190 55 -150 V100 Q0 120 -55 100 Z"
    top = max(-230 + 340 * (1 - level), -150)
    body = (f'<clipPath id="{id_}-clip"><path d="{shape}"/></clipPath>'
            f'<path d="{shape}" fill="{WATER_LIGHT}"/>'
            f'<g clip-path="url(#{id_}-clip)"><rect id="{id_}-water" x="-60" y="{top}" width="120" height="300" fill="{WATER}"/></g>'
            f'<path d="{shape}" fill="none" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M-34 -120 V60" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity=".7"/>'
            f'<rect x="-48" y="-40" width="96" height="70" rx="8" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
            f'<g id="{id_}-cap"><rect x="-36" y="-268" width="72" height="42" rx="10" fill="{WATER_DARK}" stroke="{INK}" stroke-width="{SW}"/></g>')
    return place(cx, cy, g(id_, body), s)


def glass(id_, cx, cy, s=1.0, level=0.75):
    """Ly nước: miệng rộng 200, đáy 150, cao 260 (gốc ở đáy giữa). Nhóm `<id>-water` là phần nước."""
    yt = -260 * level
    xt = 75 + 25 * level
    body = (f'<path d="M-100 -260 L-75 0 H75 L100 -260 Z" fill="#EAF6FD"/>'
            f'<g id="{id_}-water"><path d="M{-xt + 4} {yt} L-71 -4 H71 L{xt - 4} {yt} Z" fill="{WATER}"/>'
            f'<path d="M{-xt + 4} {yt} Q{-xt / 2} {yt - 12} 0 {yt} Q{xt / 2} {yt + 12} {xt - 4} {yt}" fill="none" '
            f'stroke="{WATER_DARK}" stroke-width="5"/></g>'
            f'<path d="M-100 -260 L-75 0 H75 L100 -260" fill="none" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M-70 -230 L-55 -30" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity=".8"/>')
    return place(cx, cy, g(id_, body), s)


def person_fill(id_, cx, cy, h=700, level=0.6):
    """Hình bóng người đổ nước tới `level` (0–1 theo chiều cao). Nhóm `<id>-water` dịch dọc để đổi mực nước:
    dịch y = -h·Δlevel (trong hệ tọa độ 700 đơn vị: -700·Δlevel)."""
    k = h / 700
    sil = ("M0 0 m-60 0 a60 60 0 1 0 120 0 a60 60 0 1 0 -120 0 Z "
           "M-110 150 Q-110 110 -60 110 H60 Q110 110 110 150 L130 420 Q132 445 106 445 H80 L70 690 Q68 700 50 700 H18 "
           "Q4 700 2 690 L0 520 L-2 690 Q-4 700 -18 700 H-50 Q-68 700 -70 690 L-80 445 H-106 Q-132 445 -130 420 Z")
    wy = 760 - 820 * level
    wave = f"M-220 {wy} Q-165 {wy - 18} -110 {wy} T0 {wy} T110 {wy} T220 {wy} V900 H-220 Z"
    body = (f'<clipPath id="{id_}-clip"><path d="{sil}"/></clipPath>'
            f'<path d="{sil}" fill="#1D4262"/>'
            f'<g clip-path="url(#{id_}-clip)"><g id="{id_}-water"><path d="{wave}" fill="{WATER}"/></g></g>'
            f'<path d="{sil}" fill="none" stroke="{WHITE}" stroke-width="7" stroke-linejoin="round"/>')
    return f'<g transform="translate({cx} {cy - h / 2 + 60 * k}) scale({k})">{g(id_, body)}</g>'


def heart(id_, cx, cy, s=1.0):
    body = (f'<path d="M0 60 C-90 0 -110 -50 -80 -80 C-50 -110 -10 -90 0 -60 C10 -90 50 -110 80 -80 C110 -50 90 0 0 60 Z" '
            f'fill="{RED}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M-60 -60 q12 -16 30 -10" fill="none" stroke="#FF9A9D" stroke-width="8" stroke-linecap="round"/>')
    return place(cx, cy, g(id_, body), s)


def sun(id_, cx, cy, s=1.0):
    rays = "".join(f'<line x1="0" y1="-78" x2="0" y2="-108" stroke="{YELLOW}" stroke-width="12" stroke-linecap="round" '
                   f'transform="rotate({a})"/>' for a in range(0, 360, 45))
    return place(cx, cy, g(id_, rays + f'<circle r="60" fill="{YELLOW}" stroke="{INK}" stroke-width="{SW}"/>'), s)


def thermometer(id_, cx, cy, s=1.0, level=0.5):
    body = (f'<rect x="-22" y="-160" width="44" height="190" rx="22" fill="#F5F7FA" stroke="{INK}" stroke-width="{SW}"/>'
            f'<rect id="{id_}-hg" x="-10" y="{20 - 170 * level}" width="20" height="{170 * level + 20}" rx="10" fill="{RED}"/>'
            f'<circle cx="0" cy="44" r="40" fill="{RED}" stroke="{INK}" stroke-width="{SW}"/>')
    return place(cx, cy, g(id_, body), s)


def pictogram(id_, cx, cy, s=1.0, kind="run", color=WHITE):
    """Người tượng hình: run (chạy), stand, preg (mang thai), elder (chống gậy)."""
    st = f'stroke="{color}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    extra = ""
    if kind == "run":
        lim, head = "M10 -40 L-20 30 L-60 60 M-20 30 L20 70 L10 120 M0 -20 L-50 0 M0 -20 L40 -50 L70 -30", (20, -80)
    elif kind == "preg":
        lim, head = "M0 -40 V60 M0 60 L-20 130 M0 60 L20 130 M0 -20 L-40 30 M0 -20 L40 20", (0, -80)
        extra = f'<path d="M6 -10 Q64 22 6 60" fill="{color}" stroke="{color}" stroke-width="8"/>'
    elif kind == "elder":
        lim, head = "M-10 -40 Q0 0 -6 60 M-6 60 L-30 130 M-6 60 L16 130 M-4 -20 L40 20 M40 20 L46 130", (-20, -78)
    else:
        lim, head = "M0 -40 V60 M0 60 L-24 130 M0 60 L24 130 M0 -20 L-44 30 M0 -20 L44 30", (0, -80)
    body = f'<path d="{lim}" {st}/><circle cx="{head[0]}" cy="{head[1]}" r="26" fill="{color}"/>{extra}'
    return place(cx, cy, g(id_, body), s)


def kidney(id_, cx, cy, s=1.0, flip=False):
    sc = f"scale({-s} {s})" if flip else f"scale({s})"
    body = (f'<path d="M20 -110 C90 -120 120 -40 110 20 C100 90 50 130 0 110 C-30 98 -20 60 -40 40 C-60 20 -90 10 -80 -40 '
            f'C-70 -90 -20 -104 20 -110 Z" fill="#D9706B" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M-30 30 C-10 0 -10 -30 -40 -50" fill="none" stroke="#B2504C" stroke-width="10" stroke-linecap="round"/>')
    return f'<g transform="translate({cx} {cy}) {sc}">{g(id_, body)}</g>'


def bathtub(id_, cx, cy, s=1.0):
    body = (f'<path d="M-230 -40 H230 V20 Q230 110 140 110 H-140 Q-230 110 -230 20 Z" fill="#F5F7FA" stroke="{INK}" '
            f'stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<rect x="-214" y="-32" width="428" height="30" rx="8" fill="{WATER}"/>'
            f'<path d="M-160 110 V140 M160 110 V140" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
            f'<rect x="-250" y="-60" width="500" height="26" rx="13" fill="#DDE6EE" stroke="{INK}" stroke-width="{SW}"/>')
    return place(cx, cy, g(id_, body), s)


def gauge(id_, cx, cy, r=120, label=None, label_color=WHITE):
    """Đồng hồ bán nguyệt vẽ ở tọa độ tuyệt đối; kim `<id>-n` xoay quanh (cx, cy): 0° thẳng đứng, ±90° hai đầu."""
    def arc(a0, a1, col):
        x0, y0 = cx + r * math.cos(math.radians(180 + a0)), cy + r * math.sin(math.radians(180 + a0))
        x1, y1 = cx + r * math.cos(math.radians(180 + a1)), cy + r * math.sin(math.radians(180 + a1))
        return f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="26"/>'
    body = (f'<path d="M{cx - r - 26} {cy} A{r + 26} {r + 26} 0 0 1 {cx + r + 26} {cy} Z" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>'
            + arc(6, 110, TEAL) + arc(110, 145, YELLOW) + arc(145, 174, CORAL)
            + f'<g id="{id_}-n"><path d="M{cx - 9} {cy} L{cx} {cy - r + 6} L{cx + 9} {cy} Z" fill="{INK}"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="14" fill="{INK}"/>')
    if label:
        body += text(cx, cy + 56, label, 34, 800, label_color, "middle")
    return g(id_, body)


def balance(id_, cx, cy, s=1.0, left="", right=""):
    """Cân đĩa: đòn `<id>-beam` xoay quanh trục (0, 0); đĩa `<id>-L`, `<id>-R`.
    left/right: SVG đặt lên đĩa, tọa độ tương đối tâm mặt đĩa (đáy đồ vật ở y = 0)."""
    def pan(side, x):
        items = left if side == "L" else right
        return (f'<g id="{id_}-{side}"><path d="M{x} 0 L{x - 120} 170 M{x} 0 L{x + 120} 170" stroke="{INK}" stroke-width="5"/>'
                f'<g transform="translate({x} 170)">{items}</g>'
                f'<path d="M{x - 160} 170 H{x + 160} Q{x + 140} 232 {x} 232 Q{x - 140} 232 {x - 160} 170 Z" fill="{YELLOW}" '
                f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/></g>')
    body = (f'<path d="M-30 420 H30 L16 0 H-16 Z" fill="{WOOD}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<rect x="-180" y="410" width="360" height="40" rx="14" fill="{WOOD}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<g id="{id_}-beam"><rect x="-460" y="-14" width="920" height="28" rx="14" fill="{WOOD_TOP}" stroke="{INK}" stroke-width="{SW}"/>'
            f'{pan("L", -440)}{pan("R", 440)}</g>'
            f'<circle r="24" fill="{YELLOW}" stroke="{INK}" stroke-width="{SW}"/>')
    return place(cx, cy, g(id_, body), s)


def lamp(id_, cx, cy, color, r=40):
    return place(cx, cy, g(id_, f'<circle r="{r}" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<circle cx="{-r * 0.3}" cy="{-r * 0.3}" r="{r * 0.25}" fill="#FFFFFF" opacity=".7"/>'))


def report1945(id_, x, y, words=("≈ 2,5 LÍT / NGÀY", "PHẦN LỚN ĐÃ CÓ", "SẴN TRONG THỨC ĂN")):
    lines = "".join(f'<rect x="{x + 50}" y="{y + 150 + k * 46}" width="{300 - (k % 3) * 60}" height="14" rx="7" fill="#C9BFA8"/>'
                    for k in range(3))
    return g(id_, f"""<path d="M{x} {y} H{x + 380} L{x + 440} {y + 60} V{y + 560} H{x} Z" fill="#F1E6C8" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
<path d="M{x + 380} {y} V{y + 60} H{x + 440}" fill="#D9CBA4" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>
{text(x + 50, y + 100, "1945", 64, 900, INK)}{lines}
<rect id="{id_}-hl1" x="{x + 36}" y="{y + 298}" width="372" height="62" rx="10" fill="{YELLOW}" opacity="0"/>
{text(x + 52, y + 342, words[0], 38, 900, INK)}
<rect id="{id_}-hl2" x="{x + 36}" y="{y + 392}" width="372" height="110" rx="10" fill="{GAS}" opacity="0"/>
{text(x + 52, y + 434, words[1], 34, 900, "#5E5340")}
{text(x + 52, y + 480, words[2], 34, 900, "#5E5340")}""")


def magnifier(id_, cx, cy, s=1.0):
    body = (f'<path d="M60 60 L150 150" stroke="{INK}" stroke-width="40" stroke-linecap="round"/>'
            f'<path d="M60 60 L150 150" stroke="{WOOD}" stroke-width="26" stroke-linecap="round"/>'
            f'<circle r="90" fill="#DDF3FB" fill-opacity=".45" stroke="{INK}" stroke-width="16"/>'
            f'<path d="M-50 -30 a60 60 0 0 1 40 -30" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>')
    return place(cx, cy, g(id_, body), s)


def watermelon(id_, cx, cy, s=1.0):
    seeds = "".join(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="10" fill="{INK}"/>'
                    for x, y in ((-60, 30), (-20, 50), (20, 50), (60, 30), (-30, 14), (30, 14)))
    body = (f'<path d="M-120 0 A120 120 0 0 0 120 0 Z" fill="#2F9E6E" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M-104 0 A104 104 0 0 0 104 0 Z" fill="#F5F7FA"/>'
            f'<path d="M-94 0 A94 94 0 0 0 94 0 Z" fill="#F2575C"/>{seeds}'
            f'<path d="M-120 0 H120" stroke="{INK}" stroke-width="{SW}"/>')
    return place(cx, cy, g(id_, body), s)


def bowl(id_, cx, cy, s=1.0, fill="#F7D774", steam=True, rice=False):
    top = (f'<ellipse cx="0" cy="-10" rx="120" ry="26" fill="{fill}" stroke="{INK}" stroke-width="5"/>' if not rice else
           f'<path d="M-118 -10 Q-100 -80 0 -84 Q100 -80 118 -10 Z" fill="#F5F7FA" stroke="{INK}" stroke-width="5"/>')
    body = (top + f'<path d="M-130 -10 H130 Q120 90 0 96 Q-120 90 -130 -10 Z" fill="#E6EEF3" stroke="{INK}" stroke-width="{SW}" '
                  f'stroke-linejoin="round"/><path d="M-100 30 H100" stroke="{TEAL}" stroke-width="10"/>')
    if steam:
        body += (f'<path d="M-30 -50 q-14 -20 0 -40 q14 -20 0 -40 M30 -50 q-14 -20 0 -40" fill="none" stroke="#DDE6EE" '
                 f'stroke-width="8" stroke-linecap="round"/>')
    return place(cx, cy, g(id_, body), s)


def urine_scale(id_, x, y, w=140, h=180, gap=18):
    return g(id_, "".join(
        f'<g id="{id_}-{k}"><rect x="{x + k * (w + gap)}" y="{y}" width="{w}" height="{h}" rx="24" fill="{c}" '
        f'stroke="{INK}" stroke-width="{SW}"/></g>' for k, c in enumerate(URINE)))


def stone(id_, cx, cy, s=1.0):
    body = (f'<path d="M-70 -20 L-40 -70 L10 -60 L40 -90 L80 -40 L70 10 L90 50 L30 80 L-20 60 L-70 70 L-90 20 Z" '
            f'fill="#B8A88A" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M-30 -20 l20 10 M20 -30 l10 20 M10 40 l-20 -6" stroke="#8A7B60" stroke-width="7" stroke-linecap="round"/>')
    return place(cx, cy, g(id_, body), s)


def person_icon(id_, cx, cy, s=1.0, color=WHITE):
    return place(cx, cy, g(id_, f'<circle cy="-34" r="16" fill="{color}"/>'
                                f'<path d="M-24 34 V0 Q-24 -12 0 -12 Q24 -12 24 0 V34 Z" fill="{color}"/>'), s)


def wc_door(id_, x, y):
    return g(id_, f"""<rect x="{x}" y="{y}" width="260" height="560" rx="10" fill="#7A5233" stroke="{INK}" stroke-width="{SW}"/>
<circle cx="{x + 220}" cy="{y + 300}" r="14" fill="{YELLOW}" stroke="{INK}" stroke-width="4"/>
<rect x="{x + 60}" y="{y + 60}" width="140" height="80" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>
{text(x + 130, y + 118, "WC", 52, 900, INK, "middle")}""")


def bubble(id_, cx, cy, w, h, label, color=PAPER, txt=INK, size=56):
    """Bong bóng lời khuyên bo tròn có đuôi nhỏ."""
    body = (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M{-w / 4} {h / 2 - 3} l-24 40 l50 -40 Z" fill="{color}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<rect x="{-w / 4 - 30}" y="{h / 2 - 12}" width="64" height="14" fill="{color}"/>'
            + text(0, size * 0.36, label, size, 900, txt, "middle"))
    return place(cx, cy, g(id_, body))
