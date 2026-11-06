"""Why do we sleep? — dựng HyperFrames từ audio/timeline.json + audio/words.json.
Chạy:  py build.py      (trong thư mục video\\)
Bộ dựng chung: scripts\\hf\\minh_hoa.py (nhân vật PNG, bảng, nhạc) + ve3.py (đồ vật giấc ngủ).
"""
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from hf import core  # noqa: E402

core.init(__file__)
from hf.core import *  # noqa: E402,F401,F403
from hf.core import SCENES, WORDS, DURATION  # noqa: E402,F401
from hf.minh_hoa import *  # noqa: E402,F401,F403
from hf.ve3 import *  # noqa: E402,F401,F403

WATER = "#4FB3E8"
NIGHT = "#2B3F7A"

# Phòng ngủ (assets/bg/phong-ngu.jpg, 1920×1080): tọa độ đồ vật
R_CLOCK, R_MUG, R_BOOKS, R_WINDOW, R_BED, R_LAMP = (239, 115), (690, 640), (480, 690), (1033, 230), (1600, 600), (230, 380)
R_CX, R_FEET, R_H = 1130, 1062, 760


def end_of(c, sid):
    return c.loc(SCENES[sid]["end"])


def fade_seq(c, sels, t, dur=0.25):
    for s in sels:
        c.blur_out(s, t, dur)


def note(id_, x, y, s, size=30):
    return text(x, y, s, size, 600, GREY, "middle", id_=id_)


# ---------------------------------------------------------------- 01 · Title
def s01():
    c = comp("01")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', moon("s01-moon", 1180, 330, 1.3),
              zzz("s01-z", 1290, 260, 1.2, NIGHT), char("s01-boy", "ngap", 1600, 1010, 760)]
    words = ["Why", "do", "we", "<br>", "sleep?"]
    spans = "".join("<br>" if w == "<br>" else
                    f'<span id="s01-w{k}" class="w{" hot" if w == "sleep?" else ""}">{w}</span> ' for k, w in enumerate(words))
    c.css.append(f"#s01-title {{ left: 130px; top: 300px; font-size: 160px; font-weight: 800; line-height: 1.05; color: {INK}; "
                 f"letter-spacing: -0.01em; }} #s01-title .hot {{ color: {NIGHT}; }} #s01-title .w {{ display: inline-block; }}")
    c.html.append(f'<div id="s01-title" class="txt">{spans}</div>')
    c.pop("#s01-moon", 0.1, 0.6, "50% 50%", "back.out(1.6)", 0.3)
    for k in range(3):
        c.blur_in(f"#s01-z-{k}", 0.6 + 0.25 * k, 0.2)
    c.tl.ft("#s01-boy", {"y": 80, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "back.out(1.6)"}, 0.4)
    for k, w in enumerate(words):
        if w != "<br>":
            c.blur_in(f"#s01-w{k}", 0.25 + 0.1 * k, 0.15)
    return c


# ---------------------------------------------------------------- 02 · Opening story
def s02():
    c = comp("02")
    p = c.cid
    poses = ["suy-nghi", "goc-chatgpt", "ngap", "dau-dau", "ngac-nhien"]
    gray = f'<rect id="{p}-dawn" x="0" y="0" width="1920" height="1080" fill="#C9CED6" opacity="0"/>'
    over = (gray + chip(f"{p}-t9", R_CLOCK[0] + 330, 120, "9:00 PM · EXAM TOMORROW", 46)
            + chip(f"{p}-ch", R_BOOKS[0] + 60, 520, "3 CHAPTERS TO GO", 44, CORAL, WHITE)
            + chip(f"{p}-plan", 1130, 230, "PLAN: NO SLEEP", 52)
            + chip(f"{p}-t12", R_CLOCK[0] + 60, 260, "12:00 AM", 44) + chip(f"{p}-t2", R_CLOCK[0] + 60, 260, "2:00 AM", 44, CORAL, WHITE)
            + chip(f"{p}-t6", R_WINDOW[0], 420, "6:00 AM", 48))
    cam, st = scene_comp(c, "phong-ngu", poses, R_CX, R_FEET, R_H, over)
    # lớp học buổi sáng
    c.svg.append(g(f"{p}-cls", f'<image href="assets/bg/lop-hoc-bang.jpg" width="1920" height="1080"/>'
                   + text(600, 330, "FINAL EXAM", 110, 800, WHITE, "middle") + text(600, 450, "9:00 AM", 70, 700, YELLOW, "middle")
                   + char(f"{p}-ex-dau", "dau-dau", 1500, 1050, 780) + char(f"{p}-ex-ng", "ngac-nhien", 1500, 1050, 780)
                   + "".join(text(1290 + k * 90, 300 - k * 40, "?", 120, 900, CORAL, id_=f"{p}-q{k}", extra=" " + OUTLINE) for k in range(3))
                   + "".join(label(f"{p}-f{k}", 600, 700 + 90 * k, w, 72, col, "middle")
                             for k, (w, col) in enumerate((("FOGGY", WHITE), ("GRUMPY", CORAL), ("SLOW", YELLOW))))
                   + virus(f"{p}-v0", 1250, 560, 0.8) + virus(f"{p}-v1", 1720, 470, 0.6)
                   + chip(f"{p}-cold", 1500, 220, "+3 DAYS: A COLD", 54, CORAL, WHITE)))
    c.svg.append(f'<rect id="{p}-dim" width="1920" height="1080" fill="{INK}" opacity="0"/>')
    c.svg.append(label(f"{p}-worth", 960, 560, "WORTH IT?", 160, YELLOW, "middle"))
    hid = [f"#{p}-{x}" for x in ("t9", "ch", "plan", "t12", "t2", "t6", "cls", "ex-ng-w", "cold", "worth", "v0", "v1")]
    c.hide(*hid, *[f"#{p}-q{k}" for k in range(3)], *[f"#{p}-f{k}" for k in range(3)])
    T = lambda pre: S(c, "02", pre)
    end = end_of(c, "02")

    frame(c, 0, 960, 540, 1.0, cam, st)
    popl(c, f"#{p}-t9", 0.3)
    idle(c, f"{p}-suy-nghi", 0, T("You pour"), 0)
    t = T("There are still")
    c.show(f"#{p}-t9", t, False)
    frame(c, t, R_BOOKS[0] + 60, R_BOOKS[1] - 120, 2.0, cam, st)
    popl(c, f"#{p}-ch", t + 0.3, snd="thump")
    t = T("So you make")
    c.show(f"#{p}-ch", t, False)
    frame(c, t, R_CX - 40, 560, 1.4, cam, st)
    popl(c, f"#{p}-plan", t + 0.3)
    t = T("You pour")
    c.show(f"#{p}-plan", t, False)
    frame(c, t, R_MUG[0], R_MUG[1] - 60, 2.4, cam, st)
    show_pose(c, poses, "goc-chatgpt", t)
    t = T("Midnight")
    frame(c, t, R_CLOCK[0] + 60, R_CLOCK[1] + 120, 2.2, cam, st)
    popl(c, f"#{p}-t12", t + 0.1)
    c.tl.to(f"#{p}-clock-dummy", {"duration": 0.01}, t) if False else None
    t2 = c.at("02", "Two in the morning")
    c.show(f"#{p}-t12", t2, False)
    popl(c, f"#{p}-t2", t2)
    t = c.at("02", "The words start")
    c.show(f"#{p}-t2", t, False)
    frame(c, t, R_CX, 560, 1.7, cam, st)
    show_pose(c, poses, "ngap", t)
    idle(c, f"{p}-ngap", t, T("At six"), 1)
    t = T("At six")
    frame(c, t, R_WINDOW[0], R_WINDOW[1] + 80, 1.8, cam, st)
    c.tl.to(f"#{p}-dawn", {"opacity": 0.35, "duration": 1.2, "ease": "sine.inOut"}, t)
    popl(c, f"#{p}-t6", t + 0.2)
    t = T("At nine")
    c.show(f"#{p}-t6", t, False)
    c.show(f"#{p}-cls", t)
    c.sfx("whoosh", t)
    idle(c, f"{p}-ex-dau", t, T("And the answer"), 2)
    t = T("And the answer")
    swap(c, f"{p}-ex-dau", f"{p}-ex-ng", t)
    for k in range(3):
        c.pop(f"#{p}-q{k}", t + 0.3 + 0.3 * k, 0.4)
        c.sfx("pop", t + 0.3 + 0.3 * k)
    t = T("You feel foggy")
    for k in range(3):
        c.show(f"#{p}-q{k}", t, False)
    swap(c, f"{p}-ex-ng", f"{p}-ex-dau", t)
    for k, w in enumerate(("foggy", "grumpy", "slow")):
        popl(c, f"#{p}-f{k}", c.at("02", w), snd="pop" if k == 0 else None)
    t = T("Three days later")
    for k in range(3):
        c.blur_out(f"#{p}-f{k}", t - 0.2, 0.2)
    popl(c, f"#{p}-cold", t, snd="thump")
    for k in range(2):
        c.pop(f"#{p}-v{k}", t + 0.3 + 0.2 * k, 0.5)
    t = T("Was that")
    c.show(f"#{p}-cold", t, False)
    c.tl.to(f"#{p}-dim", {"opacity": 0.6, "duration": 0.4}, t)
    popl(c, f"#{p}-worth", t + 0.2, snd="thump")
    return c


