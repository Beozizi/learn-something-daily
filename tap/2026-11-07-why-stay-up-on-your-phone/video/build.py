"""Why do you stay up late on your phone even when you're exhausted? — dựng HyperFrames từ audio/timeline.json + audio/words.json.
Chạy:  py build.py      (trong thư mục video\\)
Bộ dựng chung: scripts\\hf\\minh_hoa.py (nhân vật PNG, bảng, nhạc, phụ đề) + ve3.py (điện thoại, dòng tin, bàn đạp…).
"""
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from hf import core  # noqa: E402

core.init(__file__)
from hf.core import *  # noqa: E402,F401,F403
from hf.core import SCENES, WORDS, DURATION  # noqa: E402,F401
from hf.minh_hoa import *  # noqa: E402,F401,F403
from hf.ve2 import bubble, gauge, lamp, person_icon  # noqa: E402,F401
from hf.ve3 import *  # noqa: E402,F401,F403

BLUE = "#4FB3E8"
NAVY = "#1D4262"
# Phòng ngủ (assets/bg/phong-ngu.jpg): đồng hồ tường, đồng hồ báo thức, giường, cửa sổ; nhân vật đứng giữa phòng
R_CLOCK, R_ALARM, R_BED, R_WINDOW = (239, 118), (1265, 485), (1620, 560), (930, 260)
R_CX, R_FEET, R_H = 1080, 1062, 760


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


# ---------------------------------------------------------------- 01 · Title
def s01():
    c = comp("01")
    c.svg += [f'<rect width="1920" height="1080" fill="{NAVY}"/>',
              f'<ellipse id="s01-glow" cx="1600" cy="560" rx="420" ry="360" fill="{BLUE}" opacity=".0"/>',
              moon("s01-moon", 1760, 150, 0.8), char("s01-boy", "dien-thoai", 1600, 1010, 760)]
    words = ["Why", "do", "you", "stay", "up", "<br>", "late", "on", "your", "phone?"]
    spans = "".join("<br>" if w == "<br>" else
                    f'<span id="s01-w{k}" class="w{" hot" if w in ("late", "phone?") else ""}">{w}</span> ' for k, w in enumerate(words))
    c.css.append(f"#s01-title {{ left: 130px; top: 300px; font-size: 128px; font-weight: 800; line-height: 1.08; color: {WHITE}; "
                 f"letter-spacing: -0.01em; }} #s01-title .hot {{ color: {YELLOW}; }} #s01-title .w {{ display: inline-block; }}")
    c.html.append(f'<div id="s01-title" class="txt">{spans}</div>')
    c.tl.to("#s01-glow", {"opacity": 0.35, "duration": 1.2, "ease": "sine.inOut"}, 0.3)
    c.tl.ft("#s01-boy", {"y": 80, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.6, "ease": "back.out(1.6)"}, 0.4)
    for k, w in enumerate(words):
        if w != "<br>":
            c.blur_in(f"#s01-w{k}", 0.25 + 0.08 * k, 0.15)
    return c


# ---------------------------------------------------------------- 02 · Opening story (bedroom)
def s02():
    c = comp("02")
    p = c.cid
    poses = ["ngap", "dien-thoai", "dau-dau", "suy-nghi"]
    hx, hy = R_CX, R_FEET - R_H * 0.8
    dim = f'<rect id="{p}-night" width="1920" height="1080" fill="#0B1A3A" opacity=".25"/>'
    over = (dim + chip(f"{p}-t11", R_CLOCK[0] + 200, 300, "11:00 PM", 56)
            + chip(f"{p}-al", R_ALARM[0], R_ALARM[1] - 120, "ALARM 7:00", 48, CORAL, WHITE)
            + chip(f"{p}-one", hx - 330, hy + 40, "JUST ONE THING", 44)
            + notif(f"{p}-n1", hx - 340, hy + 170, "▶ NEXT VIDEO", 360)
            + notif(f"{p}-n2", hx - 340, hy + 270, "💬 NEW MESSAGE", 360)
            + chip(f"{p}-more", hx + 300, hy - 60, "JUST ONE MORE…", 48)
            + chip(f"{p}-t140", R_CLOCK[0] + 200, 300, "1:40 AM", 64, CORAL, WHITE))
    cam, st = scene_comp(c, "phong-ngu", poses, R_CX, R_FEET, R_H, over)
    c.svg.append(g(f"{p}-cls", f'<image href="assets/bg/lop-hoc-bang.jpg" width="1920" height="1080"/>'
                   + char(f"{p}-ex", "ngap", 1500, 1050, 780) + chip(f"{p}-nx", 600, 300, "NEXT DAY · 9:00 AM", 60)))
    c.svg.append(f'<rect id="{p}-dim" width="1920" height="1080" fill="{INK}" opacity="0"/>')
    c.svg.append(label(f"{p}-why", 960, 540, "WHY CAN'T I PUT IT DOWN?", 104, YELLOW, "middle"))
    c.svg.append(label(f"{p}-meh", 960, 300, "NOT EVEN THAT FUN", 80, WHITE, "middle"))
    hid = [f"#{p}-{x}" for x in ("t11", "al", "one", "n1", "n2", "more", "t140", "cls", "why", "meh")]
    c.hide(*hid)
    t_ = lambda pre: S(c, "02", pre)
    end = end_of(c, "02")
    frame(c, 0, 960, 540, 1.0, cam, st)
    popl(c, f"#{p}-t11", 0.3)
    idle(c, f"{p}-ngap", 0, t_("So you pick"), 0)
    t = t_("Your alarm")
    c.show(f"#{p}-t11", t, False)
    frame(c, t, R_ALARM[0], R_ALARM[1] - 40, 2.2, cam, st)
    popl(c, f"#{p}-al", t + 0.2, snd="thump")
    t = t_("So you pick")
    c.show(f"#{p}-al", t, False)
    frame(c, t, hx - 120, hy + 140, 1.5, cam, st)
    show_pose(c, poses, "dien-thoai", t)
    popl(c, f"#{p}-one", t + 0.2)
    t = t_("One video")
    c.show(f"#{p}-one", t, False)
    popl(c, f"#{p}-n1", t + 0.1)
    popl(c, f"#{p}-n2", c.at("02", "a message"))
    t = t_("Your eyes are")
    fade_seq(c, [f"#{p}-n1", f"#{p}-n2"], t - 0.2)
    frame(c, t, hx + 60, hy + 60, 1.8, cam, st)
    popl(c, f"#{p}-more", c.at("02", "just one more"))
    idle(c, f"{p}-dien-thoai", t_("So you pick"), t_("You look up"), 1)
    t = t_("You look up")
    c.show(f"#{p}-more", t, False)
    frame(c, t, R_CLOCK[0] + 120, R_CLOCK[1] + 140, 2.0, cam, st)
    c.tl.to(f"#{p}-night", {"opacity": 0.5, "duration": 0.6}, t)
    show_pose(c, poses, "dau-dau", t)
    popl(c, f"#{p}-t140", t + 0.3, snd="thump")
    t = t_("The next day")
    c.show(f"#{p}-t140", t, False)
    c.show(f"#{p}-cls", t)
    c.sfx("whoosh", t)
    popl(c, f"#{p}-nx", t + 0.2)
    idle(c, f"{p}-ex", t, t_("And that night"), 2)
    t = t_("And that night")
    c.show(f"#{p}-cls", t, False)
    c.sfx("whoosh", t)
    frame(c, t, 960, 540, 1.0, cam, st)
    show_pose(c, poses, "dien-thoai", t)
    c.show(f"#{p}-t11", t + 0.2)
    t = t_("You're not even")
    c.show(f"#{p}-t11", t, False)
    show_pose(c, poses, "suy-nghi", t)
    popl(c, f"#{p}-meh", t + 0.1)
    t = t_("So why can't")
    c.blur_out(f"#{p}-meh", t - 0.2, 0.2)
    c.tl.to(f"#{p}-dim", {"opacity": 0.6, "duration": 0.4}, t)
    popl(c, f"#{p}-why", t + 0.2, snd="thump")
    return c


