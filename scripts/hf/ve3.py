"""Đồ vật SVG bổ sung (tập Why we sleep): trăng, Zzz, sóng não, bình chứa, thụ thể, biểu đồ giấc ngủ,
hộp thư / tủ hồ sơ, tế bào não, virus, lá chắn, ống tiêm, kháng thể, ô tô, pin, biển báo.
Mọi hàm trả về chuỗi SVG; id_ dùng cho GSAP. Vẽ quanh (0, 0) rồi đặt bằng place() khi có tham số cx, cy.
"""
from .ve import INK, SW, PAPER, YELLOW, CORAL, TEAL, WHITE, GREY, WOOD, PINK, place, g, text

NIGHT = "#2B3F7A"
MOON = "#FFE9A8"
WATERB = "#4FB3E8"


def moon(id_, cx, cy, s=1.0):
    return place(cx, cy, g(id_, f'<path d="M30 -70 A80 80 0 1 0 60 50 A64 64 0 1 1 30 -70 Z" fill="{MOON}" stroke="{INK}" stroke-width="{SW}" '
                                f'stroke-linejoin="round"/>'), s)


def zzz(id_, x, y, s=1.0, color=WHITE):
    zs = "".join(text(k * 46, -k * 52, "Z", 56 - k * 10, 900, color, "middle", id_=f"{id_}-{k}") for k in range(3))
    return place(x, y, g(id_, zs), s)


def wave(id_, x, y, w, amp, period, color=TEAL, width=8):
    """Đường sóng điện não từ (x, y) dài w; pathLength=1 để vẽ dần bằng c.draw()."""
    n = max(int(w / period * 8), 8)
    pts = []
    import math
    for k in range(n + 1):
        px = x + w * k / n
        py = y - amp * math.sin(2 * math.pi * (px - x) / period) * (1 if k % 3 else 0.85)
        pts.append(f"{px:.1f} {py:.1f}")
    return (f'<path id="{id_}" d="M{" L".join(pts)}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')


def tank(id_, x, y, w, h, color, label="", level=0.0):
    """Bình chứa: #id_-fill co giãn theo scaleY (gốc đáy) để đầy/vơi."""
    lv = h * level
    return g(id_, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="#1D4262" stroke="{INK}" stroke-width="{SW}"/>'
                  f'<g id="{id_}-fill"><rect x="{x + 10}" y="{y + 10}" width="{w - 20}" height="{h - 20}" rx="18" fill="{color}"/></g>'
                  f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="none" stroke="{INK}" stroke-width="{SW}"/>'
                  + (text(x + w / 2, y + h + 60, label, 40, 900, color, "middle") if label else ""))


def receptor(id_, cx, cy, s=1.0):
    """Thụ thể (ổ cắm hình chữ U) trên màng tế bào."""
    return place(cx, cy, g(id_, f'<path d="M-70 0 V-60 H-34 V-24 A34 34 0 0 0 34 -24 V-60 H70 V0 Z" fill="{PINK}" stroke="{INK}" '
                                f'stroke-width="{SW}" stroke-linejoin="round"/>'), s)


def adenosine(id_, cx, cy, s=1.0):
    return place(cx, cy, g(id_, f'<circle r="30" fill="{YELLOW}" stroke="{INK}" stroke-width="{SW}"/>'
                                + text(0, 12, "A", 34, 900, INK, "middle")), s)