# ---------------------------------------------------------------- 03 · The puzzle
def s03():
    c = comp("03")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [pie_third(f"{p}-pie", 1000, 480, 200), label(f"{p}-l3", 1000, 780, "≈ 1/3 OF YOUR LIFE: ASLEEP", 56, YELLOW, "middle"),
              zzz(f"{p}-z", 1080, 330, 1.0), label(f"{p}-ls", 1550, 360, "STILL · EYES CLOSED", 46, WHITE, "middle"),
              label(f"{p}-ld", 1550, 450, "CAN'T REACT TO DANGER", 46, CORAL, "middle"),
              label(f"{p}-la", 1270, 900, "NO KNOWN ANIMAL CLEARLY SKIPS SLEEP", 50, TEAL, "middle"),
              text(1270, 945, "Cirelli & Tononi, 2008", 28, 500, GREY, "middle", id_=f"{p}-src"),
              label(f"{p}-what", 1270, 560, "SO WHAT IS IT FOR?", 110, YELLOW, "middle")]
    close()
    end = end_of(c, "03")
    c.hide(f"#{p}-pie", f"#{p}-l3", f"#{p}-z", f"#{p}-ls", f"#{p}-ld", f"#{p}-la", f"#{p}-src", f"#{p}-what")
    t = S(c, "03", "Here's")
    c.pop(f"#{p}-pie", t, 0.5)
    c.sfx("pop", t)
    c.tl.ft(f"#{p}-pie-night", {"scale": 0.2, "svgOrigin": "1000 480"}, {"scale": 1, "svgOrigin": "1000 480", "duration": 0.6,
                                                                         "ease": "back.out(1.6)"}, c.at("03", "a third"))
    popl(c, f"#{p}-l3", c.at("03", "a third"), snd=None)
    t = S(c, "03", "Lying still")
    c.blur_in(f"#{p}-ls", t)
    for k in range(3):
        c.blur_in(f"#{p}-z-{k}", t + 0.2 * k, 0.2)
    popl(c, f"#{p}-ld", c.at("03", "unable to react"), snd="thump")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", S(c, "03", "For an animal"))
    t = S(c, "03", "And yet")
    popl(c, f"#{p}-la", t)
    c.blur_in(f"#{p}-src", t + 0.3)
    t = S(c, "03", "So sleep must")
    fade_seq(c, [f"#{p}-pie", f"#{p}-l3", f"#{p}-z", f"#{p}-ls", f"#{p}-ld", f"#{p}-la", f"#{p}-src"], t - 0.2)
    swap(c, f"{p}-ngac-nhien", f"{p}-suy-nghi", t)
    popl(c, f"#{p}-what", t + 0.2, snd="thump")
    idle(c, f"{p}-suy-nghi", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 04 · Clue one: brain waves
def s04():
    c = comp("04")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    rows = [("aw", 300, "AWAKE", 14, 40, WHITE), ("dp", 560, "DEEP SLEEP", 70, 240, WATER), ("rem", 820, "REM", 16, 46, CORAL)]
    for k, (sid, y, lb, amp, per, col) in enumerate(rows):
        c.svg.append(g(f"{p}-{sid}", text(640, y + 14, lb, 40, 900, col, "start") + wave(f"{p}-{sid}-w", 980, y, 820, amp, per, col)))
    c.svg += [label(f"{p}-c1", 1270, 150, "CLUE 1 · BRAIN WAVES", 60, YELLOW, "middle"),
              label(f"{p}-dream", 1490, 885, "VIVID DREAMS", 40, WHITE, "middle"),
              label(f"{p}-act", 1490, 940, "≈ AS ACTIVE AS AWAKE", 44, CORAL, "middle"),
              label(f"{p}-off", 1270, 560, "BRAIN ≠ OFF", 150, YELLOW, "middle")]
    close()
    end = end_of(c, "04")
    c.hide(*[f"#{p}-{r[0]}" for r in rows], f"#{p}-c1", f"#{p}-dream", f"#{p}-act", f"#{p}-off")
    popl(c, f"#{p}-c1", S(c, "04", "Let's collect"))
    t = S(c, "04", "Clue one")
    c.show(f"#{p}-aw", t + 0.6)
    c.draw(f"#{p}-aw-w", t + 0.6, 1.4, "none")
    t = S(c, "04", "In deep sleep")
    c.show(f"#{p}-dp", t)
    c.draw(f"#{p}-dp-w", t, 1.8, "none")
    c.sfx("whoosh", t)
    t = S(c, "04", "Later in the night")
    c.show(f"#{p}-rem", t)
    c.draw(f"#{p}-rem-w", t, 1.4, "none")
    popl(c, f"#{p}-dream", S(c, "04", "That's when"))
    t = S(c, "04", "And during REM")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-act", t + 0.3, snd="thump")
    t = S(c, "04", "So the brain")
    fade_seq(c, [f"#{p}-aw", f"#{p}-dp", f"#{p}-rem", f"#{p}-dream", f"#{p}-act", f"#{p}-c1"], t - 0.2)
    popl(c, f"#{p}-off", t, snd="thump")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 05 · Clues two and three: memory
def s05():
    c = comp("05")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    cards = "".join(card(f"{p}-k{k}", 820 + (k % 4) * 110, 640 + (k // 4) * 80, 0.9, [YELLOW, TEAL, CORAL, WHITE][k % 4]) for k in range(8))
    c.svg += [label(f"{p}-c2", 1270, 150, "CLUE 2 · SLEEP ON IT", 60, YELLOW, "middle"),
              g(f"{p}-A", moon(f"{p}-am", 900, 360, 0.8) + label(f"{p}-al", 900, 520, "LEARN → SLEEP", 46, WHITE, "middle")
                + label(f"{p}-ar", 900, 600, "REMEMBER MORE ✓", 46, TEAL, "middle")),
              g(f"{p}-B", sun(f"{p}-bs", 1600, 360, 0.7) + label(f"{p}-bl", 1600, 520, "LEARN → STAY AWAKE", 46, WHITE, "middle")
                + label(f"{p}-br", 1600, 600, "REMEMBER LESS", 46, GREY, "middle")),
              note(f"{p}-s2", 1270, 690, "Rasch & Born, Physiological Reviews, 2013", 28),
              label(f"{p}-c3", 1270, 150, "CLUE 3 · THE ALL-NIGHTER", 60, YELLOW, "middle"),
              g(f"{p}-nt", moon(f"{p}-nm", 820, 330, 0.6) + text(950, 350, "NO SLEEP", 48, 900, CORAL, "start")
                + f'<line x1="760" y1="330" x2="1240" y2="330" stroke="{CORAL}" stroke-width="10" opacity=".0"/>'),
              g(f"{p}-pics", cards + text(1000, 820, "NEW PICTURES TO LEARN", 34, 800, GREY, "middle")),
              g(f"{p}-bars", f'<rect x="1440" y="{860 - 360}" width="150" height="360" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + f'<rect id="{p}-b2" x="1650" y="{860 - 292}" width="150" height="292" rx="14" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                + text(1515, 910, "SLEPT", 32, 800, WHITE, "middle") + text(1725, 910, "NO SLEEP", 32, 800, WHITE, "middle")),
              label(f"{p}-19", 1620, 470, "≈ 19% LESS", 56, CORAL, "middle"),
              note(f"{p}-s3", 1620, 948, "Yoo et al., Nature Neuroscience, 2007", 28)]
    close()
    end = end_of(c, "05")
    c.hide(f"#{p}-c2", f"#{p}-A", f"#{p}-B", f"#{p}-s2", f"#{p}-c3", f"#{p}-nt", f"#{p}-pics", f"#{p}-bars", f"#{p}-19", f"#{p}-s3",
           *[f"#{p}-k{k}" for k in range(8)])
    t = S(c, "05", "Clue two")
    popl(c, f"#{p}-c2", t)
    c.pop(f"#{p}-A", t + 0.5, 0.5)
    c.pop(f"#{p}-B", t + 1.0, 0.5)
    c.blur_in(f"#{p}-s2", t + 1.4)
    t = S(c, "05", "Clue three")
    fade_seq(c, [f"#{p}-c2", f"#{p}-A", f"#{p}-B", f"#{p}-s2"], t - 0.25)
    popl(c, f"#{p}-c3", t)
    c.blur_in(f"#{p}-nt", c.at("05", "all night"))
    t = c.at("05", "a set of pictures")
    c.show(f"#{p}-pics", t)
    for k in range(8):
        c.pop(f"#{p}-k{k}", t + 0.07 * k, 0.3)
    c.sfx("pop", t)
    t = S(c, "05", "Two days later")
    c.pop(f"#{p}-bars", t, 0.5, "50% 100%")
    c.tl.ft(f"#{p}-b2", {"scaleY": 1.23, "transformOrigin": "50% 100%"}, {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.9,
                                                                           "ease": "power2.inOut"}, t + 0.6)
    for k in (1, 3, 6):
        c.tl.to(f"#{p}-k{k}", {"opacity": 0.15, "duration": 0.4}, t + 0.8)
    popl(c, f"#{p}-19", c.at("05", "nineteen percent"), snd="thump")
    c.blur_in(f"#{p}-s3", c.at("05", "nineteen percent", off=0.3))
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", c.at("05", "nineteen percent"))
    idle(c, f"{p}-ngac-nhien", c.at("05", "nineteen percent", off=0.6), end, 2)
    return c


# ---------------------------------------------------------------- 06 · Clue four: colds
def s06():
    c = comp("06")
    p = c.cid
    close = board(c, ("suy-nghi", "lo-lang"))
    week = "".join(moon(f"{p}-m{k}", 760 + k * 150, 330, 0.45) for k in range(7))
    c.svg += [label(f"{p}-c4", 1270, 150, "CLUE 4 · THE COLD VIRUS", 60, YELLOW, "middle"),
              g(f"{p}-wk", week + text(1210, 450, "SLEEP MEASURED FOR A WEEK", 38, 800, GREY, "middle")),
              virus(f"{p}-v", 1270, 330, 1.4), label(f"{p}-q", 1270, 500, "QUARANTINE", 56, WHITE, "middle"),
              g(f"{p}-bars", f'<rect x="900" y="{880 - 80}" width="200" height="80" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + f'<rect id="{p}-b1" x="1440" y="{880 - 330}" width="200" height="330" rx="14" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                + text(1000, 935, "SLEPT > 7 H", 36, 800, WHITE, "middle") + text(1540, 935, "SLEPT < 6 H", 36, 800, WHITE, "middle")),
              label(f"{p}-4x", 1540, 500, "≈ 4× MORE COLDS", 64, CORAL, "middle"),
              note(f"{p}-src", 1270, 230, "Prather et al., Sleep, 2015", 28)]
    close()
    end = end_of(c, "06")
    c.hide(f"#{p}-c4", f"#{p}-wk", f"#{p}-v", f"#{p}-q", f"#{p}-bars", f"#{p}-4x", f"#{p}-src", *[f"#{p}-m{k}" for k in range(7)])
    t = S(c, "06", "Clue four")
    popl(c, f"#{p}-c4", t)
    c.show(f"#{p}-wk", t + 0.4)
    for k in range(7):
        c.pop(f"#{p}-m{k}", t + 0.6 + 0.12 * k, 0.3)
    c.sfx("pop", t + 0.6)
    t = S(c, "06", "Then they dripped")
    c.blur_out(f"#{p}-wk", t - 0.2, 0.2)
    popl(c, f"#{p}-v", t + 0.1, snd="thump")
    c.tl.ft(f"#{p}-v", {"rotation": -8, "svgOrigin": "1270 330"}, {"rotation": 8, "svgOrigin": "1270 330", "duration": 0.5,
                                                                  "yoyo": True, "repeat": 5, "ease": "sine.inOut"}, t + 0.6)
    popl(c, f"#{p}-q", c.at("06", "quarantine"), snd=None)
    t = S(c, "06", "People who had")
    c.blur_out(f"#{p}-q", t - 0.2, 0.2)
    c.tl.to(f"#{p}-v", {"scale": 0.5, "y": -60, "svgOrigin": "1270 330", "duration": 0.5}, t)
    c.pop(f"#{p}-bars", t + 0.3, 0.5, "50% 100%")
    c.tl.ft(f"#{p}-b1", {"scaleY": 0.25, "transformOrigin": "50% 100%"}, {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.9,
                                                                           "ease": "power2.out"}, c.at("06", "four times"))
    swap(c, f"{p}-suy-nghi", f"{p}-lo-lang", c.at("06", "four times"))
    popl(c, f"#{p}-4x", c.at("06", "four times", off=0.4), snd="thump")
    c.blur_in(f"#{p}-src", c.at("06", "four times", off=0.6))
    idle(c, f"{p}-lo-lang", c.at("06", "four times", off=0.8), end, 2)
    return c


def opt_row(prefix, x, y, letter, icon, lab):
    return g(prefix, f"""<rect id="{prefix}-box" x="{x - 30}" y="{y - 86}" width="1170" height="172" rx="28" fill="none" stroke="{YELLOW}" stroke-width="8" opacity="0"/>
{text(x + 50, y + 44, letter, 128, 900, YELLOW, "middle")}
<g transform="translate({x + 270} {y})">{icon}</g>
{text(x + 430, y + 16, lab, 40, 800, WHITE)}
<line id="{prefix}-strike" x1="{x - 20}" y1="{y}" x2="{x + 1130}" y2="{y}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>""")


def options(prefix, x=690):
    return (opt_row(f"{prefix}a", x, 300, "A", battery(f"{prefix}-bat", 0, 0, 0.8), "POWER DOWN TO SAVE ENERGY")
            + opt_row(f"{prefix}b", x, 530, "B", power_switch(f"{prefix}-sw", 0, 0, 0.75), "BRAIN SWITCHES OFF")
            + opt_row(f"{prefix}c", x, 760, "C", moon(f"{prefix}-mn", 0, 0, 0.7), "NIGHT SHIFT: FILE · FIX · DEFEND"))


# ---------------------------------------------------------------- 07 · The question
def s07():
    c = comp("07")
    p = c.cid
    close = board(c)
    c.svg += [options(f"{p}-o"), label(f"{p}-q", 1270, 560, "WHAT IS SLEEP FOR?", 96, WHITE, "middle")]
    close()
    idle(c, f"{p}-suy-nghi", 0, end_of(c, "07"), 2)
    c.hide(f"#{p}-q")
    popl(c, f"#{p}-q", S(c, "07", "So what"))
    t_a = S(c, "07", "A:")
    c.blur_out(f"#{p}-q", t_a - 0.3, 0.25)
    for L, pre in (("a", "A:"), ("b", "B:"), ("c", "Or C:")):
        t = S(c, "07", pre)
        c.hide(f"#{p}-o{L}")
        c.tl.ft(f"#{p}-o{L}", {"autoAlpha": 0, "x": 60, "filter": "blur(8px)"},
                {"autoAlpha": 1, "x": 0, "filter": "blur(0px)", "duration": 0.45, "ease": "expo.out"}, t)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 08 · Take a guess
def s08():
    c = comp("08")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>',
              f'<circle cx="1590" cy="560" r="220" fill="{NIGHT}" stroke="{INK}" stroke-width="10"/>',
              text(1590, 300, "PAUSE THE VIDEO", 44, 900, INK, "middle"),
              g("s08-n", "".join(text(1590, 660, str(n), 300, 900, WHITE, "middle", id_=f"s08-n{n}") for n in (3, 2, 1)))]
    lines = [("h", "Take a guess first!"),
             ("f", "1. In deep sleep and REM, the brain stays busy."),
             ("f", "2. Sleep after learning → you remember more."),
             ("f", "3. No sleep the night before → about 19% less learned."),
             ("f", "4. Under 6 hours → about 4× more colds."),
             ("o", "A. Power down to save energy"), ("o", "B. The brain switches off to rest"),
             ("o", "C. A night shift: file memories, fix, defend")]
    c.css.append(f"#s08-card {{ left: 130px; top: 110px; width: 1180px; color: {INK}; }}"
                 "#s08-card .h { font-size: 80px; font-weight: 800; margin-bottom: 30px; letter-spacing: -0.01em; }"
                 "#s08-card .f { font-size: 38px; font-weight: 600; line-height: 1.3; margin-bottom: 14px; }"
                 "#s08-card .o { font-size: 42px; font-weight: 800; margin-top: 8px; line-height: 1.25; }"
                 "#s08-card .gap { height: 26px; }")
    items = []
    for k, (cls, tx) in enumerate(lines):
        if cls == "o" and lines[k - 1][0] == "f":
            items.append('<div class="gap"></div>')
        items.append(f'<div id="s08-l{k}" class="{cls}">{tx}</div>')
    c.html.append(f'<div id="s08-card" class="txt" data-hold="true">{"".join(items)}</div>')
    for k in range(len(lines)):
        c.blur_in(f"#s08-l{k}", 0.1 + 0.07 * k, 0.18)
    c.hide("#s08-n2", "#s08-n1")
    c.tl.ft("#s08-n3", {"scale": 0.4, "transformOrigin": "50% 50%"},
            {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.5, "ease": "back.out(1.8)"}, 0.2)
    c.sfx("pop", 0.2)
    for a, b, t in ((3, 2, 3.4), (2, 1, 6.4)):
        c.show(f"#s08-n{a}", t, False)
        c.pop(f"#s08-n{b}", t, 0.5, "50% 50%", "back.out(1.8)", 0.4)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 09 · The key
def s09():
    c = comp("09")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [g(f"{p}-off", power_switch(f"{p}-sw", 1000, 420, 1.4) + label(f"{p}-ol", 1000, 650, "OFF SWITCH", 56, WHITE, "middle")
                + f'<line id="{p}-x" x1="820" y1="240" x2="1180" y2="600" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" '
                  f'stroke="{CORAL}" stroke-width="18" stroke-linecap="round"/>'),
              sign(f"{p}-ns", 1520, 380, "NIGHT SHIFT", 470, YELLOW, 64),
              moon(f"{p}-mn", 1720, 210, 0.6),
              label(f"{p}-how", 1270, 880, "FIRST: HOW DO YOU FALL ASLEEP?", 58, WHITE, "middle")]
    close()
    end = end_of(c, "09")
    c.hide(f"#{p}-off", f"#{p}-ns", f"#{p}-mn", f"#{p}-how")
    t = S(c, "09", "The key")
    c.pop(f"#{p}-off", t, 0.5)
    c.sfx("pop", t)
    t = c.at("09", "isn't an off switch")
    c.draw(f"#{p}-x", t + 0.3, 0.4)
    c.sfx("thump", t + 0.4)
    t = c.at("09", "different work mode")
    c.pop(f"#{p}-ns", t, 0.6, "50% 100%", "back.out(1.6)")
    c.pop(f"#{p}-mn", t + 0.3, 0.5)
    c.sfx("pop", t)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    popl(c, f"#{p}-how", S(c, "09", "To see"))
    idle(c, f"{p}-vui", t + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 10 · Sleep pressure (adenosine, caffeine)
def s10():
    c = comp("10")
    p = c.cid
    close = board(c, ("suy-nghi", "ngap", "ngac-nhien"))
    TX, TY, TW, TH = 700, 230, 220, 520
    hours = "".join(text(TX + TW + 30, TY + TH - k * (TH / 4) + 10, h, 30, 700, GREY, "start", id_=f"{p}-h{k}")
                    for k, h in enumerate(("7 AM", "11 AM", "3 PM", "7 PM", "11 PM")))
    recs = "".join(receptor(f"{p}-r{k}", 1230 + k * 190, 640, 1.0) for k in range(4))
    ads = "".join(adenosine(f"{p}-a{k}", 1230 + k * 190, 420, 1.0) for k in range(4))
    cafs = "".join(caffeine(f"{p}-cf{k}", 1230 + k * 190, 300, 1.0) for k in range(4))
    c.svg += [tank(f"{p}-tk", TX, TY, TW, TH, YELLOW, "ADENOSINE"), hours, moon(f"{p}-mn", TX + TW / 2, TY - 60, 0.5),
              label(f"{p}-sp", 1500, 200, "SLEEP PRESSURE", 70, YELLOW, "middle"),
              g(f"{p}-mem", f'<rect x="1100" y="640" width="780" height="40" rx="10" fill="#E9C9E0" stroke="{INK}" stroke-width="6"/>' + recs),
              ads, cafs,
              label(f"{p}-park", 1500, 820, "CAFFEINE TAKES THE PARKING SPOTS", 44, WHITE, "middle"),
              label(f"{p}-still", 1500, 900, "ADENOSINE IS STILL THERE", 44, YELLOW, "middle"),
              g(f"{p}-hl", coffee_cup(f"{p}-cup", 1000, 420, 1.2)
                + label(f"{p}-hl1", 1460, 380, "HALF STILL IN YOUR BODY", 52, WHITE, "middle")
                + label(f"{p}-hl2", 1460, 460, "4–6 HOURS LATER", 64, YELLOW, "middle")),
              g(f"{p}-dk", label(f"{p}-dk1", 1270, 690, "STRONG DOSE 6 H BEFORE BED", 52, WHITE, "middle")
                + label(f"{p}-dk2", 1270, 790, "≈ 1 HOUR LESS SLEEP", 80, CORAL, "middle")
                + note(f"{p}-dk3", 1270, 860, "Drake et al., J Clin Sleep Med, 2013 · 400 mg", 28))]
    close()
    end = end_of(c, "10")
    c.hide(f"#{p}-tk", f"#{p}-mn", f"#{p}-sp", f"#{p}-mem", f"#{p}-park", f"#{p}-still", f"#{p}-hl", f"#{p}-dk",
           *[f"#{p}-h{k}" for k in range(5)], *[f"#{p}-a{k}" for k in range(4)], *[f"#{p}-cf{k}" for k in range(4)])
    FILL = f"#{p}-tk-fill"
    t = S(c, "10", "From the moment")
    c.pop(f"#{p}-tk", t, 0.5, "50% 100%")
    c.tl.set(FILL, {"scaleY": 0.05, "transformOrigin": "50% 100%"}, 0)
    c.tl.to(FILL, {"scaleY": 0.45, "transformOrigin": "50% 100%", "duration": 2.5, "ease": "none"}, t + 0.4)
    for k in range(3):
        c.blur_in(f"#{p}-h{k}", t + 0.4 + 0.8 * k, 0.2)
    t = S(c, "10", "The longer")
    c.tl.to(FILL, {"scaleY": 0.95, "transformOrigin": "50% 100%", "duration": 2.2, "ease": "power1.in"}, t)
    c.blur_in(f"#{p}-h3", t + 0.4)
    c.blur_in(f"#{p}-h4", t + 1.2)
    swap(c, f"{p}-suy-nghi", f"{p}-ngap", c.at("10", "the sleepier"))
    popl(c, f"#{p}-sp", S(c, "10", "Scientists call"), snd="thump")
    t = S(c, "10", "While you sleep")
    c.pop(f"#{p}-mn", t, 0.5)
    c.tl.to(FILL, {"scaleY": 0.05, "transformOrigin": "50% 100%", "duration": 2.0, "ease": "power2.inOut"}, t + 0.3)
    c.sfx("whoosh", t + 0.3)
    swap(c, f"{p}-ngap", f"{p}-suy-nghi", c.at("10", "wake up refreshed"))
    t = S(c, "10", "Caffeine works")
    c.blur_out(f"#{p}-sp", t - 0.2, 0.2)
    c.pop(f"#{p}-mem", t, 0.5, "50% 100%")
    for k in range(4):
        c.pop(f"#{p}-a{k}", t + 0.2 + 0.1 * k, 0.4)
    for k in range(4):
        c.tl.ft(f"#{p}-cf{k}", {"autoAlpha": 1, "y": -220}, {"autoAlpha": 1, "y": 290, "duration": 0.6, "ease": "power2.in"}, t + 1.0 + 0.15 * k)
        c.tl.to(f"#{p}-a{k}", {"x": (-1) ** k * 60, "y": -150, "rotation": 20, "duration": 0.5, "ease": "power2.out"}, t + 1.45 + 0.15 * k)
    c.sfx("pop", t + 1.5)
    popl(c, f"#{p}-park", c.at("10", "parking spots"), snd=None)
    t = S(c, "10", "The adenosine is")
    popl(c, f"#{p}-still", t, snd="pop")
    for k in range(4):
        c.tl.ft(f"#{p}-a{k}", {"scale": 1}, {"scale": 1.2, "transformOrigin": "50% 50%", "duration": 0.3, "yoyo": True, "repeat": 3}, t + 0.2)
    t = S(c, "10", "And caffeine lingers")
    fade_seq(c, [f"#{p}-tk", f"#{p}-mn", f"#{p}-mem", f"#{p}-park", f"#{p}-still", *[f"#{p}-h{k}" for k in range(5)],
                 *[f"#{p}-a{k}" for k in range(4)], *[f"#{p}-cf{k}" for k in range(4)]], t - 0.25)
    c.show(f"#{p}-hl", t)
    c.pop(f"#{p}-cup", t, 0.5, "50% 100%")
    popl(c, f"#{p}-hl1", c.at("10", "half of it"), snd=None)
    popl(c, f"#{p}-hl2", c.at("10", "four to six hours"), snd="thump")
    t = S(c, "10", "In one study")
    c.tl.to(f"#{p}-hl", {"y": -120, "duration": 0.5, "ease": "power2.inOut"}, t)
    c.show(f"#{p}-dk", t + 0.2)
    c.blur_in(f"#{p}-dk1", t + 0.2)
    popl(c, f"#{p}-dk2", c.at("10", "cut sleep"), snd="thump")
    c.blur_in(f"#{p}-dk3", c.at("10", "cut sleep", off=0.3))
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", c.at("10", "cut sleep"))
    idle(c, f"{p}-ngac-nhien", c.at("10", "cut sleep", off=0.6), end, 1)
    return c


# ---------------------------------------------------------------- 11 · The body clock
def s11():
    c = comp("11")
    p = c.cid
    close = board(c, ("suy-nghi", "ngap"))
    CX, CY = 1000, 470
    arc = f'<path id="{p}-arc" d="M680 470 A320 320 0 0 1 1320 470" fill="none" stroke="#1D4262" stroke-width="10" stroke-dasharray="20 18"/>'
    mel = (f'<path id="{p}-mel" d="M1150 900 C1350 900 1450 890 1560 820 C1650 760 1700 640 1820 600" fill="none" stroke="{TEAL}" '
           f'stroke-width="12" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')
    c.svg += [label(f"{p}-t", 1270, 150, "FORCE 2 · THE BODY CLOCK", 60, YELLOW, "middle"),
              g(f"{p}-br", brain(f"{p}-brain", CX, CY, 1.3) + f'<circle id="{p}-dot" cx="{CX + 20}" cy="{CY + 40}" r="20" fill="{YELLOW}" stroke="{INK}" stroke-width="5"/>'),
              label(f"{p}-mc", CX, 720, "MASTER CLOCK", 52, YELLOW, "middle"),
              label(f"{p}-24", CX, 800, "≈ 24 H 11 MIN", 64, WHITE, "middle"),
              note(f"{p}-src", CX, 860, "Czeisler et al., Science, 1999", 28),
              g(f"{p}-sky", arc + sun(f"{p}-sun", 680, 470, 0.6) + moon(f"{p}-mn", 1320, 470, 0.55)),
              label(f"{p}-reset", 1000, 300, "DAYLIGHT RESETS IT", 52, YELLOW, "middle"),
              g(f"{p}-mg", mel + text(1820, 570, "MELATONIN", 40, 900, TEAL, "end")
                + text(1180, 960, "DAY", 30, 800, GREY, "middle") + text(1760, 960, "NIGHT", 30, 800, GREY, "middle")),
              label(f"{p}-eq", 1490, 380, "HIGH PRESSURE + NIGHT SIGNAL", 46, WHITE, "middle"),
              label(f"{p}-eq2", 1490, 460, "= EASY SLEEP", 64, TEAL, "middle"),
              g(f"{p}-scr", f'<rect x="1600" y="160" width="140" height="250" rx="22" fill="#CFE8F7" stroke="{INK}" stroke-width="6"/>'
                + f'<circle cx="1670" cy="285" r="160" fill="#CFE8F7" opacity=".25"/>'
                + text(1670, 470, "BRIGHT SCREENS", 34, 900, CORAL, "middle"))]
    close()
    end = end_of(c, "11")
    c.hide(f"#{p}-t", f"#{p}-br", f"#{p}-mc", f"#{p}-24", f"#{p}-src", f"#{p}-sky", f"#{p}-reset", f"#{p}-mg", f"#{p}-eq", f"#{p}-eq2", f"#{p}-scr")
    popl(c, f"#{p}-t", S(c, "11", "The second force"))
    t = S(c, "11", "Deep in your brain")
    c.pop(f"#{p}-br", t, 0.5)
    c.tl.ft(f"#{p}-dot", {"scale": 1}, {"scale": 1.5, "transformOrigin": "50% 50%", "duration": 0.4, "yoyo": True, "repeat": 5}, t + 0.5)
    popl(c, f"#{p}-mc", c.at("11", "master clock"), snd=None)
    popl(c, f"#{p}-24", c.at("11", "twenty-four") if False else c.at("11", "about", 0), snd="thump")
    c.blur_in(f"#{p}-src", c.at("11", "about", 0, off=0.4))
    t = S(c, "11", "Every morning")
    fade_seq(c, [f"#{p}-mc", f"#{p}-24", f"#{p}-src"], t - 0.2)
    c.blur_out(f"#{p}-br", t - 0.2, 0.25)
    c.show(f"#{p}-sky", t)
    c.tl.to(f"#{p}-sun", {"y": -160, "duration": 1.2, "ease": "power2.out"}, t + 0.2)
    popl(c, f"#{p}-reset", t + 0.4)
    t = S(c, "11", "In the evening")
    c.blur_out(f"#{p}-reset", t - 0.2, 0.2)
    c.tl.to(f"#{p}-sun", {"y": 0, "opacity": 0.2, "duration": 0.8}, t)
    c.tl.to(f"#{p}-mn", {"y": -160, "duration": 1.0, "ease": "power2.out"}, t + 0.4)
    c.show(f"#{p}-mg", t + 0.4)
    c.draw(f"#{p}-mel", t + 0.6, 1.6, "power1.inOut")
    swap(c, f"{p}-suy-nghi", f"{p}-ngap", c.at("11", "melatonin"))
    t = S(c, "11", "When high")
    fade_seq(c, [f"#{p}-sky"], t - 0.2)
    popl(c, f"#{p}-eq", t)
    popl(c, f"#{p}-eq2", c.at("11", "fall asleep easily"), snd="thump")
    t = S(c, "11", "Bright screens")
    fade_seq(c, [f"#{p}-eq", f"#{p}-eq2"], t - 0.2)
    c.pop(f"#{p}-scr", t, 0.5)
    c.sfx("pop", t)
    c.tl.to(f"#{p}-mel", {"opacity": 0.35, "duration": 0.5}, c.at("11", "blur"))
    idle(c, f"{p}-ngap", t + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 12 · A night in cycles
def s12():
    c = comp("12")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    HX, HY, HW, HH = 800, 300, 1000, 420
    cut_x = hypno_x(HX, HW, 6)
    c.svg += [label(f"{p}-t", 1300, 160, "ONE NIGHT · ≈ 90-MINUTE CYCLES", 56, YELLOW, "middle"),
              hypnogram(f"{p}-hy", HX, HY, HW, HH),
              label(f"{p}-ld", hypno_x(HX, HW, 2), HY + HH + 130, "DEEP SLEEP EARLY", 42, WATER, "middle"),
              label(f"{p}-lr", hypno_x(HX, HW, 6), HY - 40, "REM LATER", 42, CORAL, "middle"),
              g(f"{p}-cut", f'<rect x="{cut_x}" y="{HY - 20}" width="{HX + HW - cut_x}" height="{HH + 40}" rx="10" fill="{INK}" opacity=".72"/>'
                + text(cut_x + (HX + HW - cut_x) / 2, HY + HH / 2 + 20, "−2 H", 80, 900, CORAL, "middle")),
              label(f"{p}-lost", 1300, 960, "YOU LOSE A BIG CHUNK OF REM", 56, CORAL, "middle")]
    close()
    end = end_of(c, "12")
    c.hide(f"#{p}-t", f"#{p}-hy", f"#{p}-ld", f"#{p}-lr", f"#{p}-cut", f"#{p}-lost",
           *[f"#{p}-hy-rem{k}" for k in range(6)], *[f"#{p}-hy-deep{k}" for k in range(3)])
    t = S(c, "12", "Once you're asleep")
    popl(c, f"#{p}-t", t)
    c.show(f"#{p}-hy", t + 0.2)
    c.draw(f"#{p}-hy-line", t + 0.2, 2.2, "none")
    t = S(c, "12", "Early in the night")
    for k in range(3):
        c.pop(f"#{p}-hy-deep{k}", t + 0.2 * k, 0.35)
    c.sfx("pop", t)
    popl(c, f"#{p}-ld", t + 0.3, snd=None)
    t = S(c, "12", "Toward morning")
    for k in range(6):
        c.pop(f"#{p}-hy-rem{k}", t + 0.15 * k, 0.35)
    c.sfx("pop", t)
    popl(c, f"#{p}-lr", t + 0.3, snd=None)
    t = S(c, "12", "So if you cut")
    c.tl.ft(f"#{p}-cut", {"autoAlpha": 1, "scaleX": 0, "transformOrigin": "100% 50%"},
            {"autoAlpha": 1, "scaleX": 1, "transformOrigin": "100% 50%", "duration": 0.6, "ease": "expo.out"}, t)
    c.hide(f"#{p}-cut")
    c.sfx("whoosh", t)
    t = S(c, "12", "You lose")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-lost", t, snd="thump")
    idle(c, f"{p}-suy-nghi", 0, t, 1)
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 13 · Job one: memory
def s13():
    c = comp("13")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    IX, IY, CXc, CYc = 900, 560, 1600, 500
    cards = "".join(card(f"{p}-k{k}", IX - 70 + (k % 3) * 70, IY - 40 - (k // 3) * 46, 0.8, [YELLOW, TEAL, CORAL][k % 3]) for k in range(6))
    extra = "".join(card(f"{p}-x{k}", IX - 90 + (k % 4) * 60, IY - 70 - (k // 4) * 46, 0.8, GREY) for k in range(6))
    links = "".join(f'<path id="{p}-ln{k}" d="M{1520 + k * 30} {360 + k * 100} C{1700} {300 + k * 90} {1760} {520 - k * 40} {1660} {640 - k * 60}" '
                    f'fill="none" stroke="{CORAL}" stroke-width="8" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>'
                    for k in range(3))
    c.svg += [label(f"{p}-t", 1270, 150, "JOB 1 · MEMORY", 64, YELLOW, "middle"),
              inbox(f"{p}-in", IX, IY, 1.2), cabinet(f"{p}-cab", CXc, CYc, 1.0), cards, extra, links,
              moon(f"{p}-mn", 1250, 300, 0.6), label(f"{p}-rp", 1250, 420, "REPLAY", 46, WHITE, "middle"),
              label(f"{p}-room", IX, 300, "ROOM FOR TOMORROW", 44, TEAL, "middle"),
              label(f"{p}-full", IX, 250, "INBOX FULL!", 56, CORAL, "middle"),
              label(f"{p}-rem", 1600, 900, "REM: LINK · SOOTHE", 46, CORAL, "middle"),
              note(f"{p}-src", 1270, 948, "Rasch & Born, Physiological Reviews, 2013", 28)]
    close()
    end = end_of(c, "13")
    c.hide(f"#{p}-t", f"#{p}-in", f"#{p}-cab", f"#{p}-mn", f"#{p}-rp", f"#{p}-room", f"#{p}-full", f"#{p}-rem", f"#{p}-src",
           *[f"#{p}-k{k}" for k in range(6)], *[f"#{p}-x{k}" for k in range(6)])
    t0 = S(c, "13", "Now, the first")
    popl(c, f"#{p}-t", t0)
    c.pop(f"#{p}-in", t0 + 0.3, 0.5, "50% 100%")
    c.pop(f"#{p}-cab", t0 + 0.6, 0.5, "50% 100%")
    t = S(c, "13", "During the day")
    for k in range(6):
        c.tl.ft(f"#{p}-k{k}", {"autoAlpha": 1, "y": -260}, {"autoAlpha": 1, "y": 0, "duration": 0.45, "ease": "back.out(1.4)"}, t + 0.5 + 0.18 * k)
    c.sfx("pop", t + 0.5)
    t = S(c, "13", "During deep sleep")
    c.pop(f"#{p}-mn", t + 0.2, 0.4)
    c.blur_in(f"#{p}-rp", t + 0.4)
    for k in range(6):
        dx = CXc - (IX - 70 + (k % 3) * 70)
        dy = (CYc - 130 + (k % 3) * 100) - (IY - 40 - (k // 3) * 46)
        c.tl.to(f"#{p}-k{k}", {"x": dx, "y": dy, "scale": 0.6, "duration": 0.7, "ease": "power2.inOut"}, t + 1.0 + 0.3 * k)
    c.sfx("whoosh", t + 1.0)
    c.blur_in(f"#{p}-src", S(c, "13", "That's why"))
    t = S(c, "13", "Many researchers")
    popl(c, f"#{p}-room", t)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    t = S(c, "13", "Skip the night")
    c.blur_out(f"#{p}-room", t - 0.2, 0.2)
    for k in range(6):
        c.tl.ft(f"#{p}-x{k}", {"autoAlpha": 1, "y": -260}, {"autoAlpha": 1, "y": 0, "duration": 0.35, "ease": "back.out(1.4)"}, t + 0.1 * k)
    popl(c, f"#{p}-full", t + 0.6, snd="thump")
    swap(c, f"{p}-vui", f"{p}-suy-nghi", t)
    t = S(c, "13", "That's what happened")
    c.tl.ft(f"#{p}-in", {"rotation": -3, "svgOrigin": f"{IX} {IY}"}, {"rotation": 3, "svgOrigin": f"{IX} {IY}", "duration": 0.15,
                                                                      "yoyo": True, "repeat": 7}, t)
    t = S(c, "13", "REM sleep")
    for k in range(3):
        c.draw(f"#{p}-ln{k}", t + 0.3 + 0.3 * k, 0.6)
    popl(c, f"#{p}-rem", t + 0.4)
    idle(c, f"{p}-suy-nghi", t, end, 1)
    return c


# ---------------------------------------------------------------- 14 · Job two: cleaning
def s14():
    c = comp("14")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    GX, GY = 1000, 520
    cells = "".join(cell(f"{p}-c{k}", GX + (k % 3 - 1) * 150, GY + (k // 3 - 1) * 150, 70) for k in range(9))
    junks = "".join(junk(f"{p}-j{k}", GX - 75 + (k % 2) * 150, GY - 75 + (k // 2) * 150, 1.0) for k in range(4))
    flow = (f'<path id="{p}-flow" d="M640 520 C760 440 840 600 1000 520 C1160 440 1240 600 1380 520" fill="none" stroke="{WATER}" '
            f'stroke-width="22" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" opacity=".85"/>')
    c.svg += [label(f"{p}-t", 1270, 150, "JOB 2 · CLEANING (MAYBE)", 60, YELLOW, "middle"),
              g(f"{p}-grid", cells + junks + flow), label(f"{p}-ab", 1000, 860, "WASTE: BETA-AMYLOID", 44, "#D8C84A", "middle"),
              label(f"{p}-60", 1600, 420, "MICE: +60% SPACE", 56, WATER, "middle"),
              note(f"{p}-s1", 1600, 480, "Xie et al., Science, 2013", 28),
              g(f"{p}-hum", brain(f"{p}-hb", 1270, 560, 1.1) + wave(f"{p}-hw", 1050, 760, 440, 34, 220, WATER)
                + text(1270, 850, "HUMANS: FLUID PULSES WITH SLOW WAVES", 40, 800, WHITE, "middle")
                + text(1270, 900, "Fultz et al., Science, 2019", 28, 500, GREY, "middle")),
              f'<g transform="translate(1270 330) rotate(-4)"><g id="{p}-deb"><rect x="-450" y="-95" width="900" height="190" rx="16" fill="{SLATE}" '
              f'stroke="{CORAL}" stroke-width="10"/>{text(0, -18, "2024 MOUSE STUDY: OPPOSITE", 44, 900, CORAL, "middle")}'
              f'{text(0, 62, "STILL DEBATED", 44, 900, YELLOW, "middle")}</g></g>']
    close()
    end = end_of(c, "14")
    c.hide(f"#{p}-t", f"#{p}-grid", f"#{p}-ab", f"#{p}-60", f"#{p}-s1", f"#{p}-hum", f"#{p}-deb", *[f"#{p}-j{k}" for k in range(4)])
    popl(c, f"#{p}-t", S(c, "14", "The second job"))
    t = S(c, "14", "Your brain cells")
    c.pop(f"#{p}-grid", t, 0.5)
    for k in range(4):
        c.pop(f"#{p}-j{k}", t + 0.6 + 0.15 * k, 0.3)
    c.sfx("pop", t + 0.6)
    c.blur_in(f"#{p}-ab", c.at("14", "beta-amyloid") if False else t + 1.5)
    t = S(c, "14", "In a 2013") if any(s["text"].startswith("In a 2013") for s in WORDS["sentences"]) else S(c, "14", "In a")
    for k in range(9):
        dx, dy = (k % 3 - 1) * 45, (k // 3 - 1) * 45
        c.tl.to(f"#{p}-c{k}", {"x": dx, "y": dy, "duration": 1.0, "ease": "power2.inOut"}, t + 0.5)
    popl(c, f"#{p}-60", t + 0.6, snd="whoosh")
    c.blur_in(f"#{p}-s1", t + 0.9)
    t = S(c, "14", "Fluid flowed")
    c.draw(f"#{p}-flow", t, 1.0)
    for k in range(4):
        c.tl.to(f"#{p}-j{k}", {"x": 520 - (k % 2) * 150, "opacity": 0, "duration": 1.0, "ease": "power2.in"}, t + 0.4 + 0.15 * k)
    t = S(c, "14", "In 2019")
    fade_seq(c, [f"#{p}-grid", f"#{p}-ab", f"#{p}-60", f"#{p}-s1"], t - 0.2)
    c.pop(f"#{p}-hum", t, 0.5)
    c.draw(f"#{p}-hw", t + 0.4, 1.2, "none")
    t = S(c, "14", "But a 2024")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    c.show(f"#{p}-deb", t)
    c.tl.ft(f"#{p}-deb", {"scale": 1.6, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3,
                                                                        "ease": "power4.in"}, t)
    c.sfx("thump", t + 0.3)
    idle(c, f"{p}-suy-nghi", 0, t, 0)
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 15 · Job three: defense
def s15():
    c = comp("15")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    base = 880
    abs_n = "".join(antibody(f"{p}-ab{k}", 1300 + (k % 3) * 60, base - 60 - (k // 3) * 80, 0.8) for k in range(9))
    abs_h = "".join(antibody(f"{p}-ah{k}", 1600 + (k % 3) * 60, base - 60 - (k // 3) * 80, 0.8, CORAL) for k in range(4))
    c.svg += [label(f"{p}-t", 1270, 150, "JOB 3 · DEFENSE", 64, YELLOW, "middle"),
              shield(f"{p}-sh", 1000, 470, 1.4), virus(f"{p}-v0", 1450, 380, 0.7), virus(f"{p}-v1", 1550, 560, 0.6),
              label(f"{p}-cold", 1000, 720, "SHORT SLEEP → MORE COLDS", 46, CORAL, "middle"),
              syringe(f"{p}-sy", 1000, 400, 1.4),
              label(f"{p}-fl", 1000, 620, "FLU SHOT", 56, WHITE, "middle"),
              label(f"{p}-4h", 1000, 700, "4 H SLEEP / NIGHT", 44, CORAL, "middle"),
              g(f"{p}-ant", abs_n + abs_h + text(1360, base + 50, "SLEPT NORMALLY", 32, 800, WHITE, "middle")
                + text(1660, base + 50, "4 H / NIGHT", 32, 800, CORAL, "middle")),
              label(f"{p}-half", 1480, 420, "≈ HALF THE ANTIBODIES", 52, CORAL, "middle"),
              note(f"{p}-src", 1270, 230, "Spiegel et al., JAMA, 2002 · small study, young men", 28)]
    close()
    end = end_of(c, "15")
    c.hide(f"#{p}-t", f"#{p}-sh", f"#{p}-v0", f"#{p}-v1", f"#{p}-cold", f"#{p}-sy", f"#{p}-fl", f"#{p}-4h", f"#{p}-ant", f"#{p}-half", f"#{p}-src",
           *[f"#{p}-ab{k}" for k in range(9)], *[f"#{p}-ah{k}" for k in range(4)])
    t = S(c, "15", "The third job")
    popl(c, f"#{p}-t", t)
    c.pop(f"#{p}-sh", t + 0.3, 0.5)
    t = S(c, "15", "Remember")
    for k in range(2):
        c.pop(f"#{p}-v{k}", t + 0.2 * k, 0.4)
        c.tl.to(f"#{p}-v{k}", {"x": -260, "duration": 0.6, "ease": "power2.in", "yoyo": True, "repeat": 1}, t + 0.6 + 0.2 * k)
    popl(c, f"#{p}-cold", c.at("15", "Short sleepers"), snd="thump")
    t = S(c, "15", "Sleep also")
    fade_seq(c, [f"#{p}-sh", f"#{p}-v0", f"#{p}-v1", f"#{p}-cold"], t - 0.25)
    c.pop(f"#{p}-sy", t, 0.5)
    c.sfx("whoosh", t)
    t = S(c, "15", "In one small")
    popl(c, f"#{p}-4h", c.at("15", "four hours"))
    popl(c, f"#{p}-fl", c.at("15", "flu shot"), snd=None)
    t = S(c, "15", "Ten days later")
    fade_seq(c, [f"#{p}-sy", f"#{p}-fl", f"#{p}-4h"], t - 0.2)
    c.show(f"#{p}-ant", t)
    for k in range(9):
        c.pop(f"#{p}-ab{k}", t + 0.05 * k, 0.3)
    for k in range(4):
        c.pop(f"#{p}-ah{k}", t + 0.6 + 0.1 * k, 0.3)
    c.sfx("pop", t)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", c.at("15", "half as many"))
    popl(c, f"#{p}-half", c.at("15", "half as many"), snd="thump")
    c.blur_in(f"#{p}-src", c.at("15", "half as many", off=0.4))
    idle(c, f"{p}-suy-nghi", 0, c.at("15", "half as many"), 0)
    idle(c, f"{p}-ngac-nhien", c.at("15", "half as many", off=0.6), end, 2)
    return c


# ---------------------------------------------------------------- 16 · The hidden cost
def s16():
    c = comp("16")
    p = c.cid
    close = board(c, ("suy-nghi", "lo-lang", "ngac-nhien"))
    X0, Y0, W, H = 720, 280, 1000, 480
    lapse = f'<path id="{p}-lp" d="M{X0} {Y0 + H - 30} C{X0 + 300} {Y0 + H - 110} {X0 + 650} {Y0 + 160} {X0 + W} {Y0 + 40}" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>'
    feel = f'<path id="{p}-fe" d="M{X0} {Y0 + H - 60} C{X0 + 300} {Y0 + H - 110} {X0 + 650} {Y0 + H - 120} {X0 + W} {Y0 + H - 130}" fill="none" stroke="{TEAL}" stroke-width="12" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>'
    axes = (f'<path d="M{X0} {Y0} V{Y0 + H} H{X0 + W}" fill="none" stroke="{GREY}" stroke-width="6"/>'
            + text(X0 + W / 2, Y0 + H + 60, "14 DAYS · 6 HOURS IN BED", 36, 800, GREY, "middle"))
    c.svg += [label(f"{p}-t", 1270, 150, "A LITTLE LESS, EVERY NIGHT", 60, YELLOW, "middle"),
              g(f"{p}-ch", axes), lapse, feel,
              text(X0 + W - 10, Y0 + 20, "ATTENTION SLIPS", 36, 900, CORAL, "end", id_=f"{p}-lpl"),
              text(X0 + W - 10, Y0 + H - 160, "HOW SLEEPY THEY FELT", 36, 900, TEAL, "end", id_=f"{p}-fel"),
              label(f"{p}-1n", 1020, 400, "≈ 1 NIGHT WITHOUT SLEEP", 50, WHITE, "middle"),
              note(f"{p}-src", 1270, 875, "Van Dongen et al., Sleep, 2003", 28),
              label(f"{p}-un", 1270, 935, "THEY DIDN'T NOTICE", 52, YELLOW, "middle"),
              g(f"{p}-road", f'<rect x="600" y="760" width="1280" height="120" fill="#2A3A4A"/>'
                + "".join(f'<rect x="{640 + k * 200}" y="812" width="110" height="16" rx="6" fill="{YELLOW}"/>' for k in range(6))
                + car(f"{p}-car", 900, 740, 1.1)),
              label(f"{p}-cr1", 1270, 360, "4–5 H SLEEP IN THE PAST DAY", 54, WHITE, "middle"),
              label(f"{p}-cr2", 1270, 480, "≈ 4× CRASH RISK", 110, CORAL, "middle"),
              note(f"{p}-src2", 1270, 560, "AAA Foundation for Traffic Safety, 2016 · vs 7+ hours", 28)]
    close()
    end = end_of(c, "16")
    c.hide(f"#{p}-t", f"#{p}-ch", f"#{p}-lpl", f"#{p}-fel", f"#{p}-1n", f"#{p}-src", f"#{p}-un", f"#{p}-road", f"#{p}-cr1", f"#{p}-cr2", f"#{p}-src2")
    popl(c, f"#{p}-t", S(c, "16", "What if"))
    t = S(c, "16", "In one experiment")
    c.blur_in(f"#{p}-ch", t, 0.3)
    t = S(c, "16", "Their attention")
    c.draw(f"#{p}-lp", t, 2.4, "power1.in")
    c.blur_in(f"#{p}-lpl", t + 0.6)
    swap(c, f"{p}-suy-nghi", f"{p}-lo-lang", t)
    t = S(c, "16", "By the end")
    popl(c, f"#{p}-1n", t, snd="thump")
    c.blur_in(f"#{p}-src", t + 0.3)
    t = S(c, "16", "But they only")
    c.draw(f"#{p}-fe", t, 1.6)
    c.blur_in(f"#{p}-fel", t + 0.6)
    popl(c, f"#{p}-un", c.at("16", "didn't realize"), snd="thump")
    swap(c, f"{p}-lo-lang", f"{p}-ngac-nhien", c.at("16", "didn't realize"))
    t = S(c, "16", "On the road")
    fade_seq(c, [f"#{p}-ch", f"#{p}-lp", f"#{p}-fe", f"#{p}-lpl", f"#{p}-fel", f"#{p}-1n", f"#{p}-src", f"#{p}-un"], t - 0.25)
    c.show(f"#{p}-road", t)
    c.tl.ft(f"#{p}-car", {"x": -500}, {"x": 500, "duration": 3.0, "ease": "none"}, t)
    c.sfx("whoosh", t + 0.3)
    popl(c, f"#{p}-cr1", c.at("16", "four to five hours"))
    popl(c, f"#{p}-cr2", c.at("16", "four times"), snd="thump")
    c.blur_in(f"#{p}-src2", c.at("16", "four times", off=0.4))
    idle(c, f"{p}-ngac-nhien", c.at("16", "four times", off=0.6), end, 1)
    return c


# ---------------------------------------------------------------- 17 · Night owls and teens
def s17():
    c = comp("17")
    p = c.cid
    close = board(c, ("suy-nghi", "ngap"))
    X0, X1, Y = 720, 1820, 560
    hx = lambda h: X0 + (X1 - X0) * (h - 20) / 6  # 8 PM → 2 AM
    ticks = "".join(text(hx(h), Y + 70, lb, 32, 800, GREY, "middle") + f'<line x1="{hx(h)}" y1="{Y - 14}" x2="{hx(h)}" y2="{Y + 14}" stroke="{GREY}" stroke-width="6"/>'
                    for h, lb in ((20, "8 PM"), (22, "10 PM"), (23, "11 PM"), (24, "12 AM"), (26, "2 AM")))
    c.svg += [label(f"{p}-t", 1270, 150, "NOT EVERYONE'S CLOCK IS THE SAME", 56, YELLOW, "middle"),
              g(f"{p}-ax", f'<line x1="{X0}" y1="{Y}" x2="{X1}" y2="{Y}" stroke="{GREY}" stroke-width="8" stroke-linecap="round"/>' + ticks),
              g(f"{p}-eb", sun(f"{p}-ebs", 900, 300, 0.5) + label(f"{p}-ebl", 900, 420, "EARLY BIRDS", 44, YELLOW, "middle")),
              g(f"{p}-no", moon(f"{p}-nom", 1600, 300, 0.5) + label(f"{p}-nol", 1600, 420, "NIGHT OWLS", 44, WATER, "middle")),
              g(f"{p}-mk", f'<circle cx="{hx(21.5)}" cy="{Y}" r="26" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'),
              label(f"{p}-sh", hx(22.5), Y - 70, "PUBERTY: UP TO ≈ 2 H LATER", 44, CORAL, "middle"),
              label(f"{p}-11", 1270, 760, "MANY TEENS: HARD TO SLEEP BEFORE 11 PM", 48, WHITE, "middle"),
              chip(f"{p}-sc", 1270, 880, "SCHOOL START ≥ 8:30 AM", 56),
              note(f"{p}-src", 1270, 945, "American Academy of Pediatrics, 2014", 28),
              label(f"{p}-lazy", 1270, 330, "NOT LAZY — STILL NIGHT FOR THEIR CLOCK", 52, YELLOW, "middle")]
    close()
    end = end_of(c, "17")
    c.hide(f"#{p}-t", f"#{p}-ax", f"#{p}-eb", f"#{p}-no", f"#{p}-mk", f"#{p}-sh", f"#{p}-11", f"#{p}-sc", f"#{p}-src", f"#{p}-lazy")
    popl(c, f"#{p}-t", S(c, "17", "Your body clock"))
    t = S(c, "17", "Some people")
    c.pop(f"#{p}-eb", t, 0.5)
    c.pop(f"#{p}-no", c.at("17", "night owls"), 0.5)
    c.sfx("pop", t)
    t = S(c, "17", "And during puberty")
    fade_seq(c, [f"#{p}-eb", f"#{p}-no"], t - 0.2)
    c.blur_in(f"#{p}-ax", t, 0.3)
    c.pop(f"#{p}-mk", t + 0.2, 0.4)
    c.tl.to(f"#{p}-mk", {"x": hx(23.5) - hx(21.5), "duration": 1.2, "ease": "power2.inOut"}, c.at("17", "shifts later"))
    c.sfx("whoosh", c.at("17", "shifts later"))
    popl(c, f"#{p}-sh", c.at("17", "two hours"), snd=None)
    popl(c, f"#{p}-11", S(c, "17", "Many teenagers"), snd="thump")
    swap(c, f"{p}-suy-nghi", f"{p}-ngap", S(c, "17", "Many teenagers"))
    t = S(c, "17", "That's one reason")
    c.blur_in(f"#{p}-src", t + 0.3)
    popl(c, f"#{p}-sc", c.at("17", "eight thirty"), snd="thump")
    t = S(c, "17", "So a teenager")
    c.blur_out(f"#{p}-t", t - 0.2, 0.2)
    c.blur_out(f"#{p}-sh", t - 0.2, 0.2)
    popl(c, f"#{p}-lazy", t + 0.2)
    idle(c, f"{p}-suy-nghi", 0, S(c, "17", "Many teenagers"), 1)
    idle(c, f"{p}-ngap", S(c, "17", "Many teenagers") + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 18 · Can you catch up?
def s18():
    c = comp("18")
    p = c.cid
    close = board(c, ("suy-nghi", "lo-lang"))
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    boxes = "".join(g(f"{p}-d{k}", f'<rect x="{700 + k * 165}" y="300" width="145" height="170" rx="18" fill="{CORAL if k < 5 else TEAL}" '
                                    f'stroke="{INK}" stroke-width="6"/>' + text(772 + k * 165, 350, d, 34, 900, INK, "middle")
                       + text(772 + k * 165, 430, "5 H" if k < 5 else "ZZZ", 46, 900, WHITE if k < 5 else INK, "middle"))
                    for k, d in enumerate(days))
    c.svg += [label(f"{p}-t", 1270, 150, "SLEEP IN ON THE WEEKEND?", 64, YELLOW, "middle"), boxes,
              label(f"{p}-1h", 1550, 560, "CAUGHT UP: ≈ 1 HOUR", 50, TEAL, "middle"),
              g(f"{p}-mon", f'<rect x="700" y="640" width="145" height="170" rx="18" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                + text(772, 690, "MON", 34, 900, INK, "middle") + text(772, 770, "5 H", 46, 900, WHITE, "middle")),
              label(f"{p}-sug", 1330, 740, "HANDLING SUGAR: WORSE", 56, CORAL, "middle"),
              note(f"{p}-src", 1270, 880, "Depner et al., Current Biology, 2019", 28),
              label(f"{p}-st", 1270, 948, "STEADY SCHEDULE > SATURDAY LOAN", 52, YELLOW, "middle")]
    close()
    end = end_of(c, "18")
    c.hide(f"#{p}-t", f"#{p}-1h", f"#{p}-mon", f"#{p}-sug", f"#{p}-src", f"#{p}-st", *[f"#{p}-d{k}" for k in range(7)])
    popl(c, f"#{p}-t", S(c, "18", "What about"))
    t = S(c, "18", "In one 2019") if any(s["text"].startswith("In one 2019") for s in WORDS["sentences"]) else S(c, "18", "In one")
    for k in range(5):
        c.pop(f"#{p}-d{k}", t + 0.4 + 0.15 * k, 0.35, "50% 100%")
    c.sfx("pop", t + 0.4)
    c.blur_in(f"#{p}-src", t + 0.4)
    t = S(c, "18", "On the weekend")
    for k in (5, 6):
        c.pop(f"#{p}-d{k}", t + 0.2 * (k - 5), 0.4, "50% 100%")
    c.sfx("pop", t)
    popl(c, f"#{p}-1h", S(c, "18", "But they only"), snd="thump")
    t = S(c, "18", "And when")
    c.pop(f"#{p}-mon", t, 0.4, "50% 100%")
    swap(c, f"{p}-suy-nghi", f"{p}-lo-lang", t)
    popl(c, f"#{p}-sug", c.at("18", "handled sugar"), snd="thump")
    popl(c, f"#{p}-st", S(c, "18", "Sleep works best"))
    idle(c, f"{p}-suy-nghi", 0, t, 0)
    idle(c, f"{p}-lo-lang", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 19 · The answer
def s19():
    c = comp("19")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg.append(options(f"{p}-o"))
    close()
    end = end_of(c, "19")
    t = S(c, "19", "The answer")
    c.tl.to(f"#{p}-oc-box", {"opacity": 1, "duration": 0.3}, t)
    c.tl.ft(f"#{p}-oc", {"scale": 1}, {"scale": 1.04, "transformOrigin": "50% 50%", "duration": 0.3, "yoyo": True, "repeat": 1}, t)
    c.sfx("riser", t - 2.5)
    c.sfx("thump", t)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    c.draw(f"#{p}-oa-strike", S(c, "19", "Sleep does"), 0.4)
    c.tl.to(f"#{p}-oa", {"opacity": 0.4, "duration": 0.3}, S(c, "19", "Sleep does") + 0.4)
    c.draw(f"#{p}-ob-strike", S(c, "19", "And the brain"), 0.4)
    c.tl.to(f"#{p}-ob", {"opacity": 0.4, "duration": 0.3}, S(c, "19", "And the brain") + 0.4)
    c.sfx("pop", S(c, "19", "And the brain"))
    t = S(c, "19", "Sleep is an active")
    c.tl.to([f"#{p}-oa", f"#{p}-ob"], {"opacity": 0, "duration": 0.3}, t - 0.3)
    c.tl.to(f"#{p}-oc", {"y": -230, "duration": 0.6, "ease": "power2.inOut"}, t)
    c.sfx("whoosh", t)
    idle(c, f"{p}-suy-nghi", 0, S(c, "19", "The answer"), 1)
    idle(c, f"{p}-vui", S(c, "19", "The answer") + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 20 · How much do you need?
def s20():
    c = comp("20")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    people = "".join(person_icon(f"{p}-pp{k}", 1380 + k * 130, 520, 1.0, CORAL if k == 0 else WHITE) for k in range(3))
    tips = [("WAKE UP AT THE SAME TIME", "same time"), ("MORNING LIGHT · DIM NIGHTS", "daylight"),
            ("CAFFEINE: MORNING ONLY", "Keep caffeine"), ("DARK, COOL BEDROOM", "dark and cool"), ("NO ALCOHOL AS A SLEEP AID", "alcohol")]
    c.svg += [label(f"{p}-t", 1270, 560, "HOW MUCH SLEEP?", 104, YELLOW, "middle"),
              label(f"{p}-hab", 1270, 220, "A FEW HABITS THAT HELP", 84, YELLOW, "middle"),
              g(f"{p}-bar", f'<rect x="720" y="300" width="560" height="110" rx="24" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + text(1000, 375, "ADULTS: 7+ HOURS", 52, 900, INK, "middle")
                + text(1000, 460, "AASM & Sleep Research Society, 2015", 28, 500, GREY, "middle")),
              g(f"{p}-us", people + text(1510, 660, "1 IN 3 US ADULTS GET LESS", 36, 900, CORAL, "middle")
                + text(1510, 705, "CDC, 2016", 28, 500, GREY, "middle")),
              "".join(label(f"{p}-tp{k}", 760, 380 + k * 110, f"{k + 1}. {s}", 54, WHITE) for k, (s, _) in enumerate(tips)),
              text(760, 945, "Alcohol: Ebrahim et al., 2013 · Screens: Chang et al., 2015", 28, 500, GREY, id_=f"{p}-src")]
    close()
    end = end_of(c, "20")
    c.hide(f"#{p}-t", f"#{p}-hab", f"#{p}-bar", f"#{p}-us", f"#{p}-src", *[f"#{p}-tp{k}" for k in range(5)], *[f"#{p}-pp{k}" for k in range(3)])
    popl(c, f"#{p}-t", S(c, "20", "So how much"))
    t = S(c, "20", "Sleep experts")
    c.blur_out(f"#{p}-t", t - 0.2, 0.2)
    c.tl.ft(f"#{p}-bar", {"autoAlpha": 1, "scaleX": 0, "transformOrigin": "0% 50%"},
            {"autoAlpha": 1, "scaleX": 1, "transformOrigin": "0% 50%", "duration": 0.6, "ease": "expo.out"}, t)
    c.hide(f"#{p}-bar")
    c.sfx("whoosh", t)
    t = S(c, "20", "Yet in")
    c.show(f"#{p}-us", t)
    for k in range(3):
        c.pop(f"#{p}-pp{k}", t + 0.15 * k, 0.35, "50% 100%")
    c.sfx("pop", t)
    t = S(c, "20", "A few habits")
    fade_seq(c, [f"#{p}-bar", f"#{p}-us"], t - 0.25)
    popl(c, f"#{p}-hab", t)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    for k, pre in enumerate(("Wake up", "Get daylight", "Keep caffeine", "Keep your bedroom", "And don't")):
        tt = S(c, "20", pre)
        c.tl.ft(f"#{p}-tp{k}", {"autoAlpha": 0, "x": 60}, {"autoAlpha": 1, "x": 0, "duration": 0.4, "ease": "expo.out"}, tt)
        c.sfx("pop", tt)
    c.blur_in(f"#{p}-src", S(c, "20", "And don't") + 0.5)
    idle(c, f"{p}-suy-nghi", 0, t, 0)
    idle(c, f"{p}-vui", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 21 · Back to the exam
def s21():
    c = comp("21")
    p = c.cid
    c.svg += [g(f"{p}-a", f'<image href="assets/bg/phong-ngu.jpg" width="1920" height="1080"/>' + char(f"{p}-boy", "vui", R_CX, R_FEET, R_H)
                + chip(f"{p}-t11", R_CLOCK[0] + 330, 120, "11:00 PM · BOOKS CLOSED", 46)),
              g(f"{p}-b", f'<image href="assets/bg/phong-ngu-ngu.jpg" width="1920" height="1080"/>' + zzz(f"{p}-z", 1500, 330, 1.2, WHITE)
                + label(f"{p}-fl", 900, 900, "NIGHT SHIFT: FILING…", 64, YELLOW, "middle")),
              g(f"{p}-c", f'<image href="assets/bg/lop-hoc-bang.jpg" width="1920" height="1080"/>'
                + text(600, 330, "FINAL EXAM", 110, 800, WHITE, "middle") + text(600, 450, "✓ ✓ ✓", 90, 900, TEAL, "middle")
                + char(f"{p}-win", "vui", 1500, 1050, 780))]
    end = end_of(c, "21")
    c.hide(f"#{p}-b", f"#{p}-c", f"#{p}-t11", f"#{p}-fl", *[f"#{p}-z-{k}" for k in range(3)])
    popl(c, f"#{p}-t11", 0.3)
    idle(c, f"{p}-boy", 0, S(c, "21", "Study"), 0)
    t = S(c, "21", "Study")
    c.show(f"#{p}-b", t)
    c.tl.ft(f"#{p}-b", {"opacity": 0}, {"opacity": 1, "duration": 0.6}, t)
    for k in range(3):
        c.blur_in(f"#{p}-z-{k}", t + 0.6 + 0.3 * k, 0.25)
    popl(c, f"#{p}-fl", S(c, "21", "Let the night"), snd="pop")
    t = S(c, "21", "The next morning")
    c.show(f"#{p}-c", t)
    c.sfx("whoosh", t)
    c.tl.ft(f"#{p}-win", {"y": 40}, {"y": 0, "duration": 0.5, "ease": "back.out(2)"}, t + 0.1)
    idle(c, f"{p}-win", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 22 · End card
def s22():
    c = comp("22")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', char("s22-boy", "vui", 1600, 1010, 720)]
    lines = [("big", "Sleep isn't wasted time.<br>It's the night shift."),
             ("lab", "Key sources"),
             ("src", "Yoo et al., <i>Nat Neurosci</i> (2007) · Rasch & Born, <i>Physiol Rev</i> (2013) · Prather et al., <i>Sleep</i> (2015)"),
             ("src", "Xie et al., <i>Science</i> (2013) · Van Dongen et al., <i>Sleep</i> (2003) · Watson et al., <i>Sleep</i> (2015)"),
             ("src", "Inspired by Matthew Walker's <i>Why We Sleep</i>; figures from the original studies. Full list in the description."),
             ("safe", "For general education only, not medical advice.<br>Ongoing insomnia, loud snoring or daytime sleepiness? See a doctor.")]
    c.css.append(f"#s22-card {{ left: 130px; top: 110px; width: 1250px; color: {INK}; }}"
                 "#s22-card .big { font-size: 74px; font-weight: 800; line-height: 1.12; letter-spacing: -0.01em; margin-bottom: 48px; }"
                 "#s22-card .lab { font-size: 34px; font-weight: 800; color: #B5372A; margin-bottom: 10px; }"
                 "#s22-card .src { font-size: 30px; font-weight: 500; line-height: 1.45; color: #2A3A4A; }"
                 "#s22-card .safe { font-size: 34px; font-weight: 700; margin-top: 44px; line-height: 1.35; }")
    c.html.append('<div id="s22-card" class="txt" data-hold="true">'
                  + "".join(f'<div id="s22-l{k}" class="{cls}">{tx}</div>' for k, (cls, tx) in enumerate(lines)) + "</div>")
    for k in range(len(lines)):
        c.blur_in(f"#s22-l{k}", 0.2 + 0.12 * k, 0.2)
    c.tl.ft("#s22-boy", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "expo.out"}, 0.3)
    idle(c, "s22-boy", 1.0, end_of(c, "22"), 2)
    return c


BUILDERS = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22]


def music():
    lifts = [(0, SCENES["01"]["end"]), (SCENES["08"]["start"], SCENES["08"]["end"]), (SCENES["22"]["start"], DURATION + 1)]
    plan = [(0, SCENES["03"]["start"], ["piz"]), (SCENES["03"]["start"], SCENES["09"]["start"], ["doc", "mar"]),
            (SCENES["09"]["start"], SCENES["19"]["start"], ["lofi", "kal", "doc", "mar"]), (SCENES["19"]["start"], DURATION, ["piz"])]
    return music_plan(plan, lifts)()


if __name__ == "__main__":
    run(BUILDERS, music)
