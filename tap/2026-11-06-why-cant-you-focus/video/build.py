"""Why can't you focus on reading this? — dựng HyperFrames từ audio/timeline.json + audio/words.json.
Chạy:  py build.py      (trong thư mục video\\)
Bộ dựng chung: scripts\\hf\\minh_hoa.py (nhân vật PNG, bảng, nhạc, phụ đề) + ve3.py (điện thoại, đèn rọi, sách…).
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
# Văn phòng (assets/bg/van-phong.jpg): đồng hồ, laptop; nhân vật đứng bên phải
CLOCK, LAPTOP = (878, 132), (500, 632)
OFF_CX, OFF_FEET, OFF_H = 1500, 1050, 780


def end_of(c, sid):
    return c.loc(SCENES[sid]["end"])


def fade_seq(c, sels, t, dur=0.25):
    for s in sels:
        c.blur_out(s, t, dur)


def note(id_, x, y, s, size=28):
    return text(x, min(y, 948), s, size, 600, GREY, "middle", id_=id_)


def has(scene, prefix):
    return any(s["scene"] == scene and s["text"].startswith(prefix) for s in WORDS["sentences"])


# ---------------------------------------------------------------- 01 · Title
def s01():
    c = comp("01")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', spotlight("s01-sp", 1250, 120, 1250, 900, 420),
              char("s01-boy", "dien-thoai", 1600, 1010, 760)]
    words = ["Why", "can't", "you", "<br>", "focus", "on", "<br>", "reading", "this?"]
    spans = "".join("<br>" if w == "<br>" else
                    f'<span id="s01-w{k}" class="w{" hot" if w in ("focus", "this?") else ""}">{w}</span> ' for k, w in enumerate(words))
    c.css.append(f"#s01-title {{ left: 130px; top: 230px; font-size: 130px; font-weight: 800; line-height: 1.08; color: {INK}; "
                 f"letter-spacing: -0.01em; }} #s01-title .hot {{ color: #C9781E; }} #s01-title .w {{ display: inline-block; }}")
    c.html.append(f'<div id="s01-title" class="txt">{spans}</div>')
    c.tl.ft("#s01-sp", {"opacity": 0, "rotation": -12, "svgOrigin": "1250 120"},
            {"opacity": 1, "rotation": 8, "svgOrigin": "1250 120", "duration": 2.5, "ease": "sine.inOut"}, 0.1)
    c.tl.ft("#s01-boy", {"y": 80, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "back.out(1.6)"}, 0.4)
    for k, w in enumerate(words):
        if w != "<br>":
            c.blur_in(f"#s01-w{k}", 0.25 + 0.08 * k, 0.15)
    c.tl.ft("#s01-title", {"x": -4}, {"x": 4, "duration": 0.08, "yoyo": True, "repeat": 9, "ease": "none"}, 2.0)
    return c


# ---------------------------------------------------------------- 02 · Opening story (office)
def s02():
    c = comp("02")
    p = c.cid
    poses = ["doc-sach", "dien-thoai", "suy-nghi", "dau-dau", "ngac-nhien"]
    hx, hy = OFF_CX, OFF_FEET - OFF_H * 0.8
    over = (chip(f"{p}-t2", CLOCK[0] + 60, 300, "2:00 PM · READ BEFORE MEETING", 44)
            + chip(f"{p}-12", LAPTOP[0] + 40, 470, "12 PAGES", 56)
            + phone(f"{p}-ph", hx - 260, hy + 260, 0.9) + notif(f"{p}-nt", hx - 280, hy + 60, "SHOE SALE −20%", 400)
            + "".join(text(hx + 160 + k * 70, hy - 40 - k * 30, "?", 110, 900, YELLOW, id_=f"{p}-q{k}", extra=" " + OUTLINE) for k in range(3))
            + chip(f"{p}-x3", hx, hy - 150, "SAME PARAGRAPH ×3", 48, CORAL, WHITE)
            + bubble(f"{p}-din", hx - 330, hy - 60, 360, 120, "DINNER?", PAPER, INK, 60)
            + chip(f"{p}-tab", LAPTOP[0], 470, "+1 TAB", 56)
            + chip(f"{p}-t240", CLOCK[0] + 60, 300, "2:40 PM · PAGE 2", 48, CORAL, WHITE))
    cam, st = scene_comp(c, "van-phong", poses, OFF_CX, OFF_FEET, OFF_H, over)
    c.svg.append(label(f"{p}-broken", 960, 540, "IS MY BRAIN BROKEN?", 120, YELLOW, "middle"))
    c.svg.insert(-1, f'<rect id="{p}-dim" width="1920" height="1080" fill="{INK}" opacity="0"/>')
    hid = [f"#{p}-{x}" for x in ("t2", "12", "ph", "nt", "x3", "din", "tab", "t240", "broken")]
    c.hide(*hid, *[f"#{p}-q{k}" for k in range(3)])
    T = lambda pre: S(c, "02", pre)
    end = end_of(c, "02")
    frame(c, 0, 960, 540, 1.0, cam, st)
    popl(c, f"#{p}-t2", 0.3)
    idle(c, f"{p}-doc-sach", 0, T("You read the first"), 0)
    t = T("Just twelve")
    c.show(f"#{p}-t2", t, False)
    frame(c, t, LAPTOP[0] + 80, LAPTOP[1] - 120, 1.8, cam, st)
    popl(c, f"#{p}-12", t + 0.2, snd="thump")
    t = T("You read the first")
    c.show(f"#{p}-12", t, False)
    frame(c, t, hx - 80, hy + 120, 1.6, cam, st)
    t2 = c.at("02", "your phone buzzes")
    c.pop(f"#{p}-ph", t2, 0.4)
    # rung ngang (không dùng rotation + svgOrigin bên trong nhóm camera: làm lệch cả khung)
    c.tl.ft(f"#{p}-ph", {"x": -8}, {"x": 8, "duration": 0.06, "yoyo": True, "repeat": 11, "ease": "none"}, t2)
    c.sfx("pop", t2)
    t = T("It's nothing")
    show_pose(c, poses, "dien-thoai", t)
    c.show(f"#{p}-ph", t, False)
    popl(c, f"#{p}-nt", t + 0.1)
    t = T("You go back")
    c.show(f"#{p}-nt", t, False)
    show_pose(c, poses, "suy-nghi", t)
    for k in range(3):
        c.pop(f"#{p}-q{k}", t + 0.4 + 0.3 * k, 0.4)
    t = T("You read the same")
    for k in range(3):
        c.show(f"#{p}-q{k}", t, False)
    show_pose(c, poses, "doc-sach", t)
    popl(c, f"#{p}-x3", t + 0.2, snd="thump")
    t = T("Your eyes reach")
    c.show(f"#{p}-x3", t, False)
    c.pop(f"#{p}-din", c.at("02", "thinking about dinner"), 0.5, "100% 100%")
    c.sfx("pop", c.at("02", "thinking about dinner"))
    t = T("You open a new")
    c.show(f"#{p}-din", t, False)
    frame(c, t, LAPTOP[0] + 60, LAPTOP[1] - 120, 2.0, cam, st)
    popl(c, f"#{p}-tab", t + 0.2)
    t = T("Forty minutes")
    c.show(f"#{p}-tab", t, False)
    frame(c, t, 1150, 540, 1.2, cam, st)
    show_pose(c, poses, "dau-dau", t)
    popl(c, f"#{p}-t240", t + 0.2, snd="thump")
    t = T("You scroll back")
    c.show(f"#{p}-t240", t, False)
    frame(c, t, hx, hy + 80, 1.9, cam, st)
    show_pose(c, poses, "ngac-nhien", t)
    t = T("Is something")
    frame(c, t, 960, 540, 1.0, cam, st)
    c.tl.to(f"#{p}-dim", {"opacity": 0.6, "duration": 0.4}, t)
    popl(c, f"#{p}-broken", t + 0.2, snd="thump")
    return c


# ---------------------------------------------------------------- 03 · The goldfish claim
def s03():
    c = comp("03")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [fishbowl(f"{p}-bowl", 1000, 500, 1.2),
              label(f"{p}-h", 1490, 420, "HUMANS: 8 SECONDS?", 50, WHITE, "middle"),
              label(f"{p}-g", 1490, 520, "GOLDFISH: 9 SECONDS?", 50, "#FF9F43", "middle"),
              label(f"{p}-ev", 1270, 220, "NEWS · TALKS · ADS", 56, GREY, "middle"),
              stamp(f"{p}-ns", 1270, 760, "NO STUDY BEHIND IT", CORAL, 760, 56),
              label(f"{p}-bbc", 1270, 880, "BBC, 2017: THE SOURCE HAD NO SUCH RESEARCH", 40, WHITE, "middle"),
              label(f"{p}-fm", 1270, 770, "GOLDFISH ATTENTION SPAN: NEVER MEASURED", 46, YELLOW, "middle"),
              label(f"{p}-q", 1270, 540, "SO WHAT'S GOING ON?", 110, YELLOW, "middle")]
    close()
    end = end_of(c, "03")
    c.hide(f"#{p}-bowl", f"#{p}-h", f"#{p}-g", f"#{p}-ev", f"#{p}-ns", f"#{p}-bbc", f"#{p}-fm", f"#{p}-q")
    t = S(c, "03", "You may")
    c.pop(f"#{p}-bowl", t, 0.5)
    c.tl.ft(f"#{p}-bowl-fish", {"x": -40}, {"x": 40, "duration": 1.2, "yoyo": True, "repeat": 7, "ease": "sine.inOut"}, t)
    c.sfx("pop", t)
    t = S(c, "03", "Humans now")
    popl(c, f"#{p}-h", t)
    popl(c, f"#{p}-g", c.at("03", "shorter than a goldfish"), snd="thump")
    popl(c, f"#{p}-ev", S(c, "03", "It's been"))
    t = S(c, "03", "But when BBC")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    c.show(f"#{p}-ns", t + 0.2)
    c.tl.ft(f"#{p}-ns", {"scale": 1.6, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "power4.in"}, t + 0.2)
    c.sfx("thump", t + 0.5)
    c.blur_in(f"#{p}-bbc", S(c, "03", "The report"))
    t = S(c, "03", "And nobody")
    c.blur_out(f"#{p}-ns", t - 0.2, 0.2)
    popl(c, f"#{p}-fm", t)
    t = S(c, "03", "So if it's")
    fade_seq(c, [f"#{p}-bowl", f"#{p}-h", f"#{p}-g", f"#{p}-ev", f"#{p}-bbc", f"#{p}-fm"], t - 0.25)
    popl(c, f"#{p}-q", t, snd="thump")
    swap(c, f"{p}-ngac-nhien", f"{p}-suy-nghi", t)
    idle(c, f"{p}-suy-nghi", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 04 · Clue one: the wandering mind
def s04():
    c = comp("04")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [label(f"{p}-c1", 1270, 150, "CLUE 1 · THE WANDERING MIND", 60, YELLOW, "middle"),
              phone(f"{p}-ph", 820, 470, 1.3, buzz=False), bubble(f"{p}-ask", 1230, 320, 660, 110, "WHAT ARE YOU THINKING?", PAPER, INK, 40),
              donut(f"{p}-dn", 1500, 560, 150, 0.47), label(f"{p}-47", 1500, 580, "47%", 76, CORAL, "middle"),
              label(f"{p}-47b", 1500, 800, "THINKING ABOUT SOMETHING ELSE", 40, WHITE, "middle"),
              note(f"{p}-s1", 1500, 860, "Killingsworth & Gilbert, Science, 2010 · 2,250 people"),
              page(f"{p}-pg", 900, 560, 1.3), f'<circle id="{p}-eye" cx="760" cy="420" r="16" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>',
              bubble(f"{p}-th", 1450, 330, 420, 110, "…DINNER?", PAPER, INK, 50),
              label(f"{p}-15", 1500, 560, "≈ 1 IN 5 CHECK-INS: OFF TASK", 46, CORAL, "middle"),
              label(f"{p}-ap", 1500, 660, "EYES ON AUTOPILOT", 52, YELLOW, "middle"),
              label(f"{p}-lt", 1500, 760, "MORE ZONING OUT → LESS UNDERSTOOD", 40, WHITE, "middle"),
              note(f"{p}-s2", 1500, 830, "Schooler 2004 · Smallwood 2008 · Reichle 2010")]
    close()
    end = end_of(c, "04")
    grp1 = [f"#{p}-ph", f"#{p}-ask", f"#{p}-dn", f"#{p}-47", f"#{p}-47b", f"#{p}-s1"]
    grp2 = [f"#{p}-pg", f"#{p}-eye", f"#{p}-th", f"#{p}-15", f"#{p}-ap", f"#{p}-lt", f"#{p}-s2"]
    c.hide(f"#{p}-c1", *grp1, *grp2)
    popl(c, f"#{p}-c1", S(c, "04", "Let's collect"))
    t = S(c, "04", "Clue one")
    c.pop(f"#{p}-ph", t + 0.3, 0.4)
    c.pop(f"#{p}-ask", c.at("04", "asked what they were thinking"), 0.45, "0% 100%")
    c.sfx("pop", c.at("04", "asked what they were thinking"))
    t = S(c, "04", "Nearly half")
    c.show(f"#{p}-dn", t)
    c.tl.to(f"#{p}-dn-arc", {"strokeDashoffset": 0, "duration": 1.2, "ease": "power2.out"}, t + 0.1)
    popl(c, f"#{p}-47", c.at("04", "forty-seven") if False else t + 0.6, snd="thump")
    c.blur_in(f"#{p}-47b", t + 1.0)
    c.blur_in(f"#{p}-s1", t + 1.2)
    t = S(c, "04", "Reading is")
    fade_seq(c, grp1, t - 0.25)
    c.pop(f"#{p}-pg", t, 0.5)
    t = S(c, "04", "When researchers")
    c.pop(f"#{p}-th", t + 0.3, 0.45, "0% 100%")
    popl(c, f"#{p}-15", c.at("04", "one in five"), snd="thump")
    t = S(c, "04", "And here's")
    c.show(f"#{p}-eye", t)
    for k in range(6):
        y = 420 + k * 44
        c.tl.ft(f"#{p}-eye", {"x": 0, "y": k * 44}, {"x": 300, "y": k * 44, "duration": 0.55, "ease": "none"}, t + 0.3 + 0.6 * k)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", S(c, "04", "Your eyes are"))
    popl(c, f"#{p}-ap", S(c, "04", "Your eyes even"))
    popl(c, f"#{p}-lt", S(c, "04", "And readers"), snd="pop")
    c.blur_in(f"#{p}-s2", S(c, "04", "And readers") + 0.4)
    idle(c, f"{p}-ngac-nhien", S(c, "04", "Your eyes are") + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 05 · Clue two: the buzz
def s05():
    c = comp("05")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    scr = (f'<rect x="700" y="260" width="460" height="300" rx="20" fill="#CFE8F7" stroke="{INK}" stroke-width="6"/>'
           f'<rect x="900" y="560" width="60" height="60" fill="{GREY}"/><rect x="820" y="616" width="220" height="20" rx="8" fill="{GREY}"/>'
           + "".join(f'<circle cx="{780 + (k % 5) * 75}" cy="{330 + (k // 5) * 80}" r="18" fill="{TEAL if k != 7 else CORAL}"/>' for k in range(15)))
    c.svg += [label(f"{p}-c2", 1270, 150, "CLUE 2 · THE BUZZ", 60, YELLOW, "middle"), g(f"{p}-scr", scr),
              phone(f"{p}-ph", 1350, 520, 1.0), label(f"{p}-nt", 1350, 700, "DIDN'T ANSWER · DIDN'T TOUCH", 40, WHITE, "middle"),
              g(f"{p}-bars", f'<rect x="1500" y="{880 - 110}" width="140" height="110" rx="12" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + f'<rect id="{p}-b2" x="1690" y="{880 - 300}" width="140" height="300" rx="12" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                + text(1570, 925, "NO BUZZ", 30, 800, WHITE, "middle") + text(1760, 925, "BUZZ", 30, 800, WHITE, "middle")),
              label(f"{p}-err", 1660, 520, "MORE MISTAKES", 52, CORAL, "middle"),
              label(f"{p}-same", 1050, 800, "≈ AS BAD AS USING THE PHONE", 48, YELLOW, "middle"),
              note(f"{p}-src", 1050, 870, "Stothart et al., J Exp Psychol HPP, 2015")]
    close()
    end = end_of(c, "05")
    c.hide(f"#{p}-c2", f"#{p}-scr", f"#{p}-ph", f"#{p}-nt", f"#{p}-bars", f"#{p}-err", f"#{p}-same", f"#{p}-src")
    t = S(c, "05", "Clue two")
    popl(c, f"#{p}-c2", t)
    c.pop(f"#{p}-scr", t + 0.4, 0.5)
    t = S(c, "05", "Some of them")
    c.pop(f"#{p}-ph", t, 0.4)
    c.tl.ft(f"#{p}-ph", {"rotation": -6, "svgOrigin": "1350 520"}, {"rotation": 6, "svgOrigin": "1350 520", "duration": 0.06,
                                                                  "yoyo": True, "repeat": 15}, t + 0.3)
    c.sfx("pop", t + 0.3)
    popl(c, f"#{p}-nt", S(c, "05", "They didn't"), snd=None)
    t = S(c, "05", "Yet they")
    c.pop(f"#{p}-bars", t, 0.4, "50% 100%")
    c.tl.ft(f"#{p}-b2", {"scaleY": 0.37, "transformOrigin": "50% 100%"}, {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.9,
                                                                            "ease": "power2.out"}, t + 0.3)
    popl(c, f"#{p}-err", c.at("05", "more mistakes"), snd="thump")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", c.at("05", "more mistakes"))
    popl(c, f"#{p}-same", c.at("05", "about as many"), snd=None)
    c.blur_in(f"#{p}-src", c.at("05", "about as many", off=0.3))
    idle(c, f"{p}-ngac-nhien", c.at("05", "more mistakes", off=0.6), end, 1)
    return c


# ---------------------------------------------------------------- 06 · Clue three: the switch
def s06():
    c = comp("06")
    p = c.cid
    close = board(c, ("suy-nghi", "dau-dau"))
    arrows = (f'<path id="{p}-ar1" d="M960 400 C1060 330 1180 330 1280 400" fill="none" stroke="{YELLOW}" stroke-width="10" stroke-linecap="round" '
              f'pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>'
              f'<path id="{p}-ar2" d="M1280 560 C1180 630 1060 630 960 560" fill="none" stroke="{YELLOW}" stroke-width="10" stroke-linecap="round" '
              f'pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')
    c.svg += [label(f"{p}-c3", 1270, 150, "CLUE 3 · THE SWITCH", 60, YELLOW, "middle"),
              task_card(f"{p}-A", 840, 480, "A", TEAL), task_card(f"{p}-B", 1400, 480, "B", YELLOW), arrows,
              hourglass(f"{p}-hg", 1120, 480, 0.8), label(f"{p}-sc", 1120, 720, "SWITCH COST", 52, WHITE, "middle"),
              label(f"{p}-cx", 1120, 800, "BIGGER FOR COMPLEX TASKS", 42, CORAL, "middle"),
              f'<g id="{p}-gh" opacity=".35">{task_card(f"{p}-Ag", 1640, 330, "A", TEAL, 160, 110)}</g>',
              label(f"{p}-res", 1580, 760, "ATTENTION RESIDUE", 56, YELLOW, "middle"),
              note(f"{p}-src", 1270, 880, "Rubinstein, Meyer & Evans 2001 · Leroy 2009")]
    close()
    end = end_of(c, "06")
    c.hide(f"#{p}-c3", f"#{p}-A", f"#{p}-B", f"#{p}-hg", f"#{p}-sc", f"#{p}-cx", f"#{p}-gh", f"#{p}-res", f"#{p}-src")
    t = S(c, "06", "Clue three")
    popl(c, f"#{p}-c3", t)
    c.pop(f"#{p}-A", t + 0.4, 0.4)
    c.pop(f"#{p}-B", c.at("06", "to another"), 0.4)
    c.draw(f"#{p}-ar1", c.at("06", "to another", off=0.2), 0.5)
    c.pop(f"#{p}-hg", c.at("06", "small time cost"), 0.45)
    c.tl.ft(f"#{p}-hg", {"rotation": 0, "svgOrigin": "1120 480"}, {"rotation": 180, "svgOrigin": "1120 480", "duration": 0.6, "ease": "power2.inOut"},
            c.at("06", "small time cost", off=0.5))
    popl(c, f"#{p}-sc", c.at("06", "small time cost"), snd="pop")
    popl(c, f"#{p}-cx", S(c, "06", "The more complex"), snd=None)
    t = S(c, "06", "And when you switch")
    c.draw(f"#{p}-ar2", t, 0.5)
    fade_seq(c, [f"#{p}-hg", f"#{p}-sc", f"#{p}-cx"], t - 0.2)
    c.tl.to(f"#{p}-A", {"opacity": 0.3, "duration": 0.4}, t + 0.3)
    c.pop(f"#{p}-gh", t + 0.6, 0.5)
    swap(c, f"{p}-suy-nghi", f"{p}-dau-dau", t + 0.6)
    popl(c, f"#{p}-res", S(c, "06", "Researchers call"), snd="thump")
    c.blur_in(f"#{p}-src", S(c, "06", "Researchers call") + 0.4)
    idle(c, f"{p}-dau-dau", t + 1.2, end, 2)
    return c


# ---------------------------------------------------------------- 07 · Clue four: paper or screen
def s07():
    c = comp("07")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [label(f"{p}-c4", 1270, 150, "CLUE 4 · PAPER OR SCREEN?", 60, YELLOW, "middle"),
              book(f"{p}-bk", 880, 380, 0.9), tablet(f"{p}-tb", 1640, 380, 0.75),
              g(f"{p}-bars", f'<rect x="830" y="{820 - 220}" width="100" height="220" rx="12" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + f'<rect id="{p}-b2" x="1590" y="{820 - 190}" width="100" height="190" rx="12" fill="{WATER}" stroke="{INK}" stroke-width="6"/>'
                + text(880, 870, "PAPER", 32, 800, WHITE, "middle") + text(1640, 870, "SCREEN", 32, 800, WHITE, "middle")),
              label(f"{p}-edge", 1260, 560, "SMALL EDGE FOR PAPER", 50, TEAL, "middle"),
              label(f"{p}-rush", 1260, 640, "BIGGER WHEN RUSHED", 46, CORAL, "middle"),
              label(f"{p}-oc", 1260, 760, "SCREEN READERS: OVERCONFIDENT", 46, YELLOW, "middle"),
              note(f"{p}-src", 1260, 930, "Delgado et al., Educational Research Review, 2018 · meta-analysis")]
    close()
    end = end_of(c, "07")
    c.hide(f"#{p}-c4", f"#{p}-bk", f"#{p}-tb", f"#{p}-bars", f"#{p}-edge", f"#{p}-rush", f"#{p}-oc", f"#{p}-src")
    t = S(c, "07", "Clue four")
    popl(c, f"#{p}-c4", t)
    c.pop(f"#{p}-bk", c.at("07", "on paper"), 0.45)
    c.pop(f"#{p}-tb", c.at("07", "on screens"), 0.45)
    c.sfx("pop", c.at("07", "on screens"))
    c.blur_in(f"#{p}-src", t + 1.0)
    t = S(c, "07", "On average")
    c.pop(f"#{p}-bars", t, 0.4, "50% 100%")
    popl(c, f"#{p}-edge", c.at("07", "a little better"), snd="thump")
    t = S(c, "07", "The gap")
    popl(c, f"#{p}-rush", t)
    c.tl.to(f"#{p}-b2", {"scaleY": 0.8, "transformOrigin": "50% 100%", "duration": 0.6}, t + 0.3)
    t = S(c, "07", "And people reading")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-oc", c.at("07", "overestimate"), snd="pop")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


def opt_row(prefix, x, y, letter, icon, lab):
    return g(prefix, f"""<rect id="{prefix}-box" x="{x - 30}" y="{y - 86}" width="1170" height="172" rx="28" fill="none" stroke="{YELLOW}" stroke-width="8" opacity="0"/>
{text(x + 50, y + 44, letter, 128, 900, YELLOW, "middle")}
<g transform="translate({x + 270} {y})">{icon}</g>
{text(x + 430, y + 16, lab, 40, 800, WHITE)}
<line id="{prefix}-strike" x1="{x - 20}" y1="{y}" x2="{x + 1130}" y2="{y}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>""")


