"""Why are you tired after a day of doing nothing? — dựng HyperFrames từ audio/timeline.json + audio/words.json.
Chạy:  py build.py      (trong thư mục video\\)
Bộ dựng chung: scripts\\hf\\minh_hoa.py (nhân vật PNG, bảng, nhạc, phụ đề) + ve3.py (pin, xe đạp, nút chích điện, nhịp tim…).
Màu: run(..., mau=True) + scripts\\hf\\day_mau.py cho ảnh (nền tối hơn, dải màu rộng hơn).
"""
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from hf import core  # noqa: E402

core.init(__file__)
from hf.core import *  # noqa: E402,F401,F403
from hf.core import SCENES, WORDS, DURATION  # noqa: E402,F401
from hf.minh_hoa import *  # noqa: E402,F401,F403
from hf.ve2 import balance, bowl, heart, lamp, laptop, person_icon, pictogram  # noqa: E402,F401
from hf.ve3 import *  # noqa: E402,F401,F403

BLUE = "#4FB3E8"
NAVY = "#1D4262"
# Phòng khách ban ngày (assets/bg/phong-khach.jpg): sofa bên trái, TV bên phải, sàn trống 1/3 phải
L_CX, L_FEET, L_H = 1480, 1060, 760
L_SOFA, L_TV, L_WIN = (420, 560), (1500, 400), (1000, 250)


def end_of(c, sid):
    return c.loc(SCENES[sid]["end"])


def fade_seq(c, sels, t, dur=0.25):
    for s in sels:
        c.blur_out(s, t, dur)


def note(id_, x, y, s, size=28):
    return text(x, min(y, 948), s, size, 600, GREY, "middle", id_=id_)


def has(scene, prefix):
    return any(s["scene"] == scene and s["text"].startswith(prefix) for s in WORDS["sentences"])


def T(c, sid, *prefixes):
    """Mốc câu theo tiền tố; thử lần lượt (số có thể được ghi bằng chữ hoặc chữ số)."""
    for pre in prefixes:
        if has(sid, pre):
            return S(c, sid, pre)
    return S(c, sid, prefixes[0])


def clue(id_, s):
    return label(id_, 1270, 150, s, 58, YELLOW, "middle")


def bars(prefix, items, base=820, w=170):
    """Cột so sánh: items = [(x, cao, màu, nhãn)]; mỗi cột #prefix-b{k}."""
    return g(prefix, "".join(g(f"{prefix}-b{k}", f'<rect x="{x - w / 2}" y="{base - h}" width="{w}" height="{h}" rx="14" fill="{col}" '
                                                f'stroke="{INK}" stroke-width="6"/>' + text(x, base + 50, lab, 30, 800, WHITE, "middle"))
                             for k, (x, h, col, lab) in enumerate(items)))


def grow(c, sel, t, dur=0.6):
    c.tl.ft(sel, {"scaleY": 0, "transformOrigin": "50% 100%"}, {"scaleY": 1, "transformOrigin": "50% 100%", "duration": dur,
                                                               "ease": "power2.out"}, t)


def strike(id_, x1, y, x2):
    return (f'<line id="{id_}" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" '
            f'stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>')


# ---------------------------------------------------------------- 01 · Title
def s01():
    c = comp("01")
    c.svg += [f'<rect width="1920" height="1080" fill="{NAVY}"/>',
              f'<ellipse id="s01-glow" cx="1580" cy="600" rx="420" ry="360" fill="{YELLOW}" opacity="0"/>',
              char("s01-boy", "ngap", 1580, 1010, 760), zzz("s01-z", 1740, 250, 1.1, WHITE)]
    words = ["Why", "are", "you", "tired", "<br>", "after", "a", "day", "of", "<br>", "doing", "nothing?"]
    spans = "".join("<br>" if w == "<br>" else
                    f'<span id="s01-w{k}" class="w{" hot" if w in ("tired", "nothing?") else ""}">{w}</span> ' for k, w in enumerate(words))
    c.css.append(f"#s01-title {{ left: 130px; top: 250px; font-size: 120px; font-weight: 800; line-height: 1.08; color: {WHITE}; "
                 f"letter-spacing: -0.01em; }} #s01-title .hot {{ color: {YELLOW}; }} #s01-title .w {{ display: inline-block; }}")
    c.html.append(f'<div id="s01-title" class="txt">{spans}</div>')
    c.tl.to("#s01-glow", {"opacity": 0.18, "duration": 1.2, "ease": "sine.inOut"}, 0.3)
    c.tl.ft("#s01-boy", {"y": 80, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "back.out(1.6)"}, 0.4)
    for k in range(3):
        c.tl.ft(f"#s01-z-{k}", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 0.5}, 1.0 + 0.3 * k)
    for k, w in enumerate(words):
        if w != "<br>":
            c.blur_in(f"#s01-w{k}", 0.25 + 0.07 * k, 0.15)
    return c


# ---------------------------------------------------------------- 02 · Opening story (living room, Sunday)
def s02():
    c = comp("02")
    p = c.cid
    poses = ["ngap", "dien-thoai", "dau-dau", "suy-nghi"]
    hx, hy = L_CX, L_FEET - L_H * 0.8
    over = (chip(f"{p}-sun", 620, 150, "SUNDAY · 11:00 AM", 60)
            + chip(f"{p}-np", hx - 420, hy + 20, "NO PLANS", 52, PAPER, INK)
            + chip(f"{p}-hw", hx - 420, hy + 120, "NO HOMEWORK", 52, PAPER, INK)
            + chip(f"{p}-sofa", L_SOFA[0] + 80, L_SOFA[1] - 220, "BED → COUCH", 52)
            + chip(f"{p}-a0", L_TV[0] - 80, L_TV[1] - 170, "▶ A SHOW", 46, PAPER, INK)
            + chip(f"{p}-a1", hx - 380, hy + 60, "📱 PHONE", 46, PAPER, INK)
            + chip(f"{p}-a2", L_TV[0] - 80, L_TV[1] - 170, "▶ ANOTHER SHOW", 46, PAPER, INK)
            + chip(f"{p}-a3", 760, 640, "🍪 SNACK", 46, PAPER, INK)
            + chip(f"{p}-home", L_WIN[0], L_WIN[1], "NEVER LEFT THE HOUSE", 50, CORAL, WHITE)
            + chip(f"{p}-six", 620, 150, "6:00 PM", 64, CORAL, WHITE)
            + chip(f"{p}-ex", hx - 400, hy + 40, "EXHAUSTED", 64, CORAL, WHITE)
            + chip(f"{p}-mar", hx - 400, hy + 160, "LIKE A MARATHON?", 48, PAPER, INK))
    cam, st = scene_comp(c, "phong-khach", poses, L_CX, L_FEET, L_H, over)
    c.svg.append(f'<rect id="{p}-eve" width="1920" height="1080" fill="#F2A65A" opacity="0" style="mix-blend-mode: multiply"/>')
    c.svg.append(f'<rect id="{p}-dim" width="1920" height="1080" fill="{INK}" opacity="0"/>')
    c.svg.append(label(f"{p}-why", 960, 540, "YOU BARELY STOOD UP", 100, YELLOW, "middle"))
    hid = [f"#{p}-{x}" for x in ("sun", "np", "hw", "sofa", "a0", "a1", "a2", "a3", "home", "six", "ex", "mar", "why")]
    c.hide(*hid)
    t_ = lambda *pre: T(c, "02", *pre)
    frame(c, 0, 960, 540, 1.0, cam, st)
    popl(c, f"#{p}-sun", 0.3, snd="pop")
    idle(c, f"{p}-ngap", 0, t_("A show"), 0)
    t = t_("No plans")
    popl(c, f"#{p}-np", t)
    popl(c, f"#{p}-hw", t + 0.6, snd=None)
    t = t_("You move")
    fade_seq(c, [f"#{p}-np", f"#{p}-hw"], t - 0.2)
    frame(c, t, L_SOFA[0] + 200, L_SOFA[1], 1.5, cam, st)
    c.show(f"#{p}-sun", t, False)
    popl(c, f"#{p}-sofa", t + 0.2)
    t = t_("A show")
    c.show(f"#{p}-sofa", t, False)
    frame(c, t, 1340, 500, 1.25, cam, st)
    show_pose(c, poses, "dien-thoai", t)
    popl(c, f"#{p}-a0", t)
    for k, pre in ((1, "Your phone"), (2, "Another show"), (3, "A snack")):
        tt = t_(pre)
        c.show(f"#{p}-a{k - 1}", tt, False)
        popl(c, f"#{p}-a{k}", tt)
    idle(c, f"{p}-dien-thoai", t, t_("By six"), 1)
    t = t_("You never")
    c.show(f"#{p}-a3", t, False)
    frame(c, t, L_WIN[0], L_WIN[1] + 150, 1.6, cam, st)
    popl(c, f"#{p}-home", t + 0.2, snd="thump")
    t = t_("By six")
    c.show(f"#{p}-home", t, False)
    frame(c, t, 960, 540, 1.0, cam, st)
    c.tl.to(f"#{p}-eve", {"opacity": 0.45, "duration": 0.8}, t)
    popl(c, f"#{p}-six", t + 0.2, snd="thump")
    t = t_("You feel exhausted", "You feel")
    frame(c, t, hx - 150, hy + 120, 1.6, cam, st)
    show_pose(c, poses, "ngap", t)
    popl(c, f"#{p}-ex", t + 0.1)
    popl(c, f"#{p}-mar", t_("Like you"), snd=None)
    t = t_("But you didn't")
    fade_seq(c, [f"#{p}-ex", f"#{p}-mar"], t - 0.2)
    show_pose(c, poses, "suy-nghi", t)
    c.tl.to(f"#{p}-dim", {"opacity": 0.6, "duration": 0.4}, t_("You barely", "But you didn't") + 0.1)
    popl(c, f"#{p}-why", t_("You barely", "But you didn't") + 0.3, snd="thump")
    return c