# ---------------------------------------------------------------- 03 · Not a rare problem
def s03():
    c = comp("03")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    people = "".join(person_icon(f"{p}-pp{k}", 820 + k * 150, 400, 2.4, [WHITE, YELLOW, TEAL, PINK, BLUE, WHITE, CORAL][k]) for k in range(7))
    c.svg += [g(f"{p}-ppl", people),
              label(f"{p}-ya", 1270, 560, "YOU'RE NOT ALONE", 70, WHITE, "middle"),
              label(f"{p}-yr", 1270, 230, "2014 · UTRECHT, NETHERLANDS", 44, GREY, "middle"),
              label(f"{p}-gv", 1270, 480, "THEY GAVE IT A NAME…", 84, WHITE, "middle"),
              label(f"{p}-nm", 1270, 360, "BEDTIME", 120, YELLOW, "middle"),
              label(f"{p}-nm2", 1270, 490, "PROCRASTINATION", 104, YELLOW, "middle"),
              label(f"{p}-df", 1270, 640, "LATER THAN YOU PLANNED · NOTHING STOPPING YOU", 40, WHITE, "middle"),
              label(f"{p}-no", 1270, 760, "NO BABY · NO DEADLINE", 52, CORAL, "middle"),
              note(f"{p}-src", 1270, 900, "Kroese et al., Frontiers in Psychology, 2014")]
    close()
    end = end_of(c, "03")
    els = ["ppl", "ya", "yr", "gv", "nm", "nm2", "df", "no", "src"]
    c.hide(*[f"#{p}-{x}" for x in els])
    t = T(c, "03", "If this")
    c.pop(f"#{p}-ppl", t, 0.5)
    c.sfx("pop", t)
    popl(c, f"#{p}-ya", c.at("03", "alone"), snd=None)
    t = T(c, "03", "In twenty", "In 20", "In ")
    fade_seq(c, [f"#{p}-ppl", f"#{p}-ya"], t + 0.3)
    c.blur_in(f"#{p}-yr", t)
    c.blur_in(f"#{p}-src", t + 0.3)
    popl(c, f"#{p}-gv", t + 0.6, snd="pop")
    t = T(c, "03", "Bedtime")
    c.blur_out(f"#{p}-gv", t - 0.2, 0.2)
    popl(c, f"#{p}-nm", t, snd="thump")
    popl(c, f"#{p}-nm2", t + 0.35, snd=None)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-df", T(c, "03", "It means"), snd=None)
    popl(c, f"#{p}-no", T(c, "03", "No baby"), snd="pop")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 04 · Clue one: not about sleep
def s04():
    c = comp("04")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [clue(f"{p}-c1", "CLUE 1 · NOT ABOUT SLEEP"),
              bubble(f"{p}-q", 1270, 300, 1060, 130, "“I WANT TO GO TO BED ON TIME, BUT I JUST DON'T.”", PAPER, INK, 36),
              bars(f"{p}-r", [(900, 300, CORAL, "TOO LITTLE SLEEP"), (1270, 230, YELLOW, "TIRED NEXT DAY")], 760, 200),
              label(f"{p}-lk", 1640, 600, "LINKED", 64, WHITE, "middle"),
              label(f"{p}-sl", 1640, 690, "(SURVEYS)", 36, GREY, "middle"),
              note(f"{p}-src", 1270, 900, "Kroese et al., 2014 · 177 adults · correlations, not proof of cause"),
              label(f"{p}-ns", 1270, 470, "NOT “I DON'T WANT TO SLEEP”", 64, TEAL, "middle"),
              label(f"{p}-st", 1270, 640, "“I CAN'T STOP WHAT I'M DOING”", 64, YELLOW, "middle")]
    close()
    end = end_of(c, "04")
    g1 = [f"#{p}-r", f"#{p}-lk", f"#{p}-sl"]
    c.hide(f"#{p}-c1", f"#{p}-q", *g1, f"#{p}-src", f"#{p}-ns", f"#{p}-st")
    popl(c, f"#{p}-c1", T(c, "04", "Let's collect"))
    t = T(c, "04", "Clue one")
    c.pop(f"#{p}-q", c.at("04", "simple sentence", off=0.2), 0.5, "25% 100%")
    c.sfx("pop", c.at("04", "simple sentence", off=0.2))
    t = T(c, "04", "In surveys")
    c.pop(f"#{p}-r", t, 0.5, "50% 100%")
    popl(c, f"#{p}-lk", c.at("04", "linked"), snd="thump")
    c.blur_in(f"#{p}-sl", c.at("04", "linked", off=0.3))
    c.blur_in(f"#{p}-src", t + 0.6)
    t = T(c, "04", "But the researchers")
    fade_seq(c, g1, t - 0.25)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-ns", T(c, "04", "People weren't"), snd="pop")
    popl(c, f"#{p}-st", T(c, "04", "They seemed"), snd="thump")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 05 · Clue two: three kinds of late