def caffeine(id_, cx, cy, s=1.0):
    hexa = "M0 -34 L30 -17 L30 17 L0 34 L-30 17 L-30 -17 Z"
    return place(cx, cy, g(id_, f'<path d="{hexa}" fill="#8B5A3C" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                                + text(0, 12, "C", 32, 900, WHITE, "middle")), s)


# Biểu đồ giấc ngủ 8 giờ: mức 0 = thức, 1 = REM, 2 = N1/N2, 3 = ngủ sâu. (giờ bắt đầu, mức)
HYPNO = [(0, 0), (0.15, 2), (0.4, 3), (1.1, 2), (1.35, 1), (1.5, 2), (1.8, 3), (2.4, 2), (2.85, 1), (3.1, 2), (3.4, 3), (3.7, 2),
         (4.3, 1), (4.75, 2), (5.3, 1), (5.9, 2), (6.4, 1), (7.3, 2), (7.6, 1), (7.95, 0)]


def hypnogram(id_, x, y, w, h):
    """Đường bậc thang (vẽ dần) + dải REM (#id_-rem{k}) + dải ngủ sâu (#id_-deep{k})."""
    lv = lambda m: y + h * m / 3
    hx = lambda t: x + w * t / 8
    d, rem, deep = [], [], []
    for k, (t, m) in enumerate(HYPNO):
        t1 = HYPNO[k + 1][0] if k + 1 < len(HYPNO) else 8
        d.append(f"{'M' if k == 0 else 'L'}{hx(t):.0f} {lv(m):.0f} L{hx(t1):.0f} {lv(m):.0f}")
        if m == 1:
            rem.append(f'<rect id="{id_}-rem{len(rem)}" x="{hx(t):.0f}" y="{lv(1) - 18:.0f}" width="{hx(t1) - hx(t):.0f}" height="36" rx="10" fill="{CORAL}" opacity=".9"/>')
        if m == 3:
            deep.append(f'<rect id="{id_}-deep{len(deep)}" x="{hx(t):.0f}" y="{lv(3) - 18:.0f}" width="{hx(t1) - hx(t):.0f}" height="36" rx="10" fill="{WATERB}" opacity=".9"/>')
    axis = "".join(text(x - 24, lv(m) + 12, lb, 30, 800, GREY, "end") for m, lb in ((0, "AWAKE"), (1, "REM"), (2, "LIGHT"), (3, "DEEP")))
    hours = "".join(text(hx(t), y + h + 56, f"{t}h", 28, 700, GREY, "middle") for t in range(0, 9, 2))
    return g(id_, axis + hours + "".join(deep) + "".join(rem)
             + f'<path id="{id_}-line" d="{" ".join(d)}" fill="none" stroke="{WHITE}" stroke-width="8" stroke-linejoin="round" '
               f'pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')


def hypno_x(x, w, t):
    return x + w * t / 8


def inbox(id_, cx, cy, s=1.0, label="HIPPOCAMPUS"):
    return place(cx, cy, g(id_, f'<path d="M-130 -20 L-100 60 H100 L130 -20 Z" fill="{WOOD}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                                f'<rect x="-130" y="-34" width="260" height="20" rx="8" fill="#9C6B43" stroke="{INK}" stroke-width="5"/>'
                                + text(0, 120, label, 34, 900, YELLOW, "middle")), s)


def cabinet(id_, cx, cy, s=1.0, label="CORTEX"):
    drawers = "".join(f'<rect x="-110" y="{-150 + k * 100}" width="220" height="86" rx="10" fill="#C9D6E3" stroke="{INK}" stroke-width="5"/>'
                      f'<rect x="-30" y="{-112 + k * 100}" width="60" height="12" rx="6" fill="{INK}"/>' for k in range(3))
    return place(cx, cy, g(id_, f'<rect x="-130" y="-170" width="260" height="330" rx="16" fill="#8FA6BD" stroke="{INK}" stroke-width="{SW}"/>'
                                + drawers + text(0, 220, label, 34, 900, YELLOW, "middle")), s)


def card(id_, cx, cy, s=1.0, color=YELLOW):
    return place(cx, cy, g(id_, f'<rect x="-44" y="-30" width="88" height="60" rx="8" fill="{color}" stroke="{INK}" stroke-width="5"/>'
                                f'<path d="M-28 -10 H28 M-28 6 H14" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'), s)


def cell(id_, cx, cy, r=70, color="#E9C9E0"):
    return (f'<g id="{id_}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<circle cx="{cx - r * 0.2:.0f}" cy="{cy - r * 0.15:.0f}" r="{r * 0.28:.0f}" fill="#B27BA6" stroke="{INK}" stroke-width="4"/></g>')


def junk(id_, cx, cy, s=1.0):
    return place(cx, cy, g(id_, f'<path d="M-16 -10 L-4 -18 L14 -12 L18 4 L4 16 L-14 10 Z" fill="#B5A642" stroke="{INK}" stroke-width="4" '
                                f'stroke-linejoin="round"/>'), s)


def virus(id_, cx, cy, s=1.0, color="#7ED957"):
    spikes = "".join(f'<g transform="rotate({k * 45})"><line x1="0" y1="-40" x2="0" y2="-62" stroke="{INK}" stroke-width="6"/>'
                     f'<circle cy="-66" r="9" fill="{color}" stroke="{INK}" stroke-width="4"/></g>' for k in range(8))
    return place(cx, cy, g(id_, spikes + f'<circle r="42" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<circle cx="-12" cy="-8" r="7" fill="{INK}"/><circle cx="14" cy="6" r="5" fill="{INK}"/>'), s)


def shield(id_, cx, cy, s=1.0, color=TEAL):
    return place(cx, cy, g(id_, f'<path d="M0 -110 L90 -76 V0 C90 60 40 100 0 120 C-40 100 -90 60 -90 0 V-76 Z" fill="{color}" '
                                f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                                f'<path d="M-36 6 L-8 36 L42 -26" fill="none" stroke="{WHITE}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'), s)


def syringe(id_, cx, cy, s=1.0, r=-35):
    return place(cx, cy, g(id_, f'<rect x="-90" y="-22" width="140" height="44" rx="8" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<rect x="-84" y="-16" width="80" height="32" rx="4" fill="{WATERB}"/>'
                                f'<rect x="-130" y="-8" width="40" height="16" fill="{GREY}" stroke="{INK}" stroke-width="4"/>'
                                f'<rect x="-146" y="-26" width="16" height="52" rx="4" fill="{GREY}" stroke="{INK}" stroke-width="4"/>'
                                f'<line x1="50" y1="0" x2="120" y2="0" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'), s, r)


def antibody(id_, cx, cy, s=1.0, color=YELLOW):
    return place(cx, cy, g(id_, f'<path d="M0 40 V-4 M0 -4 L-30 -40 M0 -4 L30 -40" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>'
                                f'<path d="M0 40 V-4 M0 -4 L-30 -40 M0 -4 L30 -40" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round"/>'), s)


def car(id_, cx, cy, s=1.0, color=CORAL):
    return place(cx, cy, g(id_, f'<path d="M-150 20 V-20 Q-140 -40 -100 -44 L-60 -90 H50 L100 -44 Q146 -40 150 -10 V20 Z" fill="{color}" '
                                f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
                                f'<path d="M-50 -78 H-6 V-46 H-80 Z M8 -78 H44 L80 -46 H8 Z" fill="#CFE8F7" stroke="{INK}" stroke-width="4"/>'
                                f'<circle cx="-90" cy="24" r="32" fill="{INK}"/><circle cx="-90" cy="24" r="12" fill="{GREY}"/>'
                                f'<circle cx="90" cy="24" r="32" fill="{INK}"/><circle cx="90" cy="24" r="12" fill="{GREY}"/>'), s)


def battery(id_, cx, cy, s=1.0, level=0.2, color=CORAL):
    w = 150 * level
    return place(cx, cy, g(id_, f'<rect x="-90" y="-46" width="180" height="92" rx="14" fill="none" stroke="{WHITE}" stroke-width="10"/>'
                                f'<rect x="94" y="-18" width="16" height="36" rx="4" fill="{WHITE}"/>'
                                f'<rect x="-75" y="-31" width="{w:.0f}" height="62" rx="6" fill="{color}"/>'), s)


def sign(id_, cx, cy, label, w=420, color=YELLOW, size=50, txt=INK):
    return place(cx, cy, g(id_, f'<line x1="0" y1="40" x2="0" y2="180" stroke="{WOOD}" stroke-width="18"/>'
                                f'<rect x="{-w / 2}" y="-50" width="{w}" height="100" rx="18" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
                                + text(0, size * 0.36, label, size, 900, txt, "middle")))


def pie_third(id_, cx, cy, r=170):
    """Hình tròn ngày đêm: 2/3 vàng (THỨC), 1/3 xanh đêm (NGỦ) — #id_-night để pop riêng."""
    import math
    a = 2 * math.pi / 3
    x1, y1 = cx + r * math.sin(a), cy - r * math.cos(a)
    return g(id_, f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{YELLOW}" stroke="{INK}" stroke-width="{SW}"/>'
                  f'<path id="{id_}-night" d="M{cx} {cy} L{cx} {cy - r} A{r} {r} 0 0 1 {x1:.0f} {y1:.0f} Z" fill="{NIGHT}" '
                  f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')


def flu_bar(id_, x, base, h, w, color, label):
    return g(id_, f'<rect id="{id_}-r" x="{x - w / 2}" y="{base - h}" width="{w}" height="{h}" rx="16" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
                  + text(x, base + 56, label, 34, 800, WHITE, "middle"))


def power_switch(id_, cx, cy, s=1.0, on=False):
    """Công tắc gạt (không chữ): nút ở dưới = tắt."""
    ky = -34 if on else 34
    return place(cx, cy, g(id_, f'<rect x="-56" y="-96" width="112" height="192" rx="22" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<rect x="-30" y="-66" width="60" height="132" rx="14" fill="#C9D6E3" stroke="{INK}" stroke-width="5"/>'
                                f'<rect x="-26" y="{ky - 28}" width="52" height="56" rx="12" fill="{CORAL if not on else TEAL}" stroke="{INK}" stroke-width="5"/>'), s)


# ---------------------------------------------------------------- tập Why can't you focus
def phone(id_, cx, cy, s=1.0, buzz=True, screen="#CFE8F7"):
    """Điện thoại; #id_-bz là các vạch rung (ẩn/hiện riêng)."""
    bz = (f'<g id="{id_}-bz">' + "".join(f'<path d="M{sx * 70} -40 q{sx * 14} 20 0 40 M{sx * 88} -56 q{sx * 22} 36 0 72" fill="none" '
                                          f'stroke="{YELLOW}" stroke-width="7" stroke-linecap="round"/>' for sx in (-1, 1)) + '</g>') if buzz else ""
    return place(cx, cy, g(id_, f'<rect x="-46" y="-86" width="92" height="172" rx="16" fill="{INK}" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<rect x="-38" y="-72" width="76" height="140" rx="8" fill="{screen}"/>'
                                f'<circle cy="76" r="5" fill="{GREY}"/>' + bz), s)


def notif(id_, cx, cy, label, w=420):
    return place(cx, cy, g(id_, f'<rect x="{-w / 2}" y="-44" width="{w}" height="88" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<rect x="{-w / 2 + 16}" y="-26" width="52" height="52" rx="12" fill="{CORAL}"/>'
                                + text(-w / 2 + 88, 12, label, 32, 800, INK, "start")))


def fishbowl(id_, cx, cy, s=1.0):
    return place(cx, cy, g(id_, f'<path d="M-120 -110 H120 Q190 0 120 130 H-120 Q-190 0 -120 -110 Z" fill="#CFE8F7" stroke="{INK}" stroke-width="{SW}" opacity=".95"/>'
                                f'<path d="M-150 -20 Q0 -40 150 -20 V100 Q0 140 -150 100 Z" fill="{WATERB}" opacity=".55"/>'
                                f'<g id="{id_}-fish"><path d="M-40 30 Q0 -10 40 30 Q0 70 -40 30 Z M40 30 L70 5 L70 55 Z" fill="#FF9F43" '
                                f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><circle cx="-18" cy="24" r="5" fill="{INK}"/></g>'), s)


def spotlight(id_, x, y, tx, ty, w=220, color=YELLOW):
    """Đèn rọi từ (x, y) chiếu tới vùng quanh (tx, ty)."""
    return g(id_, f'<path d="M{x} {y} L{tx - w / 2} {ty} A{w / 2} {w / 5} 0 0 0 {tx + w / 2} {ty} Z" fill="{color}" opacity=".28"/>'
                  f'<ellipse cx="{tx}" cy="{ty}" rx="{w / 2}" ry="{w / 5}" fill="{color}" opacity=".45"/>'
                  f'<circle cx="{x}" cy="{y}" r="28" fill="{GREY}" stroke="{INK}" stroke-width="{SW}"/>')


def page(id_, cx, cy, s=1.0, lines=8):
    rows = "".join(f'<rect x="-120" y="{-130 + k * 34}" width="{240 - (60 if k % 3 == 2 else 0)}" height="12" rx="6" fill="#9FB3C8"/>' for k in range(lines))
    return place(cx, cy, g(id_, f'<rect x="-150" y="-170" width="300" height="340" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="{SW}"/>' + rows), s)


def tablet(id_, cx, cy, s=1.0):
    rows = "".join(f'<rect x="-100" y="{-110 + k * 30}" width="200" height="10" rx="5" fill="#9FB3C8"/>' for k in range(7))
    return place(cx, cy, g(id_, f'<rect x="-140" y="-180" width="280" height="360" rx="26" fill="{INK}"/>'
                                f'<rect x="-124" y="-162" width="248" height="324" rx="10" fill="#E9F3FB"/>' + rows), s)


def book(id_, cx, cy, s=1.0, color="#2F5D9A"):
    lines = "".join(f'<path d="M{sx * 24} {-60 + k * 26} H{sx * 124}" stroke="#9FB3C8" stroke-width="8" stroke-linecap="round"/>'
                    for sx in (-1, 1) for k in range(5))
    return place(cx, cy, g(id_, f'<path d="M-150 -90 Q-75 -110 0 -86 Q75 -110 150 -90 V90 Q75 70 0 94 Q-75 70 -150 90 Z" fill="{PAPER}" '
                                f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/><path d="M0 -86 V94" stroke="{INK}" stroke-width="5"/>'
                                + lines
                                + f'<path d="M-150 90 Q-75 70 0 94 Q75 70 150 90 V104 Q75 84 0 108 Q-75 84 -150 104 Z" fill="{color}" stroke="{INK}" stroke-width="5"/>'), s)


def hourglass(id_, cx, cy, s=1.0):
    return place(cx, cy, g(id_, f'<rect x="-70" y="-110" width="140" height="18" rx="6" fill="{WOOD}" stroke="{INK}" stroke-width="5"/>'
                                f'<rect x="-70" y="92" width="140" height="18" rx="6" fill="{WOOD}" stroke="{INK}" stroke-width="5"/>'
                                f'<path d="M-54 -92 H54 Q54 -30 6 0 Q54 30 54 92 H-54 Q-54 30 -6 0 Q-54 -30 -54 -92 Z" fill="#CFE8F7" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<path d="M-40 92 Q0 40 40 92 Z" fill="{YELLOW}"/><path d="M-30 -60 H30 Q20 -30 0 -14 Q-20 -30 -30 -60 Z" fill="{YELLOW}"/>'), s)


def task_card(id_, cx, cy, label, color=TEAL, w=220, h=150):
    return place(cx, cy, g(id_, f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="20" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
                                + text(0, 22, label, 64, 900, INK, "middle")))


def link_chain(prefix, x, y, labels, gap=300):
    """Ô ý tưởng nối nhau: #prefix-b{k} ô, #prefix-l{k} mắt xích giữa ô k và k+1."""
    out = []
    for k, lb in enumerate(labels):
        cx = x + k * gap
        out.append(g(f"{prefix}-b{k}", f'<rect x="{cx - 110}" y="{y - 60}" width="220" height="120" rx="20" fill="#1D4262" stroke="{TEAL}" stroke-width="6"/>'
                     + text(cx, y + 14, lb, 40, 900, WHITE, "middle")))
        if k + 1 < len(labels):
            out.append(g(f"{prefix}-l{k}", f'<ellipse cx="{cx + gap / 2 - 22}" cy="{y}" rx="34" ry="20" fill="none" stroke="{YELLOW}" stroke-width="10"/>'
                         f'<ellipse cx="{cx + gap / 2 + 22}" cy="{y}" rx="34" ry="20" fill="none" stroke="{YELLOW}" stroke-width="10"/>'))
    return "".join(out)


TAB_COLORS = ["#C9D6E3", "#F7D774", "#F7A8B8", "#A8E6CF"]


def browser_tabs(prefix, x, y, n=8, w=150):
    tabs = "".join(f'<g id="{prefix}-t{k}"><path d="M{x + k * (w - 10)} {y} l14 -50 h{w - 28} l14 50 Z" fill="{TAB_COLORS[k % 4]}" '
                   f'stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>' for k in range(n))
    return (f'<rect x="{x - 20}" y="{y}" width="{n * (w - 10) + 40}" height="240" rx="16" fill="{WHITE}" stroke="{INK}" stroke-width="{SW}"/>' + tabs)


def stamp(id_, cx, cy, label, color=CORAL, w=760, size=48, rot=-5):
    return (f'<g transform="translate({cx} {cy}) rotate({rot})"><g id="{id_}"><rect x="{-w / 2}" y="-60" width="{w}" height="120" rx="16" '
            f'fill="none" stroke="{color}" stroke-width="10"/>' + text(0, size * 0.36, label, size, 900, color, "middle") + "</g></g>")


def donut(id_, cx, cy, r, frac, color=CORAL, rest="#1D4262"):
    """Vòng tròn phần trăm: #id_-arc tô dần bằng strokeDashoffset frac → 0."""
    return g(id_, f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{rest}" stroke-width="{r * 0.36:.0f}"/>'
                  f'<circle id="{id_}-arc" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{r * 0.36:.0f}" '
                  f'pathLength="1" stroke-dasharray="{frac} 1" stroke-dashoffset="{frac}" transform="rotate(-90 {cx} {cy})"/>')


# ---------------------------------------------------------------- tập Why stay up on your phone
FEED_COLORS = ["#F7A8B8", "#A8E6CF", "#F7D774", "#C9D6E3", "#FFB38A", "#B9A8F7"]


def feed(id_, cx, cy, s=1.0, n=14):
    """Điện thoại lớn có dòng tin cuộn không đáy: tween #id_-strip theo y (âm) để cuộn."""
    cards = "".join(f'<rect x="-104" y="{-150 + k * 118}" width="208" height="102" rx="14" fill="{FEED_COLORS[k % 6]}" stroke="{INK}" stroke-width="4"/>'
                    f'<circle cx="-70" cy="{-120 + k * 118}" r="16" fill="{WHITE}"/>'
                    f'<rect x="-44" y="{-128 + k * 118}" width="120" height="14" rx="7" fill="{WHITE}"/>'
                    f'<rect x="-84" y="{-92 + k * 118}" width="160" height="12" rx="6" fill="{WHITE}" opacity=".7"/>' for k in range(n))
    return place(cx, cy, g(id_, f'<defs><clipPath id="{id_}-clip"><rect x="-116" y="-196" width="232" height="392" rx="14"/></clipPath></defs>'
                                f'<rect x="-136" y="-226" width="272" height="452" rx="34" fill="{INK}"/>'
                                f'<rect x="-116" y="-196" width="232" height="392" rx="14" fill="#E9F3FB"/>'
                                f'<g clip-path="url(#{id_}-clip)"><g id="{id_}-strip">{cards}</g></g>'
                                f'<circle cy="210" r="7" fill="{GREY}"/>'), s)


def pedal(id_, cx, cy, label, color, s=1.0):
    """Bàn đạp (ga/phanh): co giãn #id_ theo scale để to/nhỏ."""
    return place(cx, cy, g(id_, f'<rect x="-80" y="-130" width="160" height="260" rx="30" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
                                + "".join(f'<rect x="-54" y="{-96 + k * 44}" width="108" height="16" rx="8" fill="{INK}" opacity=".35"/>' for k in range(5))
                                + text(0, 200, label, 44, 900, color, "middle")), s)


def day_bar(prefix, x, y, w, segs, h=90):
    """Thanh ngày 24 giờ: segs = [(phần, màu, nhãn)]; mỗi đoạn #prefix-s{k}."""
    out, x0 = [], x
    for k, (frac, color, lab) in enumerate(segs):
        sw = w * frac
        out.append(g(f"{prefix}-s{k}", f'<rect x="{x0:.0f}" y="{y}" width="{sw:.0f}" height="{h}" fill="{color}" stroke="{INK}" stroke-width="5"/>'
                     + text(x0 + sw / 2, y + h / 2 + 12, lab, 30, 900, INK, "middle")))
        x0 += sw
    return "".join(out)


def age_curve(id_, x, y, w, h):
    """Đường giờ ngủ theo tuổi (10 → 60): muộn dần, đỉnh ~20, rồi sớm dần. pathLength=1 để vẽ dần."""
    ax = lambda age: x + w * (age - 10) / 50
    pts = [(10, 0.15), (13, 0.42), (16, 0.72), (18, 0.9), (20, 1.0), (23, 0.9), (30, 0.68), (40, 0.48), (50, 0.34), (60, 0.24)]
    d = "M" + " L".join(f"{ax(a):.0f} {y + h - h * v:.0f}" for a, v in pts)
    return (f'<path id="{id_}" d="{d}" fill="none" stroke="{YELLOW}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" '
            f'pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')


# ---- tập Why are you tired after a day of doing nothing? (2026-11-09)

def bike(id_, cx, cy, s=1.0, color=TEAL):
    """Xe đạp tập tại chỗ; bánh đà #id_-wheel xoay quanh tâm (0, 40)."""
    return place(cx, cy, g(id_, f'<path d="M-150 150 H150" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>'
                                f'<path d="M-110 150 L-40 -40 M60 150 L20 -20 L-40 -40 M-40 -40 L-60 -100 M20 -20 L60 -110" '
                                f'stroke="{color}" stroke-width="22" stroke-linecap="round" fill="none"/>'
                                f'<rect x="-100" y="-118" width="80" height="22" rx="11" fill="{INK}"/>'
                                f'<path d="M40 -120 H95" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
                                f'<g id="{id_}-wheel"><circle cx="0" cy="40" r="70" fill="#1D4262" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<path d="M0 -30 V110 M-70 40 H70" stroke="{GREY}" stroke-width="8"/></g>'
                                f'<circle cx="0" cy="40" r="12" fill="{YELLOW}" stroke="{INK}" stroke-width="5"/>'), s)


def shock_button(id_, cx, cy, s=1.0):
    """Nút bấm đỏ có tia sét; #id_-cap nhấn xuống bằng y."""
    bolt = f'<path d="M14 -150 L-26 -84 H6 L-14 -24 L34 -98 H2 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    return place(cx, cy, g(id_, f'<rect x="-110" y="10" width="220" height="70" rx="18" fill="{GREY}" stroke="{INK}" stroke-width="{SW}"/>'
                                f'<g id="{id_}-cap"><ellipse cx="0" cy="10" rx="80" ry="34" fill="{CORAL}" stroke="{INK}" stroke-width="{SW}"/></g>'
                                + g(f"{id_}-bolt", bolt)), s)


def heartbeat(id_, x, y, w, gaps, color=CORAL, width=8):
    """Đường nhịp tim từ (x, y) dài w; gaps = khoảng cách giữa các nhịp (tăng dần = tim chậm dần). pathLength=1."""
    d, px = [f"M{x} {y}"], x
    for gp in gaps:
        if px + gp + 60 > x + w:
            break
        px += gp
        d.append(f"L{px} {y} L{px + 12} {y - 70} L{px + 26} {y + 50} L{px + 38} {y - 20} L{px + 50} {y}")
        px += 50
    d.append(f"L{x + w} {y}")
    return (f'<path id="{id_}" d="{" ".join(d)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')


def pressure_curve(id_, x, y, w, h, color=YELLOW):
    """Áp lực ngủ tăng dần theo giờ thức (bão hòa); pathLength=1 để vẽ dần."""
    import math
    pts = [(x + w * k / 20, y + h - h * (1 - math.exp(-2.2 * k / 20)) / (1 - math.exp(-2.2))) for k in range(21)]
    d = "M" + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts)
    return (f'<path id="{id_}" d="{d}" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" '
            f'pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')