# ---------------------------------------------------------------- 03 · The Monday puzzle
def s03():
    c = comp("03")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [label(f"{p}-sun", 980, 230, "SUNDAY", 64, GREY, "middle"),
              label(f"{p}-mon", 1560, 230, "MONDAY", 64, YELLOW, "middle"),
              g(f"{p}-ic0", phone(f"{p}-ph", 980, 380, 0.6, buzz=False) + zzz(f"{p}-z", 1060, 360, 0.7, GREY)),
              g(f"{p}-ic1", book(f"{p}-bk", 1480, 380, 0.8) + pictogram(f"{p}-run", 1650, 380, 0.8, "run", TEAL)),
              label(f"{p}-sch", 1560, 520, "SCHOOL + FOOTBALL", 40, WHITE, "middle"),
              label(f"{p}-e6", 1270, 600, "ENERGY AT 6 PM", 40, WHITE, "middle"),
              g(f"{p}-bs", f'<rect x="900" y="{860 - 90}" width="160" height="90" rx="14" fill="{GREY}" stroke="{INK}" stroke-width="6"/>'),
              g(f"{p}-bm", f'<rect x="1480" y="{860 - 210}" width="160" height="210" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'),
              label(f"{p}-dr", 980, 920, "DRAINED", 40, CORAL, "middle"),
              label(f"{p}-bz", 1560, 920, "BUZZING", 40, TEAL, "middle"),
              label(f"{p}-bk2", 1270, 470, "BACKWARDS?", 110, YELLOW, "middle"),
              label(f"{p}-if", 1270, 360, "IF TIRED = ENERGY USED UP…", 58, WHITE, "middle"),
              label(f"{p}-rf", 1270, 590, "…REST SHOULD REFILL YOU", 58, TEAL, "middle")]
    close()
    end = end_of(c, "03")
    g1 = [f"#{p}-{x}" for x in ("sun", "mon", "ic0", "ic1", "sch", "e6", "bs", "bm", "dr", "bz")]
    c.hide(*g1, f"#{p}-bk2", f"#{p}-if", f"#{p}-rf")
    popl(c, f"#{p}-sun", 0.2, snd=None)
    c.pop(f"#{p}-ic0", 0.3, 0.5)
    t = T(c, "03", "School")
    popl(c, f"#{p}-mon", t - 0.4)
    c.pop(f"#{p}-ic1", t, 0.5)
    popl(c, f"#{p}-sch", t + 0.3, snd=None)
    t = T(c, "03", "You should")
    popl(c, f"#{p}-e6", t, snd=None)
    c.show(f"#{p}-bm", t + 0.4)
    grow(c, f"#{p}-bm", t + 0.4)
    c.sfx("pop", t + 0.4)
    t = T(c, "03", "A busy")
    c.show(f"#{p}-bs", t)
    grow(c, f"#{p}-bs", t)
    popl(c, f"#{p}-bz", t, snd=None)
    popl(c, f"#{p}-dr", T(c, "03", "An empty", "A busy") + 0.4)
    t = T(c, "03", "That's backwards", "That's")
    fade_seq(c, g1, t - 0.2)
    popl(c, f"#{p}-bk2", t, snd="thump")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    t = T(c, "03", "If tiredness")
    c.blur_out(f"#{p}-bk2", t - 0.2)
    popl(c, f"#{p}-if", t)
    popl(c, f"#{p}-rf", c.at("03", "resting", off=0.1), snd=None)
    idle(c, f"{p}-ngac-nhien", t, end, 1)
    return c