def s05():
    c = comp("05")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))

    def kind(k, x, title, icon, col):
        return g(f"{p}-k{k}", f'<rect x="{x - 170}" y="300" width="340" height="420" rx="26" fill="{NAVY}" stroke="{col}" stroke-width="7"/>'
                 + f'<g transform="translate({x} 450)">{icon}</g>' + text(x, 660, title, 30, 900, col, "middle"))

    c.svg += [clue(f"{p}-c2", "CLUE 2 · THREE KINDS OF LATE"),
              label(f"{p}-17", 1270, 240, "17 INTERVIEWS", 46, WHITE, "middle"),
              kind(0, 880, "ON PURPOSE", text(0, 40, "ME", 110, 900, YELLOW, "middle"), YELLOW),
              kind(1, 1270, "LOST TRACK", clock("x", 0, 0, 90, 1, 40), TEAL),
              kind(2, 1660, "WAITING FOR SLEEP", zzz(f"{p}-z", -40, 40, 1.4, PINK), PINK),
              label(f"{p}-own", 880, 790, "“MY TIME”", 40, WHITE, "middle"),
              note(f"{p}-src", 1270, 900, "Nauts et al., Behavioral Sleep Medicine, 2019 · small qualitative study")]
    close()
    end = end_of(c, "05")
    c.hide(f"#{p}-c2", f"#{p}-17", f"#{p}-k0", f"#{p}-k1", f"#{p}-k2", f"#{p}-own", f"#{p}-src")
    t = T(c, "05", "Clue two")
    popl(c, f"#{p}-c2", t)
    popl(c, f"#{p}-17", c.at("05", "seventeen"), snd=None)
    c.blur_in(f"#{p}-src", t + 0.8)
    t = T(c, "05", "Some stayed")
    c.pop(f"#{p}-k0", t, 0.5)
    c.sfx("pop", t)
    popl(c, f"#{p}-own", T(c, "05", "Evening"), snd=None)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", T(c, "05", "Evening"))
    t = T(c, "05", "Some simply")
    c.pop(f"#{p}-k1", t, 0.5)
    c.sfx("pop", t)
    t = T(c, "05", "And a few")
    c.pop(f"#{p}-k2", t, 0.5)
    c.sfx("pop", t)
    idle(c, f"{p}-vui", T(c, "05", "Evening") + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 06 · Clue three: night mode
def s06():
    c = comp("06")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [clue(f"{p}-c3", "CLUE 3 · THE COLOR OF THE SCREEN"),
              phone(f"{p}-pb", 900, 420, 1.3, buzz=False, screen="#CFE8F7"), phone(f"{p}-pw", 1120, 420, 1.3, buzz=False, screen="#FFD08A"),
              label(f"{p}-nm", 1010, 640, "NIGHT MODE: WARMER, LESS BLUE", 40, YELLOW, "middle"),
              label(f"{p}-167", 1560, 360, "167 YOUNG ADULTS", 50, WHITE, "middle"),
              label(f"{p}-7n", 1560, 440, "18–24 · 7 NIGHTS", 40, GREY, "middle"),
              bars(f"{p}-br", [(870, 400, TEAL, "NO PHONE"), (1270, 406, "#FFB070", "NIGHT MODE"), (1670, 404, BLUE, "PHONE")], 800, 220),
              label(f"{p}-wr", 1270, 330, "SLEEP TRACKED ON THE WRIST", 44, WHITE, "middle"),
              label(f"{p}-same", 1270, 330, "ABOUT THE SAME", 76, YELLOW, "middle"),
              note(f"{p}-src", 1270, 900, "Duraccio et al., Sleep Health, 2021 · randomized trial")]
    close()
    end = end_of(c, "06")
    g1 = [f"#{p}-pb", f"#{p}-pw", f"#{p}-nm", f"#{p}-167", f"#{p}-7n", f"#{p}-wr"]
    bs = [f"#{p}-br-b{k}" for k in range(3)]
    c.hide(f"#{p}-c3", *g1, f"#{p}-br", f"#{p}-same", f"#{p}-src", *bs)
    t = T(c, "06", "Clue three")
    popl(c, f"#{p}-c3", t)
    c.pop(f"#{p}-pb", t + 0.3, 0.4)
    c.pop(f"#{p}-pw", c.at("06", "warmer"), 0.4)
    c.sfx("pop", c.at("06", "warmer"))
    popl(c, f"#{p}-nm", c.at("06", "less blue"), snd=None)
    t = T(c, "06", "In twenty", "In 20", "In ")
    popl(c, f"#{p}-167", t + 0.3)
    c.blur_in(f"#{p}-7n", t + 0.7)
    c.blur_in(f"#{p}-src", t + 0.9)
    t = T(c, "06", "For a week")
    fade_seq(c, g1[:5], t - 0.2)
    c.show(f"#{p}-br", t)
    c.pop(bs[1], t + 0.2, 0.4, "50% 100%")
    t = T(c, "06", "Some used it")
    c.pop(bs[2], t, 0.4, "50% 100%")
    c.pop(bs[0], c.at("06", "at all"), 0.4, "50% 100%")
    c.sfx("pop", c.at("06", "at all"))
    t = T(c, "06", "Their sleep")
    popl(c, f"#{p}-wr", t, snd=None)
    t = T(c, "06", "Across")
    fade_seq(c, [f"#{p}-wr"], t - 0.2)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-same", c.at("06", "about the same"), snd="thump")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 07 · Clue four: the tired brain
def s07():
    c = comp("07")
    p = c.cid
    close = board(c, ("ngap", "ngac-nhien"))
    c.svg += [clue(f"{p}-c4", "CLUE 4 · THE TIRED BRAIN"),
              label(f"{p}-aw", 1270, 240, "AWAKE ALL NIGHT → BRAIN SCAN", 44, WHITE, "middle"),
              brain(f"{p}-br", 1050, 500, 2.0),
              f'<circle id="{p}-rw" cx="1090" cy="560" r="46" fill="{YELLOW}" opacity="0"/>',
              f'<circle id="{p}-fr" cx="880" cy="440" r="56" fill="{TEAL}" opacity=".8"/>',
              label(f"{p}-rl", 1560, 420, "REWARD ▲", 64, YELLOW, "middle"),
              label(f"{p}-bl", 1560, 540, "BRAKES ▼", 64, TEAL, "middle"),
              label(f"{p}-bl2", 1560, 600, "(FRONT OF THE BRAIN)", 32, GREY, "middle"),
              label(f"{p}-pl", 1270, 780, "MORE PICTURES RATED “PLEASANT”", 50, WHITE, "middle"),
              note(f"{p}-src", 1270, 880, "Gujar et al., Journal of Neuroscience, 2011 · 27 young adults")]
    close()
    end = end_of(c, "07")
    c.hide(f"#{p}-c4", f"#{p}-aw", f"#{p}-br", f"#{p}-fr", f"#{p}-rl", f"#{p}-bl", f"#{p}-bl2", f"#{p}-pl", f"#{p}-src")
    t = T(c, "07", "Clue four")
    popl(c, f"#{p}-c4", t)
    popl(c, f"#{p}-aw", c.at("07", "awake all night"), snd=None)
    c.pop(f"#{p}-br", t + 0.4, 0.5)
    c.show(f"#{p}-fr", t + 0.4)
    c.blur_in(f"#{p}-src", t + 0.8)
    t = T(c, "07", "In the sleep")
    c.tl.to(f"#{p}-rw", {"opacity": 0.9, "duration": 0.4}, t + 0.3)
    c.tl.ft(f"#{p}-rw", {"scale": 1, "transformOrigin": "50% 50%"}, {"scale": 1.25, "transformOrigin": "50% 50%", "duration": 0.5,
                                                                    "yoyo": True, "repeat": 5, "ease": "sine.inOut"}, t + 0.3)
    popl(c, f"#{p}-rl", c.at("07", "more strongly"), snd="pop")
    t = T(c, "07", "At the same")
    c.tl.to(f"#{p}-fr", {"opacity": 0.15, "duration": 0.8}, t + 0.3)
    popl(c, f"#{p}-bl", t + 0.3, snd="pop")
    c.blur_in(f"#{p}-bl2", T(c, "07", "Those front"))
    t = T(c, "07", "And the tired")
    swap(c, f"{p}-ngap", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-pl", t + 0.2, snd="thump")
    idle(c, f"{p}-ngap", 0, t, 0)
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


def pedals(prefix, x, y, s=1.0):
    return pedal(f"{prefix}-g", x - 110 * s, y, "GAS", TEAL, s) + pedal(f"{prefix}-b", x + 110 * s, y, "BRAKE", CORAL, s)


def opt_row(prefix, x, y, letter, icon, lab):
    return g(prefix, f"""<rect id="{prefix}-box" x="{x - 30}" y="{y - 86}" width="1170" height="172" rx="28" fill="none" stroke="{YELLOW}" stroke-width="8" opacity="0"/>
{text(x + 50, y + 44, letter, 128, 900, YELLOW, "middle")}
<g transform="translate({x + 270} {y})">{icon}</g>
{text(x + 430, y + 14, lab, 35, 800, WHITE)}
<line id="{prefix}-strike" x1="{x - 20}" y1="{y}" x2="{x + 1130}" y2="{y}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>""")


def options(prefix, x=690):
    return (opt_row(f"{prefix}a", x, 300, "A", lamp(f"{prefix}-lp", 0, 0, BLUE, 52), "BLUE LIGHT KEEPS YOU AWAKE")
            + opt_row(f"{prefix}b", x, 530, "B", pedals(f"{prefix}-pd", 0, -10, 0.42), "AVOIDING STOPPING, WEAK BRAKES")
            + opt_row(f"{prefix}c", x, 760, "C", phone(f"{prefix}-ph", 0, 0, 0.7, buzz=False, screen=CORAL), "ADDICTIVE AS A DRUG"))


# ---------------------------------------------------------------- 08 · The question
def s08():
    c = comp("08")
    p = c.cid
    close = board(c)
    c.svg += [options(f"{p}-o"), label(f"{p}-q", 1270, 560, "WHY CAN'T YOU STOP?", 96, WHITE, "middle")]
    close()
    idle(c, f"{p}-suy-nghi", 0, end_of(c, "08"), 2)
    c.hide(f"#{p}-q")
    popl(c, f"#{p}-q", T(c, "08", "So why"))
    c.blur_out(f"#{p}-q", T(c, "08", "A:", "A") - 0.3, 0.25)
    for L, pres in (("a", ("A:", "A ")), ("b", ("B:", "B ")), ("c", ("Or C:", "Or C"))):
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
             ("f", "1. Late sleepers: “I want to go to bed, but I just don't.”"),
             ("f", "2. Some stay up on purpose, some lose track of time."),
             ("f", "3. Night mode on or off: sleep about the same."),
             ("f", "4. Tired brain: reward up, brakes down."),
             ("o", "A. Blue light keeps you awake"), ("o", "B. You avoid stopping, and tired brakes are weak"),
             ("o", "C. Your phone is as addictive as a drug")]
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
    c.svg += [label(f"{p}-gs", 1270, 380, "GO TO SLEEP", 120, WHITE, "middle"),
              f'<line id="{p}-x" x1="860" y1="350" x2="1680" y2="350" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" '
              f'stroke="{CORAL}" stroke-width="16" stroke-linecap="round"/>',
              label(f"{p}-dc", 1270, 560, "A DECISION", 90, YELLOW, "middle"),
              label(f"{p}-st", 1270, 700, "…TO STOP", 130, YELLOW, "middle"),
              g(f"{p}-3", "".join(chip(f"{p}-3{k}", 860 + k * 410, 860, f"FORCE {k + 1}", 46, CORAL, WHITE) for k in range(3)))]
    close()
    end = end_of(c, "10")
    c.hide(f"#{p}-gs", f"#{p}-dc", f"#{p}-st", f"#{p}-3", *[f"#{p}-3{k}" for k in range(3)])
    t = T(c, "10", "The key")
    popl(c, f"#{p}-gs", t)
    c.draw(f"#{p}-x", c.at("10", "happens to you", off=0.2), 0.4)
    c.sfx("thump", c.at("10", "happens to you", off=0.4))
    t = T(c, "10", "It's a decision")
    popl(c, f"#{p}-dc", t, snd="pop")
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    popl(c, f"#{p}-st", T(c, "10", "A decision to"), snd="thump")
    t = T(c, "10", "And at night")
    c.show(f"#{p}-3", t)
    for k in range(3):
        popl(c, f"#{p}-3{k}", c.at("10", "three things") + 0.25 * k, snd="pop" if k == 0 else None)
    idle(c, f"{p}-vui", T(c, "10", "It's a decision") + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 11 · Force one: your own time
def s11():
    c = comp("11")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    segs = [(0.30, "#3A5A80", "SLEEP"), (0.28, GREY, "CLASS · WORK"), (0.13, "#C9D6E3", "HOME"), (0.15, PINK, "OTHERS"), (0.14, YELLOW, "YOURS")]
    c.svg += [label(f"{p}-t", 1270, 150, "FORCE 1 · TIME THAT FEELS LIKE YOURS", 56, YELLOW, "middle"),
              g(f"{p}-day", day_bar(f"{p}-d", 740, 380, 1060, segs)),
              f'<path id="{p}-ext" d="M1690 520 H1800" fill="none" stroke="{YELLOW}" stroke-width="14" stroke-linecap="round" '
              f'pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>',
              label(f"{p}-end", 1650, 590, "SLEEP = ENDING IT", 44, WHITE, "middle"),
              label(f"{p}-str", 1650, 660, "SO YOU STRETCH IT", 44, CORAL, "middle"),
              label(f"{p}-rv", 1270, 780, "“REVENGE BEDTIME PROCRASTINATION”", 52, YELLOW, "middle"),
              label(f"{p}-on", 1270, 850, "(AN INTERNET NAME · = “ON PURPOSE”)", 34, GREY, "middle")]
    close()
    end = end_of(c, "11")
    sg = [f"#{p}-d-s{k}" for k in range(5)]
    c.hide(f"#{p}-t", f"#{p}-day", f"#{p}-end", f"#{p}-str", f"#{p}-rv", f"#{p}-on", *sg)
    t = T(c, "11", "The first")
    popl(c, f"#{p}-t", t)
    t = T(c, "11", "Think about")
    c.show(f"#{p}-day", t)
    for k in range(4):
        c.pop(sg[k], t + 0.4 + 0.35 * k, 0.35)
    c.sfx("pop", t + 0.4)
    t = T(c, "11", "For many")
    c.pop(sg[4], t + 0.2, 0.45)
    c.sfx("thump", t + 0.2)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t + 0.2)
    popl(c, f"#{p}-end", T(c, "11", "Going to sleep"), snd=None)
    t = T(c, "11", "So you stretch")
    c.draw(f"#{p}-ext", t, 1.2, "power1.inOut")
    c.tl.to(sg[4], {"scaleX": 1.35, "transformOrigin": "0% 50%", "duration": 1.2, "ease": "power1.inOut"}, t)
    popl(c, f"#{p}-str", t + 0.3, snd=None)
    popl(c, f"#{p}-rv", T(c, "11", "Online"), snd="pop")
    c.blur_in(f"#{p}-on", T(c, "11", "It's the"))
    idle(c, f"{p}-vui", t, end, 1)
    return c


# ---------------------------------------------------------------- 12 · Force two: no last page
def s12():
    c = comp("12")
    p = c.cid
    close = board(c, ("suy-nghi", "dien-thoai", "ngac-nhien"))
    out_ic = (bubble(f"{p}-o0", 1480, 330, 340, 90, "MESSAGE", PAPER, INK, 36)
              + bubble(f"{p}-o1", 1480, 450, 340, 90, "PLACE TO BE", PAPER, INK, 36)
              + bubble(f"{p}-o2", 1480, 570, 340, 90, "SOMETHING ELSE", PAPER, INK, 32))
    c.svg += [label(f"{p}-t", 1270, 150, "FORCE 2 · NO LAST PAGE", 60, YELLOW, "middle"),
              book(f"{p}-bk", 900, 470, 0.9), label(f"{p}-end", 900, 640, "THE END", 50, WHITE, "middle"),
              feed(f"{p}-fd", 1300, 520, 1.15), label(f"{p}-nb", 1300, 860, "NO BOTTOM", 50, CORAL, "middle"),
              label(f"{p}-46", 1480, 240, "46 PEOPLE · 1 WEEK", 44, WHITE, "middle"), out_ic,
              label(f"{p}-out", 1480, 680, "REASONS TO STOP:", 40, YELLOW, "middle"),
              label(f"{p}-out2", 1480, 735, "OUTSIDE THE APP", 40, YELLOW, "middle"),
              note(f"{p}-s1", 1480, 790, "Rixen et al., MobileHCI 2023"),
              label(f"{p}-bed", 1480, 880, "IN BED AT NIGHT: RARE", 50, CORAL, "middle"),
              chip(f"{p}-15", 1480, 330, "15 MIN · TAKE A BREAK?", 40),
              label(f"{p}-kp", 1480, 520, "NOTICED IT…", 56, WHITE, "middle"),
              label(f"{p}-kp2", 1480, 610, "KEPT SCROLLING", 64, CORAL, "middle"),
              note(f"{p}-s2", 1480, 700, "Meinhardt et al., CHI 2025 · 72 people")]
    close()
    end = end_of(c, "12")
    g1 = [f"#{p}-bk", f"#{p}-end"]
    g2 = [f"#{p}-46", f"#{p}-o0", f"#{p}-o1", f"#{p}-o2", f"#{p}-out", f"#{p}-out2", f"#{p}-s1", f"#{p}-bed"]
    g3 = [f"#{p}-15", f"#{p}-kp", f"#{p}-kp2", f"#{p}-s2"]
    c.hide(f"#{p}-t", *g1, f"#{p}-fd", f"#{p}-nb", *g2, *g3)
    t = T(c, "12", "The second")
    popl(c, f"#{p}-t", t)
    t = T(c, "12", "A book")
    c.pop(f"#{p}-bk", t, 0.45)
    c.blur_in(f"#{p}-end", c.at("12", "last page"))
    t = T(c, "12", "But a feed")
    c.pop(f"#{p}-fd", t, 0.45)
    c.sfx("pop", t)
    c.tl.to(f"#{p}-fd-strip", {"y": -1180, "duration": 14, "ease": "none"}, t + 0.3)
    popl(c, f"#{p}-nb", c.at("12", "no bottom"), snd="thump")
    swap(c, f"{p}-suy-nghi", f"{p}-dien-thoai", t)
    t = T(c, "12", "So what makes")
    fade_seq(c, g1 + [f"#{p}-nb"], t - 0.2)
    c.tl.to(f"#{p}-fd", {"x": -350, "duration": 0.6, "ease": "power2.inOut"}, t)
    t = T(c, "12", "In one study")
    popl(c, f"#{p}-46", t, snd=None)
    c.blur_in(f"#{p}-s1", t + 0.4)
    t = T(c, "12", "Most reasons")
    for k in range(3):
        c.pop(f"#{p}-o{k}", t + 0.3 * k, 0.4, "25% 100%")
    c.sfx("pop", t)
    popl(c, f"#{p}-out", t + 1.0, snd=None)
    popl(c, f"#{p}-out2", t + 1.2, snd=None)
    t = T(c, "12", "Late at night")
    popl(c, f"#{p}-bed", t, snd="thump")
    t = T(c, "12", "In another")
    fade_seq(c, g2, t - 0.25)
    popl(c, f"#{p}-15", c.at("12", "fifteen minutes"))
    c.blur_in(f"#{p}-s2", t + 0.5)
    t = T(c, "12", "People noticed")
    swap(c, f"{p}-dien-thoai", f"{p}-ngac-nhien", t)
    popl(c, f"#{p}-kp", t, snd=None)
    popl(c, f"#{p}-kp2", c.at("12", "kept scrolling"), snd="thump")
    idle(c, f"{p}-ngac-nhien", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 13 · Force three: more gas, less brake
def s13():
    c = comp("13")
    p = c.cid
    close = board(c, ("ngap", "dau-dau"))
    c.svg += [label(f"{p}-t", 1270, 150, "FORCE 3 · MORE GAS, LESS BRAKE", 60, YELLOW, "middle"),
              pedals(f"{p}-pd", 1060, 470, 1.15),
              clock(f"{p}-ck", 1580, 420, 120, 9, 0),
              label(f"{p}-tm", 1580, 610, "9 PM → 1 AM", 44, WHITE, "middle"),
              label(f"{p}-dec", 1270, 790, "THE DECISION COMES LAST", 56, WHITE, "middle"),
              label(f"{p}-wk", 1270, 880, "WHEN YOUR BRAKES ARE WEAKEST", 52, CORAL, "middle")]
    close()
    end = end_of(c, "13")
    c.hide(f"#{p}-t", f"#{p}-pd-g", f"#{p}-pd-b", f"#{p}-ck", f"#{p}-tm", f"#{p}-dec", f"#{p}-wk")
    t = T(c, "13", "The third")
    popl(c, f"#{p}-t", t)
    c.pop(f"#{p}-pd-g", t + 0.4, 0.4)
    c.pop(f"#{p}-pd-b", t + 0.6, 0.4)
    t = T(c, "13", "Remember")
    c.tl.to(f"#{p}-pd-g", {"scale": 1.3, "transformOrigin": "50% 100%", "duration": 0.6, "ease": "back.out(2)"}, c.at("13", "reward"))
    c.sfx("pop", c.at("13", "reward"))
    t = T(c, "13", "And it loosened")
    c.tl.to(f"#{p}-pd-b", {"scale": 0.65, "transformOrigin": "50% 100%", "duration": 0.6, "ease": "power2.out"}, t + 0.3)
    c.sfx("whoosh", t + 0.3)
    t = T(c, "13", "And here's")
    c.pop(f"#{p}-ck", t, 0.45)
    c.tl.to(f"#{p}-ck-h", {"rotation": 120, "svgOrigin": "1580 420", "duration": 3.0, "ease": "power1.inOut"}, t + 0.4)
    c.tl.to(f"#{p}-ck-m", {"rotation": 1440, "svgOrigin": "1580 420", "duration": 3.0, "ease": "power1.inOut"}, t + 0.4)
    c.blur_in(f"#{p}-tm", t + 0.6)
    popl(c, f"#{p}-dec", T(c, "13", "The decision"), snd="pop")
    t = T(c, "13", "So the moment")
    swap(c, f"{p}-ngap", f"{p}-dau-dau", t)
    popl(c, f"#{p}-wk", c.at("13", "weakest"), snd="thump")
    idle(c, f"{p}-ngap", 0, t, 0)
    idle(c, f"{p}-dau-dau", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 14 · Is willpower a fuel tank?
def s14():
    c = comp("14")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [label(f"{p}-t", 1270, 150, "IS WILLPOWER A FUEL TANK?", 60, YELLOW, "middle"),
              tank(f"{p}-tk", 790, 280, 220, 420, CORAL, "WILLPOWER", 1.0),
              label(f"{p}-pop", 1450, 340, "A POPULAR IDEA FOR YEARS", 44, WHITE, "middle"),
              label(f"{p}-23", 1450, 450, "23 LABS · 2,141 PEOPLE", 52, WHITE, "middle"),
              gauge(f"{p}-g", 1450, 640, 130, "EFFECT ≈ 0", YELLOW),
              note(f"{p}-src", 1450, 880, "Hagger et al., Perspectives on Psychological Science, 2016"),
              stamp(f"{p}-db", 1270, 300, "STILL DEBATED", YELLOW, 560, 54, -3),
              label(f"{p}-ti", 1270, 480, "TIREDNESS: STRONG SUSPECT", 60, TEAL, "middle"),
              label(f"{p}-mt", 1270, 600, "MAGIC FUEL TANK: PROBABLY NOT", 56, CORAL, "middle")]
    close()
    end = end_of(c, "14")
    g1 = [f"#{p}-tk", f"#{p}-pop", f"#{p}-23", f"#{p}-g", f"#{p}-src"]
    c.hide(f"#{p}-t", *g1, f"#{p}-db", f"#{p}-ti", f"#{p}-mt")
    t = T(c, "14", "You might")
    popl(c, f"#{p}-t", t)
    c.pop(f"#{p}-tk", t + 0.3, 0.45, "50% 100%")
    c.tl.to(f"#{p}-tk-fill", {"scaleY": 0.08, "transformOrigin": "50% 100%", "duration": 2.0, "ease": "power1.in"}, c.at("14", "by night"))
    popl(c, f"#{p}-pop", T(c, "14", "That idea"), snd=None)
    t = T(c, "14", "But when")
    popl(c, f"#{p}-23", t)
    c.pop(f"#{p}-g", t + 0.6, 0.45)
    c.tl.ft(f"#{p}-g-n", {"rotation": 60, "svgOrigin": "1450 640"}, {"rotation": -84, "svgOrigin": "1450 640", "duration": 0.9, "ease": "power2.inOut"},
            c.at("14", "almost vanished"))
    c.sfx("thump", c.at("14", "almost vanished"))
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", c.at("14", "almost vanished"))
    c.blur_in(f"#{p}-src", t + 0.5)
    t = T(c, "14", "So scientists")
    fade_seq(c, g1, t - 0.25)
    c.show(f"#{p}-db", t)
    c.tl.ft(f"#{p}-db", {"scale": 1.5, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "power4.in"}, t)
    c.sfx("thump", t + 0.3)
    popl(c, f"#{p}-ti", T(c, "14", "Tiredness"), snd="pop")
    popl(c, f"#{p}-mt", T(c, "14", "A magic"), snd=None)
    idle(c, f"{p}-ngac-nhien", c.at("14", "almost vanished", off=0.6), end, 1)
    return c


# ---------------------------------------------------------------- 15 · The busy mind
def s15():
    c = comp("15")
    p = c.cid
    close = board(c, ("suy-nghi", "dau-dau"))
    head = (f'<rect x="760" y="700" width="580" height="90" rx="45" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>'
            + brain(f"{p}-brn", 1050, 560, 1.9))
    thoughts = "".join(bubble(f"{p}-th{k}", x, y, w, 80, s, PAPER, INK, 32)
                       for k, (x, y, w, s) in enumerate(((900, 300, 260, "EPISODE 6?"), (1170, 240, 260, "THAT MESSAGE"),
                                                         (1300, 380, 220, "HAHA"))))
    c.svg += [label(f"{p}-t", 1270, 150, "THE BUSY MIND", 60, YELLOW, "middle"),
              g(f"{p}-hd", head), thoughts,
              label(f"{p}-mr", 1050, 880, "MIND STILL RUNNING", 52, YELLOW, "middle"),
              label(f"{p}-bw", 1600, 470, "BINGE-WATCHING", 44, WHITE, "middle"),
              label(f"{p}-ws", 1600, 540, "→ WORSE SLEEP", 44, CORAL, "middle"),
              label(f"{p}-hn", 1600, 650, "HEAD: WIRED ✓", 40, YELLOW, "middle"),
              label(f"{p}-bd", 1600, 710, "BODY: NOT REALLY", 40, GREY, "middle"),
              note(f"{p}-src", 1270, 945, "Exelmans & Van den Bulck, J Clin Sleep Med, 2017 · survey of 423 young adults")]
    close()
    end = end_of(c, "15")
    ths = [f"#{p}-th{k}" for k in range(3)]
    c.hide(f"#{p}-t", f"#{p}-hd", *ths, f"#{p}-mr", f"#{p}-bw", f"#{p}-ws", f"#{p}-hn", f"#{p}-bd", f"#{p}-src")
    t = T(c, "15", "There's one")
    popl(c, f"#{p}-t", t)
    t = T(c, "15", "It keeps")
    c.pop(f"#{p}-hd", t, 0.45)
    for k in range(3):
        c.pop(ths[k], t + 0.5 + 0.35 * k, 0.4, "25% 100%")
    c.sfx("pop", t + 0.5)
    t = T(c, "15", "A survey")
    popl(c, f"#{p}-bw", t, snd=None)
    popl(c, f"#{p}-ws", c.at("15", "worse sleep"), snd="pop")
    c.blur_in(f"#{p}-src", t + 0.5)
    t = T(c, "15", "The link")
    popl(c, f"#{p}-mr", t)
    for k in range(3):
        c.tl.ft(ths[k], {"rotation": -3}, {"rotation": 3, "transformOrigin": "50% 50%", "duration": 0.4, "yoyo": True, "repeat": 7}, t + 0.1 * k)
    t = T(c, "15", "People's")
    swap(c, f"{p}-suy-nghi", f"{p}-dau-dau", t)
    t = T(c, "15", "It wasn't")
    popl(c, f"#{p}-hn", c.at("15", "their heads"), snd="thump")
    c.blur_in(f"#{p}-bd", t + 0.2)
    idle(c, f"{p}-dau-dau", T(c, "15", "People's") + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 16 · What about blue light?
def s16():
    c = comp("16")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [label(f"{p}-t", 1270, 150, "WHAT ABOUT BLUE LIGHT?", 60, YELLOW, "middle"),
              label(f"{p}-nq", 1270, 250, "NOT QUITE INNOCENT", 44, WHITE, "middle"),
              tablet(f"{p}-tb", 860, 500, 0.85), book(f"{p}-bk", 1180, 520, 0.8),
              label(f"{p}-12", 1020, 760, "12 ADULTS · 4 H · 5 NIGHTS", 36, WHITE, "middle"),
              label(f"{p}-mel", 1580, 380, "MELATONIN ▼", 54, BLUE, "middle"),
              label(f"{p}-clk", 1580, 470, "BODY CLOCK: LATER", 44, WHITE, "middle"),
              label(f"{p}-10", 1580, 580, "≈ 10 MIN LONGER", 60, YELLOW, "middle"),
              label(f"{p}-10b", 1580, 640, "TO FALL ASLEEP", 40, YELLOW, "middle"),
              note(f"{p}-s1", 1270, 860, "Chang et al., PNAS, 2015"),
              stamp(f"{p}-lab", 1580, 760, "4 HOURS · IN A LAB", CORAL, 520, 42, -3),
              bars(f"{p}-br", [(900, 300, TEAL, "NO PHONE"), (1180, 304, "#FFB070", "NIGHT MODE"), (1460, 302, BLUE, "PHONE")], 760, 180),
              label(f"{p}-pc", 1270, 300, "LIGHT = ONE PIECE · NOT THE BIGGEST", 52, YELLOW, "middle")]
    close()
    end = end_of(c, "16")
    g1 = [f"#{p}-nq", f"#{p}-tb", f"#{p}-bk", f"#{p}-12", f"#{p}-mel", f"#{p}-clk", f"#{p}-10", f"#{p}-10b", f"#{p}-s1", f"#{p}-lab"]
    c.hide(f"#{p}-t", *g1, f"#{p}-br", f"#{p}-pc")
    t = T(c, "16", "So is blue")
    popl(c, f"#{p}-t", t)
    popl(c, f"#{p}-nq", c.at("16", "Not quite"), snd=None)
    t = T(c, "16", "In one lab")
    c.pop(f"#{p}-tb", t, 0.45)
    c.blur_in(f"#{p}-12", t + 0.4)
    c.blur_in(f"#{p}-s1", t + 0.6)
    t = T(c, "16", "Compared")
    c.pop(f"#{p}-bk", t, 0.45)
    popl(c, f"#{p}-mel", c.at("16", "melatonin"), snd="pop")
    t = T(c, "16", "Their body")
    popl(c, f"#{p}-clk", t, snd=None)
    popl(c, f"#{p}-10", c.at("16", "ten minutes"), snd="thump")
    c.blur_in(f"#{p}-10b", c.at("16", "ten minutes", off=0.3))
    t = T(c, "16", "That's real")
    c.show(f"#{p}-lab", c.at("16", "four hours"))
    c.tl.ft(f"#{p}-lab", {"scale": 1.5, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "power4.in"},
            c.at("16", "four hours"))
    c.sfx("thump", c.at("16", "four hours", off=0.3))
    t = T(c, "16", "And remember")
    fade_seq(c, g1, t - 0.25)
    c.pop(f"#{p}-br", t, 0.45, "50% 100%")
    t = T(c, "16", "Light is")
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    popl(c, f"#{p}-pc", t, snd="pop")
    idle(c, f"{p}-vui", t + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 17 · Why it hits young people harder
def s17():
    c = comp("17")
    p = c.cid
    close = board(c, ("suy-nghi", "ngap"))
    X0, Y0, W, H = 760, 300, 1000, 420
    ax = (f'<path d="M{X0} {Y0 - 20} V{Y0 + H} H{X0 + W}" fill="none" stroke="{GREY}" stroke-width="6"/>'
          + "".join(text(X0 + W * (a - 10) / 50, Y0 + H + 50, str(a), 32, 800, GREY, "middle") for a in (10, 20, 30, 40, 50, 60))
          + text(X0 + W / 2, Y0 + H + 100, "AGE", 32, 900, GREY, "middle")
          + text(X0 - 20, Y0 + 10, "LATER", 30, 900, GREY, "end") + text(X0 - 20, Y0 + H, "EARLIER", 30, 900, GREY, "end"))
    c.svg += [label(f"{p}-t", 1270, 150, "WHY IT HITS YOUNG PEOPLE HARDER", 58, YELLOW, "middle"),
              label(f"{p}-25", 1270, 230, "≈ 25,000 PEOPLE · NATURAL SLEEP TIMES", 40, WHITE, "middle"),
              g(f"{p}-ax", ax), age_curve(f"{p}-cv", X0, Y0, W, H),
              f'<circle id="{p}-pk" cx="{X0 + W * 10 / 50:.0f}" cy="{Y0}" r="18" fill="{CORAL}" stroke="{INK}" stroke-width="5"/>',
              label(f"{p}-20", X0 + W * 10 / 50 + 40, Y0 - 10, "PEAK ≈ 20", 46, CORAL),
              note(f"{p}-src", 1500, 400, "Roenneberg et al., Current Biology, 2004"),
              label(f"{p}-ns", 1270, 885, "NOT SLEEPY AT 10 PM", 44, WHITE, "middle"),
              label(f"{p}-ea", 1270, 945, "+ EARLY ALARM = A VERY LONG EVENING", 40, YELLOW, "middle")]
    close()
    end = end_of(c, "17")
    c.hide(f"#{p}-t", f"#{p}-25", f"#{p}-ax", f"#{p}-pk", f"#{p}-20", f"#{p}-src", f"#{p}-ns", f"#{p}-ea")
    t = T(c, "17", "If you're")
    popl(c, f"#{p}-t", t)
    t = T(c, "17", "A survey")
    popl(c, f"#{p}-25", t, snd=None)
    c.blur_in(f"#{p}-ax", t + 0.3, 0.3)
    c.blur_in(f"#{p}-src", t + 0.6)
    t = T(c, "17", "Through")
    c.draw(f"#{p}-cv", t, 4.0, "none")
    t = T(c, "17", "It peaks")
    c.pop(f"#{p}-pk", t, 0.4)
    popl(c, f"#{p}-20", c.at("17", "twenty") if has("17", "It peaks") else t, snd="thump")
    t = T(c, "17", "So your body")
    swap(c, f"{p}-suy-nghi", f"{p}-ngap", t)
    popl(c, f"#{p}-ns", t, snd=None)
    popl(c, f"#{p}-ea", T(c, "17", "Combine"), snd="pop")
    idle(c, f"{p}-ngap", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 18 · Are phones ruining a generation?
def s18():
    c = comp("18")
    p = c.cid
    close = board(c, ("suy-nghi", "ngac-nhien"))
    c.svg += [label(f"{p}-t", 1270, 150, "ARE PHONES RUINING A GENERATION?", 56, YELLOW, "middle"),
              stamp(f"{p}-db", 1270, 270, "STILL DEBATED", YELLOW, 560, 54, -3),
              label(f"{p}-300", 1050, 420, "300,000+ TEENS", 52, WHITE, "middle"),
              label(f"{p}-sm", 1050, 500, "AVERAGE LINK: VERY SMALL", 42, TEAL, "middle"),
              note(f"{p}-s1", 1050, 550, "Orben & Przybylski, Nature Human Behaviour, 2019"),
              label(f"{p}-big", 1550, 640, "OTHERS: BIGGER FOR SOME", 42, CORAL, "middle"),
              note(f"{p}-s2", 1550, 690, "Twenge, Haidt et al., 2020"),
              label(f"{p}-cl", 1270, 230, "SLEEP: CLEARER EVIDENCE", 60, YELLOW, "middle"),
              label(f"{p}-20", 1270, 320, "20 STUDIES · 125,000 KIDS & TEENS", 42, WHITE, "middle"),
              bars(f"{p}-br", [(820, 150, TEAL, "NO DEVICE"), (1170, 310, CORAL, "USED AT BED"), (1520, 260, "#FFB070", "IN ROOM ONLY")], 760, 230),
              label(f"{p}-x2", 1170, 420, "≈ 2× ODDS", 44, CORAL, "middle"),
              note(f"{p}-s3", 1270, 880, "Carter et al., JAMA Pediatrics, 2016 · meta-analysis"),
              label(f"{p}-lk", 1270, 940, "LINKS, NOT PROOF OF CAUSE", 44, YELLOW, "middle")]
    close()
    end = end_of(c, "18")
    g1 = [f"#{p}-db", f"#{p}-300", f"#{p}-sm", f"#{p}-s1", f"#{p}-big", f"#{p}-s2"]
    bs = [f"#{p}-br-b{k}" for k in range(3)]
    g2 = [f"#{p}-cl", f"#{p}-20", f"#{p}-br", f"#{p}-x2", f"#{p}-s3", f"#{p}-lk"]
    c.hide(f"#{p}-t", *g1, *g2, *bs)
    t = T(c, "18", "Does that")
    popl(c, f"#{p}-t", t)
    t = T(c, "18", "That's still")
    c.show(f"#{p}-db", t)
    c.tl.ft(f"#{p}-db", {"scale": 1.5, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "power4.in"}, t)
    c.sfx("thump", t + 0.3)
    t = T(c, "18", "One large")
    popl(c, f"#{p}-300", t, snd=None)
    popl(c, f"#{p}-sm", c.at("18", "very small"), snd="pop")
    c.blur_in(f"#{p}-s1", c.at("18", "very small", off=0.3))
    t = T(c, "18", "Other researchers")
    popl(c, f"#{p}-big", t, snd=None)
    c.blur_in(f"#{p}-s2", t + 0.3)
    t = T(c, "18", "Sleep is")
    fade_seq(c, g1, t - 0.25)
    popl(c, f"#{p}-cl", t, snd="pop")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    t = T(c, "18", "A review")
    popl(c, f"#{p}-20", t, snd=None)
    c.show(f"#{p}-br", t)
    c.pop(bs[0], t + 0.4, 0.4, "50% 100%")
    t = T(c, "18", "Using a device")
    c.pop(bs[1], t, 0.4, "50% 100%")
    popl(c, f"#{p}-x2", c.at("18", "double"), snd="thump")
    t = T(c, "18", "Even having")
    c.pop(bs[2], t + 0.3, 0.4, "50% 100%")
    c.sfx("pop", t + 0.3)
    c.blur_in(f"#{p}-s3", t + 0.6)
    popl(c, f"#{p}-lk", T(c, "18", "These studies"), snd=None)
    idle(c, f"{p}-ngac-nhien", T(c, "18", "Sleep is") + 0.6, end, 1)
    return c


# ---------------------------------------------------------------- 19 · The answer
def s19():
    c = comp("19")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    c.svg += [options(f"{p}-o"),
              label(f"{p}-sp", 1500, 432, "A SMALL PIECE", 40, GREY, "middle"),
              label(f"{p}-ts", 1500, 860, "TOO SIMPLE", 40, CORAL, "middle"),
              label(f"{p}-eod", 1270, 620, "AVOIDING THE END OF YOUR DAY", 56, YELLOW, "middle")]
    close()
    end = end_of(c, "19")
    c.hide(f"#{p}-sp", f"#{p}-ts", f"#{p}-eod")
    t = T(c, "19", "So the answer")
    c.tl.to(f"#{p}-ob-box", {"opacity": 1, "duration": 0.3}, t)
    c.tl.ft(f"#{p}-ob", {"scale": 1}, {"scale": 1.04, "transformOrigin": "50% 50%", "duration": 0.3, "yoyo": True, "repeat": 1}, t)
    c.sfx("riser", t - 2.5)
    c.sfx("thump", t)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    t = T(c, "19", "You're not")
    c.tl.to([f"#{p}-oa", f"#{p}-oc"], {"opacity": 0, "duration": 0.3}, t - 0.3)
    c.tl.to(f"#{p}-ob", {"y": -230, "duration": 0.6, "ease": "power2.inOut"}, t)
    c.sfx("whoosh", t)
    popl(c, f"#{p}-eod", c.at("19", "end of your day"), snd="pop")
    t = T(c, "19", "Blue light")
    c.blur_out(f"#{p}-eod", t - 0.2, 0.2)
    c.tl.to(f"#{p}-ob", {"opacity": 0.35, "y": 0, "duration": 0.4}, t - 0.3)
    c.tl.to(f"#{p}-oa", {"opacity": 0.8, "duration": 0.3}, t)
    popl(c, f"#{p}-sp", t + 0.2, snd=None)
    t2 = c.at("19", "too simple")
    c.tl.to(f"#{p}-oc", {"opacity": 0.8, "duration": 0.3}, t2 - 0.6)
    c.draw(f"#{p}-oc-strike", t2, 0.4)
    popl(c, f"#{p}-ts", t2, snd="pop")
    idle(c, f"{p}-suy-nghi", 0, T(c, "19", "So the answer"), 1)
    idle(c, f"{p}-vui", T(c, "19", "So the answer") + 0.6, end, 0)
    return c


# ---------------------------------------------------------------- 20 · How to make stopping easier
def s20():
    c = comp("20")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"))
    tips = [("CHARGE IT OUTSIDE THE BEDROOM", "Charge"), ("ALARM: “TIME FOR BED”", "Set an alarm"),
            ("PICK THE STOP BEFORE YOU START", "Pick your"), ("ME-TIME EARLIER IN THE DAY", "And try")]
    c.svg += [label(f"{p}-hd", 1270, 200, "MAKE STOPPING EASIER", 84, YELLOW, "middle"),
              label(f"{p}-wp", 1270, 540, "DECIDE EARLIER, NOT AT 1 AM", 76, WHITE, "middle"),
              "".join(label(f"{p}-tp{k}", 740, 360 + k * 105, f"{k + 1}. {s}", 50, WHITE) for k, (s, _) in enumerate(tips)),
              label(f"{p}-38", 1270, 820, "SMALL TRIAL · 38 PEOPLE · NO PHONE 30 MIN BEFORE BED", 36, TEAL, "middle"),
              label(f"{p}-res", 1270, 885, "FELL ASLEEP FASTER · SLEPT LONGER (SELF-REPORTED)", 34, YELLOW, "middle"),
              note(f"{p}-src", 1650, 760, "He et al., PLOS ONE, 2020 · pilot")]
    close()
    end = end_of(c, "20")
    c.hide(f"#{p}-hd", f"#{p}-wp", f"#{p}-38", f"#{p}-res", f"#{p}-src", *[f"#{p}-tp{k}" for k in range(4)])
    t0 = T(c, "20", "So how")
    popl(c, f"#{p}-hd", t0)
    t = T(c, "20", "Don't count")
    popl(c, f"#{p}-wp", t, snd="thump")
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t)
    c.blur_out(f"#{p}-wp", T(c, "20", tips[0][1]) - 0.25, 0.2)
    for k, (_, pre) in enumerate(tips):
        tt = T(c, "20", pre)
        c.tl.ft(f"#{p}-tp{k}", {"autoAlpha": 0, "x": 60}, {"autoAlpha": 1, "x": 0, "duration": 0.4, "ease": "expo.out"}, tt)
        c.sfx("pop", tt)
    t = T(c, "20", "In a small")
    popl(c, f"#{p}-38", t, snd=None)
    c.blur_in(f"#{p}-src", t + 0.4)
    popl(c, f"#{p}-res", T(c, "20", "Compared"), snd="pop")
    idle(c, f"{p}-vui", t + 0.6, end, 2)
    return c


# ---------------------------------------------------------------- 21 · Back to bed
def s21():
    c = comp("21")
    p = c.cid
    c.svg += [f'<g id="{p}-cam"><image href="assets/bg/phong-ngu-ngu.jpg" width="1920" height="1080"/>'
              + zzz(f"{p}-z", 1500, 330, 1.2, WHITE) + "</g>",
              g(f"{p}-hall", f'<rect x="60" y="560" width="520" height="420" rx="30" fill="{NAVY}" stroke="{YELLOW}" stroke-width="8"/>'
                + text(320, 630, "HALLWAY", 44, 900, YELLOW, "middle") + phone(f"{p}-ph", 320, 780, 0.95, buzz=False, screen="#2B3F7A")
                + f'<path d="M320 862 V900 H560" fill="none" stroke="{GREY}" stroke-width="8"/>'
                + text(320, 955, "CHARGING", 34, 900, TEAL, "middle")),
              chip(f"{p}-t11", 960, 140, "11:00 PM", 60),
              chip(f"{p}-bor", 960, 140, "A LITTLE BORED…", 54, PAPER, INK),
              chip(f"{p}-far", 960, 140, "IT'S WAY OVER THERE", 54, PAPER, INK),
              chip(f"{p}-t1110", 960, 140, "+10 MIN · ASLEEP", 60, TEAL, INK)]
    end = end_of(c, "21")
    c.hide(f"#{p}-hall", f"#{p}-t11", f"#{p}-bor", f"#{p}-far", f"#{p}-t1110", f"#{p}-z")
    t = T(c, "21", "Eleven")
    popl(c, f"#{p}-t11", t + 0.1)
    c.pop(f"#{p}-hall", c.at("21", "hallway"), 0.5)
    c.sfx("pop", c.at("21", "hallway"))
    t = T(c, "21", "You lie")
    c.show(f"#{p}-t11", t, False)
    popl(c, f"#{p}-bor", t, snd=None)
    t = T(c, "21", "You think")
    c.show(f"#{p}-bor", t, False)
    popl(c, f"#{p}-far", c.at("21", "way over there"), snd=None)
    c.tl.ft(f"#{p}-hall", {"scale": 1}, {"scale": 1.06, "transformOrigin": "0% 100%", "duration": 0.3, "yoyo": True, "repeat": 1},
            c.at("21", "way over there"))
    t = T(c, "21", "Ten minutes")
    c.show(f"#{p}-far", t, False)
    popl(c, f"#{p}-t1110", t, snd="pop")
    c.show(f"#{p}-z", t + 0.4)
    for k in range(3):
        c.tl.ft(f"#{p}-z-{k}", {"opacity": 0, "y": 20}, {"opacity": 1, "y": 0, "duration": 0.6, "repeat": 3, "yoyo": True}, t + 0.4 + 0.3 * k)
    c.tl.ft(f"#{p}-cam", {"scale": 1.0, "transformOrigin": "78% 45%"}, {"scale": 1.12, "transformOrigin": "78% 45%", "duration": max(end - t, 1),
                                                                      "ease": "sine.inOut"}, t)
    return c


# ---------------------------------------------------------------- 22 · End card
def s22():
    c = comp("22")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', char("s22-boy", "vui", 1600, 1010, 720)]
    lines = [("big", "You're not avoiding sleep.<br>You're avoiding the end of your day."),
             ("lab", "Key sources"),
             ("src", "Kroese et al., <i>Front Psychol</i> (2014) · Nauts et al., <i>Behav Sleep Med</i> (2019) · Duraccio et al., <i>Sleep Health</i> (2021)"),
             ("src", "Gujar et al., <i>J Neurosci</i> (2011) · Rixen et al., MobileHCI (2023) · Hagger et al., <i>Perspect Psychol Sci</i> (2016)"),
             ("src", "Chang et al., <i>PNAS</i> (2015) · Carter et al., <i>JAMA Pediatr</i> (2016) · He et al., <i>PLOS ONE</i> (2020) · Full list in the description."),
             ("safe", "For general education only, not medical advice.<br>Poor sleep, low mood or worry for weeks? Talk to a doctor or a counselor.")]
    c.css.append(f"#s22-card {{ left: 130px; top: 100px; width: 1280px; color: {INK}; }}"
                 "#s22-card .big { font-size: 64px; font-weight: 800; line-height: 1.12; letter-spacing: -0.01em; margin-bottom: 44px; }"
                 "#s22-card .lab { font-size: 34px; font-weight: 800; color: #B5372A; margin-bottom: 10px; }"
                 "#s22-card .src { font-size: 29px; font-weight: 500; line-height: 1.45; color: #2A3A4A; }"
                 "#s22-card .safe { font-size: 34px; font-weight: 700; margin-top: 40px; line-height: 1.35; }")
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
    plan = [(0, SCENES["03"]["start"], ["lofi"]), (SCENES["03"]["start"], SCENES["10"]["start"], ["doc", "mar"]),
            (SCENES["10"]["start"], SCENES["19"]["start"], ["kal", "lofi", "doc", "mar"]), (SCENES["19"]["start"], DURATION, ["piz"])]
    return music_plan(plan, lifts)()


if __name__ == "__main__":
    run(BUILDERS, music, mau=True)
