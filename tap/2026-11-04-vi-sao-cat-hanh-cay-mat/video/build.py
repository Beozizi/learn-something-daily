"""Sinh dự án HyperFrames của tập từ audio/timeline.json + audio/words.json.

Chạy:  py build.py      (trong thư mục video\\)
Mọi mốc thời gian lấy từ chữ trong lời đọc, nên lồng tiếng lại chỉ cần chạy lại file này.
Sửa ở đây, không sửa tay index.html hay compositions\\*.html.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ve import *  # noqa: E402,F403

VID = Path(__file__).resolve().parent
EP = VID.parent
TIMELINE = json.loads((EP / "audio" / "timeline.json").read_text(encoding="utf-8"))
WORDS = json.loads((EP / "audio" / "words.json").read_text(encoding="utf-8"))
SCENES = {s["id"]: s for s in TIMELINE["scenes"]}
DURATION = TIMELINE["duration"]
PUNCT = ".,;:!?…“”\"'()«»"

FONT_CSS = "".join(
    f"@font-face {{ font-family: 'Be Vietnam Pro'; font-weight: {w}; src: url('assets/fonts/BeVietnamPro-{n}.ttf'); }}\n"
    for w, n in ((500, "Medium"), (600, "SemiBold"), (700, "Bold"), (800, "ExtraBold"), (900, "Black")))
OUTLINE = 'paint-order="stroke" stroke="#081420" stroke-width="12" stroke-linejoin="round"'


def norm(w):
    return w.strip(PUNCT).lower()


def word_time(scene, phrase, nth=0, which="start"):
    toks = [norm(x) for x in phrase.split()]
    ws = [w for w in WORDS["words"] if w["scene"] == scene]
    hits = [i for i in range(len(ws) - len(toks) + 1)
            if [norm(ws[i + k]["text"]) for k in range(len(toks))] == toks]
    if len(hits) <= nth:
        raise SystemExit(f"Không thấy '{phrase}' (lần {nth}) trong cảnh {scene}")
    i = hits[nth]
    return ws[i]["start"] if which == "start" else ws[i + len(toks) - 1]["end"]


def sentence_starts(scene):
    return [s["start"] for s in WORDS["sentences"] if s["scene"] == scene]


class TL:
    def __init__(self):
        self.lines = []

    def _add(self, fn, sel, *props, t):
        args = ", ".join(json.dumps(p, ensure_ascii=False) for p in props)
        self.lines.append(f"tl.{fn}({json.dumps(sel)}, {args}, {t:.3f});")

    def set(self, sel, p, t):
        self._add("set", sel, p, t=t)

    def to(self, sel, p, t):
        self._add("to", sel, p, t=t)

    def ft(self, sel, a, b, t):
        b = dict(b, immediateRender=False)
        self._add("fromTo", sel, a, b, t=t)


class Comp:
    """Một cảnh (sub-composition) chiếm khoảng [start, end) của phim."""

    def __init__(self, cid, start, end):
        self.cid, self.start, self.end = cid, start, end
        self.svg, self.html, self.css = [], [], []
        self.hidden = []
        self.tl = TL()

    def at(self, scene, phrase, nth=0, which="start", off=0.0):
        return round(word_time(scene, phrase, nth, which) - self.start + off, 3)

    def loc(self, t_abs):
        return round(t_abs - self.start, 3)

    def hide(self, *sels):
        """Ẩn từ đầu bằng CSS (tl.set ở giây 0 không hiện ở khung đầu tiên)."""
        for s in sels:
            if s not in self.hidden:
                self.hidden.append(s)

    def show(self, sel, t, on=True):
        self.tl.set(sel, {"autoAlpha": 1 if on else 0}, t)

    def draw(self, sel, t, dur=0.6, ease="power2.out"):
        self.tl.ft(sel, {"strokeDashoffset": 1.1}, {"strokeDashoffset": 0, "duration": dur, "ease": ease}, t)

    def pop(self, sel, t, dur=0.5, origin="50% 50%", ease="back.out(1.8)", frm=0.0):
        self.hide(sel)
        self.show(sel, t)
        self.tl.ft(sel, {"scale": frm, "transformOrigin": origin},
                   {"scale": 1, "transformOrigin": origin, "duration": dur, "ease": ease}, t)

    def blur_in(self, sel, t, dur=0.18):
        self.hide(sel)
        self.tl.ft(sel, {"autoAlpha": 0, "filter": "blur(8px)"}, {"autoAlpha": 1, "filter": "blur(0px)", "duration": dur,
                                                                  "ease": "power2.out"}, t)

    def blur_out(self, sel, t, dur=0.2):
        self.tl.ft(sel, {"autoAlpha": 1, "filter": "blur(0px)"}, {"autoAlpha": 0, "filter": "blur(8px)", "duration": dur,
                                                                  "ease": "power2.in"}, t)

    def sfx(self, kind, t, vol=None):
        """Đặt một hiệu ứng âm sao cho điểm nổ rơi 1 khung sau hình ở thời điểm t (giây trong cảnh)."""
        takes = SFX[kind]
        n = SFX_COUNT.get(kind, 0)
        SFX_COUNT[kind] = n + 1
        f, peak, dur, v, media_start = takes[n % len(takes)]
        SFX_EVENTS.append((round(self.start + t - peak + 1 / 24, 3), f, dur, vol if vol is not None else v, media_start))

    def write(self):
        html = f"""<template>