# ---------------------------------------------------------------- 04 · Clue one: the brain's energy bill
def s04():
    c = comp("04")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [clue(f"{p}-c", "CLUE 1 · THE BRAIN'S ENERGY BILL"),
              brain(f"{p}-br", 960, 400, 1.3),
              g(f"{p}-w", f'<rect x="1180" y="{780 - 30}" width="170" height="30" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="6"/>'
                + text(1265, 830, "2% OF WEIGHT", 34, 900, WHITE, "middle")),
              g(f"{p}-e", f'<rect x="1580" y="{780 - 300}" width="170" height="300" rx="14" fill="{YELLOW}" stroke="{INK}" stroke-width="6"/>'
                + text(1665, 830, "20% OF ENERGY", 34, 900, YELLOW, "middle")),
              label(f"{p}-ar", 960, 610, "ALWAYS ON · EVEN AT REST", 40, TEAL, "middle"),
              label(f"{p}-hd", 1270, 330, "HARD THINKING", 70, WHITE, "middle"),
              label(f"{p}-5", 1270, 500, "+5% OR LESS", 120, YELLOW, "middle"),
              label(f"{p}-lc", 1270, 590, "BLOOD FLOW TO BUSY AREAS", 40, GREY, "middle"),
              g(f"{p}-ps", battery(f"{p}-bt", 960, 770, 1.1, 0.9, TEAL) + text(1460, 788, "NO POWER-SAVING MODE", 46, 900, CORAL, "middle")),
              note(f"{p}-src", 1270, 940, "Raichle & Gusnard, PNAS, 2002")]
    close()
    end = end_of(c, "04")
    g1 = [f"#{p}-br", f"#{p}-w", f"#{p}-e", f"#{p}-ar"]
    c.hide(f"#{p}-c", *g1, f"#{p}-hd", f"#{p}-5", f"#{p}-lc", f"#{p}-ps", f"#{p}-src")
    popl(c, f"#{p}-c", T(c, "04", "Let's collect"))
    t = T(c, "04", "Clue one")
    c.pop(f"#{p}-br", t, 0.5)
    c.sfx("pop", t)
    c.show(f"#{p}-w", t + 0.8)
    grow(c, f"#{p}-w", t + 0.8, 0.4)
    c.blur_in(f"#{p}-src", t + 0.6)
    t = T(c, "04", "But it uses")
    c.show(f"#{p}-e", t)
    grow(c, f"#{p}-e", t, 0.8)
    c.sfx("riser", t - 0.3)
    t = T(c, "04", "Here's the surprise")
    popl(c, f"#{p}-ar", t + 0.4)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    t = T(c, "04", "When you do")
    fade_seq(c, g1, t - 0.2)
    popl(c, f"#{p}-hd", t)
    t = T(c, "04", "Blood flow")
    popl(c, f"#{p}-5", t, snd="thump")
    c.blur_in(f"#{p}-lc", t + 0.3)
    t = T(c, "04", "Lying on")
    c.pop(f"#{p}-ps", t, 0.5)
    c.sfx("pop", t)
    idle(c, f"{p}-ngac-nhien", T(c, "04", "Here's the surprise") + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 05 · Clue two: the dull task
def s05():
    c = comp("05")
    p = c.cid
    close = board(c, ("suy-nghi", "ngap"))
    c.svg += [clue(f"{p}-c", "CLUE 2 · THE DULL TASK"),
              laptop(f"{p}-lp", 1000, 380, 1.0),
              g(f"{p}-ck", clock(f"{p}-cl", 1500, 370, 100, 1, 0) + text(1500, 530, "60+ MIN", 46, 900, YELLOW, "middle")),
              label(f"{p}-rx", 1270, 620, "REACTIONS: SLOWER", 46, WHITE, "middle"),
              heartbeat(f"{p}-hb", 760, 760, 1060, [40, 60, 90, 130, 180, 240, 320]),
              label(f"{p}-hs", 1270, 870, "HEART: SLOWER", 46, CORAL, "middle"),
              label(f"{p}-fl", 1270, 330, "IT FELT LIKE…", 64, WHITE, "middle"),
              label(f"{p}-hw", 1270, 480, "HARD WORK", 90, GREY, "middle"),
              strike(f"{p}-x", 980, 450, 1560),
              label(f"{p}-bo", 1270, 640, "BOREDOM", 120, YELLOW, "middle"),
              note(f"{p}-src", 1270, 940, "Pattyn et al., Physiology & Behavior, 2008 · one lab study")]
    close()
    end = end_of(c, "05")
    g1 = [f"#{p}-lp", f"#{p}-ck", f"#{p}-rx", f"#{p}-hb", f"#{p}-hs"]
    c.hide(f"#{p}-c", f"#{p}-lp", f"#{p}-ck", f"#{p}-rx", f"#{p}-hs", f"#{p}-fl", f"#{p}-hw", f"#{p}-bo", f"#{p}-src")
    t = T(c, "05", "Clue two")
    popl(c, f"#{p}-c", t)
    c.pop(f"#{p}-lp", t + 0.6, 0.5)
    c.blur_in(f"#{p}-src", t + 0.8)
    t = T(c, "05", "They watched")
    c.pop(f"#{p}-ck", t, 0.5)
    c.sfx("pop", t)
    popl(c, f"#{p}-rx", T(c, "05", "As time"))
    t = T(c, "05", "Their heart")
    c.draw(f"#{p}-hb", t, 2.4, "none")
    popl(c, f"#{p}-hs", t + 0.5, snd=None)
    swap(c, f"{p}-suy-nghi", f"{p}-ngap", t)
    t = T(c, "05", "And when")
    fade_seq(c, g1, t - 0.25)
    popl(c, f"#{p}-fl", t)
    t = T(c, "05", "It sounded")
    popl(c, f"#{p}-hw", t, snd=None)
    c.draw(f"#{p}-x", c.at("05", "more like", off=-0.2), 0.4)
    popl(c, f"#{p}-bo", c.at("05", "boredom"), snd="thump")
    idle(c, f"{p}-ngap", T(c, "05", "Their heart") + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 06 · Clue three: the shock button
def s06():
    c = comp("06")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [clue(f"{p}-c", "CLUE 3 · ALONE WITH YOUR THOUGHTS"),
              label(f"{p}-yr", 1270, 230, "2014 · 11 STUDIES", 44, GREY, "middle"),
              g(f"{p}-rm", f'<rect x="830" y="300" width="420" height="380" rx="20" fill="{NAVY}" stroke="{GREY}" stroke-width="6"/>'
                + person_icon(f"{p}-pi", 1040, 520, 2.2, WHITE)),
              g(f"{p}-ck", clock(f"{p}-cl", 1560, 400, 90, 0, 15) + text(1560, 550, "6–15 MIN", 46, 900, YELLOW, "middle")),
              label(f"{p}-jt", 1560, 620, "NO PHONE · JUST THINK", 34, WHITE, "middle"),
              label(f"{p}-nf", 1270, 780, "MOST DIDN'T ENJOY IT", 60, CORAL, "middle"),
              shock_button(f"{p}-sb", 1040, 520, 1.5),
              label(f"{p}-mn", 1560, 470, "12 OF 18 MEN", 64, YELLOW, "middle"),
              label(f"{p}-wm", 1560, 600, "6 OF 24 WOMEN", 64, YELLOW, "middle"),
              label(f"{p}-al", 1560, 680, "PRESSED IT AT LEAST ONCE", 32, WHITE, "middle"),
              label(f"{p}-pn", 1270, 820, "PAIN  >  NOTHING", 90, CORAL, "middle"),
              note(f"{p}-src", 1270, 940, "Wilson et al., Science, 2014")]
    close()
    end = end_of(c, "06")
    g1 = [f"#{p}-rm", f"#{p}-ck", f"#{p}-jt", f"#{p}-nf"]
    c.hide(f"#{p}-c", f"#{p}-yr", *g1, f"#{p}-sb", f"#{p}-mn", f"#{p}-wm", f"#{p}-al", f"#{p}-pn", f"#{p}-src")
    t = T(c, "06", "Clue three")
    popl(c, f"#{p}-c", t)
    c.blur_in(f"#{p}-yr", t + 0.5)
    c.blur_in(f"#{p}-src", t + 0.8)
    t = T(c, "06", "Sit alone")
    c.pop(f"#{p}-rm", t, 0.5)
    c.pop(f"#{p}-ck", t + 0.5, 0.5)
    c.sfx("pop", t)
    popl(c, f"#{p}-jt", c.at("06", "Just think", off=-0.1), snd=None)
    popl(c, f"#{p}-nf", T(c, "06", "Most people"))
    t = T(c, "06", "In one version")
    fade_seq(c, g1, t - 0.25)
    c.pop(f"#{p}-sb", t + 0.3, 0.5)
    c.sfx("thump", t + 0.3)
    t = T(c, "06", "Twelve", "12")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    c.tl.ft(f"#{p}-sb-cap", {"y": 0}, {"y": 14, "duration": 0.12, "yoyo": True, "repeat": 3}, t)
    c.tl.ft(f"#{p}-sb-bolt", {"scale": 1, "transformOrigin": "50% 100%"}, {"scale": 1.25, "transformOrigin": "50% 100%", "duration": 0.12,
                                                                           "yoyo": True, "repeat": 3}, t)
    popl(c, f"#{p}-mn", t, snd="thump")
    popl(c, f"#{p}-al", t + 0.5, snd=None)
    popl(c, f"#{p}-wm", T(c, "06", "So did"), snd="pop")
    popl(c, f"#{p}-pn", T(c, "06", "Some people"), snd="thump")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 07 · Clue four: the easy bike ride
def s07():
    c = comp("07")
    p = c.cid
    close = board(c, ("ngap", "vui"))
    c.svg += [clue(f"{p}-c", "CLUE 4 · THE EASY BIKE RIDE"),
              label(f"{p}-36", 1270, 230, "36 TIRED YOUNG ADULTS · HEALTHY, BARELY EXERCISED", 36, WHITE, "middle"),
              bike(f"{p}-bk", 1000, 480, 1.2),
              label(f"{p}-sc", 1500, 430, "20 MIN", 64, YELLOW, "middle"),
              label(f"{p}-sc2", 1500, 510, "3× A WEEK · 6 WEEKS", 42, WHITE, "middle"),
              label(f"{p}-hdr", 1270, 255, "FATIGUE DROP", 44, WHITE, "middle"),
              bars(f"{p}-r", [(900, 360, TEAL, "EASY"), (1270, 250, BLUE, "MODERATE"), (1640, 40, GREY, "NO EXERCISE")], 820, 210),
              label(f"{p}-en", 1270, 400, "BOTH RIDING GROUPS: MORE ENERGY", 40, YELLOW, "middle"),
              label(f"{p}-nf", 1270, 330, "NOT BECAUSE THEY GOT FITTER", 46, CORAL, "middle"),
              note(f"{p}-src", 1270, 940, "Puetz et al., Psychother Psychosom, 2008 · small trial · bars illustrative")]
    close()
    end = end_of(c, "07")
    g1 = [f"#{p}-36", f"#{p}-bk", f"#{p}-sc", f"#{p}-sc2"]
    bs = [f"#{p}-r-b{k}" for k in range(3)]
    c.hide(f"#{p}-c", *g1, f"#{p}-hdr", *bs, f"#{p}-en", f"#{p}-nf", f"#{p}-src")
    t = T(c, "07", "Clue four")
    popl(c, f"#{p}-c", t)
    popl(c, f"#{p}-36", t + 1.0, snd=None)
    c.blur_in(f"#{p}-src", t + 0.8)
    t = T(c, "07", "Some rode an")
    c.pop(f"#{p}-bk", t, 0.5)
    c.sfx("pop", t)
    c.tl.to(f"#{p}-bk-wheel", {"rotation": 720, "transformOrigin": "50% 50%", "duration": 4, "ease": "none"}, t + 0.3)
    popl(c, f"#{p}-sc", t + 1.2, snd=None)
    popl(c, f"#{p}-sc2", t + 2.2, snd=None)
    t = T(c, "07", "Some rode at")
    fade_seq(c, g1, t - 0.25)
    popl(c, f"#{p}-hdr", t, snd=None)
    for k, tt in ((1, t + 0.3), (0, c.at("07", "very easy")), (2, T(c, "07", "And some"))):
        c.show(bs[k], tt)
        grow(c, bs[k], tt, 0.4)
        c.tl.to(bs[k], {"opacity": 0.35, "duration": 0.01}, tt)
        c.sfx("pop", tt)
    t = T(c, "07", "Both groups")
    popl(c, f"#{p}-en", t)
    swap(c, f"{p}-ngap", f"{p}-vui", t)
    t = T(c, "07", "The easy")
    for k in (2, 1, 0):
        c.tl.to(bs[k], {"opacity": 1, "duration": 0.3}, t + 0.15 * (2 - k))
    c.tl.ft(bs[0], {"scale": 1}, {"scale": 1.08, "transformOrigin": "50% 100%", "duration": 0.3, "yoyo": True, "repeat": 1}, t + 0.4)
    c.sfx("riser", t - 0.3)
    popl(c, f"#{p}-nf", T(c, "07", "And it wasn't"), snd="thump")
    idle(c, f"{p}-vui", T(c, "07", "Both groups") + 0.6, end, 2)
    return c


def opt_row(prefix, x, y, letter, icon, lab):
    return g(prefix, f"""<rect id="{prefix}-box" x="{x - 30}" y="{y - 86}" width="1170" height="172" rx="28" fill="none" stroke="{YELLOW}" stroke-width="8" opacity="0"/>
{text(x + 50, y + 44, letter, 128, 900, YELLOW, "middle")}
<g transform="translate({x + 270} {y})">{icon}</g>
{text(x + 430, y + 14, lab, 35, 800, WHITE)}
{strike(f"{prefix}-strike", x - 20, y, x + 1130)}""")


def options(prefix, x=690):
    return (opt_row(f"{prefix}a", x, 300, "A", battery(f"{prefix}-bt", 0, 0, 0.8, 0.15, CORAL), "YOUR BATTERY RAN LOW")
            + opt_row(f"{prefix}b", x, 530, "B", brain(f"{prefix}-br", 0, 0, 0.6), "A BRAIN SIGNAL, NOT A BATTERY")
            + opt_row(f"{prefix}c", x, 760, "C", zzz(f"{prefix}-z", -40, 40, 1.0, BLUE), "TOO MUCH SLEEP"))


# ---------------------------------------------------------------- 08 · The question
def s08():
    c = comp("08")
    p = c.cid
    close = board(c)
    c.svg += [options(f"{p}-o"), label(f"{p}-q", 1270, 560, "WHY ARE YOU TIRED?", 96, WHITE, "middle")]
    close()
    idle(c, f"{p}-suy-nghi", 0, end_of(c, "08"), 2)
    c.hide(f"#{p}-q")
    popl(c, f"#{p}-q", T(c, "08", "Why do"))
    c.blur_out(f"#{p}-q", T(c, "08", "Is it A", "Is it") - 0.3, 0.25)
    for L, pres in (("a", ("Is it A", "Is it")), ("b", ("B.", "B:", "B ")), ("c", ("Or C", "Or"))):
        t = T(c, "08", *pres)
        c.hide(f"#{p}-o{L}")
        c.tl.ft(f"#{p}-o{L}", {"autoAlpha": 0, "x": 60, "filter": "blur(8px)"},
                {"autoAlpha": 1, "x": 0, "filter": "blur(0px)", "duration": 0.45, "ease": "expo.out"}, t)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 09 · Take a guess
def s09():
    c = comp("09")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>',
              f'<circle cx="1590" cy="560" r="220" fill="{NAVY}" stroke="{INK}" stroke-width="10"/>',
              text(1590, 300, "PAUSE THE VIDEO", 44, 900, INK, "middle"),
              g("s09-n", "".join(text(1590, 660, str(n), 300, 900, YELLOW, "middle", id_=f"s09-n{n}") for n in (3, 2, 1)))]
    lines = [("h", "Take a guess first!"),
             ("f", "1. Your brain uses about the same energy resting or thinking hard."),
             ("f", "2. A long, dull task slowed people's hearts. It felt like boredom."),
             ("f", "3. Many people chose an electric shock over sitting alone."),
             ("f", "4. Easy bike rides cut fatigue most. Fitness didn't explain it."),
             ("o", "A. Your battery ran low"), ("o", "B. Tiredness is a signal from your brain, not a battery"),
             ("o", "C. You slept too much")]
    c.css.append(f"#s09-card {{ left: 130px; top: 110px; width: 1180px; color: {INK}; }}"
                 "#s09-card .h { font-size: 80px; font-weight: 800; margin-bottom: 30px; letter-spacing: -0.01em; }"
                 "#s09-card .f { font-size: 36px; font-weight: 600; line-height: 1.3; margin-bottom: 14px; }"
                 "#s09-card .o { font-size: 42px; font-weight: 800; margin-top: 8px; line-height: 1.25; }"
                 "#s09-card .gap { height: 26px; }")
    items = []
    for k, (cls, tx) in enumerate(lines):
        if cls == "o" and lines[k - 1][0] == "f":
            items.append('<div class="gap"></div>')
        items.append(f'<div id="s09-l{k}" class="{cls}">{tx}</div>')
    c.html.append(f'<div id="s09-card" class="txt" data-hold="true">{"".join(items)}</div>')
    for k in range(len(lines)):
        c.blur_in(f"#s09-l{k}", 0.1 + 0.07 * k, 0.18)
    c.hide("#s09-n2", "#s09-n1")
    c.tl.ft("#s09-n3", {"scale": 0.4, "transformOrigin": "50% 50%"},
            {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.5, "ease": "back.out(1.8)"}, 0.2)
    c.sfx("pop", 0.2)
    for a, b, t in ((3, 2, 3.4), (2, 1, 6.4)):
        c.show(f"#s09-n{a}", t, False)
        c.pop(f"#s09-n{b}", t, 0.5, "50% 50%", "back.out(1.8)", 0.4)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 10 · The key
def s10():
    c = comp("10")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [g(f"{p}-hg", bowl(f"{p}-bw", 1000, 420, 1.3) + text(1000, 590, "HUNGER", 56, 900, YELLOW, "middle")),
              label(f"{p}-sm", 1000, 690, "SMELL OF PIZZA", 40, WHITE, "middle"),
              label(f"{p}-lt", 1000, 750, "LUNCHTIME", 40, WHITE, "middle"),
              label(f"{p}-ms", 1270, 860, "A MESSAGE, NOT AN EMPTY TANK", 44, TEAL, "middle"),
              g(f"{p}-td", battery(f"{p}-bt", 1560, 420, 1.3, 0.5, GREY) + text(1560, 448, "?", 80, 900, YELLOW, "middle")
                + text(1560, 590, "TIREDNESS", 56, 900, YELLOW, "middle")),
              label(f"{p}-sg", 1270, 270, "A SIGNAL, NOT A FUEL GAUGE", 72, YELLOW, "middle")]
    close()
    end = end_of(c, "10")
    c.hide(f"#{p}-hg", f"#{p}-sm", f"#{p}-lt", f"#{p}-ms", f"#{p}-td", f"#{p}-sg")
    t = T(c, "10", "Think about")
    c.pop(f"#{p}-hg", t, 0.5)
    c.sfx("pop", t)
    t = T(c, "10", "You feel hungry when")
    popl(c, f"#{p}-sm", t, snd=None)
    popl(c, f"#{p}-lt", t + 1.2, snd=None)
    popl(c, f"#{p}-ms", T(c, "10", "Hunger is"))
    t = T(c, "10", "Many researchers")
    c.pop(f"#{p}-td", t, 0.5)
    c.sfx("pop", t)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    t = T(c, "10", "It's not")
    popl(c, f"#{p}-sg", t, snd="thump")
    idle(c, f"{p}-vui", T(c, "10", "Many researchers") + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 11 · The battery myth
def s11():
    c = comp("11")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [label(f"{p}-hd", 1270, 200, "THE BATTERY MYTH", 72, YELLOW, "middle"),
              g(f"{p}-bb", battery(f"{p}-bt", 1270, 450, 2.6, 0.3, CORAL) + text(1270, 640, "BRAIN BATTERY", 50, 900, WHITE, "middle")),
              g(f"{p}-ch", text(1270, 720, "LAZY DAY = RECHARGE?", 50, 900, TEAL, "middle")),
              strike(f"{p}-x", 960, 450, 1580),
              label(f"{p}-en", 1270, 310, "BRAIN ENERGY USE", 50, WHITE, "middle"),
              bars(f"{p}-r", [(1000, 330, TEAL, "STARING AT A WALL"), (1540, 345, YELLOW, "SOLVING PUZZLES")], 820, 220),
              label(f"{p}-sv", 1000, 450, "NO BIG SAVING", 40, GREY, "middle"),
              label(f"{p}-dr", 1540, 435, "NO BIG DRAIN", 40, GREY, "middle"),
              label(f"{p}-el", 1270, 560, "SO WHERE DOES TIRED COME FROM?", 54, YELLOW, "middle"),
              note(f"{p}-src", 1270, 940, "Raichle & Gusnard, PNAS, 2002 · bar heights illustrative")]
    close()
    end = end_of(c, "11")
    bs = [f"#{p}-r-b{k}" for k in range(2)]
    c.hide(f"#{p}-hd", f"#{p}-bb", f"#{p}-ch", f"#{p}-en", *bs, f"#{p}-sv", f"#{p}-dr", f"#{p}-el", f"#{p}-src")
    popl(c, f"#{p}-hd", T(c, "11", "Start"))
    t = T(c, "11", "If your brain")
    c.pop(f"#{p}-bb", t, 0.5)
    c.sfx("pop", t)
    popl(c, f"#{p}-ch", t + 1.4, snd=None)
    t = T(c, "11", "But your brain")
    c.draw(f"#{p}-x", t, 0.4)
    c.sfx("thump", t + 0.2)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    t2 = t + 1.4
    fade_seq(c, [f"#{p}-bb", f"#{p}-ch", f"#{p}-x"], t2 - 0.25)
    popl(c, f"#{p}-en", t2, snd=None)
    c.blur_in(f"#{p}-src", t2 + 0.2)
    for b in bs:  # mọc cùng lúc: lời đọc nói "roughly the same energy"
        c.show(b, t2)
        grow(c, b, t2)
    popl(c, f"#{p}-sv", T(c, "11", "So a day"), snd=None)
    popl(c, f"#{p}-dr", T(c, "11", "And a busy"), snd=None)
    t = T(c, "11", "The feeling")
    fade_seq(c, [f"#{p}-en", *bs, f"#{p}-sv", f"#{p}-dr"], t - 0.25)
    popl(c, f"#{p}-el", t, snd="thump")
    idle(c, f"{p}-ngac-nhien", T(c, "11", "But your brain") + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 12 · Tiredness as a message
def s12():
    c = comp("12")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [label(f"{p}-hd", 1270, 200, "IS THIS THE BEST USE OF MY TIME?", 58, YELLOW, "middle"),
              balance(f"{p}-bl", 1270, 360, 0.8, text(0, -20, "THIS TASK", 44, 900, WHITE, "middle"),
                      text(0, -20, "SOMETHING BETTER?", 40, 900, TEAL, "middle")),
              g(f"{p}-tl", lamp(f"{p}-lp", 1270, 800, CORAL, 46) + text(1270, 890, "EFFORT + FATIGUE", 40, 900, CORAL, "middle")),
              g(f"{p}-cl", hourglass(f"{p}-hgl", 1000, 450, 1.3) + text(1000, 640, "BORING CLASS", 44, 900, WHITE, "middle")
                + text(1000, 700, "ENDLESS", 40, 900, CORAL, "middle")),
              g(f"{p}-gm", clock(f"{p}-ck", 1560, 450, 110, 4, 0) + text(1560, 640, "A GAME YOU LOVE", 44, 900, WHITE, "middle")
                + text(1560, 700, "FLIES BY", 40, 900, TEAL, "middle")),
              stamp(f"{p}-hy", 1270, 820, "HYPOTHESIS · STILL DEBATED", CORAL, 760, 44),
              label(f"{p}-vl", 1270, 520, "VALUE, NOT JUST FUEL", 80, YELLOW, "middle"),
              note(f"{p}-src", 1270, 940, "Kurzban et al., Behavioral and Brain Sciences, 2013")]
    close()
    end = end_of(c, "12")
    g1 = [f"#{p}-bl", f"#{p}-tl"]
    g2 = [f"#{p}-cl", f"#{p}-gm"]
    c.hide(f"#{p}-hd", *g1, *g2, f"#{p}-hy", f"#{p}-vl", f"#{p}-src")
    t = T(c, "12", "Your brain keeps")
    popl(c, f"#{p}-hd", t)
    c.pop(f"#{p}-bl", t + 0.4, 0.5)
    c.blur_in(f"#{p}-src", t + 0.6)
    t = T(c, "12", "When the answer")
    c.tl.to(f"#{p}-bl-beam", {"rotation": 10, "transformOrigin": "50% 50%", "duration": 0.6, "ease": "back.out(2)"}, t)
    c.tl.to(f"#{p}-bl-L", {"y": -50, "duration": 0.6, "ease": "back.out(2)"}, t)
    c.tl.to(f"#{p}-bl-R", {"y": 50, "duration": 0.6, "ease": "back.out(2)"}, t)
    c.pop(f"#{p}-tl", t + 0.5, 0.5)
    c.sfx("thump", t + 0.5)
    t = T(c, "12", "Think of")
    fade_seq(c, [f"#{p}-hd", *g1], t - 0.25)
    c.pop(f"#{p}-cl", t, 0.5)
    c.pop(f"#{p}-gm", t + 1.2, 0.5)
    c.sfx("pop", t)
    t = T(c, "12", "This is still")
    popl(c, f"#{p}-hy", t, snd="thump")
    t = T(c, "12", "But it explains")
    fade_seq(c, [*g2, f"#{p}-hy"], t - 0.25)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    popl(c, f"#{p}-vl", t + 1.0)
    idle(c, f"{p}-vui", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 13 · Boredom is a warning light
def s13():
    c = comp("13")
    p = c.cid
    close = board(c, ("suy-nghi", "ngap"))
    c.svg += [label(f"{p}-hd", 1270, 200, "BOREDOM: A SIGNAL TOO", 72, YELLOW, "middle"),
              g(f"{p}-la", lamp(f"{p}-l1", 1000, 380, GREY, 70) + text(1000, 510, "ATTENTION", 50, 900, WHITE, "middle")),
              g(f"{p}-lm", lamp(f"{p}-l2", 1560, 380, GREY, 70) + text(1560, 510, "MEANING", 50, 900, WHITE, "middle")),
              g(f"{p}-on1", lamp(f"{p}-l1b", 1000, 380, CORAL, 70)),
              g(f"{p}-on2", lamp(f"{p}-l2b", 1560, 380, CORAL, 70)),
              label(f"{p}-tl", 860, 620, "TOO LITTLE", 40, TEAL, "middle"),
              label(f"{p}-tm", 1140, 620, "TOO MUCH", 40, CORAL, "middle"),
              label(f"{p}-nm", 1560, 620, "NOT MEANINGFUL TO YOU", 36, YELLOW, "middle"),
              label(f"{p}-bo", 1270, 760, "→ BORED", 90, YELLOW, "middle"),
              label(f"{p}-ft", 1270, 860, "≈ FEELS A LOT LIKE TIRED", 50, WHITE, "middle"),
              note(f"{p}-src", 1270, 940, "Westgate & Wilson, Psychological Review, 2018")]
    close()
    end = end_of(c, "13")
    c.hide(f"#{p}-hd", f"#{p}-la", f"#{p}-lm", f"#{p}-on1", f"#{p}-on2", f"#{p}-tl", f"#{p}-tm", f"#{p}-nm", f"#{p}-bo", f"#{p}-ft",
           f"#{p}-src")
    popl(c, f"#{p}-hd", T(c, "13", "Psychologists"))
    c.blur_in(f"#{p}-src", T(c, "13", "Psychologists") + 0.6)
    t = T(c, "13", "It appears when your")
    c.pop(f"#{p}-la", t, 0.5)
    c.sfx("pop", t)
    c.show(f"#{p}-on1", t + 0.8)
    t = T(c, "13", "That can")
    popl(c, f"#{p}-tl", t + 0.8, snd=None)
    popl(c, f"#{p}-tm", t + 1.8, snd=None)
    t = T(c, "13", "It also")
    c.pop(f"#{p}-lm", t, 0.5)
    c.sfx("pop", t)
    c.show(f"#{p}-on2", t + 0.8)
    popl(c, f"#{p}-nm", t + 1.0, snd=None)
    t = T(c, "13", "And boredom")
    popl(c, f"#{p}-bo", t - 0.6, snd="thump")
    popl(c, f"#{p}-ft", t + 0.3, snd=None)
    swap(c, f"{p}-suy-nghi", f"{p}-ngap", t)
    idle(c, f"{p}-ngap", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 14 · Scrolling isn't resting
def s14():
    c = comp("14")
    p = c.cid
    close = board(c, ("dien-thoai", "suy-nghi"))
    c.svg += [label(f"{p}-hd", 1270, 200, "SCROLLING ≠ RESTING", 72, YELLOW, "middle"),
              feed(f"{p}-fd", 960, 560, 1.2),
              label(f"{p}-in", 1500, 400, "LOTS OF INPUT", 54, WHITE, "middle"),
              label(f"{p}-en", 1500, 500, "≠ ENGAGED", 54, CORAL, "middle"),
              label(f"{p}-st", 1500, 620, "ATTENTION NEVER SETTLES", 36, GREY, "middle"),
              label(f"{p}-lm", 1500, 720, "LITTLE MEANING", 54, CORAL, "middle"),
              g(f"{p}-2l", lamp(f"{p}-l1", 1390, 840, CORAL, 46) + lamp(f"{p}-l2", 1610, 840, CORAL, 46)),
              note(f"{p}-src", 1270, 940, "Applying the MAC model of boredom (Westgate & Wilson, 2018)")]
    close()
    end = end_of(c, "14")
    c.hide(f"#{p}-hd", f"#{p}-fd", f"#{p}-in", f"#{p}-en", f"#{p}-st", f"#{p}-lm", f"#{p}-2l", f"#{p}-src")
    t = T(c, "14", "Here's the sneaky")
    popl(c, f"#{p}-hd", t)
    t = T(c, "14", "A day on")
    c.pop(f"#{p}-fd", t, 0.5)
    c.sfx("pop", t)
    c.tl.to(f"#{p}-fd-strip", {"y": -900, "duration": max(end - t - 0.5, 2), "ease": "none"}, t + 0.3)
    t = T(c, "14", "But lots")
    popl(c, f"#{p}-in", t, snd=None)
    popl(c, f"#{p}-en", t + 1.4)
    c.blur_in(f"#{p}-src", t + 0.4)
    popl(c, f"#{p}-st", T(c, "14", "Clip"), snd=None)
    popl(c, f"#{p}-lm", T(c, "14", "And very"))
    t = T(c, "14", "So your brain")
    c.pop(f"#{p}-2l", t, 0.5)
    c.sfx("thump", t + 0.2)
    swap(c, f"{p}-dien-thoai", f"{p}-suy-nghi", t)
    idle(c, f"{p}-dien-thoai", 0, t, 1)
    return c


# ---------------------------------------------------------------- 15 · The body winds down
def s15():
    c = comp("15")
    p = c.cid
    close = board(c, ("suy-nghi", "ngap"))
    c.svg += [label(f"{p}-hd", 1270, 200, "THE BODY WINDS DOWN", 72, YELLOW, "middle"),
              heartbeat(f"{p}-hb", 760, 470, 1060, [30, 50, 80, 120, 170, 230, 300], CORAL, 10),
              heart(f"{p}-ht", 1700, 330, 0.7),
              label(f"{p}-ua", 1270, 650, "UNDER-AROUSED", 80, TEAL, "middle"),
              label(f"{p}-hs", 1270, 750, "HEAVY · SLEEPY", 54, WHITE, "middle"),
              label(f"{p}-nw", 1270, 860, "NOT FROM WORKING HARD", 46, CORAL, "middle"),
              note(f"{p}-src", 1270, 940, "Pattyn et al., Physiology & Behavior, 2008")]
    close()
    end = end_of(c, "15")
    c.hide(f"#{p}-hd", f"#{p}-ht", f"#{p}-ua", f"#{p}-hs", f"#{p}-nw", f"#{p}-src")
    popl(c, f"#{p}-hd", 0.2)
    c.blur_in(f"#{p}-src", 0.6)
    t = T(c, "15", "When nothing")
    c.draw(f"#{p}-hb", t, 3.0, "none")
    c.pop(f"#{p}-ht", t, 0.5)
    c.tl.ft(f"#{p}-ht", {"scale": 1, "transformOrigin": "50% 50%"}, {"scale": 1.15, "transformOrigin": "50% 50%", "duration": 0.35,
                                                                     "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, t + 0.6)
    popl(c, f"#{p}-ua", t + 1.0)
    t = T(c, "15", "Your heart")
    popl(c, f"#{p}-hs", t, snd=None)
    swap(c, f"{p}-suy-nghi", f"{p}-ngap", t)
    popl(c, f"#{p}-nw", T(c, "15", "Not because"), snd="thump")
    idle(c, f"{p}-ngap", t + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 16 · Doing nothing is hard
def s16():
    c = comp("16")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    cols = [WHITE, YELLOW, TEAL, PINK, BLUE, CORAL]
    c.svg += [label(f"{p}-hd", 1270, 200, "TESTED AGAIN", 72, YELLOW, "middle"),
              g(f"{p}-ppl", "".join(person_icon(f"{p}-pp{k}", 800 + k * 94, 330, 1.5, cols[k % 6]) for k in range(11))),
              label(f"{p}-n", 1270, 480, "2,557 PEOPLE · 11 COUNTRIES", 54, WHITE, "middle"),
              bars(f"{p}-r", [(1060, 120, GREY, "JUST THINK"), (1480, 290, TEAL, "DO SOMETHING")], 820, 220),
              label(f"{p}-ev", 1270, 400, "ENJOYED MORE: IN EVERY COUNTRY", 40, TEAL, "middle"),
              label(f"{p}-nr", 1270, 470, "DOING NOTHING ≠ RESTFUL", 76, CORAL, "middle"),
              note(f"{p}-src", 1270, 940, "Buttrick et al., J Personality and Social Psychology, 2019 · bar heights illustrative")]
    close()
    end = end_of(c, "16")
    bs = [f"#{p}-r-b{k}" for k in range(2)]
    c.hide(f"#{p}-hd", f"#{p}-ppl", f"#{p}-n", *bs, f"#{p}-ev", f"#{p}-nr", f"#{p}-src")
    popl(c, f"#{p}-hd", 0.2)
    t = T(c, "16", "The main")
    c.pop(f"#{p}-ppl", t, 0.6)
    c.sfx("pop", t)
    popl(c, f"#{p}-n", t + 1.5, snd=None)
    c.blur_in(f"#{p}-src", t + 0.6)
    t = T(c, "16", "In every")
    c.blur_out(f"#{p}-ppl", t - 0.3)
    c.blur_out(f"#{p}-n", t - 0.3)
    for k, b in enumerate(bs):
        c.show(b, t + 0.25 * k)
        grow(c, b, t + 0.25 * k)
    popl(c, f"#{p}-ev", t + 0.8, snd="pop")
    t = T(c, "16", "So doing")
    fade_seq(c, [*bs, f"#{p}-ev"], t - 0.25)
    popl(c, f"#{p}-nr", t, snd="thump")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 17 · Movement makes energy
def s17():
    c = comp("17")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [label(f"{p}-hd", 1270, 200, "NOT JUST ONE STUDY", 72, YELLOW, "middle"),
              g(f"{p}-m1", f'<rect x="760" y="290" width="500" height="200" rx="24" fill="{NAVY}" stroke="{TEAL}" stroke-width="7"/>'
                + text(1010, 360, "2006 · 70 TRIALS", 40, 900, WHITE, "middle") + text(1010, 430, "6,807 PEOPLE", 52, 900, TEAL, "middle")),
              g(f"{p}-m2", f'<rect x="1300" y="290" width="500" height="200" rx="24" fill="{NAVY}" stroke="{YELLOW}" stroke-width="7"/>'
                + text(1550, 360, "2022 · 81 STUDIES", 40, 900, WHITE, "middle") + text(1550, 430, "7,050 PEOPLE", 52, 900, YELLOW, "middle")),
              label(f"{p}-ef", 1010, 620, "ENERGY ▲", 70, TEAL, "middle"),
              label(f"{p}-fg", 1550, 620, "FATIGUE ▼", 70, CORAL, "middle"),
              label(f"{p}-sm", 1270, 730, "SMALL TO MODERATE · NOT MAGIC", 44, WHITE, "middle"),
              label(f"{p}-wk", 1270, 850, "“THIS DAY IS WORTH BEING AWAKE FOR”", 44, YELLOW, "middle"),
              note(f"{p}-src", 1270, 940, "Puetz, O'Connor & Dishman, Psychol Bull, 2006 · Wender et al., Front Psychol, 2022")]
    close()
    end = end_of(c, "17")
    c.hide(f"#{p}-hd", f"#{p}-m1", f"#{p}-m2", f"#{p}-ef", f"#{p}-fg", f"#{p}-sm", f"#{p}-wk", f"#{p}-src")
    popl(c, f"#{p}-hd", T(c, "17", "One small"))
    t = T(c, "17", "In twenty", "In 20", "In ")
    c.pop(f"#{p}-m1", t, 0.5)
    c.sfx("pop", t)
    c.blur_in(f"#{p}-src", t + 0.5)
    t = T(c, "17", "Regular")
    popl(c, f"#{p}-ef", t)
    popl(c, f"#{p}-fg", t + 1.6)
    t = T(c, "17", "A newer")
    c.pop(f"#{p}-m2", t, 0.5)
    c.sfx("pop", t)
    popl(c, f"#{p}-sm", T(c, "17", "The effect"), snd="thump")
    t = T(c, "17", "But moving")
    popl(c, f"#{p}-wk", t)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    idle(c, f"{p}-vui", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 18 · Sunday jet lag
def s18():
    c = comp("18")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    x0, w = 800, 1000          # trục 20:00 → 14:00 hôm sau (18 giờ)
    hx = lambda h: x0 + w * (h - 20) / 18

    def sleep_bar(id_, y, a, b, col, lab):
        return g(id_, f'<rect x="{hx(a):.0f}" y="{y}" width="{hx(b) - hx(a):.0f}" height="80" rx="16" fill="{col}" stroke="{INK}" stroke-width="6"/>'
                 + text(x0 - 20, y + 52, lab, 34, 900, WHITE, "end"))
    ticks = "".join(text(hx(h), 730, f"{h % 24:02d}:00", 28, 700, GREY, "middle") + f'<line x1="{hx(h):.0f}" y1="330" x2="{hx(h):.0f}" y2="690" '
                    f'stroke="{GREY}" stroke-width="2" opacity=".35"/>' for h in (22, 24, 26, 28, 30, 32, 34, 36))
    c.svg += [label(f"{p}-hd", 1270, 200, "YOUR BODY CLOCK", 72, YELLOW, "middle"),
              g(f"{p}-ax", ticks),
              sleep_bar(f"{p}-sd", 360, 23, 31, TEAL, "SCHOOL"),
              sleep_bar(f"{p}-su", 560, 26, 35, CORAL, "SUNDAY"),
              g(f"{p}-gap", f'<path d="M{hx(27):.0f} 500 H{hx(29.5):.0f}" stroke="{YELLOW}" stroke-width="8" stroke-dasharray="14 10"/>'
                + text(hx(28.25), 490, "✈", 52, 900, YELLOW, "middle")),
              label(f"{p}-sj", 1270, 840, "SOCIAL JETLAG", 90, YELLOW, "middle"),
              label(f"{p}-mn", 1270, 840, "MONDAY: FLY BACK", 70, CORAL, "middle"),
              label(f"{p}-ww", 1270, 840, "SLEEP WORSE · FEEL WORSE", 60, CORAL, "middle"),
              label(f"{p}-ta", 1270, 840, "TIMING, NOT AMOUNT", 80, YELLOW, "middle"),
              note(f"{p}-src", 1270, 940, "Wittmann, Dinich, Merrow & Roenneberg, Chronobiology International, 2006 · surveys")]
    close()
    end = end_of(c, "18")
    c.hide(f"#{p}-hd", f"#{p}-ax", f"#{p}-sd", f"#{p}-su", f"#{p}-gap", f"#{p}-sj", f"#{p}-mn", f"#{p}-ww", f"#{p}-ta", f"#{p}-src")
    popl(c, f"#{p}-hd", T(c, "18", "There's one"))
    t = T(c, "18", "On school")
    c.blur_in(f"#{p}-ax", t)
    c.show(f"#{p}-sd", t + 0.1)
    c.tl.ft(f"#{p}-sd", {"scaleX": 0, "transformOrigin": "0% 50%"}, {"scaleX": 1, "transformOrigin": "0% 50%", "duration": 0.6}, t + 0.1)
    t = T(c, "18", "On Sunday")
    c.show(f"#{p}-su", t)
    c.tl.ft(f"#{p}-su", {"scaleX": 0, "transformOrigin": "0% 50%"}, {"scaleX": 1, "transformOrigin": "0% 50%", "duration": 0.6}, t)
    c.sfx("pop", t)
    t = T(c, "18", "That's like")
    c.pop(f"#{p}-gap", t, 0.5)
    c.sfx("whoosh", t)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    t = T(c, "18", "Then on")
    popl(c, f"#{p}-mn", t, snd=None)
    t = T(c, "18", "Scientists")
    c.show(f"#{p}-mn", t, False)
    popl(c, f"#{p}-sj", t, snd="thump")
    c.blur_in(f"#{p}-src", t + 0.3)
    t = T(c, "18", "In surveys")
    c.show(f"#{p}-sj", t, False)
    popl(c, f"#{p}-ww", t, snd=None)
    t = T(c, "18", "So the problem")
    c.show(f"#{p}-ww", t, False)
    popl(c, f"#{p}-ta", t, snd="thump")
    idle(c, f"{p}-ngac-nhien", T(c, "18", "That's like") + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 19 · Sleep pressure still builds
def s19():
    c = comp("19")
    p = c.cid
    close = board(c, ("ngap",))
    c.svg += [label(f"{p}-hd", 1270, 200, "SLEEP PRESSURE", 72, YELLOW, "middle"),
              f'<path id="{p}-ax" d="M800 300 V780 H1800" fill="none" stroke="{GREY}" stroke-width="6"/>',
              text(780, 320, "HIGH", 30, 900, GREY, "end"), text(1300, 840, "HOURS AWAKE →", 34, 900, GREY, "middle"),
              pressure_curve(f"{p}-cv", 810, 330, 960, 440, YELLOW),
              label(f"{p}-sm", 1560, 560, "SAME CLIMB", 44, WHITE, "middle"),
              label(f"{p}-bd", 1560, 640, "BUSY DAY", 44, TEAL, "middle"),
              label(f"{p}-ld", 1560, 710, "LAZY DAY", 44, CORAL, "middle"),
              label(f"{p}-np", 1270, 910, "A LAZY DAY DOESN'T PAUSE IT", 52, CORAL, "middle"),
              note(f"{p}-src", 1540, 300, "Borbély et al., J Sleep Research, 2016")]
    close()
    end = end_of(c, "19")
    c.hide(f"#{p}-hd", f"#{p}-bd", f"#{p}-ld", f"#{p}-sm", f"#{p}-np", f"#{p}-src")
    popl(c, f"#{p}-hd", 0.2)
    t = T(c, "19", "From the moment")
    c.draw(f"#{p}-cv", t, 3.0, "power1.inOut")
    c.blur_in(f"#{p}-src", t + 0.3)
    t = T(c, "19", "It rises")
    popl(c, f"#{p}-bd", t, snd=None)
    popl(c, f"#{p}-ld", t + 0.5, snd=None)
    popl(c, f"#{p}-sm", t + 1.2)
    popl(c, f"#{p}-np", T(c, "19", "A lazy"), snd="thump")
    idle(c, f"{p}-ngap", 0, end, 0)
    return c


# ---------------------------------------------------------------- 20 · When it's something else
def s20():
    c = comp("20")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))

    def gcard(k, x, lab):
        return g(f"{p}-k{k}", f'<rect x="{x - 170}" y="300" width="340" height="230" rx="26" fill="{NAVY}" stroke="{GREY}" stroke-width="7"/>'
                 + text(x, 430, lab, 33, 900, WHITE, "middle"))
    c.svg += [label(f"{p}-hd", 1270, 200, "NOT EVERY TIRED DAY IS BOREDOM", 60, YELLOW, "middle"),
              gcard(0, 900, "SHORT ON SLEEP"), gcard(1, 1270, "GETTING SICK"), gcard(2, 1640, "LOW MOOD"),
              label(f"{p}-rc", 1270, 630, "REAL CAUSES · REST AND CARE", 50, TEAL, "middle"),
              label(f"{p}-cl", 1270, 760, "SLEPT FINE + HEALTHY + STILL DRAINED?", 46, WHITE, "middle"),
              label(f"{p}-sg", 1270, 860, "→ THE SIGNAL TALKING", 64, YELLOW, "middle"),
              note(f"{p}-src", 1270, 940, "NHS: Tiredness and fatigue")]
    close()
    end = end_of(c, "20")
    ks = [f"#{p}-k{k}" for k in range(3)]
    c.hide(f"#{p}-hd", *ks, f"#{p}-rc", f"#{p}-cl", f"#{p}-sg", f"#{p}-src")
    popl(c, f"#{p}-hd", T(c, "20", "To be fair"))
    for k, pre in enumerate(("If you slept", "If you're getting", "And feeling")):
        t = T(c, "20", pre)
        c.pop(ks[k], t, 0.5)
        c.sfx("pop", t)
    c.blur_in(f"#{p}-src", T(c, "20", "If you slept") + 0.4)
    popl(c, f"#{p}-rc", T(c, "20", "Those are"))
    t = T(c, "20", "But if")
    popl(c, f"#{p}-cl", t, snd=None)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", T(c, "20", "That's usually"))
    popl(c, f"#{p}-sg", T(c, "20", "That's usually"), snd="thump")
    idle(c, f"{p}-vui", T(c, "20", "That's usually") + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 21 · The answer
def s21():
    c = comp("21")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [options(f"{p}-o"),
              g(f"{p}-3", chip(f"{p}-30", 900, 560, "BORED", 50, YELLOW) + chip(f"{p}-31", 1270, 560, "STILL", 50, TEAL)
                + chip(f"{p}-32", 1640, 560, "CLOCK OFF", 50, CORAL, WHITE)),
              label(f"{p}-ne", 1500, 432, "SAVES ALMOST NO ENERGY", 36, CORAL, "middle"),
              label(f"{p}-tm", 1500, 890, "HALF RIGHT: TIMING, NOT AMOUNT", 36, YELLOW, "middle")]
    close()
    end = end_of(c, "21")
    sw = [f"#{p}-3{k}" for k in range(3)]
    c.hide(f"#{p}-3", *sw, f"#{p}-ne", f"#{p}-tm")
    ta = T(c, "21", "So, the answer", "So the answer")
    c.tl.to(f"#{p}-ob-box", {"opacity": 1, "duration": 0.3}, ta)
    c.tl.ft(f"#{p}-ob", {"scale": 1}, {"scale": 1.04, "transformOrigin": "50% 50%", "duration": 0.3, "yoyo": True, "repeat": 1}, ta)
    c.sfx("riser", ta - 2.5)
    c.sfx("thump", ta)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", ta)
    t = T(c, "21", "An empty")
    c.tl.to([f"#{p}-oa", f"#{p}-oc"], {"opacity": 0, "duration": 0.3}, t - 0.3)
    c.tl.to(f"#{p}-ob", {"y": -230, "duration": 0.6, "ease": "power2.inOut"}, t)
    c.sfx("whoosh", t)
    c.show(f"#{p}-3", t + 0.4)
    t2 = T(c, "21", "Boredom")
    for k in range(3):
        popl(c, sw[k], t2 + 1.0 * k, snd="pop")
    t = T(c, "21", "A is wrong")
    fade_seq(c, [f"#{p}-3", *sw], t - 0.3)
    c.tl.to(f"#{p}-ob", {"y": 0, "duration": 0.4}, t - 0.3)  # B (đáp án) giữ sáng
    c.tl.to(f"#{p}-oa", {"opacity": 0.8, "duration": 0.3}, t)
    c.draw(f"#{p}-oa-strike", t + 0.3, 0.4)
    popl(c, f"#{p}-ne", t + 0.5, snd=None)
    t = T(c, "21", "And C")
    c.tl.to(f"#{p}-oc", {"opacity": 0.8, "duration": 0.3}, t)
    popl(c, f"#{p}-tm", t + 0.3, snd="pop")
    idle(c, f"{p}-suy-nghi", 0, ta, 1)
    idle(c, f"{p}-vui", ta + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 22 · How to actually rest
def s22():
    c = comp("22")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    tips = [("SWITCH, DON'T SHUT DOWN", "First"), ("PICK SOMETHING THAT GRABS YOU", "Pick"), ("MOVE A LITTLE · EASY IS ENOUGH", "Second"),
            ("WAKE UP NEAR YOUR USUAL TIME", "Third")]
    c.svg += [label(f"{p}-hd", 1270, 200, "HOW TO ACTUALLY REST", 80, YELLOW, "middle"),
              "".join(label(f"{p}-tp{k}", 740, 360 + k * 120, f"{k + 1}. {s}", 52, WHITE) for k, (s, _) in enumerate(tips)),
              label(f"{p}-ex", 1270, 860, "DRAWING · COOKING · A CALL WITH A FRIEND", 40, TEAL, "middle"),
              label(f"{p}-ns", 1270, 860, "NOT JUST MORE SCROLLING", 46, CORAL, "middle")]
    close()
    end = end_of(c, "22")
    c.hide(f"#{p}-hd", f"#{p}-ex", f"#{p}-ns", *[f"#{p}-tp{k}" for k in range(4)])
    t0 = T(c, "22", "So how")
    popl(c, f"#{p}-hd", t0)
    for k, (_, pre) in enumerate(tips):
        tt = T(c, "22", pre)
        c.tl.ft(f"#{p}-tp{k}", {"autoAlpha": 0, "x": 60}, {"autoAlpha": 1, "x": 0, "duration": 0.4, "ease": "expo.out"}, tt)
        c.sfx("pop", tt)
    t = T(c, "22", "Drawing")
    popl(c, f"#{p}-ex", t, snd=None)
    t2 = T(c, "22", "Not just", "Drawing") + (0 if has("22", "Not just") else 2.2)
    c.show(f"#{p}-ex", t2, False)
    popl(c, f"#{p}-ns", t2, snd=None)
    c.blur_out(f"#{p}-ns", T(c, "22", "Second") - 0.2)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", T(c, "22", "Second"))
    idle(c, f"{p}-vui", T(c, "22", "Second") + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 23 · Back to Sunday
def s23():
    c = comp("23")
    p = c.cid
    poses = ["vui", "suy-nghi"]  # bỏ "chay": mặt hoảng, ngược lời đọc
    hx, hy = L_CX, L_FEET - L_H * 0.8
    over = (chip(f"{p}-t9", 620, 150, "SUNDAY · 9:00 AM", 60, TEAL, INK)
            + chip(f"{p}-wk", hx - 400, hy + 40, "🚶 SHORT WALK", 52, PAPER, INK)
            + chip(f"{p}-bd", hx - 400, hy + 160, "1 HOUR · BUILDING SOMETHING", 46, PAPER, INK)
            + chip(f"{p}-sh", L_TV[0] - 80, L_TV[1] - 170, "▶ STILL A SHOW", 46, PAPER, INK)
            + chip(f"{p}-six", 620, 150, "6:00 PM", 64, YELLOW, INK)
            + chip(f"{p}-aw", hx - 400, hy + 40, "AWAKE", 72, TEAL, INK))
    cam, st = scene_comp(c, "phong-khach", poses, L_CX, L_FEET, L_H, over)
    c.svg.append(f'<rect id="{p}-dim" width="1920" height="1080" fill="{INK}" opacity="0"/>')
    c.svg.append(label(f"{p}-bk", 960, 540, "A BETTER KIND OF REST", 100, YELLOW, "middle"))
    end = end_of(c, "23")
    c.hide(*[f"#{p}-{x}" for x in ("t9", "wk", "bd", "sh", "six", "aw", "bk")])
    t_ = lambda *pre: T(c, "23", *pre)
    frame(c, 0, 960, 540, 1.0, cam, st)
    popl(c, f"#{p}-t9", 0.3)
    idle(c, f"{p}-vui", 0, t_("You still"), 0)
    t = t_("You go")
    c.show(f"#{p}-t9", t, False)
    frame(c, t, hx - 150, hy + 140, 1.4, cam, st)
    popl(c, f"#{p}-wk", t + 0.1)
    popl(c, f"#{p}-bd", t_("You spend", "You go") + (0 if has("23", "You spend") else 1.6), snd=None)
    t = t_("You still")
    fade_seq(c, [f"#{p}-wk", f"#{p}-bd"], t - 0.2)
    show_pose(c, poses, "suy-nghi", t)
    frame(c, t, 1200, 480, 1.2, cam, st)
    popl(c, f"#{p}-sh", t)
    t = t_("But at six")
    c.show(f"#{p}-sh", t, False)
    frame(c, t, 960, 540, 1.0, cam, st)
    popl(c, f"#{p}-six", t + 0.2, snd="pop")
    t = t_("You're not")
    show_pose(c, poses, "vui", t)
    frame(c, t, hx - 150, hy + 120, 1.5, cam, st)
    popl(c, f"#{p}-aw", t + 0.3, snd="thump")
    idle(c, f"{p}-vui", t, end, 1)
    t = t_("You didn't")
    c.show(f"#{p}-aw", t, False)
    c.tl.to(f"#{p}-dim", {"opacity": 0.6, "duration": 0.4}, t)
    popl(c, f"#{p}-bk", t + 1.4, snd="thump")
    return c


# ---------------------------------------------------------------- 24 · End card
def s24():
    c = comp("24")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', char("s24-boy", "vui", 1600, 1010, 720)]
    lines = [("big", "Tiredness isn't an empty tank.<br>It's a message."),
             ("lab", "Key sources"),
             ("src", "Raichle &amp; Gusnard, <i>PNAS</i> (2002) · Pattyn et al., <i>Physiol Behav</i> (2008)"),
             ("src", "Wilson et al., <i>Science</i> (2014) · Buttrick et al., <i>JPSP</i> (2019) · Kurzban et al., <i>BBS</i> (2013)"),
             ("src", "Puetz et al., <i>Psychother Psychosom</i> (2008) · Westgate &amp; Wilson, <i>Psychol Rev</i> (2018)"),
             ("src", "Wittmann et al., <i>Chronobiol Int</i> (2006) · Full list in the description."),
             ("safe", "For general education only, not medical advice.<br>Tired for weeks, even with enough rest? Talk to a doctor.")]
    c.css.append(f"#s24-card {{ left: 130px; top: 100px; width: 1280px; color: {INK}; }}"
                 "#s24-card .big { font-size: 64px; font-weight: 800; line-height: 1.12; letter-spacing: -0.01em; margin-bottom: 44px; }"
                 "#s24-card .lab { font-size: 34px; font-weight: 800; color: #B5372A; margin-bottom: 10px; }"
                 "#s24-card .src { font-size: 29px; font-weight: 500; line-height: 1.45; color: #2A3A4A; }"
                 "#s24-card .safe { font-size: 34px; font-weight: 700; margin-top: 40px; line-height: 1.35; }")
    c.html.append('<div id="s24-card" class="txt" data-hold="true">'
                  + "".join(f'<div id="s24-l{k}" class="{cls}">{tx}</div>' for k, (cls, tx) in enumerate(lines)) + "</div>")
    for k in range(len(lines)):
        c.blur_in(f"#s24-l{k}", 0.2 + 0.12 * k, 0.2)
    c.tl.ft("#s24-boy", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "expo.out"}, 0.3)
    idle(c, "s24-boy", 1.0, end_of(c, "24"), 2)
    return c


BUILDERS = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24]


def music():
    lifts = [(0, SCENES["01"]["end"]), (SCENES["09"]["start"], SCENES["09"]["end"]), (SCENES["24"]["start"], DURATION + 1)]
    plan = [(0, SCENES["03"]["start"], ["lofi"]), (SCENES["03"]["start"], SCENES["10"]["start"], ["doc", "mar"]),
            (SCENES["10"]["start"], SCENES["21"]["start"], ["kal", "lofi", "doc", "mar"]), (SCENES["21"]["start"], DURATION, ["piz"])]
    return music_plan(plan, lifts)()


if __name__ == "__main__":
    run(BUILDERS, music, mau=True)
