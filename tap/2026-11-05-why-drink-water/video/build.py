"""Why do you need to drink water? (English) — dựng HyperFrames từ audio/timeline.json + audio/words.json.

Bản tiếng Anh của tập 2026-11-04-vi-sao-can-uong-nuoc: giữ bố cục bảng, thay Tò (SVG) bằng nhân vật
minh họa cậu bé đeo kính (ảnh PNG đã tách nền) và dùng bối cảnh minh họa cho văn phòng, phòng họp.
Chạy:  py build.py      (trong thư mục video\\)
"""
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from hf import core  # noqa: E402

core.init(__file__)
from hf.core import *  # noqa: E402,F401,F403
from hf.core import SCENES, WORDS, DURATION  # noqa: E402

# Ảnh tư thế (assets/char/*.png, cắt sát viền, chân ở mép dưới) — tên tư thế cũ của Tò → file mới
POSE_FILE = {"dung": "goc-chatgpt", "chi-tay": "goc-chatgpt", "suy-nghi": "suy-nghi", "lo-lang": "dau-dau",
             "ngac-nhien": "ngac-nhien", "vui": "vui", "uong": "uong-nuoc", "chay": "chay"}
POSE_SIZE = {"chay": (889, 1199), "dau-dau": (685, 1208), "goc-chatgpt": (530, 1219), "ngac-nhien": (570, 1209),
             "suy-nghi": (515, 1205), "uong-nuoc": (574, 1211), "vui": (667, 1208)}


def char(uid, pose, cx, feet, h):
    """Nhân vật cao h px, chân chạm y = feet, giữa x = cx. #uid-w để ẩn/hiện, #uid để nhún/thở."""
    f = POSE_FILE[pose]
    w0, h0 = POSE_SIZE[f]
    w = h * w0 / h0
    return (f'<g id="{uid}-w"><g id="{uid}"><image href="assets/char/{f}.png" x="{cx - w / 2:.1f}" y="{feet - h:.1f}" '
            f'width="{w:.1f}" height="{h:.1f}"/></g></g>')


def to(uid, pose, x, y, h):
    """Cùng chữ ký với Tò (khung 440×540 tại x, y, cao h) để giữ nguyên bố cục cũ."""
    k = h / 540
    return char(uid, pose, x + 220 * k, y + 505 * k, 470 * k)


core.to = to  # board_to() trong core dùng hàm này


def idle(c, uid, t0, t1, seed=0):
    """Đứng yên vẫn sống: thở nhẹ và lắc rất khẽ quanh chân."""
    n = int((t1 - t0) / 1.3)
    if n >= 2:
        reps = n - 1 if (n - 1) % 2 else n - 2
        c.tl.ft(f"#{uid}", {"scaleY": 1, "rotation": 0}, {"scaleY": 1.015, "rotation": 0.6 if seed % 2 else -0.6,
                                                         "transformOrigin": "50% 100%", "duration": 1.3, "ease": "sine.inOut",
                                                         "yoyo": True, "repeat": reps}, t0 + 0.1 * (seed % 3))


LEAD = 0.2  # hình hiện sớm hơn tiếng một nhịp, để chữ không đuổi theo giọng đọc
_at = Comp.at
Comp.at = lambda self, scene, phrase, nth=0, which="start", off=0.0: max(_at(self, scene, phrase, nth, which, off - LEAD), 0)


def S(c, scene, prefix):
    """Mốc (giây trong cảnh) của câu bắt đầu bằng `prefix`."""
    for s in WORDS["sentences"]:
        if s["scene"] == scene and s["text"].startswith(prefix):
            return round(max(s["start"] - c.start - LEAD, 0), 3)
    raise SystemExit(f"Không thấy câu '{prefix}' trong cảnh {scene}")


def comp(sid, last=None):
    a, b = SCENES[sid], SCENES[last or sid]
    return Comp(f"s{sid}", a["start"], b["end"])


def label(id_, x, y, s, size=52, fill=WHITE, anchor="start", weight=900):
    return text(x, y, s, size, weight, fill, anchor, id_=id_, extra=" " + OUTLINE)


def envelope(id_, cx, cy, s=1.0):
    return place(cx, cy, g(id_, f'<rect x="-50" y="-34" width="100" height="68" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
                                f'<path d="M-50 -30 L0 6 L50 -30" fill="none" stroke="{INK}" stroke-width="5"/>'), s)


def pain_lines(id_, cx, cy, s=1.0):
    return place(cx, cy, g(id_, f'<path d="M0 0 l18 -14 l-6 22 l20 -10 M10 40 l24 -6 l-14 18 l22 2" fill="none" stroke="{RED}" '
                                f'stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'), s)


def chip(id_, cx, cy, s, size=56, fill=YELLOW, color=INK):
    w = len(s) * size * 0.62 + 60
    return g(id_, f'<rect x="{cx - w / 2:.0f}" y="{cy - size * 0.95:.0f}" width="{w:.0f}" height="{size * 1.5:.0f}" rx="{size * 0.75:.0f}" '
                  f'fill="{fill}" stroke="{INK}" stroke-width="6"/>' + text(cx, cy + size * 0.3, s, size, 900, color, "middle"))


# Văn phòng minh họa (assets/bg/van-phong.jpg, 1920×1080): đồng hồ, cốc cà phê, chai nước, laptop
CLOCK, MUG, BOTTLE, LAPTOP = (878, 132), (775, 677), (976, 609), (500, 632)
OFF_CX, OFF_FEET, OFF_H = 1500, 1050, 780


def frame(c, t, px, py, z, cam, settle):
    """Như core.frame nhưng giữ khung nhìn trong ảnh nền 1920×1080 (không lộ mép)."""
    px = min(max(px, 960 / z), 1920 - 960 / z)
    py = min(max(py, 540 / z), 1080 - 540 / z)
    core.frame(c, t, px, py, z, cam, settle)


def office_comp(c, poses, extra="", bg="van-phong"):
    p = c.cid
    figs = "".join(char(f"{p}-{pose}", pose, OFF_CX, OFF_FEET, OFF_H) for pose in poses)
    c.svg.append(f'<g id="{p}-settle"><g id="{p}-cam"><image href="assets/bg/{bg}.jpg" width="1920" height="1080"/>'
                 f'{figs}{extra}</g></g>')
    for pose in poses[1:]:
        c.hide(f"#{p}-{pose}-w")
    return f"#{p}-cam", f"#{p}-settle"


def show_pose(c, poses, which, t):
    for pose in poses:
        c.show(f"#{c.cid}-{pose}-w", t, pose == which)


# ---------------------------------------------------------------- 01 · Title
def s01():
    c = comp("01")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', glass("s01-gl", 1180, 860, 2.0, 0.7),
              char("s01-boy", "vui", 1600, 1000, 760)]
    words = ["Why", "do", "you", "need", "<br>", "to", "drink", "<br>", "water?"]
    spans = "".join("<br>" if w == "<br>" else
                    f'<span id="s01-w{k}" class="w{" hot" if w == "water?" else ""}">{w}</span> '
                    for k, w in enumerate(words))
    c.css.append(f"#s01-title {{ left: 130px; top: 230px; font-size: 140px; font-weight: 800; line-height: 1.08; color: {INK}; "
                 f"letter-spacing: -0.01em; }} #s01-title .hot {{ color: {WATER_DARK}; }} #s01-title .w {{ display: inline-block; }}")
    c.html.append(f'<div id="s01-title" class="txt">{spans}</div>')
    c.tl.ft("#s01-gl", {"scale": 0.8, "transformOrigin": "50% 100%"},
            {"scale": 1, "transformOrigin": "50% 100%", "duration": 0.7, "ease": "back.out(1.6)"}, 0)
    c.tl.ft("#s01-gl-water", {"scaleY": 0.2, "transformOrigin": "50% 100%"}, {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 1.2, "ease": "power2.out"}, 0.2)
    c.tl.ft("#s01-boy", {"y": 80, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "back.out(1.6)"}, 0.4)
    for k, w in enumerate(words):
        if w != "<br>":
            c.blur_in(f"#s01-w{k}", 0.25 + 0.08 * k, 0.15)
    return c