<style>
{FONT_CSS}
#root {{ position: absolute; inset: 0; overflow: hidden; font-family: 'Be Vietnam Pro', sans-serif; }}
#root .stage {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
#root .txt {{ position: absolute; font-family: 'Be Vietnam Pro', sans-serif; }}
{"".join(self.css)}
{"".join(f"{s} {{ opacity: 0; visibility: hidden; }}" for s in self.hidden)}
</style>
<div id="root" data-composition-id="{self.cid}" data-width="1920" data-height="1080">
<svg id="{self.cid}-stage" class="stage" viewBox="0 0 1920 1080" width="1920" height="1080">
{"".join(self.svg)}
</svg>
{"".join(self.html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(self.tl.lines)}
window.__timelines["{self.cid}"] = tl;
</script>
</template>
"""
        (VID / "compositions" / f"{self.cid}.html").write_text(html, encoding="utf-8")


# Hiệu ứng âm: loại → các bản xoay vòng (file, giây tới điểm nổ, thời lượng dùng, âm lượng, cắt đầu)
# Nguồn trong .media/manifest.jsonl; knife_chop (sfx_005) là CC BY 3.0 — phải ghi công.
SFX = {
    "whoosh": [("sfx_002.mp3", 0.065, 0.6, 0.35, 0), ("sfx_001.mp3", 0.31, 1.2, 1.6, 0)],
    "pop": [("sfx_009.mp3", 0.11, 0.7, 0.35, 0), ("sfx_003.mp3", 0.005, 0.1, 0.3, 0), ("sfx_004.mp3", 0.045, 0.4, 0.3, 0)],
    "chop": [("sfx_005.mp3", 0.361, 0.8, 0.45, 0)],
    "thump": [("sfx_006.mp3", 0.165, 0.7, 0.55, 0)],
    "riser": [("sfx_007.mp3", 2.8, 3.3, 0.3, 0.5)],
}
SFX_COUNT = {}
SFX_EVENTS = []

BLINK_GAPS = [2.3, 3.4, 2.7, 3.9, 2.1, 3.1]


def idle(c, uid, t0, t1, seed=0):
    """Tò đứng yên vẫn sống: thở, đầu nhấp nhô trễ một nhịp, chớp mắt không đều."""
    t, k = t0 + 0.7 + 0.35 * (seed % 3), seed
    while t < t1 - 0.3:
        c.tl.to(f"#{uid} .mat", {"scaleY": 0.1, "transformOrigin": "50% 50%", "duration": 0.06, "ease": "power2.in"}, t)
        c.tl.to(f"#{uid} .mat", {"scaleY": 1, "transformOrigin": "50% 50%", "duration": 0.09, "ease": "power2.out"}, t + 0.06)
        t += BLINK_GAPS[k % len(BLINK_GAPS)]
        k += 1
    n = int((t1 - t0) / 1.2)
    if n >= 2:
        reps = n - 1 if (n - 1) % 2 else n - 2
        c.tl.ft(f"#{uid} .than", {"scaleY": 1}, {"scaleY": 1.012, "transformOrigin": "50% 100%", "duration": 1.2,
                                                  "ease": "sine.inOut", "yoyo": True, "repeat": reps}, t0)
        c.tl.ft(f"#{uid} .dau", {"y": 0}, {"y": -3, "duration": 1.2, "ease": "sine.inOut", "yoyo": True,
                                           "repeat": reps}, t0 + 0.18)


def swap(c, a, b, t):
    """Đổi tư thế: nhún lấy đà → đổi → nảy về."""
    c.tl.to(f"#{a}", {"scaleY": 0.96, "scaleX": 1.03, "transformOrigin": "50% 100%", "duration": 0.12, "ease": "power2.in"}, t)
    c.show(f"#{a}-w", t + 0.12, False)
    c.show(f"#{b}-w", t + 0.12)
    c.tl.ft(f"#{b}", {"scaleY": 1.04, "scaleX": 0.97, "transformOrigin": "50% 100%"},
            {"scaleY": 1, "scaleX": 1, "transformOrigin": "50% 100%", "duration": 0.45, "ease": "back.out(3)"}, t + 0.12)


def frame(c, t, px, py, z, cam, settle):
    """Cắt sang khung mới: tâm (px, py) phóng z lần, vào lớn 104 % rồi lắng."""
    c.tl.set(cam, {"x": 960 - z * px, "y": 540 - z * py, "scale": z, "transformOrigin": "0 0"}, t)
    c.tl.ft(settle, {"scale": 1.04, "svgOrigin": "960 540"},
            {"scale": 1, "svgOrigin": "960 540", "duration": 0.45, "ease": "expo.out"}, t)


# Tò trong bếp: đứng sau mặt bếp, cao 900 px
TO_X, TO_Y, TO_H = 734, 0, 900
EYE_L = to_point(TO_X, TO_Y, TO_H, 185, 199)
EYE_R = to_point(TO_X, TO_Y, TO_H, 255, 199)
# Tò trên bảng: đứng bên trái
B_X, B_Y, B_H = 40, 330, 700


# ---------------------------------------------------------------- 01 · Tiêu đề
def s01():
    s = SCENES["01"]
    c = Comp("s01", s["start"], s["end"])
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>',
              onion("s01-onion", 1460, 640, 2.7),
              gas_wisps("s01-gas", ["M1450 360 C1410 300 1490 260 1450 200 C1420 160 1470 130 1450 90",
                                    "M1520 372 C1560 320 1500 280 1550 226",
                                    "M1390 380 C1360 330 1400 296 1370 252"])]
    words = ["Vì", "sao", "cắt", "hành", "<br>", "lại", "cay", "mắt?"]
    spans = "".join("<br>" if w == "<br>" else
                    f'<span id="s01-w{k}" class="w{" hot" if w == "cay" else ""}">{w}</span> '
                    for k, w in enumerate(words))
    c.css.append("#s01-title { left: 150px; top: 300px; font-size: 136px; font-weight: 800; line-height: 1.12; "
                 f"color: {INK}; letter-spacing: -0.01em; }} #s01-title .hot {{ color: {CORAL}; }} "
                 "#s01-title .w { display: inline-block; }")
    c.html.append(f'<div id="s01-title" class="txt">{spans}</div>')
    c.tl.ft("#s01-onion", {"scale": 0.7, "transformOrigin": "50% 100%"},
            {"scale": 1, "transformOrigin": "50% 100%", "duration": 0.7, "ease": "back.out(1.6)"}, 0)
    for k, w in enumerate(words):
        if w != "<br>":
            c.blur_in(f"#s01-w{k}", 0.25 + 0.09 * k, 0.15)
    for k in range(3):
        c.draw(f"#s01-gas-{k}", 1.3 + 0.18 * k, 0.9)
    c.tl.ft("#s01-gas", {"y": 0}, {"y": -24, "duration": 3.0, "ease": "sine.out"}, 1.3)
    return c


# ---------------------------------------------------------------- 02 · Mở truyện
def s02():
    s = SCENES["02"]
    c = Comp("s02", s["start"], s["end"])
    S = [c.loc(t) for t in sentence_starts("02")]
    lx, ly = EYE_L
    rx, ry = EYE_R
    tears = "".join(
        f'<path id="s02-tear-{n}-o" d="{d}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>'
        f'<path id="s02-tear-{n}" d="{d}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" fill="none" stroke="{TEAR}" stroke-width="15" stroke-linecap="round"/>'
        for n, d in (("l", f"M{lx - 4:.0f} {ly + 52:.0f} C{lx - 14:.0f} {ly + 100:.0f} {lx - 2:.0f} {ly + 150:.0f} {lx - 20:.0f} {ly + 230:.0f}"),
                     ("r", f"M{rx + 4:.0f} {ly + 52:.0f} C{rx + 14:.0f} {ry + 100:.0f} {rx + 2:.0f} {ry + 150:.0f} {rx + 22:.0f} {ry + 230:.0f}")))
    world = [kitchen_back("s02"),
             to("s02-dung", "dung", TO_X, TO_Y, TO_H),
             to("s02-lo", "lo-lang", TO_X, TO_Y, TO_H),
             to("s02-suy", "suy-nghi", TO_X, TO_Y, TO_H),
             g("s02-red", f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="50" fill="{CORAL}" opacity=".38"/>'
                          f'<circle cx="{rx:.0f}" cy="{ry:.0f}" r="50" fill="{CORAL}" opacity=".38"/>'),
             g("s02-tears", tears),
             kitchen_front(),
             basket("s02-basket", 420, 584, 5, 1.1),
             cutting_board(960, 668, 440, 34),
             onion("s02-onion", 1170, 612, 0.62),
             gas_wisps("s02-gas", ["M1160 560 C1120 500 1190 460 1140 400 C1110 360 1150 330 1130 290",
                                   "M1196 570 C1236 520 1176 480 1216 430 C1236 400 1206 370 1226 340",
                                   "M1136 575 C1106 530 1146 500 1106 450"], 13),
             knife("s02-knife", 1440, 512, 0.9, 0, sharp=False, flip=True)]
    c.svg.append(f'<g id="s02-settle"><g id="s02-cam">{"".join(world)}</g></g>')
    c.svg.append(g("s02-drawer", f"""<rect width="1920" height="1080" fill="{WOOD}"/>
<rect x="150" y="130" width="1620" height="820" rx="36" fill="#4A3020" stroke="{INK}" stroke-width="10"/>
<rect x="190" y="170" width="1540" height="740" rx="24" fill="none" stroke="#3A2416" stroke-width="6"/>
{knife("s02-dk1", 640, 400, 2.0, 0, sharp=True)}
{knife("s02-dk2", 640, 690, 2.0, 0, sharp=False)}
{text(1400, 430, "SẮC", 96, 900, WHITE, extra=" id='s02-l1' " + OUTLINE)}
{text(1400, 720, "CÙN", 96, 900, CORAL, extra=" id='s02-l2' " + OUTLINE)}"""))
    c.svg.append(text(1480, 380, "20", 300, 900, YELLOW, id_="s02-n20", extra=" " + OUTLINE))
    c.svg.append(g("s02-q", text(140, 300, "NHANH?", 120, 900, WHITE, id_="s02-q1", extra=" " + OUTLINE)
                   + text(1360, 300, "CHẬM?", 120, 900, WHITE, id_="s02-q2", extra=" " + OUTLINE)))
    c.hide("#s02-knife", "#s02-lo-w", "#s02-suy-w", "#s02-red", "#s02-drawer", "#s02-n20", "#s02-q1", "#s02-q2", "#s02-l1", "#s02-l2")
    cam, st = "#s02-cam", "#s02-settle"

    # 1 · Bếp toàn cảnh, 6:00
    frame(c, 0, 960, 540, 1.0, cam, st)
    idle(c, "s02-dung", 0, S[3], 0)
    c.tl.to("#s02-clock-m", {"rotation": "+=6", "svgOrigin": "1620 250", "duration": 0.15, "ease": "back.out(3)"},
            c.at("02", "bảy giờ"))
    # 2 · Cận dao chạm củ hành
    frame(c, S[2], 1200, 590, 2.5, cam, st)
    c.show("#s02-knife", S[2])
    c.show("#s02-knife", S[3], False)
    c.tl.ft("#s02-knife", {"y": -170, "rotation": -6}, {"y": 0, "rotation": 0, "duration": 0.7, "ease": "expo.out"}, S[2] + 0.15)
    tc = c.at("02", "chạm")
    c.tl.to("#s02-knife", {"y": 16, "duration": 0.12, "ease": "power2.in"}, tc)
    c.sfx("chop", tc + 0.12)
    c.tl.to("#s02-knife", {"y": 10, "duration": 0.3, "ease": "power2.out"}, tc + 0.12)
    for k in range(3):
        c.draw(f"#s02-gas-{k}", tc + 0.35 + 0.2 * k, 1.1)
    # 3–4 · Cận mặt: cay, rồi nước mắt
    frame(c, S[3], 1110, 380, 2.3, cam, st)
    c.show("#s02-dung-w", S[3], False)
    c.show("#s02-lo-w", S[3])
    idle(c, "s02-lo", S[3], S[5], 2)
    c.tl.ft("#s02-gas", {"y": 0}, {"y": -60, "duration": 2.5, "ease": "sine.inOut"}, S[3])
    tcay = c.at("02", "cay", 0)
    c.tl.ft("#s02-lo .dau", {"rotation": 0}, {"rotation": -5, "transformOrigin": "50% 95%", "duration": 0.18,
                                               "ease": "power2.out", "yoyo": True, "repeat": 3}, tcay)
    tn = c.at("02", "nước mắt")
    for n in ("l", "r"):
        c.draw(f"#s02-tear-{n}-o", tn + (0 if n == "l" else 0.2), 1.2, "power1.in")
        c.draw(f"#s02-tear-{n}", tn + (0 if n == "l" else 0.2), 1.2, "power1.in")
    # 5 · Rổ hành, còn 20 củ
    frame(c, S[5], 440, 560, 2.1, cam, st)
    c.pop("#s02-n20", c.at("02", "hai mươi"), 0.5, "50% 50%")
    c.sfx("pop", c.at("02", "hai mươi"))
    c.show("#s02-n20", S[6], False)
    c.tl.to("#s02-gas", {"autoAlpha": 0, "duration": 0.4}, S[4] + 0.6)
    # 6 · Ngăn kéo hai dao
    c.show("#s02-drawer", S[6])
    c.tl.ft("#s02-drawer", {"y": 260}, {"y": 0, "duration": 0.6, "ease": "expo.out"}, S[6])
    c.sfx("whoosh", S[6] + 0.1)
    c.pop("#s02-l1", c.at("02", "sắc"), 0.4, "0% 50%")
    c.sfx("pop", c.at("02", "sắc"))
    c.tl.ft("#s02-dk1-spark", {"scale": 0, "rotation": 0, "transformOrigin": "50% 50%"},
            {"scale": 1.4, "rotation": 90, "transformOrigin": "50% 50%", "duration": 0.5, "ease": "back.out(2)"}, c.at("02", "sắc"))
    c.pop("#s02-l2", c.at("02", "cùn"), 0.4, "0% 50%")
    c.sfx("pop", c.at("02", "cùn"))
    c.show("#s02-drawer", S[7], False)
    # 7 · Phân vân: nhanh hay chậm
    frame(c, S[7], 1100, 420, 1.5, cam, st)
    c.show("#s02-lo-w", S[7], False)
    c.show("#s02-suy-w", S[7])
    c.show("#s02-tears", S[7], False)
    idle(c, "s02-suy", S[7], S[8], 1)
    c.pop("#s02-q1", c.at("02", "nhanh"), 0.45, "50% 50%")
    c.sfx("pop", c.at("02", "nhanh"))
    c.pop("#s02-q2", c.at("02", "chậm"), 0.45, "50% 50%")
    c.sfx("pop", c.at("02", "chậm"))
    c.tl.to("#s02-suy .mat", {"x": -6, "duration": 0.2}, c.at("02", "nhanh"))
    c.tl.to("#s02-suy .mat", {"x": 8, "duration": 0.25}, c.at("02", "chậm"))
    c.show("#s02-q1", S[8], False)
    c.show("#s02-q2", S[8], False)
    # 8 · Mắt đỏ hoe, đồng hồ nhảy tới 7:00
    frame(c, S[8], 1330, 380, 1.55, cam, st)
    c.show("#s02-suy-w", S[8], False)
    c.show("#s02-lo-w", S[8])
    c.show("#s02-tears", S[8])
    idle(c, "s02-lo", S[8], c.loc(s["end"]), 4)
    tk = c.at("02", "đón khách")
    c.tl.to("#s02-clock-m", {"rotation": "+=354", "svgOrigin": "1620 250", "duration": 0.9, "ease": "power2.inOut"}, tk)
    c.sfx("whoosh", tk + 0.45)
    c.tl.to("#s02-clock-h", {"rotation": "+=30", "svgOrigin": "1620 250", "duration": 0.9, "ease": "power2.inOut"}, tk)
    th = c.at("02", "đỏ hoe")
    c.tl.ft("#s02-red", {"autoAlpha": 0}, {"autoAlpha": 1, "duration": 0.4, "ease": "power2.out"}, th)
    return c


def board_to(c, uid, pose="suy-nghi", hidden=False):
    c.svg.append(to(uid, pose, B_X, B_Y, B_H))
    if hidden:
        c.hide(f"#{uid}-w")


def burst(c, prefix, n, t, spread=(-160, -20), dist=(140, 320), dur=0.7):
    """Giọt nước bắn ra theo hình quạt, hướng và độ xa cố định (không ngẫu nhiên)."""
    import math
    for k in range(n):
        a = math.radians(spread[0] + (spread[1] - spread[0]) * ((k * 7) % n) / max(n - 1, 1))
        d = dist[0] + (dist[1] - dist[0]) * ((k * 5) % n) / max(n - 1, 1)
        c.tl.ft(f"#{prefix}-{k}", {"x": 0, "y": 0, "opacity": 1},
                {"x": d * math.cos(a), "y": d * math.sin(a) + 40, "duration": dur, "ease": "power2.out"}, t + 0.015 * k)
        c.tl.to(f"#{prefix}-{k}", {"opacity": 0, "duration": 0.25, "ease": "power1.in"}, t + 0.015 * k + dur)


# ---------------------------------------------------------------- 03 · Dữ kiện
def s03():
    s = SCENES["03"]
    c = Comp("s03", s["start"], s["end"])
    X0, X1, X2 = 640, 640 + 1240, 640 + 2480
    mol = "".join(molecule(f"s03-m{k}", X0 + 400 + (k % 2) * 120, 430 + (k // 2) * 110) for k in range(6))
    sci = "".join(scissors(f"s03-x{k}", X0 + 820, 450 + k * 110, 1.0) for k in range(3))
    nerves = "".join(
        f'<path id="s03-nv-{k}" d="{d}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" fill="none" stroke="{YELLOW}" stroke-width="10" stroke-linecap="round"/>'
        for k, d in enumerate([f"M{X1 + 690} 470 l-50 -40", f"M{X1 + 676} 540 l-64 -6",
                               f"M{X1 + 676} 600 l-62 18", f"M{X1 + 692} 660 l-48 44"]))
    strip = f"""
{text(X0 + 30, 230, "1", 170, 900, WHITE, id_="s03-n1")}
<g id="s03-cellg"><rect x="{X0 + 300}" y="340" width="760" height="420" rx="44" fill="{CELL}" stroke="{INK}" stroke-width="8"/>
<line id="s03-div-a" x1="{X0 + 680}" y1="360" x2="{X0 + 680}" y2="550" stroke="{INK}" stroke-width="7" stroke-dasharray="20 14"/>
<line id="s03-div-b" x1="{X0 + 680}" y1="550" x2="{X0 + 680}" y2="740" stroke="{INK}" stroke-width="7" stroke-dasharray="20 14"/>
<g id="s03-mols">{mol}</g><g id="s03-scis">{sci}</g></g>
{gas_cloud("s03-cloud", X0 + 680, 250, 1.1, "KHÍ CAY")}
{text(X1 + 30, 230, "2", 170, 900, WHITE, id_="s03-n2")}
{eye_side("s03-eye", X1 + 880, 560, 160)}
<g id="s03-nv">{nerves}</g>
{text(X1 + 560, 420, "!", 120, 900, YELLOW, id_="s03-bang", extra=" " + OUTLINE)}
{gas_cloud("s03-cloud2", X1 + 260, 540, 1.0, "KHÍ CAY")}
{text(X2 + 30, 230, "3", 170, 900, WHITE, id_="s03-n3")}
{cell_row("s03-r", X2 + 300, 650, 8, 86, 120)}
{droplets("s03-d", X2 + 665, 640, 12)}
{blade_tip("s03-blade", X2 + 665, 300, sharp=False)}"""
    c.svg += [slate_frame(), '<clipPath id="s03-win"><rect x="620" y="28" width="1272" height="1024"/></clipPath>', f'<g clip-path="url(#s03-win)"><g id="s03-strip">{strip}</g></g>']
    board_to(c, "s03-to")
    c.svg.append(slate_border())
    c.hide("#s03-n1", "#s03-cellg", "#s03-cloud", "#s03-n2", "#s03-eye", "#s03-bang", "#s03-cloud2", "#s03-n3")
    c.tl.set("#s03-to .mat", {"x": 7}, 0)
    idle(c, "s03-to", 0, c.loc(s["end"]), 1)
    # 1
    c.pop("#s03-n1", c.at("03", "Một"), 0.45)
    th = c.at("03", "hai chất", 0)
    c.pop("#s03-cellg", th, 0.6, "50% 50%", "back.out(1.4)", 0.3)
    c.sfx("pop", th)
    for k in range(6):
        c.tl.ft(f"#s03-m{k}", {"scale": 0, "transformOrigin": "50% 50%"},
                {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.4, "ease": "back.out(2)"}, th + 0.3 + 0.06 * k)
    tn = c.at("03", "hai ngăn")
    for k in range(3):
        c.tl.ft(f"#s03-x{k}", {"scale": 0, "transformOrigin": "50% 50%"},
                {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.4, "ease": "back.out(2)"}, tn + 0.08 * k)
    tv = c.at("03", "tế bào vỡ", 0)
    c.tl.to("#s03-div-a", {"rotation": -28, "y": -50, "opacity": 0, "transformOrigin": "50% 0%", "duration": 0.5, "ease": "power3.out"}, tv)
    c.tl.to("#s03-div-b", {"rotation": 28, "y": 50, "opacity": 0, "transformOrigin": "50% 100%", "duration": 0.5, "ease": "power3.out"}, tv)
    c.tl.ft("#s03-cellg", {"x": 0}, {"x": 10, "duration": 0.06, "yoyo": True, "repeat": 5, "ease": "none"}, tv)
    tm = c.at("03", "trộn vào nhau")
    c.tl.to("#s03-mols", {"x": 150, "duration": 0.9, "ease": "power2.inOut"}, tm)
    c.tl.to("#s03-scis", {"x": -170, "duration": 0.9, "ease": "power2.inOut"}, tm)
    c.pop("#s03-cloud", c.at("03", "khí cay", 0), 0.6, "50% 100%", "back.out(1.6)", 0.2)
    # 2
    t2 = c.at("03", "Hai", 2)
    c.tl.to("#s03-strip", {"x": -1240, "duration": 1.0, "ease": "power2.inOut"}, t2 - 0.25)
    c.sfx("whoosh", t2 + 0.25)
    c.pop("#s03-n2", t2 + 0.3, 0.45)
    c.pop("#s03-eye", t2 + 0.5, 0.6, "50% 50%", "back.out(1.4)", 0.4)
    c.sfx("pop", t2 + 0.5)
    c.pop("#s03-cloud2", c.at("03", "bay lên"), 0.5, "50% 100%")
    c.tl.to("#s03-cloud2", {"x": 400, "y": 0, "duration": 1.3, "ease": "power2.inOut"}, c.at("03", "bay lên", off=0.3))
    tdt = c.at("03", "đầu dây thần kinh")
    for k in range(4):
        c.draw(f"#s03-nv-{k}", tdt + 0.08 * k, 0.4)
    tb = c.at("03", "báo động")
    c.tl.ft("#s03-nv", {"opacity": 1}, {"opacity": 0.25, "duration": 0.12, "yoyo": True, "repeat": 5, "ease": "none"}, tb)
    c.pop("#s03-bang", tb, 0.4)
    # 3
    t3 = c.at("03", "Ba", 1)
    c.tl.to("#s03-strip", {"x": -2480, "duration": 1.0, "ease": "power2.inOut"}, t3 - 0.25)
    c.sfx("whoosh", t3 + 0.25)
    c.pop("#s03-n3", t3 + 0.3, 0.45)
    ta = c.at("03", "ấn xuống")
    c.tl.ft("#s03-blade", {"y": -60}, {"y": 312, "duration": 0.8, "ease": "power2.in"}, ta - 0.3)
    tc = c.at("03", "chống lại")
    for k, sy in ((2, 0.86), (3, 0.72), (4, 0.72), (5, 0.86)):
        c.tl.to(f"#s03-r-{k}", {"scaleY": sy, "transformOrigin": "50% 100%", "duration": 1.4, "ease": "power1.inOut"}, tc)
    c.tl.to("#s03-r-skin", {"y": 26, "duration": 1.4, "ease": "power1.inOut"}, tc)
    c.tl.to("#s03-blade", {"y": 345, "duration": 1.4, "ease": "power1.inOut"}, tc)
    tdu = c.at("03", "mới đứt")
    c.tl.to("#s03-blade", {"y": 430, "duration": 0.14, "ease": "power3.in"}, tdu)
    c.sfx("chop", tdu + 0.1)
    for k in (3, 4):
        c.tl.to(f"#s03-r-{k}-b", {"opacity": 1, "duration": 0.12}, tdu + 0.1)
    burst(c, "s03-d", 6, tdu + 0.1)
    tvt = c.at("03", "vỡ tung")
    for j, k in enumerate((2, 5, 1, 6)):
        c.tl.to(f"#s03-r-{k}-b", {"opacity": 1, "duration": 0.12}, tvt + 0.12 * j)
    burst(c, "s03-d", 12, c.at("03", "bắn ra"), dist=(200, 420))
    return c


def options(prefix, x=720):
    return (option_row(f"{prefix}a", x, 300, "A", False, "CẮT THẬT NHANH")
            + option_row(f"{prefix}b", x, 530, "B", True, "CẮT CHẬM RÃI")
            + option_row(f"{prefix}c", x, 760, "C", False, "CHẬM, NHẸ TAY"))


# ---------------------------------------------------------------- 04 · Câu hỏi
def s04():
    s = SCENES["04"]
    c = Comp("s04", s["start"], s["end"])
    c.svg.append(slate_frame())
    board_to(c, "s04-to")
    c.svg += [options("s04-o"), slate_border()]
    idle(c, "s04-to", 0, c.loc(s["end"]), 2)
    c.tl.set("#s04-to .mat", {"x": 7}, 0)
    for L in "abc":
        t = c.at("04", L.upper())
        c.hide(f"#s04-o{L}")
        c.tl.ft(f"#s04-o{L}", {"autoAlpha": 0, "x": 60, "filter": "blur(8px)"},
                {"autoAlpha": 1, "x": 0, "filter": "blur(0px)", "duration": 0.45, "ease": "expo.out"}, t)
        c.tl.to("#s04-to .mat", {"y": {"a": -6, "b": 0, "c": 6}[L], "duration": 0.2}, t)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 05 · Thử đoán
def s05():
    s = SCENES["05"]
    c = Comp("s05", s["start"], s["end"])
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>',
              f'<circle cx="1560" cy="560" r="230" fill="{YELLOW}" stroke="{INK}" stroke-width="10"/>',
              text(1560, 290, "TẠM DỪNG VIDEO", 44, 900, INK, "middle"),
              g("s05-n", "".join(text(1560, 650, str(n), 300, 900, INK, "middle", id_=f"s05-n{n}") for n in (3, 2, 1)))]
    lines = [("h", "Thử đoán trước nhé!"),
             ("f", "1. Hai chất trong tế bào hành chỉ gặp nhau khi tế bào vỡ → tạo ra khí cay."),
             ("f", "2. Khí cay bay lên mắt, dây thần kinh báo động → chảy nước mắt."),
             ("f", "3. Lưỡi dao ép mô càng mạnh → càng nhiều tế bào vỡ, nước bắn ra."),
             ("o", "A. Dao cùn, cắt thật nhanh"), ("o", "B. Dao sắc, cắt chậm rãi"), ("o", "C. Dao cùn, cắt chậm, nhẹ tay")]
    c.css.append(f"#s05-card {{ left: 140px; top: 120px; width: 1100px; color: {INK}; }}"
                 "#s05-card .h { font-size: 84px; font-weight: 800; margin-bottom: 34px; letter-spacing: -0.01em; }"
                 "#s05-card .f { font-size: 38px; font-weight: 600; line-height: 1.3; margin-bottom: 18px; }"
                 "#s05-card .o { font-size: 46px; font-weight: 800; margin-top: 10px; }"
                 "#s05-card .gap { height: 30px; }")
    items = []
    for k, (cls, tx) in enumerate(lines):
        if cls == "o" and lines[k - 1][0] == "f":
            items.append('<div class="gap"></div>')
        items.append(f'<div id="s05-l{k}" class="{cls}">{tx}</div>')
    c.html.append(f'<div id="s05-card" class="txt" data-hold="true">{"".join(items)}</div>')
    for k in range(len(lines)):
        c.blur_in(f"#s05-l{k}", 0.1 + 0.07 * k, 0.18)
    c.hide("#s05-n2", "#s05-n1")
    c.sfx("pop", 0.2)
    c.tl.ft("#s05-n3", {"scale": 0.4, "transformOrigin": "50% 50%"},
            {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.5, "ease": "back.out(1.8)"}, 0.2)
    for a, b, t in ((3, 2, 3.4), (2, 1, 6.4)):
        c.show(f"#s05-n{a}", t, False)
        c.pop(f"#s05-n{b}", t, 0.5, "50% 50%", "back.out(1.8)", 0.4)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 06 · Chìa khóa
def s06():
    s = SCENES["06"]
    c = Comp("s06", s["start"], s["end"])
    c.svg.append(slate_frame())
    board_to(c, "s06-to")
    c.svg.append(g("s06-bub", f"""<circle cx="560" cy="560" r="18" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>
<circle cx="640" cy="500" r="28" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>
<path d="M760 420 C700 300 820 170 980 210 C1060 120 1300 110 1380 190 C1520 120 1760 190 1740 320 C1830 380 1790 560 1640 560 C1580 650 1340 650 1260 590 C1140 660 900 650 860 560 C720 590 650 470 760 420 Z" fill="{PAPER}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
<rect x="880" y="268" width="390" height="112" rx="14" fill="{GAS}"/>
{text(900, 356, "KHÍ CAY", 88, 900, INK)}
{text(1320, 356, "CÓ SẴN", 88, 900, INK)}
<line id="s06-strike" x1="1300" y1="326" x2="1660" y2="326" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>
{text(900, 500, "TẾ BÀO VỠ → KHÍ CAY", 70, 900, INK, id_="s06-new")}"""))
    c.svg.append(slate_border())
    c.css.append(f"#s06-qs {{ left: 700px; top: 760px; width: 1120px; font-size: 76px; font-weight: 800; color: {WHITE}; "
                 f"line-height: 1.15; letter-spacing: -0.01em; }} #s06-qs b {{ color: {YELLOW}; font-weight: 900; }}")
    c.html.append('<div id="s06-qs" class="txt">Cách nào làm vỡ <b>ÍT</b> tế bào nhất?</div>')
    idle(c, "s06-to", 0, c.loc(s["end"]), 0)
    c.tl.set("#s06-to .mat", {"x": 6, "y": -6}, 0)
    c.pop("#s06-bub", 0.15, 0.6, "0% 100%", "back.out(1.3)", 0.3)
    c.sfx("pop", 0.15)
    c.draw("#s06-strike", c.at("06", "không có sẵn", which="end", off=-0.3), 0.4)
    c.blur_in("#s06-new", c.at("06", "tế bào vỡ"), 0.2)
    c.blur_in("#s06-qs", c.at("06", "cách nào"), 0.2)
    return c


# ---------------------------------------------------------------- 07–09 · Bảng giải thích
def s07():
    s, e = SCENES["07"], SCENES["09"]
    c = Comp("s07", s["start"], e["end"])
    mpos = [(770, 480), (880, 480), (770, 600), (880, 600), (770, 720), (880, 720)]
    mols = "".join(molecule(f"s07-m{k}", x, y) for k, (x, y) in enumerate(mpos))
    inter = "".join(place(x + 10, y - 8, g(f"s07-i{k}", f'<circle r="15" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>'))
                    for k, (x, y) in enumerate(mpos))
    scis = "".join(scissors(f"s07-x{k}", 1150, 480 + k * 120, 1.0) for k in range(3))
    enz = "".join(enzyme2(f"s07-e{k}", 1420, 480 + k * 120, 1.0) for k in range(3))
    tears = "".join(tear(f"s07-t{k}", 1462, 640, 1.0) for k in range(3))
    nerve = lambda id_, d: (f'<path id="{id_}" d="{d}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" '
                            f'fill="none" stroke="{YELLOW}" stroke-width="12" stroke-linecap="round"/>')
    A = f"""<g id="s07-cellg"><rect x="680" y="380" width="620" height="460" rx="44" fill="{CELL}" stroke="{INK}" stroke-width="8"/>
<line id="s07-div-a" x1="1000" y1="400" x2="1000" y2="610" stroke="{INK}" stroke-width="7" stroke-dasharray="20 14"/>
<line id="s07-div-b" x1="1000" y1="610" x2="1000" y2="820" stroke="{INK}" stroke-width="7" stroke-dasharray="20 14"/>
<g id="s07-mols">{mols}</g>{inter}<g id="s07-scis">{scis}</g></g>
<g id="s07-enz">{enz}</g>
{text(700, 350, "LƯU HUỲNH", 40, 800, TEAL, id_="s07-lb1")}
{text(1060, 350, "ENZYME CẮT", 40, 800, GREY, id_="s07-lb2")}
{text(760, 895, "ENZYME 2", 40, 800, YELLOW, id_="s07-lb3")}
{gas_cloud("s07-cloud", 990, 290, 1.0, "KHÍ CAY")}
{nerve("s07-nv1", "M1478 520 C1520 430 1580 360 1650 300")}
{nerve("s07-nv2", "M1720 300 C1760 360 1760 410 1730 450")}
{eye_side("s07-eye", 1620, 600, 140)}
{brain("s07-brain", 1700, 210, 0.75)}
{gland("s07-gland", 1720, 470, 1.0)}
{tears}
{text(1340, 820, "GIÁC MẠC", 40, 800, WHITE, id_="s07-lb4")}
{text(1500, 130, "NÃO", 40, 800, WHITE, "end", id_="s07-lb5")}
{text(1745, 410, "TUYẾN LỆ", 36, 800, WHITE, "middle", id_="s07-lb6")}
{text(1620, 990, "PHẢN XẠ BẢO VỆ", 60, 900, WHITE, "middle", id_="s07-lb7", extra=" " + OUTLINE)}"""
    B = f"""{cell_row("s07-L", 700, 720, 5, 80, 120)}
{cell_row("s07-R", 1290, 720, 6, 80, 120)}
{droplets("s07-dl", 912, 700, 4)}
{droplets("s07-dr", 1545, 700, 16, 14)}
{blade_tip("s07-bl", 912, 330, sharp=True)}
{blade_tip("s07-br", 1545, 330, sharp=False)}
{text(912, 920, "MŨI SẮC", 44, 900, WHITE, "middle", id_="s07-lb8")}
{text(1545, 920, "MŨI CÙN", 44, 900, CORAL, "middle", id_="s07-lb9")}
<g id="s07-film"><rect x="700" y="80" width="150" height="104" rx="12" fill="{INK}"/>
{"".join(f'<rect x="{712 + k * 34}" y="{88}" width="20" height="14" rx="3" fill="{WHITE}"/><rect x="{712 + k * 34}" y="{162}" width="20" height="14" rx="3" fill="{WHITE}"/>' for k in range(4))}
<rect x="722" y="110" width="106" height="44" rx="6" fill="{TEAR}"/>
{text(880, 140, "ĐẠI HỌC CORNELL · 2025", 46, 900, WHITE)}</g>
{text(880, 190, "5.000–20.000 khung hình mỗi giây", 34, 600, GREY, id_="s07-fps")}
{text(1010, 560, "×1", 100, 900, WHITE, "middle", id_="s07-x1", extra=" " + OUTLINE)}
{text(1650, 340, "×40", 150, 900, CORAL, "middle", id_="s07-x40", extra=" " + OUTLINE)}
{nerve("s07-streak", "M1500 690 L1390 430").replace(YELLOW, WHITE)}
{text(1370, 420, "40 m/s", 64, 900, WHITE, "end", id_="s07-v40", extra=" " + OUTLINE)}
{text(1250, 1010, "CẮT NHANH → ×4 GIỌT", 56, 900, YELLOW, "middle", id_="s07-x4", extra=" " + OUTLINE)}
{text(70, 1030, "Wu et al., PNAS 2025", 28, 500, GREY, id_="s07-src")}"""
    C = (options("s07-o")
         + f'<ellipse id="s07-ring" cx="1275" cy="530" rx="595" ry="128" pathLength="1" stroke-dasharray="1 1.2" '
           f'stroke-dashoffset="1.1" fill="none" stroke="{YELLOW}" stroke-width="12"/>')
    c.svg += [slate_frame(), g("s07-a", A), g("s07-b", B), g("s07-c", C)]
    board_to(c, "s07-suy")
    board_to(c, "s07-vui", "vui", hidden=True)
    c.svg.append(slate_border())
    end = c.loc(e["end"])
    c.hide("#s07-cellg", "#s07-enz", "#s07-cloud", "#s07-eye", "#s07-brain", "#s07-gland",
           "#s07-b", "#s07-c", *[f"#s07-lb{k}" for k in range(1, 8)], *[f"#s07-i{k}" for k in range(6)],
           *[f"#s07-t{k}" for k in range(3)])
    c.tl.set("#s07-suy .mat", {"x": 7}, 0)
    # A · bên trong tế bào
    c.pop("#s07-cellg", c.at("07", "phóng to"), 0.7, "50% 50%", "expo.out", 0.15)
    c.sfx("pop", c.at("07", "phóng to"))
    tl_ = c.at("07", "lưu huỳnh")
    c.blur_in("#s07-lb1", tl_)
    for k in range(6):
        c.tl.ft(f"#s07-m{k}", {"scale": 0, "transformOrigin": "50% 50%"},
                {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.4, "ease": "back.out(2)"}, tl_ - 0.4 + 0.06 * k)
    tk = c.at("07", "chiếc kéo", 0)
    for k in range(3):
        c.tl.ft(f"#s07-x{k}", {"scale": 0, "transformOrigin": "50% 50%"},
                {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.4, "ease": "back.out(2)"}, c.at("07", "một enzyme") + 0.08 * k)
    c.blur_in("#s07-lb2", tk)
    tr = c.at("07", "màng ngăn rách")
    c.tl.to("#s07-div-a", {"rotation": -28, "y": -50, "opacity": 0, "transformOrigin": "50% 0%", "duration": 0.5, "ease": "power3.out"}, tr + 0.3)
    c.tl.to("#s07-div-b", {"rotation": 28, "y": 50, "opacity": 0, "transformOrigin": "50% 100%", "duration": 0.5, "ease": "power3.out"}, tr + 0.3)
    tcut = c.at("07", "chiếc kéo", 1)
    c.tl.to("#s07-scis", {"x": -200, "duration": 0.7, "ease": "power2.inOut"}, tcut)
    ttg = c.at("07", "chất trung gian", 0)
    for k in range(6):
        c.tl.to(f"#s07-m{k}", {"scale": 0, "transformOrigin": "50% 50%", "duration": 0.25, "ease": "power3.in"}, ttg + 0.05 * k)
        c.show(f"#s07-i{k}", ttg + 0.2 + 0.05 * k)
        c.tl.ft(f"#s07-i{k}", {"scale": 0, "transformOrigin": "50% 50%"},
                {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.35, "ease": "back.out(2)"}, ttg + 0.2 + 0.05 * k)
    te2 = c.at("07", "enzyme thứ hai")
    c.show("#s07-enz", te2)
    c.tl.ft("#s07-enz", {"x": 300}, {"x": -440, "duration": 0.9, "ease": "expo.out"}, te2)
    c.blur_in("#s07-lb3", te2 + 0.3)
    tkc = c.at("07", "thành khí cay")
    for k, (x, y) in enumerate(mpos):
        c.tl.to(f"#s07-i{k}", {"x": 990 - x, "y": 290 - y, "scale": 0.3, "opacity": 0, "duration": 0.6, "ease": "power2.in"}, tkc + 0.04 * k)
    c.pop("#s07-cloud", tkc + 0.5, 0.6, "50% 100%", "back.out(1.6)", 0.2)
    tkb = c.at("07", "Khí bay lên mắt")
    c.pop("#s07-eye", tkb, 0.6, "50% 50%", "back.out(1.4)", 0.4)
    c.sfx("pop", tkb)
    c.tl.to("#s07-cloud", {"x": 380, "y": 270, "scale": 0.85, "duration": 1.3, "ease": "power2.inOut"}, tkb + 0.2)
    c.tl.to("#s07-suy .mat", {"x": 10, "y": -4, "duration": 0.4}, tkb)
    tdt = c.at("07", "Dây thần kinh")
    c.draw("#s07-nv1", tdt, 0.8)
    c.blur_in("#s07-lb4", c.at("07", "giác mạc"))
    tn = c.at("07", "não", 0)
    c.pop("#s07-brain", tn, 0.5)
    c.sfx("pop", tn)
    c.blur_in("#s07-lb5", tn + 0.1)
    tn2 = c.at("07", "não", 1)
    c.draw("#s07-nv2", tn2, 0.6)
    c.pop("#s07-gland", c.at("07", "tuyến lệ"), 0.5)
    c.sfx("pop", c.at("07", "tuyến lệ"))
    c.blur_in("#s07-lb6", c.at("07", "tuyến lệ", off=0.1))
    tx = c.at("07", "xả nước")
    for k in range(3):
        c.show(f"#s07-t{k}", tx + 0.35 * k)
        c.tl.ft(f"#s07-t{k}", {"y": 0, "opacity": 1}, {"y": 190, "opacity": 0, "duration": 0.9, "ease": "power2.in"}, tx + 0.35 * k)
    c.tl.to("#s07-cloud", {"scale": 0.2, "opacity": 0, "duration": 0.7, "ease": "power2.in"}, c.at("07", "rửa sạch"))
    c.pop("#s07-lb7", c.at("07", "phản xạ bảo vệ"), 0.5)
    # B · lưỡi dao
    tb0 = c.at("08", "Giờ hãy nhìn")
    c.blur_out("#s07-a", tb0, 0.25)
    c.sfx("whoosh", tb0)
    c.show("#s07-b", tb0 + 0.2)
    c.hide(*[f"#s07-lb{k}" for k in (8, 9)], "#s07-film", "#s07-fps", "#s07-x1", "#s07-x40", "#s07-v40", "#s07-x4", "#s07-src")
    c.tl.ft("#s07-bl", {"y": -500}, {"y": 0, "duration": 0.7, "ease": "expo.out"}, tb0 + 0.3)
    c.tl.ft("#s07-br", {"y": -500}, {"y": 0, "duration": 0.7, "ease": "expo.out"}, tb0 + 0.45)
    c.tl.to("#s07-suy .mat", {"x": 8, "y": 0, "duration": 0.3}, tb0)
    tm = c.at("08", "mũi rất mỏng")
    c.blur_in("#s07-lb8", tm)
    tg = c.at("08", "cắt gọn")
    c.tl.to("#s07-bl", {"y": 470, "duration": 0.45, "ease": "power2.in"}, tg)
    c.tl.to("#s07-L-2-b", {"opacity": 1, "duration": 0.12}, tg + 0.3)
    c.sfx("chop", tg + 0.3, 0.3)
    burst(c, "s07-dl", 4, tg + 0.3, dist=(80, 140))
    tt = c.at("08", "mũi tù")
    c.blur_in("#s07-lb9", tt)
    tdm = c.at("08", "đè mạnh")
    c.tl.to("#s07-br", {"y": 360, "duration": 0.6, "ease": "power2.in"}, tdm)
    teb = c.at("08", "ép bẹp")
    for k, sy in ((1, 0.84), (2, 0.68), (3, 0.68), (4, 0.84)):
        c.tl.to(f"#s07-R-{k}", {"scaleY": sy, "transformOrigin": "50% 100%", "duration": 0.9, "ease": "power1.inOut"}, teb)
    c.tl.to("#s07-R-skin", {"y": 34, "duration": 0.9, "ease": "power1.inOut"}, teb)
    c.tl.to("#s07-br", {"y": 400, "duration": 0.9, "ease": "power1.inOut"}, teb)
    txq = c.at("08", "xuyên qua")
    c.tl.to("#s07-br", {"y": 470, "duration": 0.14, "ease": "power3.in"}, txq)
    c.sfx("chop", txq + 0.1)
    for j, k in enumerate((2, 3, 1, 4, 0, 5)):
        c.tl.to(f"#s07-R-{k}-b", {"opacity": 1, "duration": 0.12}, txq + 0.1 + 0.07 * j)
    burst(c, "s07-dr", 16, txq + 0.1, dist=(180, 420))
    tco = c.at("08", "Đại học Cornell")
    c.pop("#s07-film", tco, 0.5, "0% 50%")
    c.blur_in("#s07-src", tco)
    c.blur_in("#s07-fps", c.at("08", "hàng nghìn khung hình"))
    t40 = c.at("08", "bốn mươi lần")
    c.pop("#s07-x40", t40, 0.55)
    c.sfx("thump", t40)
    c.pop("#s07-x1", t40 + 0.35, 0.45)
    burst(c, "s07-dr", 16, t40 - 0.4, dist=(180, 420))
    tms = c.at("08", "bốn mươi mét")
    c.draw("#s07-streak", tms, 0.3, "power3.out")
    c.pop("#s07-v40", tms + 0.15, 0.45, "100% 50%")
    c.pop("#s07-x4", c.at("08", "Cắt càng nhanh"), 0.5)
    # C · loại trừ
    tc0 = c.at("09", "Giờ hãy loại trừ")
    c.blur_out("#s07-b", tc0, 0.25)
    c.sfx("whoosh", tc0)
    c.show("#s07-c", tc0 + 0.2)
    for j, L in enumerate("abc"):
        c.tl.ft(f"#s07-o{L}", {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "expo.out"}, tc0 + 0.25 + 0.1 * j)
    for L, nth in (("a", 1), ("c", 2)):
        tp = c.at("09", f"Phương án {L.upper()}")
        c.tl.ft(f"#s07-o{L}-box", {"opacity": 0}, {"opacity": 1, "duration": 0.2}, tp)
        tlo = c.at("09", "Loại", nth)
        c.draw(f"#s07-o{L}-strike", tlo, 0.3, "power3.out")
        c.sfx("pop", tlo)
        c.tl.to(f"#s07-o{L}-box", {"opacity": 0, "duration": 0.2}, tlo + 0.5)
        c.tl.to(f"#s07-o{L}", {"opacity": 0.5, "duration": 0.3}, tlo + 0.6)
    tb = c.at("09", "phương án B")
    c.draw("#s07-ring", tb, 0.6)
    c.sfx("pop", tb)
    swap(c, "s07-suy", "s07-vui", c.at("09", "Còn lại"))
    c.tl.ft("#s07-ob", {"scale": 1}, {"scale": 1.05, "transformOrigin": "40% 50%", "duration": 0.25, "yoyo": True, "repeat": 1,
                                      "ease": "power2.out"}, c.at("09", "Ít tế bào vỡ nhất"))
    idle(c, "s07-suy", 0, c.at("09", "Còn lại"), 3)
    idle(c, "s07-vui", c.at("09", "Còn lại") + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 10 · Đáp án
def s10():
    s = SCENES["10"]
    c = Comp("s10", s["start"], s["end"])
    hx, hy = 1165, 642
    slices = "".join(place(1030 - k * 34, 662, g(f"s10-sl{k}", f'<ellipse rx="22" ry="12" fill="#F1E3C2" stroke="{INK}" stroke-width="4"/>'))
                     for k in range(4))
    world = [kitchen_back("s10", 6, 40), to("s10-to", "dung", TO_X, TO_Y, TO_H), kitchen_front(),
             basket("s10-basket", 420, 584, 5, 1.1), cutting_board(900, 668, 500, 34), slices,
             onion("s10-onion", 1110, 612, 0.62), knife("s10-knife", hx, hy, 0.9, 0, sharp=True, flip=True),
             sparkle("s10-sp1", EYE_R[0] + 70, EYE_R[1] - 50, 1.2), sparkle("s10-sp2", EYE_L[0] - 70, EYE_L[1] - 40, 0.9)]
    c.svg += [g("s10-k", f'<g id="s10-settle"><g id="s10-cam">{"".join(world)}</g></g>'),
              g("s10-b", f'<rect width="1920" height="1080" fill="{SLATE}"/>'
                         + text(960, 720, "B", 560, 900, YELLOW, "middle", extra=" " + OUTLINE)
                         + f'<circle id="s10-ring" cx="960" cy="530" r="300" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" fill="none" stroke="{YELLOW}" stroke-width="16"/>'
                         + slate_border())]
    tk = c.at("10", "Bạn chọn")
    c.tl.ft("#s10-b", {"scale": 1.3, "svgOrigin": "960 540", "filter": "blur(10px)", "opacity": 0},
            {"scale": 1, "svgOrigin": "960 540", "filter": "blur(0px)", "opacity": 1, "duration": 0.35, "ease": "power3.out"}, 0.05)
    c.draw("#s10-ring", 0.4, 0.5)
    c.sfx("riser", 0.3)
    c.sfx("thump", 0.3)
    c.show("#s10-b", tk, False)
    frame(c, tk, 1060, 470, 1.35, "#s10-cam", "#s10-settle")
    c.hide("#s10-sp1", "#s10-sp2", *[f"#s10-sl{k}" for k in range(4)])
    c.tl.ft("#s10-knife", {"rotation": 0}, {"rotation": 12, "transformOrigin": "17% 50%", "duration": 0.42, "ease": "sine.inOut",
                                             "yoyo": True, "repeat": 5}, tk + 0.3)
    for k in range(4):
        c.pop(f"#s10-sl{k}", tk + 0.75 + 0.84 * k, 0.3)
        c.sfx("chop", tk + 0.75 + 0.84 * k)
    for k in range(4, 0, -1):
        c.tl.to(f"#s10-basket-o{k}", {"scale": 0, "transformOrigin": "50% 100%", "duration": 0.3, "ease": "back.in(2)"},
                tk + 0.4 + 0.75 * (4 - k))
    tr = c.at("10", "mắt bạn vẫn ráo")
    for k, sp in enumerate(("#s10-sp1", "#s10-sp2")):
        c.pop(sp, tr + 0.15 * k, 0.4)
        c.tl.ft(sp, {"rotation": 0}, {"rotation": 90, "duration": 1.0, "ease": "power2.out"}, tr + 0.15 * k + 0.5)
    idle(c, "s10-to", tk, c.loc(s["end"]), 2)
    return c


# ---------------------------------------------------------------- 11 · Bất ngờ
def s11():
    s = SCENES["11"]
    c = Comp("s11", s["start"], s["end"])
    drops = lambda pfx, x, y, n: "".join(
        f'<circle id="{pfx}-{k}" cx="{x + (k % 5) * 56}" cy="{y + (k // 5) * 56}" r="20" fill="{CELL}" stroke="{INK}" stroke-width="4"/>'
        for k in range(n))
    A = f"""{fridge("s11-fr", 740, 220, 400, 700)}
{text(1250, 360, "HÀNH THƯỜNG", 44, 900, WHITE, id_="s11-lt")}{g("s11-dt", drops("s11-dt", 1270, 410, 5))}
{text(1250, 600, "HÀNH ƯỚP LẠNH 1 °C", 44, 900, TEAR, id_="s11-ll")}{g("s11-dl", drops("s11-dl", 1270, 650, 9))}
{text(940, 560, "?", 300, 900, CORAL, "middle", id_="s11-q", extra=" " + OUTLINE)}
<g transform="translate(1290 930) rotate(-5)"><g id="s11-stamp"><rect x="-430" y="-62" width="860" height="110" rx="14" fill="{SLATE}" stroke="{CORAL}" stroke-width="10"/>
{text(0, 18, "CHƯA ĐƯỢC CHỨNG MINH", 60, 900, CORAL, "middle")}</g></g>"""
    B = f"""{text(700, 420, "2002", 230, 900, WHITE, id_="s11-y")}
{enzyme2("s11-enz", 1420, 330, 2.2)}
{text(1420, 480, "ENZYME TẠO KHÍ CAY", 44, 900, YELLOW, "middle", id_="s11-el")}
{text(720, 560, "TRƯỚC ĐÓ: TƯỞNG KHÍ TỰ SINH", 50, 800, WHITE, id_="s11-my")}
<line id="s11-ms" x1="710" y1="542" x2="1490" y2="542" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>
{medal("s11-medal", 1700, 770, 1.0)}
{switch("s11-sw", 820, 840, 0.9)}
{onion("s11-on", 1080, 900, 0.55)}
{gas_cloud("s11-cl", 1080, 790, 0.7)}"""
    c.svg += [slate_frame(), g("s11-a", A), g("s11-b", B)]
    board_to(c, "s11-suy")
    board_to(c, "s11-ngac", "ngac-nhien", hidden=True)
    board_to(c, "s11-vui", "vui", hidden=True)
    c.svg.append(slate_border())
    c.hide("#s11-fr", "#s11-lt", "#s11-dt", "#s11-ll", "#s11-dl", "#s11-q", "#s11-stamp", "#s11-b",
           "#s11-y", "#s11-enz", "#s11-el", "#s11-my", "#s11-medal", "#s11-sw", "#s11-on", "#s11-cl")
    c.tl.set("#s11-suy .mat", {"x": 7}, 0)
    c.pop("#s11-fr", c.at("11", "tủ lạnh"), 0.6, "50% 100%", "back.out(1.4)", 0.5)
    c.sfx("pop", c.at("11", "tủ lạnh"))
    c.tl.ft("#s11-fr-door", {"scaleX": 1}, {"scaleX": 0.1, "transformOrigin": "0% 50%", "duration": 0.6, "ease": "power3.inOut"},
            c.at("11", "trước khi cắt"))
    c.sfx("whoosh", c.at("11", "trước khi cắt"))
    tl1 = c.at("11", "hành ướp lạnh")
    c.blur_in("#s11-lt", tl1)
    c.show("#s11-dt", tl1)
    for k in range(5):
        c.tl.ft(f"#s11-dt-{k}", {"scale": 0, "transformOrigin": "50% 50%"},
                {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "back.out(2)"}, tl1 + 0.06 * k)
    tl2 = c.at("11", "ít giọt hơn")
    c.blur_in("#s11-ll", tl2)
    c.show("#s11-dl", tl2)
    for k in range(9):
        c.tl.ft(f"#s11-dl-{k}", {"scale": 0, "transformOrigin": "50% 50%"},
                {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "back.out(2)"}, c.at("11", "nhiều hơn") + 0.06 * k
                if k >= 5 else tl2 + 0.06 * k)
    c.pop("#s11-q", c.at("11", "cần thêm thí nghiệm"), 0.5)
    c.sfx("pop", c.at("11", "cần thêm thí nghiệm"))
    c.tl.to("#s11-q", {"autoAlpha": 0, "duration": 0.2}, c.at("11", "chưa được chứng minh") - 0.1)
    c.show("#s11-stamp", c.at("11", "chưa được chứng minh"))
    c.sfx("thump", c.at("11", "chưa được chứng minh") + 0.3)
    c.tl.ft("#s11-stamp", {"scale": 1.7, "transformOrigin": "50% 50%"},
            {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "power4.in"}, c.at("11", "chưa được chứng minh"))
    # B
    tb = c.at("11", "Và còn một điều")
    c.blur_out("#s11-a", tb, 0.25)
    c.sfx("whoosh", tb)
    c.show("#s11-b", tb + 0.2)
    swap(c, "s11-suy", "s11-ngac", c.at("11", "bất ngờ"))
    ty = c.at("11", "năm 2002")
    c.pop("#s11-y", ty, 0.5, "0% 100%")
    c.sfx("pop", ty)
    te = c.at("11", "enzyme chuyên tạo khí cay")
    c.pop("#s11-enz", te, 0.5)
    c.blur_in("#s11-el", te + 0.2)
    c.blur_in("#s11-my", c.at("11", "Trước đó"))
    c.draw("#s11-ms", c.at("11", "tự sinh ra", which="end"), 0.35, "power3.out")
    tig = c.at("11", "Ig Nobel")
    c.show("#s11-medal", tig)
    c.sfx("whoosh", tig)
    c.tl.ft("#s11-medal", {"rotation": -28, "y": -200}, {"rotation": 0, "y": 0, "transformOrigin": "50% 0%", "duration": 1.6,
                                                         "ease": "elastic.out(1, 0.35)"}, tig)
    swap(c, "s11-ngac", "s11-vui", c.at("11", "bật cười"))
    tg = c.at("11", "tắt gen")
    c.pop("#s11-sw", tg - 0.3, 0.4)
    c.pop("#s11-on", tg - 0.2, 0.4, "50% 100%")
    c.pop("#s11-cl", tg - 0.1, 0.4, "50% 100%")
    c.tl.to("#s11-sw-lever", {"y": 70, "fill": CORAL, "duration": 0.25, "ease": "back.out(2)"}, tg + 0.2)
    c.sfx("pop", tg + 0.2)
    c.tl.to("#s11-cl", {"scale": 0.3, "transformOrigin": "50% 100%", "duration": 0.8, "ease": "power2.inOut"}, c.at("11", "rất ít khí cay"))
    idle(c, "s11-suy", 0, c.at("11", "bất ngờ"), 0)
    idle(c, "s11-ngac", c.at("11", "bất ngờ") + 0.6, c.at("11", "bật cười"), 2)
    idle(c, "s11-vui", c.at("11", "bật cười") + 0.6, c.loc(s["end"]), 4)
    return c


# ---------------------------------------------------------------- 12 · Kết
def s12():
    s = SCENES["12"]
    c = Comp("s12", s["start"], s["end"])
    S = [c.loc(t) for t in sentence_starts("12")]
    hand = to_point(TO_X, TO_Y, TO_H, 322, 216)
    world = [kitchen_back("s12", 7, 0), bell("s12-bell", 640, 360, 1.0),
             g("s12-ding", f'<path d="M560 300 l-34 -20 M560 360 h-40 M560 420 l-34 20 M720 300 l34 -20 M720 360 h40 M720 420 l34 20" '
                           f'stroke="{YELLOW}" stroke-width="10" stroke-linecap="round"/>'),
             plate("s12-plate", hand[0] + 30, hand[1] - 20, 0.9),
             to("s12-vui", "vui", TO_X, TO_Y, TO_H), to("s12-ngac", "ngac-nhien", TO_X, TO_Y, TO_H), kitchen_front(), cutting_board(960, 668, 440, 34),
             rice_cooker("s12-rc", 560, 610, 1.0),
             sparkle("s12-sp1", EYE_R[0] + 70, EYE_R[1] - 50, 1.2), sparkle("s12-sp2", EYE_L[0] - 70, EYE_L[1] - 40, 0.9)]
    c.svg.append(f'<g id="s12-settle"><g id="s12-cam">{"".join(world)}</g></g>')
    c.hide("#s12-ngac-w", "#s12-ding", "#s12-sp1", "#s12-sp2")
    cam, st = "#s12-cam", "#s12-settle"
    frame(c, 0, 960, 540, 1.0, cam, st)
    tk = c.at("12", "Khách tới")
    c.show("#s12-ding", tk)
    c.tl.ft("#s12-bell", {"rotation": 0}, {"rotation": 14, "transformOrigin": "50% 0%", "duration": 0.09, "yoyo": True, "repeat": 7,
                                            "ease": "sine.inOut"}, tk)
    c.show("#s12-ding", tk + 0.8, False)
    frame(c, S[2], 1150, 420, 1.5, cam, st)
    tr = c.at("12", "mắt ráo hoảnh")
    for k, sp in enumerate(("#s12-sp1", "#s12-sp2")):
        c.pop(sp, tr + 0.15 * k, 0.4)
    c.tl.ft("#s12-vui", {"scale": 1}, {"scale": 1.04, "transformOrigin": "50% 100%", "duration": 0.4, "ease": "back.out(2)"},
            c.at("12", "tự hào"))
    tn = c.at("12", "nồi cơm")
    frame(c, tn, 560, 590, 2.4, cam, st)
    tc = c.at("12", "chưa cắm")
    frame(c, tc, 1110, 380, 2.2, cam, st)
    c.show("#s12-vui-w", tc, False)
    c.show("#s12-plate", tc, False)
    c.show("#s12-sp1", tc, False)
    c.show("#s12-sp2", tc, False)
    c.show("#s12-ngac-w", tc)
    idle(c, "s12-vui", 0, tc, 1)
    idle(c, "s12-ngac", tc, c.loc(s["end"]), 3)
    return c


# ---------------------------------------------------------------- 13 · Thẻ cuối
def s13():
    s = SCENES["13"]
    c = Comp("s13", s["start"], s["end"])
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', to("s13-to", "vui", 1380, 330, 680)]
    lines = [("big", "Dao sắc, cắt chậm:<br>ít tế bào vỡ, ít cay."),
             ("lab", "Nguồn"),
             ("src", "Imai và cộng sự, <i>Nature</i> 419:685 (2002)"),
             ("src", "Eady và cộng sự, <i>Plant Physiology</i> 147:2096 (2008)"),
             ("src", "Wu và cộng sự, <i>PNAS</i> 122(42) (2025) — Đại học Cornell"),
             ("src", "StatPearls: Corneal Reflex (NCBI Bookshelf)"),
             ("safe", "Dao sắc cũng dễ đứt tay hơn — cắt chậm và cẩn thận.")]
    c.css.append(f"#s13-card {{ left: 140px; top: 130px; width: 1220px; color: {INK}; }}"
                 "#s13-card .big { font-size: 92px; font-weight: 800; line-height: 1.12; letter-spacing: -0.01em; margin-bottom: 60px; }"
                 "#s13-card .lab { font-size: 36px; font-weight: 800; color: #B5372A; margin-bottom: 14px; }"
                 "#s13-card .src { font-size: 34px; font-weight: 500; line-height: 1.45; color: #2A3A4A; }"
                 "#s13-card .safe { font-size: 36px; font-weight: 700; margin-top: 54px; }")
    c.html.append('<div id="s13-card" class="txt" data-hold="true">'
                  + "".join(f'<div id="s13-l{k}" class="{cls}">{tx}</div>' for k, (cls, tx) in enumerate(lines)) + "</div>")
    for k in range(len(lines)):
        c.blur_in(f"#s13-l{k}", 0.2 + 0.12 * k, 0.2)
    c.tl.ft("#s13-to", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "expo.out"}, 0.3)
    c.tl.ft("#s13-to .tay-phai", {"rotation": 0}, {"rotation": -14, "transformOrigin": "20% 90%", "duration": 0.35, "ease": "sine.inOut",
                                                    "yoyo": True, "repeat": 5}, 1.0)
    idle(c, "s13-to", 0.3, c.loc(s["end"]), 2)
    return c


BUILDERS = [s01, s02, s03, s04, s05, s06, s07, s10, s11, s12, s13]


sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from cau_hinh import FFMPEG  # noqa: E402


def prep_audio():
    """Chuẩn hóa lời đọc về -16 LUFS (đỉnh -1,5 dB) và chép nhạc vào assets/ khi nguồn mới hơn."""
    import shutil
    import subprocess
    src, dst = EP / "audio" / "loi-doc.wav", VID / "assets" / "loi-doc.wav"
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(src), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", "48000", str(dst)], check=True)
    (VID / "assets" / "bgm").mkdir(exist_ok=True)
    for m in ("bgm_001.wav", "bgm_002.wav"):
        if not (VID / "assets" / "bgm" / m).exists():
            shutil.copy(VID / ".media" / "audio" / "bgm" / m, VID / "assets" / "bgm" / m)


def music_tags():
    """Nhạc nền: pizzicato cho truyện và kết, marimba nối 3 lần cho phần bảng.
    Mức 0,14 dưới lời đọc; nâng lên 0,35 khi không có lời (tiêu đề, đếm ngược, thẻ cuối)."""
    t_story = SCENES["03"]["start"]
    t_pause0, t_pause1 = SCENES["05"]["start"], SCENES["05"]["end"]
    t_ans, t_card = SCENES["10"]["start"], SCENES["13"]["start"]
    lo, hi = 0.14, 0.35

    def lane(points):
        pts = ",".join(f'{{"t":{t:.2f},"v":{v}}}' for t, v in points)
        return f"data-automation='{{\"version\":1,\"lanes\":[{{\"target\":\"volume\",\"points\":[{pts}]}}]}}'"

    clips = []
    # 1 · pizzicato: tiêu đề + mở truyện
    clips.append(("bgm1", "bgm/bgm_001.wav", 0, t_story + 0.6, 0, 0.0, 0.8,
                  lane([(0, hi), (SCENES["01"]["end"] - 0.4, hi), (SCENES["01"]["end"] + 0.4, lo)])))
    # 2 · marimba x3, mỗi đoạn 44 s, chồng mờ 1,2 s
    seg, xf, t = 44.0, 1.2, t_story
    k = 0
    while t < t_ans - 3:
        dur = min(seg, t_ans + 0.6 - t)
        pts = [(0, lo)]
        if t < t_pause1 and t + dur > t_pause0:
            pts = [(0, lo), (max(t_pause0 + 0.3 - t, 0), lo), (max(t_pause0 + 1.0 - t, 0.01), hi),
                   (t_pause1 - 0.6 - t, hi), (t_pause1 - t, lo)]
        clips.append((f"bgm2{k}", "bgm/bgm_002.wav", t, dur, 0, xf if k else 0.6, xf, lane(pts)))
        t += seg - xf
        k += 1
    # 3 · pizzicato: đáp án → hết, nâng ở thẻ cuối, mờ dần 2 s cuối
    clips.append(("bgm3", "bgm/bgm_001.wav", t_ans, DURATION - t_ans, 0, 0.6, 2.0,
                  lane([(0, lo), (t_card + 0.3 - t_ans, lo), (t_card + 1.2 - t_ans, hi)])))
    return "\n".join(
        f'      <audio id="{i}" class="clip" data-start="{s:.3f}" data-duration="{d:.3f}" data-track-index="{40 + n}" '
        f'data-volume="1" data-media-start="{ms}" data-fade-in="{fi}" data-fade-out="{fo}" {ln} src="assets/{f}"></audio>'
        for n, (i, f, s, d, ms, fi, fo, ln) in enumerate(clips))


def write_index(comps):
    prep_audio()
    sfx_tags = "\n".join(
        f'      <audio id="sfx{k:02d}" class="clip" data-start="{max(t, 0):.3f}" data-duration="{dur:.3f}" '
        f'data-track-index="{31 + k % 3}" data-volume="{v}"'
        + (f' data-media-start="{ms}"' if ms else "") + f' data-fade-out="0.08" src="assets/sfx/{f}"></audio>'
        for k, (t, f, dur, v, ms) in enumerate(sorted(SFX_EVENTS)))
    hosts = "\n".join(
        f'      <div id="{c.cid}" data-composition-id="{c.cid}" data-composition-src="compositions/{c.cid}.html" '
        f'data-start="{c.start:.3f}" data-duration="{c.end - c.start:.3f}" data-track-index="{k + 1}" '
        f'data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
        for k, c in enumerate(comps))
    (VID / "index.html").write_text(f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {SLATE}; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION:.3f}" data-width="1920" data-height="1080">
{hosts}
      <audio id="vo" class="clip" data-start="0" data-duration="{DURATION:.3f}" data-track-index="30" data-volume="1" src="assets/loi-doc.wav"></audio>
{sfx_tags}
{music_tags()}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    comps = [b() for b in BUILDERS]
    for c in comps:
        c.write()
    write_index(comps)
    print(f"{len(comps)} cảnh → {VID}")


if __name__ == "__main__":
    main()