def options(prefix, x=690):
    return (opt_row(f"{prefix}a", x, 300, "A", fishbowl(f"{prefix}-fb", 0, 0, 0.42), "SPAN SHORTER THAN A GOLDFISH")
            + opt_row(f"{prefix}b", x, 530, "B", phone(f"{prefix}-ph", 0, 0, 0.7, buzz=False, screen=CORAL), "PHONE BROKE YOUR BRAIN")
            + opt_row(f"{prefix}c", x, 760, "C", spotlight(f"{prefix}-sp", -60, -60, 30, 50, 120), "A SPOTLIGHT, PULLED AWAY"))


# ---------------------------------------------------------------- 08 · The question
def s08():
    c = comp("08")
    p = c.cid
    close = board(c)
    c.svg += [options(f"{p}-o"), label(f"{p}-q", 1270, 560, "WHY CAN'T YOU FOCUS?", 96, WHITE, "middle")]
    close()
    idle(c, f"{p}-suy-nghi", 0, end_of(c, "08"), 2)
    c.hide(f"#{p}-q")
    popl(c, f"#{p}-q", S(c, "08", "So why"))
    c.blur_out(f"#{p}-q", S(c, "08", "A:") - 0.3, 0.25)
    for L, pre in (("a", "A:"), ("b", "B:"), ("c", "Or C:")):
        t = S(c, "08", pre)
        c.hide(f"#{p}-o{L}")
        c.tl.ft(f"#{p}-o{L}", {"autoAlpha": 0, "x": 60, "filter": "blur(8px)"},
                {"autoAlpha": 1, "x": 0, "filter": "blur(0px)", "duration": 0.45, "ease": "expo.out"}, t)
        c.sfx("pop", t)
    return c