# ---------------------------------------------------------------- 02 · Opening story (office)
def s02():
    c = comp("02")
    poses = ["dung", "lo-lang", "suy-nghi", "ngac-nhien"]
    p = c.cid
    hx, hy = OFF_CX, OFF_FEET - OFF_H * 0.78
    over = (envelope(f"{p}-env0", 520, 520, 1.0) + envelope(f"{p}-env1", 520, 520, 0.9) + envelope(f"{p}-env2", 520, 520, 1.1)
            + pain_lines(f"{p}-pain", hx - 230, hy - 120, 1.6) + pain_lines(f"{p}-pain2", hx + 170, hy - 100, 1.3)
            + "".join(text(1680 + k * 70, 330 - k * 30, "?", 110, 900, YELLOW, id_=f"{p}-q{k}", extra=" " + OUTLINE) for k in range(3))
            + chip(f"{p}-t7", CLOCK[0], 300, "7:00 AM") + chip(f"{p}-t15", CLOCK[0], 300, "3:00 PM", fill=CORAL, color=WHITE)
            + chip(f"{p}-t2h", CLOCK[0], 300, "+2 HOURS"))
    cam, st = office_comp(c, poses, over)
    c.svg.append(label(f"{p}-t16", 960, 900, "4:00 PM · PRESENTATION", 80, YELLOW, "middle"))
    c.svg.append(label(f"{p}-how", 960, 210, "HOW MUCH?", 130, WHITE, "middle"))
    c.hide(f"#{p}-env0", f"#{p}-env1", f"#{p}-env2", f"#{p}-pain", f"#{p}-pain2", f"#{p}-q0", f"#{p}-q1", f"#{p}-q2",
           f"#{p}-t16", f"#{p}-how", f"#{p}-t7", f"#{p}-t15", f"#{p}-t2h")
    T = lambda pre: S(c, "02", pre)
    end = c.loc(SCENES["02"]["end"])

    frame(c, 0, 960, 540, 1.0, cam, st)
    popl(c, f"#{p}-t7", 0.3)
    idle(c, f"{p}-dung", 0, T("A dull headache"), 0)
    t = T("You walk into")
    c.show(f"#{p}-t7", t, False)
    frame(c, t, MUG[0], MUG[1] - 60, 2.2, cam, st)
    t = T("Your first meeting")
    frame(c, t, CLOCK[0], CLOCK[1] + 60, 2.4, cam, st)
    popl(c, f"#{p}-t2h", t + 0.3, snd="whoosh")
    t = T("Then come the emails")
    c.show(f"#{p}-t2h", t, False)
    frame(c, t, 620, 500, 1.6, cam, st)
    for k, (dx, dy) in enumerate(((-200, -200), (60, -280), (260, -170))):
        c.show(f"#{p}-env{k}", t + 0.3 * k)
        c.tl.ft(f"#{p}-env{k}", {"x": 0, "y": 0, "scale": 0.3}, {"x": dx, "y": dy, "scale": 1, "duration": 0.7, "ease": "expo.out"},
                t + 0.3 * k)
        c.sfx("pop", t + 0.3 * k)
    t = T("The water bottle on")
    frame(c, t, BOTTLE[0], BOTTLE[1] - 20, 2.6, cam, st)
    for k in range(3):
        c.show(f"#{p}-env{k}", t, False)
    t = T("Three in the afternoon")
    frame(c, t, CLOCK[0], CLOCK[1] + 60, 2.4, cam, st)
    popl(c, f"#{p}-t15", t + 0.2, snd="thump")
    t = T("A dull headache")
    c.show(f"#{p}-t15", t, False)
    frame(c, t, hx, hy + 60, 1.9, cam, st)
    show_pose(c, poses, "lo-lang", t)
    c.show(f"#{p}-pain", t + 0.4)
    c.show(f"#{p}-pain2", t + 0.6)
    for sel, d in ((f"#{p}-pain", 0.4), (f"#{p}-pain2", 0.6)):
        c.tl.ft(sel, {"scale": 0.8, "transformOrigin": "50% 50%"}, {"scale": 1.15, "transformOrigin": "50% 50%", "duration": 0.35,
                                                                    "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, t + d)
    t = T("You read the same")
    c.show(f"#{p}-pain", t, False)
    c.show(f"#{p}-pain2", t, False)
    frame(c, t, 1450, 500, 1.4, cam, st)
    show_pose(c, poses, "suy-nghi", t)
    for k in range(3):
        c.pop(f"#{p}-q{k}", t + 0.45 + 0.4 * k, 0.4)
        c.sfx("pop", t + 0.45 + 0.4 * k)
    idle(c, f"{p}-suy-nghi", t, T("Your lips are dry"), 1)
    t = T("Your lips are dry")
    for k in range(3):
        c.show(f"#{p}-q{k}", t, False)
    frame(c, t, hx, hy + 80, 2.0, cam, st)
    show_pose(c, poses, "lo-lang", t)
    idle(c, f"{p}-lo-lang", t, T("And at four"), 2)
    t = T("And at four")
    frame(c, t, 1100, 560, 1.15, cam, st)
    popl(c, f"#{p}-t16", t + 0.5, snd="thump")
    t = T("You reach for")
    c.show(f"#{p}-t16", t, False)
    frame(c, t, 1240, 600, 1.5, cam, st)
    show_pose(c, poses, "dung", t)
    swap(c, f"{p}-dung", f"{p}-suy-nghi", c.at("02", "then you stop"))
    t = T("How much is")
    popl(c, f"#{p}-how", t)
    t = T("Should you just")
    c.show(f"#{p}-how", t, False)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    frame(c, t, 1240, 560, 1.3, cam, st)
    idle(c, f"{p}-ngac-nhien", t + 0.5, end, 3)
    return c


# ---------------------------------------------------------------- 03 · The problem
def s03():
    c = comp("03")
    p = c.cid
    bubbles = [("8 GLASSES", 470, 250, 420, "eight glasses"), ("3 LITERS", 1130, 230, 380, "three liters"),
               ("ONLY WHEN THIRSTY", 560, 560, 620, "when you're thirsty"), ("MORE = MORE DETOX", 1080, 790, 640, "the more you drink")]
    extra = "".join(bubble(f"{p}-b{k}", x, y, w, 130, lb, size=54) for k, (lb, x, y, w, _) in enumerate(bubbles))
    cam, st = office_comp(c, ["suy-nghi"], extra)
    frame(c, 0, 1000, 540, 1.08, cam, st)
    idle(c, f"{p}-suy-nghi", 0, c.loc(SCENES["03"]["end"]), 0)
    for k, (*_, word) in enumerate(bubbles):
        t = c.at("03", word)
        c.pop(f"#{p}-b{k}", t, 0.5, "50% 100%", "back.out(1.8)", 0.3)
        c.sfx("pop", t)
    t = S(c, "03", "To find out")
    for k in range(4):
        c.tl.to(f"#{p}-b{k}", {"scale": 0, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "back.in(2)"}, t + 0.06 * k)
    c.sfx("whoosh", t)
    z = 2.0
    c.tl.to(cam, {"x": 960 - z * min(OFF_CX, 1920 - 960 / z), "y": 540 - z * (OFF_FEET - OFF_H * 0.6), "scale": z, "transformOrigin": "0 0",
                  "duration": 1.6, "ease": "power2.inOut"}, t + 0.6)
    return c


def board(c, poses=("suy-nghi",), look=None):
    """Nền bảng + nhân vật bên trái (tư thế đầu hiện, các tư thế khác ẩn)."""
    c.svg.append(slate_frame())
    for k, pose in enumerate(poses):
        board_to(c, f"{c.cid}-{pose}", pose, hidden=k > 0)
    return lambda: c.svg.append(slate_border())


def popl(c, sel, t, origin="50% 50%", snd="pop", dur=0.45):
    c.pop(sel, t, dur, origin)
    if snd:
        c.sfx(snd, t)


# ---------------------------------------------------------------- 04 · You are water
def s04():
    c = comp("04")
    p = c.cid
    close = board(c)
    PX, PY, PH = 1040, 560, 760
    k = PH / 700
    head_y = PY - PH / 2 + 60 * k
    c.svg += [person_fill(f"{p}-me", PX, PY, PH, 0.6),
              label(f"{p}-l60", PX + 170, head_y + 760 * k - 820 * 0.6 * k - 40, "60%", 110, WATER, "start"),
              g(f"{p}-mini", person_fill(f"{p}-baby", 1530, 800, 300, 0.75) + person_fill(f"{p}-old", 1730, 700, 520, 0.55)
                + label(f"{p}-l75", 1530, 610, "75%", 64, WATER, "middle") + label(f"{p}-l55", 1730, 400, "55%", 64, WATER, "middle")
                + text(1530, 1000, "NEWBORN", 34, 800, GREY, "middle", id_=f"{p}-n75")
                + text(1730, 1000, "OLDER ADULT", 34, 800, GREY, "middle", id_=f"{p}-n55")),
              g(f"{p}-org", label(f"{p}-o1", PX + 160, head_y + 20, "BRAIN · HEART ≈ 73%", 48, WHITE)
                + label(f"{p}-o2", PX + 160, head_y + 290, "LUNGS ≈ 83%", 48, WHITE)
                + label(f"{p}-o3", PX + 160, head_y + 640, "BONES ≈ 31%", 48, WHITE)
                + text(PX + 160, head_y + 720, "Mitchell et al., 1945", 28, 500, GREY, id_=f"{p}-osrc")),
              g(f"{p}-split", f'<rect id="{p}-in" x="700" y="330" width="760" height="190" rx="24" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + f'<rect id="{p}-out" x="1470" y="330" width="380" height="190" rx="24" fill="{WATER}" stroke="{INK}" stroke-width="6"/>'
                + label(f"{p}-lin", 1080, 445, "INSIDE CELLS · 2/3", 56, WHITE, "middle")
                + label(f"{p}-lout", 1660, 445, "OUTSIDE · 1/3", 50, WHITE, "middle")
                + text(1660, 580, "BLOOD + BETWEEN CELLS", 34, 800, WATER, "middle", id_=f"{p}-lout2")),
              g(f"{p}-cyc", f'<circle cx="1280" cy="820" r="120" fill="none" stroke="{WATER}" stroke-width="14" stroke-dasharray="40 26" id="{p}-ring"/>'
                + "".join(label(f"{p}-c{k2}", x, y, w, 44, WHITE, "middle")
                          for k2, (x, y, w) in enumerate(((1280, 660, "FLOWS"), (1530, 840, "EVAPORATES"), (1280, 1000, "FILTERED"), (1030, 840, "REPLACED"))))),
              tear(f"{p}-drop", 1660, 820, 3.0), label(f"{p}-l3", 1270, 560, "1 DROP · 3 JOBS", 90, WHITE, "middle")]
    close()
    end = c.loc(SCENES["04"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 1)
    c.hide(f"#{p}-l60", f"#{p}-mini", f"#{p}-baby", f"#{p}-old", f"#{p}-l75", f"#{p}-l55", f"#{p}-n75", f"#{p}-n55",
           f"#{p}-o1", f"#{p}-o2", f"#{p}-o3", f"#{p}-osrc", f"#{p}-split", f"#{p}-cyc", f"#{p}-drop",
           *[f"#{p}-c{k2}" for k2 in range(4)], f"#{p}-lin", f"#{p}-lout", f"#{p}-lout2")
    c.pop(f"#{p}-me", 0.2, 0.6, "50% 100%", "back.out(1.4)", 0.6)
    c.tl.ft(f"#{p}-me-water", {"y": 600}, {"y": 0, "duration": 1.6, "ease": "power2.out"}, c.at("04", "sixty percent", off=-0.8))
    c.sfx("whoosh", c.at("04", "sixty percent", off=-0.4))
    popl(c, f"#{p}-l60", c.at("04", "sixty percent", off=0.5), "0% 50%")
    t = c.at("04", "Newborn")
    c.show(f"#{p}-mini", t)
    popl(c, f"#{p}-baby", t, "50% 100%")
    c.tl.ft(f"#{p}-baby-water", {"y": 600}, {"y": 0, "duration": 1.0, "ease": "power2.out"}, t + 0.2)
    c.blur_in(f"#{p}-l75", t + 0.6)
    c.blur_in(f"#{p}-n75", t + 0.6)
    t = c.at("04", "Older adults")
    popl(c, f"#{p}-old", t, "50% 100%")
    c.tl.ft(f"#{p}-old-water", {"y": 600}, {"y": 0, "duration": 1.0, "ease": "power2.out"}, t + 0.2)
    c.blur_in(f"#{p}-l55", t + 0.6)
    c.blur_in(f"#{p}-n55", t + 0.6)
    t = c.at("04", "every organ")
    c.blur_out(f"#{p}-mini", t, 0.25)
    c.blur_out(f"#{p}-l60", t, 0.25)
    c.show(f"#{p}-org", t)
    popl(c, f"#{p}-o1", c.at("04", "brain and heart"), "0% 50%")
    c.blur_in(f"#{p}-osrc", c.at("04", "brain and heart"))
    popl(c, f"#{p}-o2", c.at("04", "lungs"), "0% 50%")
    popl(c, f"#{p}-o3", c.at("04", "Bones"), "0% 50%")
    t = c.at("04", "two-thirds")
    for sel in (f"#{p}-me", f"#{p}-org"):
        c.blur_out(sel, t - 0.5, 0.25)
    c.show(f"#{p}-split", t - 0.3)
    c.hide(f"#{p}-in", f"#{p}-out")
    c.tl.ft(f"#{p}-in", {"autoAlpha": 1, "scaleX": 0, "transformOrigin": "0% 50%"},
            {"autoAlpha": 1, "scaleX": 1, "transformOrigin": "0% 50%", "duration": 0.7, "ease": "expo.out"}, t)
    c.sfx("whoosh", t)
    c.blur_in(f"#{p}-lin", t + 0.5)
    t = c.at("04", "The rest")
    c.tl.ft(f"#{p}-out", {"autoAlpha": 1, "scaleX": 0, "transformOrigin": "0% 50%"},
            {"autoAlpha": 1, "scaleX": 1, "transformOrigin": "0% 50%", "duration": 0.5, "ease": "expo.out"}, t)
    c.blur_in(f"#{p}-lout", t + 0.4)
    c.blur_in(f"#{p}-lout2", c.at("04", "in your blood"))
    t = c.at("04", "never sits still")
    c.show(f"#{p}-cyc", t)
    c.tl.ft(f"#{p}-ring", {"rotation": 0}, {"rotation": 360, "svgOrigin": "1280 820", "duration": 8, "ease": "none"}, t)
    for k2, w in enumerate(("flows", "evaporates", "filtered", "replaced")):
        popl(c, f"#{p}-c{k2}", c.at("04", w))
    t = c.at("04", "a drop")
    c.blur_out(f"#{p}-cyc", t - 0.3, 0.25)
    c.blur_out(f"#{p}-split", t - 0.3, 0.25)
    popl(c, f"#{p}-drop", t, "50% 100%")
    c.tl.to(f"#{p}-drop", {"x": -500, "duration": 1.6, "ease": "power2.inOut"}, c.at("04", "three main jobs"))
    c.hide(f"#{p}-l3")
    c.blur_in(f"#{p}-l3", c.at("04", "a drop", off=0.3))
    return c


# ---------------------------------------------------------------- 05 · The delivery river
def s05():
    c = comp("05")
    p = c.cid
    close = board(c)
    Y0, Y1 = 400, 580
    reds = "".join(f'<g id="{p}-r{k}"><circle cx="560" cy="{Y0 + 50 + (k % 2) * 70}" r="26" fill="{RED}" stroke="{INK}" stroke-width="5"/>'
                   f'<circle cx="560" cy="{Y0 + 50 + (k % 2) * 70}" r="10" fill="#B8323A"/></g>' for k in range(8))
    boxes = "".join(f'<g id="{p}-y{k}"><rect x="538" y="{Y0 + 70 - 22 + (k % 2) * 30}" width="44" height="44" rx="8" fill="{YELLOW}" '
                    f'stroke="{INK}" stroke-width="5"/></g>' for k in range(6))
    waste = "".join(f'<g id="{p}-w{k}"><circle cx="1960" cy="{Y1 - 40}" r="18" fill="{GREY}" stroke="{INK}" stroke-width="5"/></g>'
                    for k in range(6))
    river = (f'<clipPath id="{p}-clip"><rect x="640" y="{Y0 - 40}" width="1240" height="{Y1 - Y0 + 80}"/></clipPath>'
             f'<g id="{p}-water"><rect x="620" y="{Y0}" width="1300" height="{Y1 - Y0}" fill="{WATER}" opacity=".85"/></g>'
             f'<g clip-path="url(#{p}-clip)">{reds}{boxes}{waste}</g>'
             f'<g id="{p}-wt"><rect x="620" y="{Y0 - 26}" width="1300" height="26" fill="{PINK}" stroke="{INK}" stroke-width="5"/></g>'
             f'<g id="{p}-wb"><rect x="620" y="{Y1}" width="1300" height="26" fill="{PINK}" stroke="{INK}" stroke-width="5"/></g>')
    c.svg += [g(f"{p}-riv", river), heart(f"{p}-heart", 820, 220, 1.0),
              label(f"{p}-lh", 940, 340, "PLASMA: MOSTLY WATER", 50, WHITE),
              label(f"{p}-ln", 1250, 700, "NUTRIENTS + OXYGEN →", 48, YELLOW, "middle"),
              label(f"{p}-lw", 1250, 770, "← WASTE", 48, GREY, "middle"),
              g(f"{p}-gut", f'<path d="M820 900 a70 70 0 1 1 0.1 0" fill="none" stroke="{WATER}" stroke-width="14" stroke-dasharray="36 22"/>'
                + label(f"{p}-g1", 940, 880, "GUT: ~8 LITERS OF FLUID A DAY", 50, WHITE)
                + label(f"{p}-g2", 940, 950, "→ ALMOST ALL ABSORBED BACK", 46, WATER))]
    close()
    end = c.loc(SCENES["05"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 2)
    c.hide(f"#{p}-lh", f"#{p}-ln", f"#{p}-lw", f"#{p}-gut", f"#{p}-g1", f"#{p}-g2")
    c.pop(f"#{p}-riv", 0.1, 0.6, "0% 50%", "expo.out", 0.6)
    c.pop(f"#{p}-heart", 0.3, 0.5)
    t_dry = S(c, "05", "When you run low")
    t_fast = S(c, "05", "And your heart")
    beats = int((t_fast - 0.3) / 0.8)
    c.tl.ft(f"#{p}-heart", {"scale": 1}, {"scale": 1.12, "transformOrigin": "50% 60%", "duration": 0.4, "ease": "sine.inOut",
                                          "yoyo": True, "repeat": beats * 2 - 1}, 0.8)
    c.tl.ft(f"#{p}-heart", {"scale": 1}, {"scale": 1.14, "transformOrigin": "50% 60%", "duration": 0.22, "ease": "sine.inOut",
                                          "yoyo": True, "repeat": int((end - t_fast) / 0.44) * 2 - 1}, t_fast + 0.1)
    for k in range(8):
        c.tl.ft(f"#{p}-r{k}", {"x": 0}, {"x": 1400, "duration": 4.2, "ease": "none", "repeat": 5}, 0.1 + k * 0.52)
    t_n = c.at("05", "nutrients")
    for k in range(6):
        c.tl.ft(f"#{p}-y{k}", {"x": 0}, {"x": 1400, "duration": 4.6, "ease": "none", "repeat": 3}, t_n - 1.5 + k * 0.75)
    t_w = c.at("05", "waste")
    for k in range(6):
        c.tl.ft(f"#{p}-w{k}", {"x": 0}, {"x": -1400, "duration": 4.6, "ease": "none", "repeat": 3}, t_w - 1.2 + k * 0.75)
    popl(c, f"#{p}-lh", c.at("05", "plasma"), "0% 50%")
    popl(c, f"#{p}-ln", t_n)
    popl(c, f"#{p}-lw", t_w)
    t = c.at("05", "In your gut")
    c.show(f"#{p}-gut", t)
    popl(c, f"#{p}-g1", t, "0% 50%")
    c.blur_in(f"#{p}-g2", S(c, "05", "Then almost all"))
    for sel in (f"#{p}-ln", f"#{p}-lw"):
        c.blur_out(sel, t - 0.2, 0.2)
    c.blur_out(f"#{p}-gut", t_dry - 0.2, 0.25)
    c.tl.to(f"#{p}-wt", {"y": 50, "duration": 1.2, "ease": "power2.inOut"}, t_dry + 0.3)
    c.tl.to(f"#{p}-wb", {"y": -50, "duration": 1.2, "ease": "power2.inOut"}, t_dry + 0.3)
    c.tl.to(f"#{p}-water", {"scaleY": 0.45, "transformOrigin": "50% 50%", "duration": 1.2, "ease": "power2.inOut"}, t_dry + 0.3)
    c.sfx("whoosh", t_dry + 0.3)
    return c


# ---------------------------------------------------------------- 06 · The air conditioner
def s06():
    c = comp("06")
    p = c.cid
    close = board(c)
    drops = "".join(tear(f"{p}-d{k}", 780 + k * 150, 640, 1.2) for k in range(7))
    vapor = "".join(f'<path id="{p}-v{k}" d="M{780 + k * 150} 610 C{760 + k * 150} 560 {810 + k * 150} 520 {780 + k * 150} 460 '
                    f'C{760 + k * 150} 420 {800 + k * 150} 400 {785 + k * 150} 360" pathLength="1" stroke-dasharray="1 1.2" '
                    f'stroke-dashoffset="1.1" fill="none" stroke="{TEAR}" stroke-width="12" stroke-linecap="round"/>' for k in range(7))
    heat = "".join(place(780 + k * 150 + 40, 470, g(f"{p}-h{k}", f'<path d="M0 30 V-30 M-16 -12 L0 -32 L16 -12" fill="none" '
                                                                 f'stroke="{CORAL}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'))
                   for k in range(0, 7, 2))
    skin = (f'<rect x="640" y="650" width="1240" height="260" fill="#F2C29B" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="640" y="650" width="1240" height="40" fill="#E9AE85"/>'
            f'<path d="M640 800 C900 780 1200 830 1880 790" fill="none" stroke="#D9906A" stroke-width="8"/>'
            + "".join(f'<path d="M{780 + k * 150} 690 V780" stroke="#C97A55" stroke-width="10" stroke-linecap="round"/>' for k in range(7)))
    c.svg += [g(f"{p}-skin", skin + text(680, 880, "SKIN", 44, 900, "#9A5A3A")), g(f"{p}-drops", drops), g(f"{p}-vap", vapor + heat),
              thermometer(f"{p}-th", 1780, 400, 1.1, 0.85),
              sun(f"{p}-sun", 1520, 170, 0.9), pictogram(f"{p}-run", 1260, 230, 0.9, "run"),
              label(f"{p}-l2", 1150, 500, "≈ 2 LITERS / HOUR", 96, YELLOW, "middle")]
    close()
    end = c.loc(SCENES["06"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 0)
    c.hide(f"#{p}-sun", f"#{p}-run", f"#{p}-l2", *[f"#{p}-d{k}" for k in range(7)], *[f"#{p}-h{k}" for k in range(0, 7, 2)])
    c.pop(f"#{p}-skin", 0.1, 0.6, "50% 100%", "expo.out", 0.7)
    c.pop(f"#{p}-th", 0.4, 0.5, "50% 100%")
    t = c.at("06", "skin releases sweat")
    for k in range(7):
        c.pop(f"#{p}-d{k}", t + 0.08 * k, 0.4, "50% 100%")
    c.sfx("pop", t)
    t = c.at("06", "sweat evaporates")
    for k in range(7):
        c.draw(f"#{p}-v{k}", t + 0.07 * k, 0.8)
        c.tl.to(f"#{p}-d{k}", {"scale": 0.4, "opacity": 0.4, "transformOrigin": "50% 100%", "duration": 0.8}, t + 0.07 * k)
    th = c.at("06", "carries heat")
    for k in range(0, 7, 2):
        c.show(f"#{p}-h{k}", th)
        c.tl.ft(f"#{p}-h{k}", {"y": 40}, {"y": -160, "duration": 1.6, "ease": "power1.out"}, th)
        c.tl.to(f"#{p}-h{k}", {"opacity": 0, "duration": 0.4}, th + 1.3)
    c.tl.to(f"#{p}-th-hg", {"scaleY": 0.6, "transformOrigin": "50% 100%", "duration": 1.4, "ease": "power2.inOut"}, th)
    c.sfx("whoosh", th)
    popl(c, f"#{p}-sun", c.at("06", "The hotter"))
    popl(c, f"#{p}-run", c.at("06", "the more you move"))
    t = c.at("06", "two liters of sweat")
    c.blur_out(f"#{p}-vap", t - 0.3, 0.25)
    popl(c, f"#{p}-l2", t, snd="thump", dur=0.5)
    for k in range(7):
        c.tl.to(f"#{p}-d{k}", {"scale": 1.3, "opacity": 1, "transformOrigin": "50% 100%", "duration": 0.4, "ease": "back.out(2)"}, t + 0.05 * k)
    return c


# ---------------------------------------------------------------- 07 · The filter plant
def s07():
    c = comp("07")
    p = c.cid
    close = board(c)
    c.svg += [g(f"{p}-kid", kidney(f"{p}-k1", 1150, 470, 1.0) + kidney(f"{p}-k2", 1420, 470, 1.0, flip=True)),
              g(f"{p}-pipe", f'<path d="M680 470 H1020 M990 440 L1030 470 L990 500" fill="none" stroke="{RED}" stroke-width="22" '
                             f'stroke-linecap="round" stroke-linejoin="round"/>' + label(f"{p}-lm", 700, 430, "BLOOD", 48, RED)),
              g(f"{p}-tub", bathtub(f"{p}-bt", 900, 830, 0.8) + label(f"{p}-l180", 900, 990, "≈ 180 LITERS / DAY", 54, WHITE, "middle")),
              g(f"{p}-loop", f'<path id="{p}-arc" d="M1100 340 C1150 180 1420 180 1470 340" pathLength="1" stroke-dasharray="1 1.2" '
                             f'stroke-dashoffset="1.1" fill="none" stroke="{TEAL}" stroke-width="16" stroke-linecap="round"/>'
                + label(f"{p}-l99", 1285, 170, "> 99% ABSORBED BACK", 54, TEAL, "middle")),
              g(f"{p}-uri", glass(f"{p}-gl", 1450, 930, 0.6, 0.6) + label(f"{p}-l15", 1450, 1010, "URINE ≈ 1.5 LITERS", 44, WHITE, "middle")),
              g(f"{p}-adj", label(f"{p}-a1", 1640, 640, "SHORT → HOLD ON", 40, WATER, "middle")
                + label(f"{p}-a2", 1640, 700, "EXTRA → LET GO", 40, YELLOW, "middle")),
              g(f"{p}-gau", gauge(f"{p}-gg", 1720, 340, 110, "SPEED LIMIT"))]
    close()
    end = c.loc(SCENES["07"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 3)
    c.hide(f"#{p}-tub", f"#{p}-loop", f"#{p}-uri", f"#{p}-adj", f"#{p}-gau", f"#{p}-pipe", f"#{p}-l99", f"#{p}-a1", f"#{p}-a2")
    c.pop(f"#{p}-kid", 0.2, 0.6, "50% 50%", "back.out(1.4)", 0.4)
    c.pop(f"#{p}-pipe", c.at("07", "two kidneys"), 0.5, "0% 50%", "expo.out", 0.2)
    popl(c, f"#{p}-tub", c.at("07", "one hundred and eighty"), "50% 100%")
    t = c.at("07", "ninety-nine")
    c.show(f"#{p}-loop", t)
    c.draw(f"#{p}-arc", t, 0.7)
    c.pop(f"#{p}-l99", t + 0.3, 0.45)
    c.sfx("whoosh", t)
    popl(c, f"#{p}-uri", c.at("07", "one and a half"), "50% 100%")
    c.show(f"#{p}-adj", c.at("07", "can also adjust"))
    c.blur_in(f"#{p}-a1", c.at("07", "hold on to water"))
    c.blur_in(f"#{p}-a2", c.at("07", "let more go"))
    t = c.at("07", "speed limit")
    c.blur_out(f"#{p}-adj", t - 0.2, 0.2)
    popl(c, f"#{p}-gau", t, "50% 100%")
    c.tl.ft(f"#{p}-gg-n", {"rotation": -60}, {"rotation": 78, "svgOrigin": "1720 340", "duration": 1.2, "ease": "power2.inOut"}, t + 0.3)
    c.tl.ft(f"#{p}-gg-n", {"rotation": 78}, {"rotation": 84, "svgOrigin": "1720 340", "duration": 0.1, "yoyo": True, "repeat": 7,
                                             "ease": "none"}, t + 1.6)
    return c


# ---------------------------------------------------------------- 08 · The water scale
def s08():
    c = comp("08")
    p = c.cid
    close = board(c)
    left = (tear(f"{p}-i1", -90, -40, 1.6).replace(TEAR, URINE[2]) + tear(f"{p}-i2", 0, -40, 1.6)
            + place(90, -40, g(f"{p}-i3", f'<path d="M-40 0 C-60 -30 -20 -50 0 -30 C10 -60 50 -50 44 -20 C70 -20 60 10 40 10 Z" '
                                          f'fill="#DDE6EE" stroke="{INK}" stroke-width="5"/>')))
    right = (glass(f"{p}-i4", -70, 0, 0.45, 0.8) + bowl(f"{p}-i5", 80, -20, 0.55, steam=False)
             + tear(f"{p}-i6", 150, -110, 0.8))
    c.svg += [balance(f"{p}-bal", 1240, 330, 0.85, left, right),
              label(f"{p}-lo", 866, 230, "OUT", 60, CORAL, "middle"), label(f"{p}-li", 1614, 230, "IN", 60, TEAL, "middle"),
              text(866, 620, "URINE · SWEAT · BREATH", 30, 800, GREY, "middle", id_=f"{p}-lo2"),
              text(1614, 620, "DRINKS · FOOD", 30, 800, GREY, "middle", id_=f"{p}-li2"),
              label(f"{p}-lt", 1240, 960, "≈ 2–3 LITERS A DAY (FOOD INCLUDED)", 54, YELLOW, "middle"),
              label(f"{p}-lm", 1614, 700, "+ a little from metabolism", 34, GREY, "middle", 800)]
    close()
    end = c.loc(SCENES["08"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 2)
    c.hide(*[f"#{p}-i{k}" for k in range(1, 7)], f"#{p}-lo", f"#{p}-li", f"#{p}-lo2", f"#{p}-li2", f"#{p}-lt", f"#{p}-lm")
    c.pop(f"#{p}-bal", 0.15, 0.6, "50% 100%", "back.out(1.4)", 0.5)
    BEAM = {"transformOrigin": "50% 5.7%"}
    popl(c, f"#{p}-lo", c.at("08", "On the left"))
    for k, w in ((1, "through urine"), (2, "through sweat"), (3, "every breath")):
        popl(c, f"#{p}-i{k}", c.at("08", w), "50% 100%")
    c.blur_in(f"#{p}-lo2", c.at("08", "every breath"))
    t = c.at("08", "sitting still")
    c.tl.ft(f"#{p}-bal-beam", {"rotation": 0, **BEAM}, {"rotation": -5, **BEAM, "duration": 0.8, "ease": "power2.inOut"}, t)
    popl(c, f"#{p}-li", c.at("08", "On the right"))
    popl(c, f"#{p}-i4", c.at("08", "from drinks"), "50% 100%")
    popl(c, f"#{p}-i5", c.at("08", "from food"), "50% 100%")
    c.blur_in(f"#{p}-li2", c.at("08", "from food"))
    c.tl.to(f"#{p}-bal-beam", {"rotation": 0, **BEAM, "duration": 0.8, "ease": "back.out(1.6)"}, c.at("08", "from food", off=0.2))
    t = c.at("08", "makes a little water")
    popl(c, f"#{p}-i6", t, "50% 100%")
    c.blur_in(f"#{p}-lm", t + 0.3)
    popl(c, f"#{p}-lt", c.at("08", "two to three liters"), dur=0.5)
    t = c.at("08", "out of balance")
    c.tl.to(f"#{p}-bal-beam", {"rotation": -8, **BEAM, "duration": 0.35, "ease": "power2.out"}, t)
    c.tl.to(f"#{p}-bal-beam", {"rotation": 0, **BEAM, "duration": 0.9, "ease": "elastic.out(1, 0.4)"}, t + 0.8)
    c.sfx("whoosh", t)
    return c


# ---------------------------------------------------------------- 09 · The sensor
def s09():
    c = comp("09")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    GX, GY = 1420, 520
    c.svg += [brain(f"{p}-br", 960, 300, 1.1), gauge(f"{p}-gg", GX, GY, 150, "BLOOD CONCENTRATION"),
              lamp(f"{p}-off", 1760, 300, "#4A5A68", 46), lamp(f"{p}-yel", 1760, 300, YELLOW, 46), lamp(f"{p}-red", 1760, 300, CORAL, 46),
              label(f"{p}-pct", GX, GY - 210, "+1–2%", 64, YELLOW, "middle"),
              g(f"{p}-adh", f'<rect x="-70" y="-40" width="140" height="80" rx="40" fill="{YELLOW}" stroke="{INK}" stroke-width="6"/>'
                + text(0, 18, "ADH", 48, 900, INK, "middle")),
              kidney(f"{p}-kid", 1180, 860, 0.7),
              f'<rect id="{p}-uri" x="1330" y="790" width="110" height="150" rx="22" fill="{URINE[1]}" stroke="{INK}" stroke-width="6"/>',
              text(1460, 880, "URINE", 32, 800, GREY, "start", id_=f"{p}-urit"),
              bubble(f"{p}-thirst", 640, 380, 340, 120, "THIRSTY!", YELLOW, INK, 60),
              glass(f"{p}-gl", 640, 960, 0.6, 0.85),
              pictogram(f"{p}-old", 1680, 850, 1.0, "elder"),
              label(f"{p}-lold", 1680, 1010, "THIRST: LATER, WEAKER", 44, GREY, "middle")]
    close()
    end = c.loc(SCENES["09"]["end"])
    c.hide(f"#{p}-yel", f"#{p}-red", f"#{p}-pct", f"#{p}-adh", f"#{p}-kid", f"#{p}-uri", f"#{p}-urit", f"#{p}-thirst",
           f"#{p}-gl", f"#{p}-old", f"#{p}-lold", f"#{p}-gg", f"#{p}-off")
    popl(c, f"#{p}-br", S(c, "09", "Because deep"))
    t = c.at("09", "diluted or concentrated")
    c.pop(f"#{p}-gg", t - 0.4, 0.5, "50% 100%")
    c.pop(f"#{p}-off", t - 0.2, 0.4)
    N = f"#{p}-gg-n"
    O = {"svgOrigin": f"{GX} {GY}"}
    c.tl.ft(N, {"rotation": -10, **O}, {"rotation": 10, **O, "duration": 0.6, "ease": "sine.inOut", "yoyo": True, "repeat": 3}, t)
    c.tl.to(N, {"rotation": 35, **O, "duration": 0.9, "ease": "power2.inOut"}, c.at("09", "more concentrated"))
    t = c.at("09", "one to two percent")
    c.tl.to(N, {"rotation": 52, **O, "duration": 0.6, "ease": "power2.out"}, t)
    popl(c, f"#{p}-pct", t)
    t = c.at("09", "warning light")
    c.show(f"#{p}-yel", t)
    c.sfx("pop", t)
    t = c.at("09", "a hormone")
    c.show(f"#{p}-adh", t)
    c.tl.ft(f"#{p}-adh", {"x": 960, "y": 400, "scale": 0}, {"x": 960, "y": 400, "scale": 1, "duration": 0.4, "ease": "back.out(2)"}, t)
    c.sfx("pop", t)
    t = c.at("09", "ADH tells")
    c.pop(f"#{p}-kid", t - 0.3, 0.45)
    c.show(f"#{p}-uri", t - 0.3)
    c.show(f"#{p}-urit", t - 0.3)
    c.tl.to(f"#{p}-adh", {"x": 1180, "y": 740, "duration": 1.0, "ease": "power2.inOut"}, t)
    c.sfx("whoosh", t)
    c.tl.to(f"#{p}-uri", {"attr": {"fill": URINE[4]}, "scaleY": 0.6, "transformOrigin": "50% 100%", "duration": 1.0},
            c.at("09", "gets darker", off=-0.4))
    t = c.at("09", "second signal")
    c.show(f"#{p}-red", t)
    popl(c, f"#{p}-thirst", t, "20% 100%", snd="thump")
    t = S(c, "09", "You drink")
    popl(c, f"#{p}-gl", t, "50% 100%")
    c.tl.to(N, {"rotation": 0, **O, "duration": 1.0, "ease": "power2.inOut"}, t + 0.3)
    c.blur_out(f"#{p}-thirst", t + 0.3, 0.2)
    c.show(f"#{p}-red", c.at("09", "goes off"), False)
    c.show(f"#{p}-yel", c.at("09", "goes off"), False)
    c.tl.to(f"#{p}-uri", {"attr": {"fill": URINE[1]}, "scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.8}, t + 0.6)
    c.tl.to(f"#{p}-adh", {"opacity": 0, "duration": 0.3}, t + 0.3)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t + 0.2)
    t = c.at("09", "older adults")
    for sel in (f"#{p}-kid", f"#{p}-uri", f"#{p}-urit", f"#{p}-gl"):
        c.blur_out(sel, t - 0.3, 0.2)
    popl(c, f"#{p}-old", t)
    c.blur_in(f"#{p}-lold", c.at("09", "arrives later"))
    c.tl.to(N, {"rotation": 55, **O, "duration": 1.2, "ease": "power2.inOut"}, t + 0.4)
    c.show(f"#{p}-yel", c.at("09", "arrives later", off=0.3))
    c.tl.ft(f"#{p}-yel", {"opacity": 0.25}, {"opacity": 0.6, "duration": 0.5, "yoyo": True, "repeat": 3}, c.at("09", "arrives later", off=0.3))
    idle(c, f"{p}-suy-nghi", 0, S(c, "09", "You drink"), 1)
    idle(c, f"{p}-vui", S(c, "09", "You drink") + 0.8, end, 2)
    return c


# ---------------------------------------------------------------- 10 · Running low
def s10():
    c = comp("10")
    p = c.cid
    close = board(c, ("suy-nghi", "lo-lang"))

    def panel(id_, x, title, lines, icons):
        body = (f'<rect x="{x}" y="160" width="560" height="560" rx="30" fill="#1D4262" stroke="{INK}" stroke-width="6"/>'
                + text(x + 280, 240, title, 50, 900, YELLOW, "middle") + icons
                + "".join(text(x + 280, 560 + 60 * k, ln, 40, 800, WHITE, "middle") for k, ln in enumerate(lines)))
        return g(id_, body)
    icons_f = (pain_lines(f"{p}-pf", 830, 380, 1.6)
               + place(990, 400, g(f"{p}-bat", f'<rect x="-50" y="-30" width="100" height="60" rx="10" fill="none" stroke="{WHITE}" stroke-width="8"/>'
                                               f'<rect x="54" y="-12" width="10" height="24" fill="{WHITE}"/><rect x="-40" y="-20" width="22" height="40" fill="{CORAL}"/>'))
               + text(1130, 430, "?", 110, 900, WHITE, "middle"))
    icons_m = (place(1440, 400, g(f"{p}-eye", f'<path d="M-70 0 Q0 -60 70 0 Q0 60 -70 0 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
                                              f'<circle r="22" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
                                              f'<path d="M-70 -10 Q0 -40 70 -10" fill="none" stroke="{INK}" stroke-width="8"/>'))
               + brain(f"{p}-mb", 1660, 400, 0.6))
    c.svg += [panel(f"{p}-pa", 680, "WOMEN · ~1.4% LOST", ["HEADACHE · TIRED", "HARD TO FOCUS"], icons_f),
              panel(f"{p}-pb", 1300, "MEN · MILD", ["LESS ALERT", "WORKING MEMORY DIPS"], icons_m),
              f'<g transform="translate(1270 830) rotate(-3)"><g id="{p}-stamp"><rect x="-480" y="-56" width="960" height="100" rx="14" '
              f'fill="{SLATE}" stroke="{YELLOW}" stroke-width="8"/>{text(0, 16, "RESULTS ACROSS STUDIES STILL MIXED", 44, 900, YELLOW, "middle")}</g></g>',
              text(1270, 990, "Armstrong 2012 · Ganio 2011", 28, 500, GREY, "middle", id_=f"{p}-src"),
              g(f"{p}-sport", sun(f"{p}-sun", 1600, 260, 0.9) + pictogram(f"{p}-run", 1000, 420, 1.6, "run")
                + label(f"{p}-l2", 1270, 760, "LOSE > 2% BODY WEIGHT → LESS ENDURANCE", 50, YELLOW, "middle")
                + text(1270, 840, "especially in the heat · ACSM 2007", 34, 600, GREY, "middle")),
              g(f"{p}-sev", place(1270, 330, g(f"{p}-cross", f'<circle r="110" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                                                              f'<path d="M-25 -65 H25 V-25 H65 V25 H25 V65 H-25 V25 H-65 V-25 H-25 Z" fill="#FFFFFF"/>'))
                + label(f"{p}-s1", 1270, 580, "LONG DIARRHEA, VOMITING → DANGEROUS", 54, CORAL, "middle")
                + label(f"{p}-s2", 1270, 680, "WATER + SALTS (ORS) · SEE A DOCTOR", 54, WHITE, "middle")),
              label(f"{p}-q", 1270, 540, "IGNORE THE SIGNALS?", 88, WHITE, "middle"),
              label(f"{p}-sy0", 1270, 300, "HEADACHE", 76, CORAL, "middle"),
              label(f"{p}-sy1", 1270, 410, "SLUGGISH", 76, YELLOW, "middle"),
              label(f"{p}-sy2", 1270, 520, "HARD TO FOCUS", 76, WHITE, "middle"),
              label(f"{p}-t3", 1270, 790, "3:00 PM", 160, WHITE, "middle")]
    close()
    end = c.loc(SCENES["10"]["end"])
    c.hide(f"#{p}-pa", f"#{p}-pb", f"#{p}-stamp", f"#{p}-src", f"#{p}-sport", f"#{p}-sev", f"#{p}-s1", f"#{p}-s2", f"#{p}-t3",
           f"#{p}-q", f"#{p}-sy0", f"#{p}-sy1", f"#{p}-sy2")
    popl(c, f"#{p}-q", S(c, "10", "So what happens"))
    t = c.at("10", "In one experiment")
    c.blur_out(f"#{p}-q", t - 0.3, 0.25)
    popl(c, f"#{p}-pa", t, "50% 100%")
    c.blur_in(f"#{p}-src", t)
    popl(c, f"#{p}-pb", c.at("10", "Another experiment"), "50% 100%")
    t = c.at("10", "The results across")
    c.show(f"#{p}-stamp", t)
    c.tl.ft(f"#{p}-stamp", {"scale": 1.6, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3,
                                                                          "ease": "power4.in"}, t)
    c.sfx("thump", t + 0.3)
    t = c.at("10", "But for exercise")
    for sel in (f"#{p}-pa", f"#{p}-pb", f"#{p}-stamp", f"#{p}-src"):
        c.blur_out(sel, t, 0.25)
    c.show(f"#{p}-sport", t + 0.2)
    c.tl.ft(f"#{p}-run", {"x": -300}, {"x": 0, "duration": 0.8, "ease": "expo.out"}, t + 0.2)
    c.sfx("whoosh", t + 0.2)
    t = c.at("10", "Severe dehydration")
    c.blur_out(f"#{p}-sport", t - 0.3, 0.25)
    c.show(f"#{p}-sev", t)
    c.pop(f"#{p}-cross", t, 0.5)
    c.sfx("thump", t)
    c.blur_in(f"#{p}-s1", c.at("10", "can be dangerous", off=-0.4))
    c.blur_in(f"#{p}-s2", c.at("10", "Then you need"))
    t = S(c, "10", "Headache")
    c.blur_out(f"#{p}-sev", t - 0.3, 0.25)
    swap(c, f"{p}-suy-nghi", f"{p}-lo-lang", t)
    for k, pre in enumerate(("Headache", "Sluggish", "Hard to focus")):
        popl(c, f"#{p}-sy{k}", S(c, "10", pre) + 0.2, snd="pop")
    popl(c, f"#{p}-t3", S(c, "10", "That's you"), snd="thump")
    idle(c, f"{p}-suy-nghi", 0, t, 1)
    idle(c, f"{p}-lo-lang", t + 0.6, end, 2)
    return c


def opt_row(prefix, x, y, letter, icon, lab):
    return g(prefix, f"""<rect id="{prefix}-box" x="{x - 30}" y="{y - 86}" width="1170" height="172" rx="28" fill="none" stroke="{YELLOW}" stroke-width="8" opacity="0"/>
{text(x + 50, y + 44, letter, 128, 900, YELLOW, "middle")}
<g transform="translate({x + 290} {y})">{icon}</g>
{text(x + 470, y + 16, lab, 48, 800, WHITE)}
<line id="{prefix}-strike" x1="{x - 20}" y1="{y}" x2="{x + 1130}" y2="{y}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>""")


def options(prefix, x=690):
    eight = "".join(glass(f"{prefix}-g{k}", -105 + (k % 4) * 70, -12 + (k // 4) * 70, 0.24, 0.75) for k in range(8))
    check = glass(f"{prefix}-gb", -40, 70, 0.5, 0.7) + f'<path d="M30 -10 L60 25 L120 -50" fill="none" stroke="{TEAL}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
    spill = (glass(f"{prefix}-gc", 0, 70, 0.5, 1.0) + tear(f"{prefix}-s1", -70, 40, 0.9) + tear(f"{prefix}-s2", 70, 20, 0.8)
             + tear(f"{prefix}-s3", 60, 70, 0.7))
    return (opt_row(f"{prefix}a", x, 300, "A", eight, "EXACTLY 8 GLASSES A DAY")
            + opt_row(f"{prefix}b", x, 530, "B", check, "DRINK WHEN THIRSTY")
            + opt_row(f"{prefix}c", x, 760, "C", spill, "THE MORE, THE BETTER"))


# ---------------------------------------------------------------- 11 · The question
def s11():
    c = comp("11")
    p = c.cid
    close = board(c)
    c.svg.append(options(f"{p}-o"))
    c.svg.append(label(f"{p}-q", 1270, 560, "HOW SHOULD YOU DRINK?", 84, WHITE, "middle"))
    close()
    idle(c, f"{p}-suy-nghi", 0, c.loc(SCENES["11"]["end"]), 2)
    c.hide(f"#{p}-q")
    popl(c, f"#{p}-q", S(c, "11", "So, on"))
    c.blur_out(f"#{p}-q", c.at("11", "a", 1) - 0.3, 0.25)
    for L, nth in (("a", 1), ("b", 0), ("c", 0)):
        t = c.at("11", L, nth)
        c.hide(f"#{p}-o{L}")
        c.tl.ft(f"#{p}-o{L}", {"autoAlpha": 0, "x": 60, "filter": "blur(8px)"},
                {"autoAlpha": 1, "x": 0, "filter": "blur(0px)", "duration": 0.45, "ease": "expo.out"}, t)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 12 · Take a guess
def s12():
    c = comp("12")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>',
              f'<circle cx="1590" cy="560" r="220" fill="{WATER}" stroke="{INK}" stroke-width="10"/>',
              text(1590, 300, "PAUSE THE VIDEO", 44, 900, INK, "middle"),
              g("s12-n", "".join(text(1590, 660, str(n), 300, 900, INK, "middle", id_=f"s12-n{n}") for n in (3, 2, 1)))]
    lines = [("h", "Take a guess first!"),
             ("f", "1. Your body loses water all the time, even sitting still."),
             ("f", "2. Thicker blood → ADH holds water, then thirst kicks in."),
             ("f", "3. Needs change with heat, exercise and age."),
             ("f", "4. Your kidneys have a speed limit."),
             ("o", "A. Exactly 8 glasses a day"), ("o", "B. Drink when thirsty, more when needed, check your pee"),
             ("o", "C. The more, the better")]
    c.css.append(f"#s12-card {{ left: 130px; top: 110px; width: 1180px; color: {INK}; }}"
                 "#s12-card .h { font-size: 80px; font-weight: 800; margin-bottom: 30px; letter-spacing: -0.01em; }"
                 "#s12-card .f { font-size: 38px; font-weight: 600; line-height: 1.3; margin-bottom: 14px; }"
                 "#s12-card .o { font-size: 42px; font-weight: 800; margin-top: 8px; line-height: 1.25; }"
                 "#s12-card .gap { height: 26px; }")
    items = []
    for k, (cls, tx) in enumerate(lines):
        if cls == "o" and lines[k - 1][0] == "f":
            items.append('<div class="gap"></div>')
        items.append(f'<div id="s12-l{k}" class="{cls}">{tx}</div>')
    c.html.append(f'<div id="s12-card" class="txt" data-hold="true">{"".join(items)}</div>')
    for k in range(len(lines)):
        c.blur_in(f"#s12-l{k}", 0.1 + 0.07 * k, 0.18)
    c.hide("#s12-n2", "#s12-n1")
    c.tl.ft("#s12-n3", {"scale": 0.4, "transformOrigin": "50% 50%"},
            {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.5, "ease": "back.out(1.8)"}, 0.2)
    c.sfx("pop", 0.2)
    for a, b, t in ((3, 2, 3.4), (2, 1, 6.4)):
        c.show(f"#s12-n{a}", t, False)
        c.pop(f"#s12-n{b}", t, 0.5, "50% 50%", "back.out(1.8)", 0.4)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 13 · The key
def s13():
    c = comp("13")
    p = c.cid
    close = board(c)
    c.svg.append(g(f"{p}-bub", f"""<circle cx="560" cy="560" r="18" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>
<circle cx="640" cy="500" r="28" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>
<path d="M760 420 C700 300 820 170 980 210 C1060 120 1300 110 1380 190 C1520 120 1760 190 1740 320 C1830 380 1790 560 1640 560 C1580 650 1340 650 1260 590 C1140 660 900 650 860 560 C720 590 650 470 760 420 Z" fill="{PAPER}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
{balance(f"{p}-bal", 1010, 300, 0.3)}
{text(1200, 340, "A FIXED NUMBER", 50, 900, INK)}
<line id="{p}-strike" x1="1190" y1="322" x2="1640" y2="322" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>
{text(1220, 470, "BALANCE", 96, 900, WATER_DARK, id_=f"{p}-cb")}"""))
    close()
    c.css.append(f"#{p}-qs {{ left: 700px; top: 770px; width: 1120px; font-size: 76px; font-weight: 800; color: {WHITE}; "
                 f"line-height: 1.15; }} #{p}-qs b {{ color: {YELLOW}; font-weight: 900; }}")
    c.html.append(f'<div id="{p}-qs" class="txt">Where did <b>8 glasses</b> come from?</div>')
    idle(c, f"{p}-suy-nghi", 0, c.loc(SCENES["13"]["end"]), 0)
    c.pop(f"#{p}-bub", 0.15, 0.6, "0% 100%", "back.out(1.3)", 0.3)
    c.sfx("pop", 0.15)
    c.draw(f"#{p}-strike", c.at("13", "fixed number", which="end", off=-0.3), 0.4)
    c.sfx("pop", c.at("13", "fixed number", which="end"))
    c.blur_in(f"#{p}-cb", c.at("13", "It needs balance"), 0.2)
    c.blur_in(f"#{p}-qs", S(c, "13", "So where did"), 0.2)
    return c


# ---------------------------------------------------------------- 14 · The eight-glasses myth
def s14():
    c = comp("14")
    p = c.cid
    close = board(c)
    glasses8 = "".join(glass(f"{p}-g{k}", 740 + k * 145, 600, 0.5, 0.75) for k in range(8))
    cols = [(820, "WOMEN", "2.0 L", 0.62), (1060, "MEN", "2.5 L", 0.78), (1420, "WOMEN", "2.7 L", 0.84), (1660, "MEN", "3.7 L", 1.0)]
    tall = "".join(g(f"{p}-t{k}", glass(f"{p}-tg{k}", x, 690, 0.8, lv) + label(f"{p}-tl{k}", x, 760, sx, 42, GREY, "middle") + label(f"{p}-tv{k}", x, 820, v, 52, WHITE, "middle"))
                   for k, (x, sx, v, lv) in enumerate(cols))
    c.svg += [g(f"{p}-eight", glasses8), label(f"{p}-l2", 1250, 760, "8 × 250 ML ≈ 2 LITERS", 70, YELLOW, "middle"),
              report1945(f"{p}-rep", 760, 250, ("≈ 2.5 LITERS / DAY", "MOST OF IT IS", "ALREADY IN FOOD")),
              magnifier(f"{p}-mag", 1500, 470, 1.2),
              label(f"{p}-lv", 1580, 720, "HEINZ VALTIN · 2002", 52, WHITE, "middle"),
              label(f"{p}-lno", 1560, 830, "8 GLASSES: NO SOLID EVIDENCE", 44, CORAL, "middle"),
              tall, label(f"{p}-heu", 940, 420, "EUROPE · EFSA 2010", 46, TEAL, "middle"),
              label(f"{p}-hus", 1540, 420, "USA · 2004", 46, TEAL, "middle"),
              label(f"{p}-ref", 1240, 260, "DAILY REFERENCE VALUE", 76, WHITE, "middle"),
              label(f"{p}-food", 1250, 900, "TOTAL WATER, INCLUDING WATER IN FOOD", 44, YELLOW, "middle"),
              text(1250, 980, "Based on what healthy people typically take in", 34, 600, GREY, "middle", id_=f"{p}-why")]
    close()
    end = c.loc(SCENES["14"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 3)
    c.hide(f"#{p}-l2", f"#{p}-rep", f"#{p}-mag", f"#{p}-lv", f"#{p}-lno", f"#{p}-heu", f"#{p}-hus", f"#{p}-food", f"#{p}-why", f"#{p}-ref",
           *[f"#{p}-g{k}" for k in range(8)], *[f"#{p}-t{k}" for k in range(4)])
    t = S(c, "14", "Eight glasses")
    for k in range(8):
        c.pop(f"#{p}-g{k}", t + 0.08 * k, 0.35, "50% 100%")
    c.sfx("pop", t)
    popl(c, f"#{p}-l2", c.at("14", "about two liters"), snd="thump")
    t = S(c, "14", "In 1945")
    c.blur_out(f"#{p}-eight", t - 0.2, 0.25)
    c.blur_out(f"#{p}-l2", t - 0.2, 0.25)
    c.pop(f"#{p}-rep", t, 0.6, "50% 100%", "back.out(1.4)", 0.6)
    c.sfx("whoosh", t)
    c.tl.to(f"#{p}-rep-hl1", {"opacity": 1, "duration": 0.3}, c.at("14", "two and a half liters"))
    c.tl.to(f"#{p}-rep-hl2", {"opacity": 1, "duration": 0.3}, c.at("14", "already in your food"))
    t = S(c, "14", "In 2002")
    popl(c, f"#{p}-mag", t)
    c.blur_in(f"#{p}-lv", t + 0.2)
    t = c.at("14", "simply been forgotten")
    c.tl.to(f"#{p}-mag", {"x": -500, "y": 190, "duration": 0.8, "ease": "power2.inOut"}, t - 0.6)
    c.tl.ft(f"#{p}-rep-hl2", {"opacity": 1}, {"opacity": 0.2, "duration": 0.2, "yoyo": True, "repeat": 5}, t)
    popl(c, f"#{p}-lno", c.at("14", "no scientific evidence"), snd="thump")
    t = S(c, "14", "Today")
    for sel in (f"#{p}-rep", f"#{p}-mag", f"#{p}-lv", f"#{p}-lno"):
        c.blur_out(sel, t - 0.2, 0.25)
    popl(c, f"#{p}-ref", t + 0.1)
    c.blur_in(f"#{p}-heu", t + 0.2)
    popl(c, f"#{p}-t0", S(c, "14", "About two liters"), "50% 100%")
    popl(c, f"#{p}-t1", S(c, "14", "For men"), "50% 100%")
    c.blur_in(f"#{p}-food", S(c, "14", "That's total water"))
    c.blur_in(f"#{p}-hus", S(c, "14", "In the United States"))
    popl(c, f"#{p}-t2", c.at("14", "two point seven"), "50% 100%")
    popl(c, f"#{p}-t3", c.at("14", "three point seven"), "50% 100%")
    c.blur_out(f"#{p}-food", S(c, "14", "The numbers differ"), 0.2)
    c.blur_in(f"#{p}-why", S(c, "14", "They reflect"))
    return c


# ---------------------------------------------------------------- 15 · Where water comes from
def s15():
    c = comp("15")
    p = c.cid
    close = board(c)
    can = place(1640, 430, g(f"{p}-can", f'<rect x="-50" y="-100" width="100" height="190" rx="16" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                                          f'<rect x="-36" y="-118" width="72" height="22" rx="8" fill="{GREY}" stroke="{INK}" stroke-width="5"/>'
                                          f'<path d="M-50 -20 H50" stroke="#FFFFFF" stroke-width="10"/>'))
    c.svg += [watermelon(f"{p}-wm", 790, 470, 1.0), bowl(f"{p}-soup", 1020, 470, 0.85), bowl(f"{p}-rice", 1240, 470, 0.85, rice=True, steam=False),
              label(f"{p}-lf", 1000, 640, "≈ 1/5 – 1/3 FROM FOOD", 44, YELLOW, "middle"),
              label(f"{p}-l90", 790, 330, "> 90% WATER", 48, WHITE, "middle"),
              coffee_cup(f"{p}-cof", 1460, 470, 1.0), can, glass(f"{p}-gl", 1790, 540, 0.65, 0.8),
              label(f"{p}-lc", 1470, 640, "✓ 4 CUPS/DAY", 40, TEAL, "middle"),
              text(1470, 700, "≈ water · regular drinkers · 2014", 30, 600, GREY, "middle", id_=f"{p}-lc2"),
              label(f"{p}-ls", 1640, 260, "+ SUGAR", 46, CORAL, "middle"),
              label(f"{p}-lg", 1790, 330, "BEST", 44, WATER, "middle"),
              urine_scale(f"{p}-us", 760, 440, 160, 200, 24),
              label(f"{p}-u1", 930, 400, "HYDRATED ✓", 52, TEAL, "middle"),
              label(f"{p}-u2", 1430, 400, "DRINK MORE", 52, CORAL, "middle"),
              text(1220, 760, "MEDICINES, VITAMINS CAN CHANGE IT · JUST A HINT", 38, 800, GREY, "middle", id_=f"{p}-u3"),
              text(1220, 820, "Armstrong et al., 1994", 28, 500, GREY, "middle", id_=f"{p}-u4"),
              g(f"{p}-q", label(f"{p}-q1", 1270, 500, "WHERE DOES YOUR", 84, WHITE, "middle")
                + label(f"{p}-q2", 1270, 610, "WATER COME FROM?", 84, WATER, "middle"))]
    close()
    end = c.loc(SCENES["15"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 1)
    food = (f"#{p}-wm", f"#{p}-soup", f"#{p}-rice", f"#{p}-lf", f"#{p}-l90", f"#{p}-cof", f"#{p}-can", f"#{p}-gl", f"#{p}-lc",
            f"#{p}-lc2", f"#{p}-ls", f"#{p}-lg")
    c.hide(*food, f"#{p}-us", f"#{p}-u1", f"#{p}-u2", f"#{p}-u3", f"#{p}-u4", *[f"#{p}-us-{k}" for k in range(5)])
    c.hide(f"#{p}-q")
    popl(c, f"#{p}-q", S(c, "15", "So where"))
    t = S(c, "15", "About a fifth")
    c.blur_out(f"#{p}-q", t - 0.3, 0.25)
    for k, sel in enumerate((f"#{p}-wm", f"#{p}-soup", f"#{p}-rice")):
        popl(c, sel, t + 0.4 * k, "50% 100%", snd="pop" if k == 0 else None)
    popl(c, f"#{p}-lf", c.at("15", "a fifth"), snd=None)
    t = c.at("15", "Watermelon")
    c.tl.ft(f"#{p}-wm", {"scale": 1}, {"scale": 1.15, "transformOrigin": "50% 100%", "duration": 0.25, "yoyo": True, "repeat": 1}, t)
    popl(c, f"#{p}-l90", c.at("15", "ninety percent"))
    popl(c, f"#{p}-cof", c.at("15", "Tea and coffee"), "50% 100%")
    c.blur_in(f"#{p}-lc", c.at("15", "At four cups"))
    c.blur_in(f"#{p}-lc2", c.at("15", "At four cups", off=0.4))
    popl(c, f"#{p}-can", c.at("15", "Soft drinks"), "50% 100%")
    popl(c, f"#{p}-ls", c.at("15", "sugar"))
    popl(c, f"#{p}-gl", c.at("15", "So plain water"), "50% 100%")
    c.blur_in(f"#{p}-lg", c.at("15", "best choice"))
    t = c.at("15", "look at the color", off=-0.35)
    for sel in food:
        c.blur_out(sel, t, 0.25)
    t = c.at("15", "look at the color")
    c.show(f"#{p}-us", t)
    for k in range(5):
        c.pop(f"#{p}-us-{k}", t + 0.08 * k, 0.35, "50% 100%")
    c.sfx("pop", t)
    popl(c, f"#{p}-u1", c.at("15", "Pale straw yellow"))
    popl(c, f"#{p}-u2", c.at("15", "Dark yellow"))
    c.blur_in(f"#{p}-u3", c.at("15", "Some medicines"))
    c.blur_in(f"#{p}-u4", c.at("15", "Some medicines", off=0.3))
    return c


# ---------------------------------------------------------------- 16 · When to drink more
def s16():
    c = comp("16")
    p = c.cid
    close = board(c, ("suy-nghi", "lo-lang"))
    icons = [(sun(f"{p}-i0", 760, 420, 0.8), "HOT", "it's hot"),
             (pictogram(f"{p}-i1", 1000, 420, 0.9, "run"), "EXERCISE", "exercise hard"),
             (thermometer(f"{p}-i2", 1240, 430, 0.9, 0.85), "SICK", "a fever"),
             (pictogram(f"{p}-i3", 1480, 420, 0.9, "preg"), "PREGNANT", "Pregnant"),
             (pictogram(f"{p}-i4", 1720, 420, 0.9, "elder"), "OLDER", "Older adults")]
    na = "".join(place(1300 + (k % 4) * 140, 450 + (k // 4) * 80, g(f"{p}-na{k}", f'<circle r="26" fill="{YELLOW}" stroke="{INK}" stroke-width="5"/>'
                                                                               + text(0, 10, "Na", 26, 900, INK, "middle")))
                 for k in range(8))
    medal_svg = place(1000, 520, g(f"{p}-med", f'<path d="M-60 -220 L-14 -40 L14 -40 L60 -220 Z" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                                                f'<circle cy="40" r="100" fill="{YELLOW}" stroke="{INK}" stroke-width="6"/>'
                                                + text(0, 28, "BOSTON", 34, 900, INK, "middle") + text(0, 76, "2002", 44, 900, INK, "middle")))
    c.svg += ["".join(icon for icon, _, _ in icons),
              "".join(text(x, 620, lb, 40, 900, WHITE, "middle", id_=f"{p}-il{k}")
                      for k, (x, (_, lb, _)) in enumerate(zip((760, 1000, 1240, 1480, 1720), icons))),
              g(f"{p}-gau", gauge(f"{p}-gg", 900, 560, 150, "KIDNEY SPEED LIMIT")),
              g(f"{p}-blood", f'<rect x="1220" y="370" width="620" height="200" rx="30" fill="{WATER}" stroke="{INK}" stroke-width="6"/>{na}'),
              label(f"{p}-hypo", 1530, 680, "HYPONATREMIA", 70, CORAL, "middle"),
              label(f"{p}-ttl", 1240, 250, "DRINK MORE WHEN…", 76, YELLOW, "middle"),
              label(f"{p}-more", 1270, 560, "MORE ≠ BETTER", 110, CORAL, "middle"),
              medal_svg, label(f"{p}-l13", 1450, 520, "≈ 13%", 140, CORAL, "middle"),
              text(1450, 600, "of runners tested", 36, 700, WHITE, "middle", id_=f"{p}-l13b"),
              text(1270, 760, "Highest risk: gained weight during the race = drank more than they sweated", 30, 700, GREY, "middle", id_=f"{p}-lw"),
              f'<g id="{p}-warn"><rect x="660" y="830" width="1220" height="110" rx="20" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
              + text(1270, 902, "HEART OR KIDNEY DISEASE: FOLLOW YOUR DOCTOR", 40, 900, "#FFFFFF", "middle") + "</g>"]
    close()
    end = c.loc(SCENES["16"]["end"])
    c.hide(*[f"#{p}-i{k}" for k in range(5)], *[f"#{p}-il{k}" for k in range(5)], f"#{p}-gau", f"#{p}-blood", f"#{p}-hypo",
           f"#{p}-med", f"#{p}-l13", f"#{p}-l13b", f"#{p}-lw", f"#{p}-warn", f"#{p}-more", f"#{p}-ttl")
    popl(c, f"#{p}-ttl", S(c, "16", "There are times"))
    for k, (_, _, w) in enumerate(icons):
        t = c.at("16", w)
        popl(c, f"#{p}-i{k}", t, "50% 100%")
        c.blur_in(f"#{p}-il{k}", t + 0.2)
    t = c.at("16", "more is not always better")
    c.blur_out(f"#{p}-ttl", t - 0.2, 0.2)
    for k in range(5):
        c.blur_out(f"#{p}-i{k}", t - 0.2, 0.2)
        c.blur_out(f"#{p}-il{k}", t - 0.2, 0.2)
    swap(c, f"{p}-suy-nghi", f"{p}-lo-lang", t)
    popl(c, f"#{p}-more", t + 0.3, snd="thump")
    c.blur_out(f"#{p}-more", c.at("16", "speed limit", off=-0.6), 0.2)
    t = c.at("16", "speed limit")
    popl(c, f"#{p}-gau", t - 0.4, "50% 100%")
    c.tl.ft(f"#{p}-gg-n", {"rotation": -40}, {"rotation": 80, "svgOrigin": "900 560", "duration": 1.0, "ease": "power2.in"}, t)
    t = c.at("16", "dilutes the sodium")
    c.pop(f"#{p}-blood", t - 0.5, 0.5, "0% 50%", "expo.out", 0.4)
    for k in range(8):
        c.tl.to(f"#{p}-na{k}", {"x": (k % 4 - 1.5) * 18, "y": (k // 4 - 0.5) * 30, "scale": 0.7, "opacity": 0.55, "duration": 1.2,
                                "ease": "power2.inOut"}, t + 0.2)
    popl(c, f"#{p}-hypo", c.at("16", "hyponatremia", 0), snd="thump")
    t = c.at("16", "Boston Marathon")
    for sel in (f"#{p}-gau", f"#{p}-blood", f"#{p}-hypo"):
        c.blur_out(sel, t - 0.2, 0.25)
    c.show(f"#{p}-med", t)
    c.tl.ft(f"#{p}-med", {"rotation": -25, "y": -200}, {"rotation": 0, "y": 0, "transformOrigin": "50% 0%", "duration": 1.4,
                                                       "ease": "elastic.out(1, 0.4)"}, t)
    c.sfx("whoosh", t)
    popl(c, f"#{p}-l13", c.at("16", "thirteen percent"), snd="thump")
    c.blur_in(f"#{p}-l13b", c.at("16", "thirteen percent", off=0.3))
    c.blur_in(f"#{p}-lw", S(c, "16", "The risk was highest"))
    t = c.at("16", "heart or kidney disease")
    c.show(f"#{p}-warn", t)
    c.tl.ft(f"#{p}-warn", {"y": 160}, {"y": 0, "duration": 0.5, "ease": "expo.out"}, t)
    c.sfx("whoosh", t)
    idle(c, f"{p}-suy-nghi", 0, c.at("16", "more is not always better"), 1)
    idle(c, f"{p}-lo-lang", c.at("16", "more is not always better", off=0.6), end, 3)
    return c


# ---------------------------------------------------------------- 17 · Elimination
def s17():
    c = comp("17")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [options(f"{p}-o"),
              f'<ellipse id="{p}-ring" cx="1265" cy="530" rx="600" ry="128" pathLength="1" stroke-dasharray="1 1.2" '
              f'stroke-dashoffset="1.1" fill="none" stroke="{YELLOW}" stroke-width="12"/>']
    close()
    end = c.loc(SCENES["17"]["end"])
    for j, L in enumerate("abc"):
        c.tl.ft(f"#{p}-o{L}", {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0, "duration": 0.45, "ease": "expo.out"}, 0.2 + 0.1 * j)
    for L, nth in (("a", 0), ("c", 1)):
        tp = c.at("17", f"Option {L.upper()}")
        c.tl.ft(f"#{p}-o{L}-box", {"opacity": 0}, {"opacity": 1, "duration": 0.2}, tp)
        tlo = c.at("17", "Out", nth)
        c.draw(f"#{p}-o{L}-strike", tlo, 0.3, "power3.out")
        c.sfx("pop", tlo)
        c.tl.to(f"#{p}-o{L}-box", {"opacity": 0, "duration": 0.2}, tlo + 0.5)
        c.tl.to(f"#{p}-o{L}", {"opacity": 0.5, "duration": 0.3}, tlo + 0.6)
    t = c.at("17", "option B")
    c.draw(f"#{p}-ring", t, 0.6)
    c.sfx("pop", t)
    tl_ = S(c, "17", "That leaves")
    swap(c, f"{p}-suy-nghi", f"{p}-vui", tl_)
    idle(c, f"{p}-suy-nghi", 0, tl_, 3)
    idle(c, f"{p}-vui", tl_ + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 18 · The answer
def s18():
    c = comp("18")
    p = c.cid
    poses = ["uong", "vui"]
    extra = place(1180, 300, g(f"{p}-chip", f'<rect x="-50" y="-50" width="100" height="100" rx="18" fill="{URINE[1]}" stroke="{INK}" stroke-width="6"/>'
                                            f'<path d="M-22 0 L-4 20 L28 -22" fill="none" stroke="{TEAL}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'))
    cam, st = office_comp(c, poses, extra)
    c.svg += [label(f"{p}-no", 960, 950, "NO NEED TO FORCE A WHOLE LITER", 66, CORAL, "middle"),
              g(f"{p}-b", f'<rect width="1920" height="1080" fill="{SLATE}"/>'
                + text(960, 720, "B", 560, 900, YELLOW, "middle", extra=" " + OUTLINE)
                + f'<circle id="{p}-ring" cx="960" cy="530" r="300" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" '
                  f'fill="none" stroke="{YELLOW}" stroke-width="16"/>' + slate_border())]
    c.hide(f"#{p}-no", f"#{p}-chip")
    end = c.loc(SCENES["18"]["end"])
    tq = S(c, "18", "Back to three")
    c.tl.ft(f"#{p}-b", {"scale": 1.3, "svgOrigin": "960 540", "filter": "blur(10px)", "opacity": 0},
            {"scale": 1, "svgOrigin": "960 540", "filter": "blur(0px)", "opacity": 1, "duration": 0.35, "ease": "power3.out"}, 0.05)
    c.draw(f"#{p}-ring", 0.4, 0.5)
    c.sfx("riser", 0.3)
    c.sfx("thump", 0.3)
    c.show(f"#{p}-b", tq, False)
    frame(c, tq, OFF_CX - 100, OFF_FEET - OFF_H * 0.62, 1.8, cam, st)
    c.tl.ft(f"#{p}-uong", {"rotation": 0}, {"rotation": -3, "transformOrigin": "50% 100%", "duration": 0.6, "yoyo": True, "repeat": 3,
                                           "ease": "sine.inOut"}, c.at("18", "a few sips"))
    c.sfx("pop", c.at("18", "one more glass"))
    t = S(c, "18", "No need to force")
    popl(c, f"#{p}-no", t, snd="thump")
    t = S(c, "18", "From tomorrow")
    c.show(f"#{p}-no", t, False)
    frame(c, t, 1150, 560, 1.15, cam, st)
    swap(c, f"{p}-uong", f"{p}-vui", t)
    c.tl.ft(cam, {"x": 960 - 1.15 * 1150, "y": 540 - 1.15 * 560, "scale": 1.15, "transformOrigin": "0 0"},
            {"x": 960 - 1.7 * BOTTLE[0], "y": 540 - 1.7 * (BOTTLE[1] - 60), "scale": 1.7, "transformOrigin": "0 0",
             "duration": 1.2, "ease": "power2.inOut"}, c.at("18", "where you can see it", off=-0.3))
    c.sfx("whoosh", c.at("18", "where you can see it", off=-0.2))
    t = c.at("18", "pale straw yellow")
    frame(c, t, 1300, 480, 1.25, cam, st)
    popl(c, f"#{p}-chip", t + 0.2)
    idle(c, f"{p}-vui", t + 0.5, end, 0)
    return c


# ---------------------------------------------------------------- 19 · The surprise: kidney stones
def s19():
    c = comp("19")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    base, k = 860, 20

    def bar(id_, x, pct, col, lb):
        h = pct * k
        return g(id_, f'<rect id="{id_}-r" x="{x - 110}" y="{base - h}" width="220" height="{h}" rx="16" fill="{col}" stroke="{INK}" stroke-width="6"/>'
                 + label(f"{id_}-v", x, base - h - 30, f"{pct}%", 90, col, "middle")
                 + text(x, base + 60, lb, 36, 800, WHITE, "middle"))
    c.svg += [stone(f"{p}-st", 820, 330, 1.4), label(f"{p}-lst", 820, 520, "KIDNEY STONES", 54, WHITE, "middle"),
              label(f"{p}-hd", 1330, 200, "ITALY · 1996 · ~200 PEOPLE · 5 YEARS", 44, YELLOW, "middle"),
              bar(f"{p}-b1", 1250, 12, WATER, "DRANK ENOUGH (≥ 2 L PEE)"), bar(f"{p}-b2", 1650, 27, CORAL, "OTHER GROUP"),
              text(1450, 980, "stones came back · Borghi et al.", 30, 600, GREY, "middle", id_=f"{p}-src"),
              f'<g id="{p}-aua"><rect x="680" y="590" width="1180" height="160" rx="24" fill="#1D4262" stroke="{TEAL}" stroke-width="6"/>'
              + text(1270, 660, "AUA GUIDELINE 2014, FOR PEOPLE WHO'VE HAD STONES:", 36, 900, TEAL, "middle")
              + text(1270, 722, "DRINK ENOUGH TO PEE ≥ 2.5 LITERS A DAY", 48, 900, WHITE, "middle") + "</g>",
              label(f"{p}-one", 1270, 540, "+1 SURPRISING BENEFIT", 80, YELLOW, "middle")]
    close()
    end = c.loc(SCENES["19"]["end"])
    c.hide(f"#{p}-st", f"#{p}-lst", f"#{p}-hd", f"#{p}-b1", f"#{p}-b2", f"#{p}-src", f"#{p}-aua", f"#{p}-b1-v", f"#{p}-b2-v")
    c.hide(f"#{p}-one")
    popl(c, f"#{p}-one", S(c, "19", "And there's"))
    c.blur_out(f"#{p}-one", S(c, "19", "In 1996") - 0.3, 0.25)
    ts = c.at("19", "surprising benefit")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", ts)
    t = S(c, "19", "In 1996")
    popl(c, f"#{p}-st", t)
    c.blur_in(f"#{p}-lst", t + 0.3)
    c.blur_in(f"#{p}-hd", c.at("19", "nearly two hundred"))
    t = S(c, "19", "One group")
    c.show(f"#{p}-b1", t)
    c.tl.set(f"#{p}-b1-r", {"scaleY": 0.05, "transformOrigin": "50% 100%"}, t)
    c.blur_in(f"#{p}-src", t)
    t = c.at("19", "twelve percent")
    c.tl.to(f"#{p}-b1-r", {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.8, "ease": "expo.out"}, t)
    popl(c, f"#{p}-b1-v", t + 0.5)
    t = S(c, "19", "In the other group")
    c.show(f"#{p}-b2", t)
    c.tl.set(f"#{p}-b2-r", {"scaleY": 0.05, "transformOrigin": "50% 100%"}, t)
    t = c.at("19", "twenty-seven percent")
    c.tl.to(f"#{p}-b2-r", {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.9, "ease": "expo.out"}, t)
    popl(c, f"#{p}-b2-v", t + 0.5, snd="thump")
    t = S(c, "19", "The American Urological")
    for sel in (f"#{p}-b1", f"#{p}-b2", f"#{p}-src", f"#{p}-hd"):
        c.blur_out(sel, t - 0.2, 0.25)
    c.show(f"#{p}-aua", t)
    c.tl.ft(f"#{p}-aua", {"y": 120}, {"y": 0, "duration": 0.6, "ease": "expo.out"}, t)
    c.sfx("whoosh", t)
    idle(c, f"{p}-suy-nghi", 0, ts, 1)
    idle(c, f"{p}-ngac-nhien", ts + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 20 · The twist: meeting room
def s20():
    c = comp("20")
    p = c.cid
    DOOR = (1810, 560)
    c.svg += [f'<image href="assets/bg/phong-hop.jpg" width="1920" height="1080"/>',
              f'<g id="{p}-slide">{text(758, 300, "WATER & YOUR BODY", 60, 900, INK, "middle")}'
              f'<path d="M500 520 L640 440 L760 470 L900 340 L1060 380" fill="none" stroke="{WATER}" stroke-width="16" '
              f'stroke-linecap="round" stroke-linejoin="round"/></g>',
              f'<g id="{p}-ok">{text(758, 600, "BALANCE ✓", 64, 900, TEAL, "middle")}</g>',
              char(f"{p}-vui", "vui", 1320, 880, 600), char(f"{p}-chay", "chay", 1320, 880, 560),
              "".join(text(x, y, "👏", 64, 400, INK, "middle", id_=f"{p}-cl{k}")
                      for k, (x, y) in enumerate(((120, 700), (420, 690), (760, 690), (1080, 700))))]
    c.hide(f"#{p}-ok", f"#{p}-chay-w", *[f"#{p}-cl{k}" for k in range(4)])
    end = c.loc(SCENES["20"]["end"])
    t = c.at("20", "applauds")
    for k in range(4):
        c.show(f"#{p}-cl{k}", t + 0.05 * k)
        c.tl.ft(f"#{p}-cl{k}", {"y": 0, "scale": 1}, {"y": -18, "scale": 1.15, "transformOrigin": "50% 50%", "duration": 0.15,
                                                     "yoyo": True, "repeat": 9, "ease": "sine.inOut"}, t + 0.05 * k)
        c.show(f"#{p}-cl{k}", t + 3.2, False)
    c.sfx("pop", t)
    t = c.at("20", "take a bow")
    c.tl.to(f"#{p}-vui", {"rotation": 10, "transformOrigin": "50% 100%", "duration": 0.35, "ease": "power2.out", "yoyo": True, "repeat": 1}, t)
    t = c.at("20", "dash straight")
    swap(c, f"{p}-vui", f"{p}-chay", t)
    c.tl.to(f"#{p}-chay-w", {"x": DOOR[0] - 1320, "duration": 0.7, "ease": "power3.in"}, t + 0.15)
    c.tl.to(f"#{p}-chay-w", {"opacity": 0, "duration": 0.1}, t + 0.82)
    c.sfx("whoosh", t + 0.2)
    c.sfx("thump", t + 0.85)
    popl(c, f"#{p}-ok", c.at("20", "keeping its balance"))
    idle(c, f"{p}-vui", 0, c.at("20", "take a bow"), 2)
    return c


# ---------------------------------------------------------------- 21 · End card
def s21():
    c = comp("21")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', char("s21-to", "vui", 1600, 1010, 720)]
    lines = [("big", "Thirsty? Drink.<br>Hot, active or sick? Drink more.<br>Don't force it."),
             ("lab", "Key sources"),
             ("src", "Popkin et al., <i>Nutrition Reviews</i> (2010) · EFSA (2010) · US National Academies (2004)"),
             ("src", "Valtin, <i>Am J Physiol</i> (2002) · Almond et al., <i>NEJM</i> (2005) · Borghi et al., <i>J Urol</i> (1996)"),
             ("src", "Full list in the description."),
             ("safe", "For general education only, not medical advice.<br>Heart or kidney disease: follow your doctor's advice.")]
    c.css.append(f"#s21-card {{ left: 130px; top: 110px; width: 1250px; color: {INK}; }}"
                 "#s21-card .big { font-size: 74px; font-weight: 800; line-height: 1.12; letter-spacing: -0.01em; margin-bottom: 48px; }"
                 "#s21-card .lab { font-size: 34px; font-weight: 800; color: #B5372A; margin-bottom: 10px; }"
                 "#s21-card .src { font-size: 30px; font-weight: 500; line-height: 1.45; color: #2A3A4A; }"
                 "#s21-card .safe { font-size: 34px; font-weight: 700; margin-top: 44px; line-height: 1.35; }")
    c.html.append('<div id="s21-card" class="txt" data-hold="true">'
                  + "".join(f'<div id="s21-l{k}" class="{cls}">{tx}</div>' for k, (cls, tx) in enumerate(lines)) + "</div>")
    for k in range(len(lines)):
        c.blur_in(f"#s21-l{k}", 0.2 + 0.12 * k, 0.2)
    c.tl.ft("#s21-to", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "expo.out"}, 0.3)
    idle(c, "s21-to", 1.0, c.loc(SCENES["21"]["end"]), 2)
    return c


BUILDERS = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21]

TRACKS = {"piz": 65.0, "mar": 46.0, "kal": 30.0, "lofi": 30.0, "doc": 39.0}


def music():
    """Giống bản tiếng Việt: pizzicato (truyện) → tài liệu/marimba → lofi/kalimba/tài liệu/marimba → pizzicato.
    Mức 0,14 dưới lời; 0,35 ở tiêu đề, đếm ngược, thẻ cuối."""
    lo, hi, xf = 0.14, 0.35, 1.2
    lifts = [(0, SCENES["01"]["end"]), (SCENES["12"]["start"], SCENES["12"]["end"]), (SCENES["21"]["start"], DURATION + 1)]
    plan = [(0, SCENES["04"]["start"], ["piz"]), (SCENES["04"]["start"], SCENES["11"]["start"], ["doc", "mar"]),
            (SCENES["11"]["start"], SCENES["18"]["start"], ["lofi", "kal", "doc", "mar"]), (SCENES["18"]["start"], DURATION, ["piz"])]
    tags, n = [], 0
    for a, b, cycle in plan:
        t, k = a, 0
        while t < b - 2:
            name = cycle[k % len(cycle)]
            dur = min(TRACKS[name], b + 0.6 - t, DURATION - t)
            pts = [(0, lo)]
            for la, lb in lifts:
                if la < t + dur and lb > t:
                    pts += [(max(la + 0.3 - t, 0.01), lo), (max(la + 1.0 - t, 0.02), hi), (max(lb - 0.6 - t, 0.03), hi), (max(lb - t, 0.04), lo)]
            pts = sorted({round(x, 2): v for x, v in pts}.items())
            if pts[0][0] > 0:
                pts = [(0, lo)] + pts
            last_seg = t + dur >= DURATION - 0.1
            tags.append(audio_tag(f"bgm{n:02d}", f"bgm/{name}.wav", t, dur, 40 + n % 4, 0.6 if k else 0.4,
                                  2.0 if last_seg else xf, pts))
            t += dur - xf
            k += 1
            n += 1
    return "\n".join(tags)


if __name__ == "__main__":
    core.run(BUILDERS, music, subs=True)