# ---------------------------------------------------------------- 09 · Take a guess
def s09():
    c = comp("09")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>',
              f'<circle cx="1590" cy="560" r="220" fill="#C9781E" stroke="{INK}" stroke-width="10"/>',
              text(1590, 300, "PAUSE THE VIDEO", 44, 900, INK, "middle"),
              g("s09-n", "".join(text(1590, 660, str(n), 300, 900, WHITE, "middle", id_=f"s09-n{n}") for n in (3, 2, 1)))]
    lines = [("h", "Take a guess first!"),
             ("f", "1. Minds drift ~half the time; readers' eyes keep moving anyway."),
             ("f", "2. Just a buzz, untouched, means more mistakes."),
             ("f", "3. Every switch costs time and leaves residue."),
             ("f", "4. Screens: slightly worse understanding, more overconfidence."),
             ("o", "A. Attention span shorter than a goldfish"), ("o", "B. The phone broke your brain for good"),
             ("o", "C. A spotlight that keeps getting pulled away")]
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
    c.svg += [g(f"{p}-tk", tank(f"{p}-tank", 760, 300, 200, 360, YELLOW, "ATTENTION TANK", 0.4)
                + f'<line id="{p}-x" x1="720" y1="280" x2="1000" y2="700" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" '
                  f'stroke="{CORAL}" stroke-width="18" stroke-linecap="round"/>'),
              spotlight(f"{p}-sp", 1500, 200, 1380, 640, 360), label(f"{p}-sl", 1450, 800, "A SPOTLIGHT YOU KEEP AIMING", 50, YELLOW, "middle"),
              label(f"{p}-rd", 1270, 900, "WHAT DOES READING NEED?", 52, WHITE, "middle")]
    close()
    end = end_of(c, "10")
    c.hide(f"#{p}-tk", f"#{p}-sp", f"#{p}-sl", f"#{p}-rd")
    t = S(c, "10", "The key")
    c.pop(f"#{p}-tk", t, 0.5, "50% 100%")
    c.draw(f"#{p}-x", c.at("10", "runs empty", off=0.1), 0.4)
    c.sfx("thump", c.at("10", "runs empty", off=0.3))
    t = S(c, "10", "It's more like")
    c.tl.ft(f"#{p}-sp", {"autoAlpha": 0, "rotation": -20, "svgOrigin": "1500 200"},
            {"autoAlpha": 1, "rotation": 0, "svgOrigin": "1500 200", "duration": 0.6, "ease": "back.out(1.4)"}, t)
    c.hide(f"#{p}-sp")
    c.tl.to(f"#{p}-sp", {"rotation": 14, "svgOrigin": "1500 200", "duration": 0.5, "yoyo": True, "repeat": 3, "ease": "sine.inOut"},
            c.at("10", "pulled off target"))
    popl(c, f"#{p}-sl", t + 0.4, snd="pop")
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    popl(c, f"#{p}-rd", S(c, "10", "To see why"))
    idle(c, f"{p}-vui", t + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 11 · Reading is a chain
def s11():
    c = comp("11")
    p = c.cid
    close = board(c, ("suy-nghi", "dau-dau"))
    c.svg += [label(f"{p}-t", 1270, 150, "READING = A CHAIN OF IDEAS", 60, YELLOW, "middle"),
              link_chain(f"{p}-ch", 780, 430, ["IDEA 1", "IDEA 2", "IDEA 3", "IDEA 4"], 330),
              label(f"{p}-mm", 1270, 600, "YOUR MENTAL MODEL OF THE TEXT", 46, TEAL, "middle"),
              label(f"{p}-fr", 1270, 690, "FRAGILE", 70, CORAL, "middle"),
              f'<path id="{p}-back" d="M1440 520 C1300 640 1000 640 840 520" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round" '
              f'pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" marker-end=""/>',
              label(f"{p}-rr", 1270, 820, "→ READ IT AGAIN (×3)", 60, YELLOW, "middle"),
              note(f"{p}-src", 1270, 900, "Kintsch, Comprehension, 1998")]
    close()
    end = end_of(c, "11")
    boxes = [f"#{p}-ch-b{k}" for k in range(4)]
    links = [f"#{p}-ch-l{k}" for k in range(3)]
    c.hide(f"#{p}-t", f"#{p}-mm", f"#{p}-fr", f"#{p}-rr", f"#{p}-src", *boxes, *links)
    popl(c, f"#{p}-t", S(c, "11", "Reading isn't"))
    t = S(c, "11", "To understand")
    for k in range(4):
        c.pop(boxes[k], t + 0.5 * k, 0.4)
        if k < 3:
            c.pop(links[k], t + 0.5 * k + 0.3, 0.3)
    c.sfx("pop", t)
    popl(c, f"#{p}-mm", S(c, "11", "It builds"), snd=None)
    c.blur_in(f"#{p}-src", S(c, "11", "It builds") + 0.4)
    popl(c, f"#{p}-fr", S(c, "11", "That chain"), snd="thump")
    t = S(c, "11", "If your spotlight")
    c.tl.to(links[1], {"y": 80, "rotation": 25, "opacity": 0, "transformOrigin": "50% 50%", "duration": 0.6, "ease": "power2.in"}, t + 0.6)
    c.sfx("whoosh", t + 0.6)
    swap(c, f"{p}-suy-nghi", f"{p}-dau-dau", t + 0.6)
    t = S(c, "11", "Then the next")
    c.tl.to(boxes[2], {"opacity": 0.3, "duration": 0.3}, t)
    c.tl.to(boxes[3], {"opacity": 0.3, "duration": 0.3}, t)
    c.draw(f"#{p}-back", c.at("11", "go back"), 0.5)
    popl(c, f"#{p}-rr", S(c, "11", "That's why"), snd="thump")
    idle(c, f"{p}-dau-dau", t, end, 1)
    return c


# ---------------------------------------------------------------- 12 · Pull one: your own mind
def s12():
    c = comp("12")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [label(f"{p}-t", 1270, 150, "PULL 1 · YOUR OWN MIND", 60, YELLOW, "middle"),
              brain(f"{p}-br", 960, 460, 1.6),
              g(f"{p}-dmn", "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="{YELLOW}" opacity=".85"/>' for x, y in ((900, 400), (1010, 470), (960, 520)))),
              label(f"{p}-dl", 960, 680, "DEFAULT MODE NETWORK", 48, YELLOW, "middle"),
              label(f"{p}-mp", 1500, 380, "MEMORIES · PLANS · DAYDREAMS", 36, WHITE, "middle"),
              label(f"{p}-nd", 1560, 470, "NOT A DEFECT", 54, TEAL, "middle"),
              label(f"{p}-st", 1560, 570, "…BUT IT STEALS THE THREAD", 44, CORAL, "middle"),
              label(f"{p}-nn", 1270, 780, "OFTEN UNNOTICED — UNTIL A PAGE LATER", 48, WHITE, "middle"),
              label(f"{p}-hb", 1270, 870, "HARDER OR DULLER TEXT → MORE DRIFT", 48, YELLOW, "middle"),
              note(f"{p}-src", 960, 740, "Mason et al., Science, 2007 · Feng et al., 2013")]
    close()
    end = end_of(c, "12")
    c.hide(f"#{p}-t", f"#{p}-br", f"#{p}-dmn", f"#{p}-dl", f"#{p}-mp", f"#{p}-nd", f"#{p}-st", f"#{p}-nn", f"#{p}-hb", f"#{p}-src")
    t = S(c, "12", "The first thing")
    popl(c, f"#{p}-t", t)
    c.pop(f"#{p}-br", t + 0.3, 0.5)
    t = S(c, "12", "When your attention")
    c.show(f"#{p}-dmn", t + 0.3)
    c.tl.ft(f"#{p}-dmn", {"opacity": 0.3}, {"opacity": 1, "duration": 0.5, "yoyo": True, "repeat": 5}, t + 0.3)
    popl(c, f"#{p}-dl", c.at("12", "default mode network"), snd="pop")
    c.blur_in(f"#{p}-src", c.at("12", "default mode network", off=0.4))
    popl(c, f"#{p}-mp", S(c, "12", "It's busy"), snd=None)
    popl(c, f"#{p}-nd", S(c, "12", "Mind wandering isn't"), snd="pop")
    popl(c, f"#{p}-st", S(c, "12", "But while"), snd="thump")
    t = S(c, "12", "And often")
    fade_seq(c, [f"#{p}-dl", f"#{p}-src"], t - 0.2)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-nn", t, snd=None)
    popl(c, f"#{p}-hb", S(c, "12", "The harder"), snd="pop")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 13 · Pull two: cues
def s13():
    c = comp("13")
    p = c.cid
    close = board(c, ("suy-nghi", "dien-thoai", "ngac-nhien"))
    c.svg += [label(f"{p}-t", 1270, 150, "PULL 2 · CUES", 60, YELLOW, "middle"),
              phone(f"{p}-ph", 900, 460, 1.4), spotlight(f"{p}-sp", 1500, 220, 1500, 620, 300),
              bubble(f"{p}-who", 1450, 360, 400, 110, "WHO WAS IT?", PAPER, INK, 48),
              g(f"{p}-wk", f'<rect x="760" y="{820 - 300}" width="200" height="300" rx="14" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                + f'<rect x="1040" y="{820 - 170}" width="200" height="170" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + text(860, 870, "ALERTS ON", 32, 800, WHITE, "middle") + text(1140, 870, "ALERTS OFF", 32, 800, WHITE, "middle")),
              label(f"{p}-mi", 1560, 560, "MORE INATTENTION", 54, CORAL, "middle"),
              note(f"{p}-s1", 1560, 620, "Kushlev et al., CHI 2016 · 221 students"),
              phone(f"{p}-sil", 820, 470, 1.4, buzz=False),
              label(f"{p}-dr", 1360, 380, "2017: \"MERE PRESENCE DRAINS YOU\"", 40, WHITE, "middle"),
              stamp(f"{p}-nr", 1360, 560, "DIDN'T REPLICATE", CORAL, 620, 52),
              note(f"{p}-s2", 1360, 670, "Ruiz Pardo & Minda, Acta Psychologica, 2022"),
              label(f"{p}-bz", 1270, 830, "THE EVIDENCE IS AGAINST THE BUZZ", 54, YELLOW, "middle")]
    close()
    end = end_of(c, "13")
    g1 = [f"#{p}-ph", f"#{p}-sp", f"#{p}-who"]
    g2 = [f"#{p}-wk", f"#{p}-mi", f"#{p}-s1"]
    g3 = [f"#{p}-sil", f"#{p}-dr", f"#{p}-nr", f"#{p}-s2", f"#{p}-bz"]
    c.hide(f"#{p}-t", *g1, *g2, *g3)
    t = S(c, "13", "The second pull")
    popl(c, f"#{p}-t", t)
    c.pop(f"#{p}-ph", t + 0.3, 0.4)
    t = S(c, "13", "A buzz")
    c.tl.ft(f"#{p}-ph", {"rotation": -6, "svgOrigin": "900 460"}, {"rotation": 6, "svgOrigin": "900 460", "duration": 0.06, "yoyo": True, "repeat": 13}, t)
    c.sfx("pop", t)
    c.show(f"#{p}-sp", t + 0.2)
    c.tl.ft(f"#{p}-sp", {"rotation": 0, "svgOrigin": "1500 220"}, {"rotation": 35, "svgOrigin": "1500 220", "duration": 0.8, "ease": "power3.inOut"},
            c.at("13", "it works"))
    t = S(c, "13", "Even if")
    swap(c, f"{p}-suy-nghi", f"{p}-dien-thoai", t)
    c.pop(f"#{p}-who", t + 0.3, 0.45, "0% 100%")
    t = S(c, "13", "In one experiment")
    fade_seq(c, g1, t - 0.25)
    c.pop(f"#{p}-wk", t, 0.5, "50% 100%")
    c.blur_in(f"#{p}-s1", t + 0.4)
    popl(c, f"#{p}-mi", S(c, "13", "With alerts on"), snd="thump")
    t = S(c, "13", "What about")
    fade_seq(c, g2, t - 0.25)
    swap(c, f"{p}-dien-thoai", f"{p}-suy-nghi", t)
    c.pop(f"#{p}-sil", t, 0.45)
    popl(c, f"#{p}-dr", S(c, "13", "A 2017") if has("13", "A 2017") else S(c, "13", "A "), snd=None)
    t = S(c, "13", "But later")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    c.show(f"#{p}-nr", t + 0.2)
    c.tl.ft(f"#{p}-nr", {"scale": 1.6, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "power4.in"}, t + 0.2)
    c.sfx("thump", t + 0.5)
    c.blur_in(f"#{p}-s2", t + 0.6)
    popl(c, f"#{p}-bz", S(c, "13", "So it's"), snd="pop")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 14 · Pull three: switching
def s14():
    c = comp("14")
    p = c.cid
    close = board(c, ("suy-nghi", "dau-dau"))
    c.svg += [label(f"{p}-t", 1270, 150, "PULL 3 · SWITCHING", 60, YELLOW, "middle"),
              g(f"{p}-br", browser_tabs(f"{p}-bt", 720, 290, 8)),
              label(f"{p}-1s", 1270, 620, "FEELS LIKE 1 SECOND", 48, WHITE, "middle"),
              label(f"{p}-rl", 1270, 700, "COMING BACK = RELOAD THE CHAIN", 46, CORAL, "middle"),
              f'<g id="{p}-gh" opacity=".4">{notif(f"{p}-em", 1270, 420, "UNFINISHED EMAIL…", 480)}</g>',
              label(f"{p}-20", 1270, 860, "×20 SWITCHES = 40 MINUTES GONE", 56, YELLOW, "middle")]
    close()
    end = end_of(c, "14")
    tabs = [f"#{p}-bt-t{k}" for k in range(8)]
    c.hide(f"#{p}-t", f"#{p}-br", f"#{p}-1s", f"#{p}-rl", f"#{p}-gh", f"#{p}-20", *tabs)
    t = S(c, "14", "The third pull")
    popl(c, f"#{p}-t", t)
    c.show(f"#{p}-br", t + 0.3)
    c.pop(tabs[0], t + 0.3, 0.3)
    t = S(c, "14", "Opening a new")
    c.pop(tabs[1], t, 0.3, "50% 100%")
    popl(c, f"#{p}-1s", c.at("14", "one second"), snd="pop")
    popl(c, f"#{p}-rl", S(c, "14", "But coming"), snd="thump")
    t = S(c, "14", "Part of your")
    c.pop(f"#{p}-gh", t, 0.45)
    swap(c, f"{p}-suy-nghi", f"{p}-dau-dau", t)
    t = S(c, "14", "Do that")
    for k in range(2, 8):
        c.pop(tabs[k], t + 0.15 * (k - 2), 0.25, "50% 100%")
    c.sfx("pop", t)
    popl(c, f"#{p}-20", c.at("14", "forty minutes"), snd="thump")
    idle(c, f"{p}-dau-dau", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 15 · Pull four: screens
def s15():
    c = comp("15")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [label(f"{p}-t", 1270, 150, "PULL 4 · THE SCREEN ITSELF?", 60, YELLOW, "middle"),
              tablet(f"{p}-tb", 900, 520, 1.0),
              f'<path id="{p}-sw" d="M840 640 C900 560 960 480 990 380" fill="none" stroke="{YELLOW}" stroke-width="12" stroke-linecap="round" '
              f'pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>',
              label(f"{p}-fd", 1500, 340, "MESSAGES · FEEDS · HEADLINES", 40, WHITE, "middle"),
              label(f"{p}-sk", 1500, 450, "SKIM MODE?", 76, YELLOW, "middle"),
              label(f"{p}-fc", 1500, 560, "READ FASTER, CHECK LESS", 46, CORAL, "middle"),
              label(f"{p}-ov", 1500, 650, "→ OVERCONFIDENCE?", 46, WHITE, "middle"),
              stamp(f"{p}-st", 1270, 830, "AN IDEA STILL BEING TESTED", YELLOW, 820, 48, -3)]
    close()
    end = end_of(c, "15")
    c.hide(f"#{p}-t", f"#{p}-tb", f"#{p}-fd", f"#{p}-sk", f"#{p}-fc", f"#{p}-ov", f"#{p}-st")
    t = S(c, "15", "The fourth")
    popl(c, f"#{p}-t", t)
    c.pop(f"#{p}-tb", t + 0.3, 0.5)
    t = S(c, "15", "We do a lot")
    c.draw(f"#{p}-sw", t, 0.5)
    c.tl.ft(f"#{p}-sw", {"strokeDashoffset": 0}, {"strokeDashoffset": -1.1, "duration": 0.5, "repeat": 3, "ease": "none"}, t + 0.6)
    popl(c, f"#{p}-fd", t + 0.2, snd="whoosh")
    popl(c, f"#{p}-sk", S(c, "15", "One idea"), snd="pop")
    popl(c, f"#{p}-fc", S(c, "15", "We read faster"), snd=None)
    t = S(c, "15", "That could")
    popl(c, f"#{p}-ov", t, snd=None)
    t = S(c, "15", "But this")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    c.show(f"#{p}-st", t)
    c.tl.ft(f"#{p}-st", {"scale": 1.5, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "power4.in"}, t)
    c.sfx("thump", t + 0.3)
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 16 · Long stretches
def s16():
    c = comp("16")
    p = c.cid
    close = board(c, ("ngap", "vui"))
    X0, Y0, W, H = 740, 300, 1000, 420
    drop = (f'<path id="{p}-dp" d="M{X0} {Y0 + 60} C{X0 + 300} {Y0 + 80} {X0 + 600} {Y0 + 220} {X0 + W} {Y0 + 330}" fill="none" stroke="{CORAL}" '
            f'stroke-width="12" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')
    flat = (f'<path id="{p}-fl" d="M{X0} {Y0 + 60} L{X0 + 330} {Y0 + 70} L{X0 + 340} {Y0 + 50} L{X0 + 660} {Y0 + 66} L{X0 + 670} {Y0 + 52} L{X0 + W} {Y0 + 66}" '
            f'fill="none" stroke="{TEAL}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>')
    brk = "".join(f'<g id="{p}-bk{k}"><line x1="{X0 + x}" y1="{Y0 - 10}" x2="{X0 + x}" y2="{Y0 + H}" stroke="{YELLOW}" stroke-width="6" stroke-dasharray="14 10"/>'
                  + text(X0 + x, Y0 - 24, "BREAK", 30, 900, YELLOW, "middle") + "</g>" for k, x in enumerate((335, 665)))
    c.svg += [label(f"{p}-t", 1270, 150, "LONG STRETCHES", 60, YELLOW, "middle"),
              g(f"{p}-ax", f'<path d="M{X0} {Y0} V{Y0 + H} H{X0 + W}" fill="none" stroke="{GREY}" stroke-width="6"/>'
                + text(X0 + W / 2, Y0 + H + 56, "50 MINUTES ON ONE TASK", 34, 800, GREY, "middle")
                + text(X0 - 20, Y0 + 20, "SCORE", 30, 800, GREY, "end")),
              drop, flat, brk,
              text(X0 + W - 10, Y0 + 390, "NO BREAKS", 34, 900, CORAL, "end", id_=f"{p}-dl"),
              text(X0 + W - 10, Y0 + 30, "2 TINY BREAKS", 34, 900, TEAL, "end", id_=f"{p}-fll"),
              note(f"{p}-src", 1270, 880, "Ariga & Lleras, Cognition, 2011 · small study"),
              label(f"{p}-tip", 1270, 840, "STEP AWAY ON PURPOSE → COME BACK SHARPER", 46, YELLOW, "middle")]
    close()
    end = end_of(c, "16")
    c.hide(f"#{p}-t", f"#{p}-ax", f"#{p}-dl", f"#{p}-fll", f"#{p}-src", f"#{p}-tip", f"#{p}-bk0", f"#{p}-bk1")
    popl(c, f"#{p}-t", S(c, "16", "There's one"))
    t = S(c, "16", "When people")
    c.blur_in(f"#{p}-ax", t, 0.3)
    c.draw(f"#{p}-dp", t + 0.3, 2.0, "power1.in")
    c.blur_in(f"#{p}-dl", t + 2.0)
    t = S(c, "16", "In a small")
    c.blur_in(f"#{p}-src", t + 0.3)
    c.pop(f"#{p}-bk0", t + 0.6, 0.4)
    c.pop(f"#{p}-bk1", t + 0.9, 0.4)
    c.draw(f"#{p}-fl", c.at("16", "didn't show"), 1.6)
    c.blur_in(f"#{p}-fll", c.at("16", "didn't show", off=1.0))
    t = S(c, "16", "So stepping")
    c.blur_out(f"#{p}-src", t - 0.2, 0.2)
    swap(c, f"{p}-ngap", f"{p}-vui", t)
    popl(c, f"#{p}-tip", t + 0.2, snd="pop")
    idle(c, f"{p}-ngap", 0, t, 0)
    idle(c, f"{p}-vui", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 17 · Is multitasking rewiring you?
def s17():
    c = comp("17")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    screens = "".join(tablet(f"{p}-s{k}", 1010 + k * 170, 400 - (k % 2) * 40, 0.45) for k in range(4))
    bars = [(900, 380, "2009"), (1080, 170, "LATER"), (1260, 120, "LATER"), (1440, 90, "POOLED")]
    c.svg += [label(f"{p}-t", 1270, 150, "IS MULTITASKING REWIRING YOU?", 58, YELLOW, "middle"),
              g(f"{p}-scr", screens),
              label(f"{p}-09", 1270, 640, "2009: WORSE AT IGNORING DISTRACTIONS", 44, WHITE, "middle"),
              label(f"{p}-hl", 1270, 740, "HEADLINES!", 60, CORAL, "middle"),
              g(f"{p}-ch", "".join(f'<g id="{p}-b{k}"><rect x="{x - 60}" y="{820 - h}" width="120" height="{h}" rx="12" fill="{CORAL if k == 0 else WATER}" '
                                   f'stroke="{INK}" stroke-width="6"/>' + text(x, 870, lb, 30, 800, WHITE, "middle") + "</g>" for k, (x, h, lb) in enumerate(bars))),
              label(f"{p}-mx", 1640, 520, "MIXED RESULTS", 50, YELLOW, "middle"),
              label(f"{p}-sm", 1640, 610, "SMALL LINK · STILL UNCLEAR", 44, TEAL, "middle"),
              note(f"{p}-src", 1270, 930, "Ophir et al., PNAS, 2009 · Wiradhany & Nieuwenstein, 2017"),
              label(f"{p}-no", 1270, 300, "NO PROOF OF A REWIRED BRAIN", 56, WHITE, "middle")]
    close()
    end = end_of(c, "17")
    c.hide(f"#{p}-t", f"#{p}-scr", f"#{p}-09", f"#{p}-hl", f"#{p}-ch", f"#{p}-mx", f"#{p}-sm", f"#{p}-src", f"#{p}-no",
           *[f"#{p}-b{k}" for k in range(4)])
    t = S(c, "17", "What about")
    popl(c, f"#{p}-t", t)
    c.pop(f"#{p}-scr", t + 0.3, 0.5)
    t = S(c, "17", "A well-known") if has("17", "A well-known") else S(c, "17", "A ")
    popl(c, f"#{p}-09", t)
    popl(c, f"#{p}-hl", S(c, "17", "It made"), snd="thump")
    t = S(c, "17", "But when")
    fade_seq(c, [f"#{p}-scr", f"#{p}-09", f"#{p}-hl"], t - 0.25)
    c.show(f"#{p}-ch", t)
    c.pop(f"#{p}-b0", t, 0.4, "50% 100%")
    c.pop(f"#{p}-b1", t + 0.6, 0.4, "50% 100%")
    c.pop(f"#{p}-b2", t + 1.0, 0.4, "50% 100%")
    popl(c, f"#{p}-mx", c.at("17", "mixed"), snd="pop")
    t = S(c, "17", "Pooling")
    c.pop(f"#{p}-b3", t, 0.4, "50% 100%")
    popl(c, f"#{p}-sm", c.at("17", "small"), snd=None)
    c.blur_in(f"#{p}-src", t + 0.4)
    t = S(c, "17", "So we")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-no", t, snd="thump")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 18 · Can you train it?
def s18():
    c = comp("18")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [label(f"{p}-t", 1270, 150, "CAN YOU TRAIN YOUR SPOTLIGHT?", 60, YELLOW, "middle"),
              label(f"{p}-n", 1270, 250, "48 STUDENTS · 2 WEEKS", 48, WHITE, "middle"),
              g(f"{p}-mf", f'<rect x="720" y="320" width="480" height="300" rx="24" fill="#1D4262" stroke="{TEAL}" stroke-width="6"/>'
                + text(960, 400, "MINDFULNESS", 48, 900, TEAL, "middle") + text(960, 470, "NOTICE THE DRIFT", 34, 800, WHITE, "middle")
                + text(960, 520, "→ COME BACK", 34, 800, WHITE, "middle")),
              g(f"{p}-nu", f'<rect x="1340" y="320" width="480" height="300" rx="24" fill="#1D4262" stroke="{GREY}" stroke-width="6"/>'
                + text(1580, 400, "NUTRITION", 48, 900, GREY, "middle") + text(1580, 470, "COMPARISON CLASS", 34, 800, WHITE, "middle")),
              label(f"{p}-r1", 960, 700, "LESS MIND WANDERING ↓", 44, TEAL, "middle"),
              label(f"{p}-r2", 960, 780, "BETTER READING SCORES ↑", 44, TEAL, "middle"),
              note(f"{p}-src", 1270, 880, "Mrazek et al., Psychological Science, 2013 · small study"),
              label(f"{p}-sk", 1580, 740, "A SKILL YOU CAN PRACTICE", 46, YELLOW, "middle")]
    close()
    end = end_of(c, "18")
    c.hide(f"#{p}-t", f"#{p}-n", f"#{p}-mf", f"#{p}-nu", f"#{p}-r1", f"#{p}-r2", f"#{p}-src", f"#{p}-sk")
    popl(c, f"#{p}-t", S(c, "18", "Can you"))
    t = S(c, "18", "In a 2013") if has("18", "In a 2013") else S(c, "18", "In a")
    popl(c, f"#{p}-n", t, snd=None)
    c.blur_in(f"#{p}-src", t + 0.5)
    c.pop(f"#{p}-mf", S(c, "18", "Half learned"), 0.5)
    c.sfx("pop", S(c, "18", "Half learned"))
    c.pop(f"#{p}-nu", S(c, "18", "The other half"), 0.5)
    t = S(c, "18", "Afterward")
    popl(c, f"#{p}-r1", t + 0.2)
    popl(c, f"#{p}-r2", c.at("18", "scored higher"), snd="thump")
    swap(c, f"{p}-suy-nghi", f"{p}-vui", c.at("18", "scored higher"))
    popl(c, f"#{p}-sk", S(c, "18", "It was a small"), snd=None)
    idle(c, f"{p}-vui", c.at("18", "scored higher", off=0.6), end, 0)
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
    c.draw(f"#{p}-oa-strike", S(c, "19", "The eight"), 0.4)
    c.tl.to(f"#{p}-oa", {"opacity": 0.4, "duration": 0.3}, S(c, "19", "The eight") + 0.4)
    c.draw(f"#{p}-ob-strike", S(c, "19", "And there's"), 0.4)
    c.tl.to(f"#{p}-ob", {"opacity": 0.4, "duration": 0.3}, S(c, "19", "And there's") + 0.4)
    c.sfx("pop", S(c, "19", "And there's"))
    t = S(c, "19", "Your attention")
    c.tl.to([f"#{p}-oa", f"#{p}-ob"], {"opacity": 0, "duration": 0.3}, t - 0.3)
    c.tl.to(f"#{p}-oc", {"y": -230, "duration": 0.6, "ease": "power2.inOut"}, t)
    c.sfx("whoosh", t)
    idle(c, f"{p}-suy-nghi", 0, S(c, "19", "The answer"), 1)
    idle(c, f"{p}-vui", S(c, "19", "The answer") + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 20 · How to hold the spotlight
def s20():
    c = comp("20")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    tips = [("NOTIFICATIONS OFF · PHONE AWAY", "Turn off"), ("ONE TAB · ONE TASK", "Keep one tab"),
            ("IMPORTANT TEXT? PAPER + TIME", "For text"), ("DRIFTED? BACK ONE SENTENCE", "When you notice"),
            ("SHORT, PLANNED BREAKS", "And take")]
    c.svg += [label(f"{p}-t", 1270, 560, "YOU CAN HOLD IT LONGER", 100, YELLOW, "middle"),
              label(f"{p}-hd", 1270, 220, "HOLD THE SPOTLIGHT", 84, YELLOW, "middle"),
              "".join(label(f"{p}-tp{k}", 760, 380 + k * 110, f"{k + 1}. {s}", 52, WHITE) for k, (s, _) in enumerate(tips))]
    close()
    end = end_of(c, "20")
    c.hide(f"#{p}-t", f"#{p}-hd", *[f"#{p}-tp{k}" for k in range(5)])
    t0 = S(c, "20", "The good news")
    popl(c, f"#{p}-t", t0)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t0)
    t = S(c, "20", tips[0][1])
    c.blur_out(f"#{p}-t", t - 0.25, 0.2)
    popl(c, f"#{p}-hd", t - 0.1, snd=None)
    for k, (_, pre) in enumerate(tips):
        tt = S(c, "20", pre)
        c.tl.ft(f"#{p}-tp{k}", {"autoAlpha": 0, "x": 60}, {"autoAlpha": 1, "x": 0, "duration": 0.4, "ease": "expo.out"}, tt)
        c.sfx("pop", tt)
    idle(c, f"{p}-vui", t0 + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 21 · Back to the article
def s21():
    c = comp("21")
    p = c.cid
    poses = ["doc-sach", "vui"]
    over = (chip(f"{p}-dw", LAPTOP[0] + 40, 470, "PHONE: SILENT, IN THE DRAWER", 40)
            + chip(f"{p}-25", CLOCK[0] + 60, 300, "25 MIN READ · 2 MIN STRETCH", 44)
            + chip(f"{p}-3", CLOCK[0] + 60, 300, "3:00 PM · PAGE 12 ✓", 52, TEAL, INK))
    cam, st = scene_comp(c, "van-phong", poses, OFF_CX, OFF_FEET, OFF_H, over)
    c.svg.append(chip(f"{p}-rw", 960, 160, "↺ REWIND 10 SECONDS", 60, YELLOW, INK))
    c.hide(f"#{p}-dw", f"#{p}-25", f"#{p}-3", f"#{p}-rw")
    T = lambda pre: S(c, "21", pre)
    end = end_of(c, "21")
    frame(c, 0, 960, 540, 1.0, cam, st)
    idle(c, f"{p}-doc-sach", 0, T("By three"), 0)
    t = T("Phone on silent")
    frame(c, t, LAPTOP[0] + 80, LAPTOP[1] - 120, 1.7, cam, st)
    popl(c, f"#{p}-dw", t + 0.1)
    t = T("Twenty-five") if has("21", "Twenty-five") else T("Twenty")
    c.show(f"#{p}-dw", t, False)
    frame(c, t, 1100, 520, 1.2, cam, st)
    popl(c, f"#{p}-25", t + 0.1)
    t = T("By three")
    c.show(f"#{p}-25", t, False)
    show_pose(c, poses, "vui", t)
    popl(c, f"#{p}-3", t + 0.2, snd="thump")
    t = T("And if your")
    c.show(f"#{p}-3", t, False)
    frame(c, t, 960, 540, 1.0, cam, st)
    popl(c, f"#{p}-rw", t + 0.2)
    c.tl.ft(f"#{p}-rw", {"rotation": 0, "svgOrigin": "960 160"}, {"rotation": -4, "svgOrigin": "960 160", "duration": 0.3, "yoyo": True, "repeat": 5},
            t + 0.8)
    idle(c, f"{p}-vui", t, end, 2)
    return c


# ---------------------------------------------------------------- 22 · End card
def s22():
    c = comp("22")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', char("s22-boy", "doc-sach", 1600, 1010, 720)]
    lines = [("big", "Your attention isn't broken.<br>It's being pulled."),
             ("lab", "Key sources"),
             ("src", "Killingsworth & Gilbert, <i>Science</i> (2010) · Stothart et al., <i>JEP:HPP</i> (2015) · Delgado et al., <i>Educ Res Rev</i> (2018)"),
             ("src", "Kushlev et al., CHI (2016) · Ruiz Pardo & Minda (2022) · Mrazek et al., <i>Psychol Sci</i> (2013) · BBC (2017)"),
             ("src", "Full list in the description."),
             ("safe", "For general education only, not medical advice.<br>Focus problems that hurt school, work or daily life? Talk to a doctor.")]
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
    lifts = [(0, SCENES["01"]["end"]), (SCENES["09"]["start"], SCENES["09"]["end"]), (SCENES["22"]["start"], DURATION + 1)]
    plan = [(0, SCENES["03"]["start"], ["piz"]), (SCENES["03"]["start"], SCENES["10"]["start"], ["doc", "mar"]),
            (SCENES["10"]["start"], SCENES["19"]["start"], ["lofi", "kal", "doc", "mar"]), (SCENES["19"]["start"], DURATION, ["piz"])]
    return music_plan(plan, lifts)()


if __name__ == "__main__":
    run(BUILDERS, music)
