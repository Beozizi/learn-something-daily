"""Tập 2 — Vì sao cần uống nước? Sinh dự án HyperFrames từ audio/timeline.json + audio/words.json.

Chạy:  py build.py      (trong thư mục video\\)
Lõi dùng chung ở scripts\\hf (core.py, ve.py, ve2.py).
"""
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from hf import core  # noqa: E402

core.init(__file__)
from hf.core import *  # noqa: E402,F401,F403
from hf.core import SCENES, WORDS, DURATION  # noqa: E402


def S(c, scene, prefix):
    """Mốc (giây trong cảnh) của câu bắt đầu bằng `prefix`."""
    for s in WORDS["sentences"]:
        if s["scene"] == scene and s["text"].startswith(prefix):
            return round(s["start"] - c.start, 3)
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


def office_world(p, hour, minute, poses):
    """Văn phòng: tường, Tò (các tư thế, ẩn trừ tư thế đầu), bàn, laptop, cà phê, chai nước."""
    parts = [office_back(p, hour, minute)]
    parts += [to(f"{p}-{pose}", pose, TO_X, TO_Y, TO_H) for pose in poses]
    parts += [office_front(), laptop(f"{p}-lap", 1150, 702, 0.9), coffee_cup(f"{p}-cup", 760, 690, 0.8),
              bottle(f"{p}-bot", 1520, 690, 0.8)]
    return "".join(parts)


def office_comp(c, hour, minute, poses, extra=""):
    p = c.cid
    c.svg.append(f'<g id="{p}-settle"><g id="{p}-cam">{office_world(p, hour, minute, poses)}{extra}</g></g>')
    for pose in poses[1:]:
        c.hide(f"#{p}-{pose}-w")
    return f"#{p}-cam", f"#{p}-settle"


def show_pose(c, poses, which, t):
    for pose in poses:
        c.show(f"#{c.cid}-{pose}-w", t, pose == which)


# ---------------------------------------------------------------- 01 · Tiêu đề
def s01():
    c = comp("01")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', glass("s01-gl", 1480, 860, 2.2, 0.7)]
    words = ["Vì", "sao", "cần", "<br>", "uống", "nước?"]
    spans = "".join("<br>" if w == "<br>" else
                    f'<span id="s01-w{k}" class="w{" hot" if w == "nước?" else ""}">{w}</span> '
                    for k, w in enumerate(words))
    c.css.append(f"#s01-title {{ left: 150px; top: 300px; font-size: 150px; font-weight: 800; line-height: 1.1; color: {INK}; "
                 f"letter-spacing: -0.01em; }} #s01-title .hot {{ color: {WATER_DARK}; }} #s01-title .w {{ display: inline-block; }}")
    c.html.append(f'<div id="s01-title" class="txt">{spans}</div>')
    c.tl.ft("#s01-gl", {"scale": 0.8, "transformOrigin": "50% 100%"},
            {"scale": 1, "transformOrigin": "50% 100%", "duration": 0.7, "ease": "back.out(1.6)"}, 0)
    c.tl.ft("#s01-gl-water", {"scaleY": 0.2, "transformOrigin": "50% 100%"}, {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 1.2, "ease": "power2.out"}, 0.2)
    for k, w in enumerate(words):
        if w != "<br>":
            c.blur_in(f"#s01-w{k}", 0.25 + 0.09 * k, 0.15)
    return c


# ---------------------------------------------------------------- 02 · Mở truyện (văn phòng)
def s02():
    c = comp("02")
    poses = ["dung", "lo-lang", "suy-nghi", "chi-tay", "ngac-nhien"]
    p = c.cid
    lx, ly = EYE_L
    over = (envelope(f"{p}-env0", 1150, 560, 1.0) + envelope(f"{p}-env1", 1150, 560, 0.9) + envelope(f"{p}-env2", 1150, 560, 1.1)
            + pain_lines(f"{p}-pain", lx - 150, ly - 150, 1.6)
            + "".join(text(1290 + k * 70, 300 - k * 30, "?", 110, 900, YELLOW, id_=f"{p}-q{k}", extra=" " + OUTLINE) for k in range(3)))
    cam, st = office_comp(c, 7, 0, poses, over)
    c.svg.append(label(f"{p}-t16", 1300, 900, "16:00 · THUYẾT TRÌNH", 80, YELLOW, "middle"))
    c.svg.append(label(f"{p}-how", 960, 210, "BAO NHIÊU?", 130, WHITE, "middle"))
    c.hide(f"#{p}-env0", f"#{p}-env1", f"#{p}-env2", f"#{p}-pain", f"#{p}-q0", f"#{p}-q1", f"#{p}-q2", f"#{p}-t16", f"#{p}-how")
    T = lambda pre: S(c, "02", pre)
    end = c.loc(SCENES["02"]["end"])

    frame(c, 0, 960, 540, 1.0, cam, st)
    idle(c, f"{p}-dung", 0, T("Đầu bạn"), 0)
    # cà phê
    frame(c, T("Bạn đến văn phòng"), 900, 520, 1.6, cam, st)
    c.tl.ft(f"#{p}-cup-steam", {"y": 10, "opacity": 0.3}, {"y": -16, "opacity": 1, "duration": 1.2, "ease": "sine.inOut", "yoyo": True,
                                                           "repeat": 1}, T("Bạn đến văn phòng"))
    # 2 tiếng họp: đồng hồ quay
    t = T("Cuộc họp đầu tiên")
    frame(c, t, 1520, 260, 2.4, cam, st)
    c.tl.to(f"#{p}-clock-m", {"rotation": "+=720", "svgOrigin": "1620 250", "duration": 1.4, "ease": "power2.inOut"}, t + 0.2)
    c.tl.to(f"#{p}-clock-h", {"rotation": "+=60", "svgOrigin": "1620 250", "duration": 1.4, "ease": "power2.inOut"}, t + 0.2)
    c.sfx("whoosh", t + 0.5)
    # email, báo cáo
    t = T("Rồi đến email")
    frame(c, t, 1150, 520, 1.7, cam, st)
    for k, (dx, dy) in enumerate(((-260, -220), (40, -300), (280, -200))):
        c.show(f"#{p}-env{k}", t + 0.3 * k)
        c.tl.ft(f"#{p}-env{k}", {"x": 0, "y": 0, "scale": 0.3}, {"x": dx, "y": dy, "scale": 1, "duration": 0.7, "ease": "expo.out"},
                t + 0.3 * k)
        c.sfx("pop", t + 0.3 * k)
    # chai nước còn nguyên nắp
    t = T("Chai nước trên bàn")
    frame(c, t, 1520, 560, 2.4, cam, st)
    for k in range(3):
        c.show(f"#{p}-env{k}", t, False)
    c.tl.ft(f"#{p}-bot-cap", {"rotation": 0}, {"rotation": 6, "transformOrigin": "50% 100%", "duration": 0.12, "yoyo": True,
                                               "repeat": 3}, t + 0.8)
    # 3 giờ chiều
    t = T("Ba giờ chiều")
    frame(c, t, 1520, 260, 2.4, cam, st)
    c.tl.set(f"#{p}-clock-h", {"rotation": 90, "svgOrigin": "1620 250"}, t)
    c.tl.set(f"#{p}-clock-m", {"rotation": 0, "svgOrigin": "1620 250"}, t)
    c.sfx("pop", t)
    # đau đầu
    t = T("Đầu bạn")
    frame(c, t, 1110, 360, 2.3, cam, st)
    show_pose(c, poses, "lo-lang", t)
    c.show(f"#{p}-pain", t + 0.4)
    c.tl.ft(f"#{p}-pain", {"scale": 0.8, "transformOrigin": "50% 50%"}, {"scale": 1.15, "transformOrigin": "50% 50%", "duration": 0.35,
                                                                        "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, t + 0.4)
    c.show(f"#{p}-pain", T("Bạn đọc"), False)
    idle(c, f"{p}-lo-lang", t, T("Bạn đọc"), 2)
    # đọc ba lần
    t = T("Bạn đọc")
    frame(c, t, 1150, 420, 1.6, cam, st)
    show_pose(c, poses, "suy-nghi", t)
    for k in range(3):
        c.pop(f"#{p}-q{k}", t + 0.45 + 0.4 * k, 0.4)
        c.sfx("pop", t + 0.45 + 0.4 * k)
    for k in range(3):
        c.show(f"#{p}-q{k}", T("Môi khô"), False)
    idle(c, f"{p}-suy-nghi", t, T("Môi khô"), 1)
    # môi khô, uể oải
    t = T("Môi khô")
    frame(c, t, 1110, 380, 2.2, cam, st)
    show_pose(c, poses, "lo-lang", t)
    c.tl.ft(f"#{p}-lo-lang .dau", {"y": 0, "rotation": 0}, {"y": 14, "rotation": -6, "transformOrigin": "50% 95%", "duration": 1.0,
                                                          "ease": "power2.inOut"}, t + 0.3)
    # 16:00 thuyết trình
    t = T("Và bốn giờ")
    frame(c, t, 1410, 330, 1.9, cam, st)
    c.tl.set(f"#{p}-clock-h", {"rotation": 120, "svgOrigin": "1620 250"}, t)
    c.pop(f"#{p}-t16", t + 0.5, 0.5)
    c.sfx("thump", t + 0.5)
    c.show(f"#{p}-t16", T("Bạn với lấy"), False)
    # với lấy chai nước, khựng lại
    t = T("Bạn với lấy")
    frame(c, t, 1300, 450, 1.5, cam, st)
    show_pose(c, poses, "chi-tay", t)
    c.tl.ft(f"#{p}-chi-tay .tay-phai", {"rotation": -14}, {"rotation": 0, "transformOrigin": "15% 50%", "duration": 0.6,
                                                          "ease": "back.out(2)"}, t)
    swap(c, f"{p}-chi-tay", f"{p}-suy-nghi", c.at("02", "khựng lại"))
    # bao nhiêu?
    t = T("Uống bao nhiêu")
    c.pop(f"#{p}-how", t, 0.5)
    c.sfx("pop", t)
    t = T("Có phải cứ ráng")
    c.show(f"#{p}-how", t, False)
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    c.tl.ft(f"#{p}-bot", {"scale": 1}, {"scale": 1.7, "transformOrigin": "50% 100%", "duration": 0.9, "ease": "back.out(1.6)"},
            c.at("02", "thật nhiều"))
    c.sfx("whoosh", c.at("02", "thật nhiều"))
    idle(c, f"{p}-ngac-nhien", t + 0.5, end, 3)
    return c


# ---------------------------------------------------------------- 03 · Đặt vấn đề
def s03():
    c = comp("03")
    p = c.cid
    bubbles = [("8 CỐC", 540, 260, 360, "tám cốc"), ("3 LÍT", 1610, 300, 340, "ba lít"),
               ("KHÁT MỚI UỐNG", 640, 580, 560, "khát mới uống"), ("CÀNG NHIỀU CÀNG THẢI ĐỘC", 1420, 620, 740, "uống càng nhiều")]
    extra = "".join(bubble(f"{p}-b{k}", x, y, w, 130, lb, size=54) for k, (lb, x, y, w, _) in enumerate(bubbles))
    cam, st = office_comp(c, 15, 30, ["suy-nghi", "ngac-nhien"], extra)
    frame(c, 0, 1050, 470, 1.25, cam, st)
    idle(c, f"{p}-suy-nghi", 0, c.loc(SCENES["03"]["end"]), 0)
    for k, (*_, word) in enumerate(bubbles):
        t = c.at("03", word)
        c.pop(f"#{p}-b{k}", t, 0.5, "50% 100%", "back.out(1.8)", 0.3)
        c.sfx("pop", t)
        c.tl.to(f"#{p}-suy-nghi .mat", {"x": -6 if k % 2 == 0 else 8, "duration": 0.2}, t)
    t = c.at("03", "Để biết ai đúng")
    for k in range(4):
        c.tl.to(f"#{p}-b{k}", {"scale": 0, "transformOrigin": "50% 50%", "duration": 0.3, "ease": "back.in(2)"}, t + 0.06 * k)
    c.sfx("whoosh", t)
    c.tl.to(cam, {"x": 960 - 2.2 * 1110, "y": 540 - 2.2 * 380, "scale": 2.2, "transformOrigin": "0 0", "duration": 1.6,
                  "ease": "power2.inOut"}, t + 0.6)
    return c


def board(c, poses=("suy-nghi",), look=(7, 0)):
    """Nền bảng + Tò bên trái (tư thế đầu hiện, các tư thế khác ẩn)."""
    c.svg.append(slate_frame())
    for k, pose in enumerate(poses):
        board_to(c, f"{c.cid}-{pose}", pose, hidden=k > 0)
    c.tl.set(f"#{c.cid}-{poses[0]} .mat", {"x": look[0], "y": look[1]}, 0)
    return lambda: c.svg.append(slate_border())


def popl(c, sel, t, origin="50% 50%", snd="pop", dur=0.45):
    c.pop(sel, t, dur, origin)
    if snd:
        c.sfx(snd, t)


# ---------------------------------------------------------------- 04 · Bạn là nước
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
                + text(1530, 1000, "SƠ SINH", 34, 800, GREY, "middle", id_=f"{p}-n75")
                + text(1730, 1000, "CAO TUỔI", 34, 800, GREY, "middle", id_=f"{p}-n55")),
              g(f"{p}-org", label(f"{p}-o1", PX + 160, head_y + 20, "NÃO · TIM ≈ 73%", 48, WHITE)
                + label(f"{p}-o2", PX + 160, head_y + 290, "PHỔI ≈ 83%", 48, WHITE)
                + label(f"{p}-o3", PX + 160, head_y + 640, "XƯƠNG ≈ 31%", 48, WHITE)
                + text(PX + 160, head_y + 720, "Mitchell và cộng sự, 1945", 28, 500, GREY, id_=f"{p}-osrc")),
              g(f"{p}-split", f'<rect id="{p}-in" x="700" y="330" width="760" height="190" rx="24" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                + f'<rect id="{p}-out" x="1470" y="330" width="380" height="190" rx="24" fill="{WATER}" stroke="{INK}" stroke-width="6"/>'
                + label(f"{p}-lin", 1080, 445, "TRONG TẾ BÀO · 2/3", 56, WHITE, "middle")
                + label(f"{p}-lout", 1660, 445, "NGOÀI · 1/3", 52, WHITE, "middle")
                + text(1660, 580, "MÁU + KHE GIỮA TẾ BÀO", 34, 800, WATER, "middle", id_=f"{p}-lout2")),
              g(f"{p}-cyc", f'<circle cx="1280" cy="820" r="120" fill="none" stroke="{WATER}" stroke-width="14" stroke-dasharray="40 26" id="{p}-ring"/>'
                + "".join(label(f"{p}-c{k2}", x, y, w, 44, WHITE, "middle")
                          for k2, (x, y, w) in enumerate(((1280, 660, "CHẢY"), (1520, 840, "BỐC HƠI"), (1280, 1000, "ĐƯỢC LỌC"), (1040, 840, "THAY MỚI"))))),
              tear(f"{p}-drop", 1660, 820, 3.0), label(f"{p}-l3", 1270, 560, "1 GIỌT NƯỚC · 3 CÔNG VIỆC", 80, WHITE, "middle")]
    close()
    end = c.loc(SCENES["04"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 1)
    c.hide(f"#{p}-l60", f"#{p}-mini", f"#{p}-baby", f"#{p}-old", f"#{p}-l75", f"#{p}-l55", f"#{p}-n75", f"#{p}-n55",
           f"#{p}-o1", f"#{p}-o2", f"#{p}-o3", f"#{p}-osrc", f"#{p}-split", f"#{p}-cyc", f"#{p}-drop",
           *[f"#{p}-c{k2}" for k2 in range(4)], f"#{p}-lin", f"#{p}-lout", f"#{p}-lout2")
    c.pop(f"#{p}-me", 0.2, 0.6, "50% 100%", "back.out(1.4)", 0.6)
    c.tl.ft(f"#{p}-me-water", {"y": 600}, {"y": 0, "duration": 1.6, "ease": "power2.out"}, c.at("04", "sáu mươi phần trăm", off=-0.8))
    c.sfx("whoosh", c.at("04", "sáu mươi phần trăm", off=-0.4))
    popl(c, f"#{p}-l60", c.at("04", "sáu mươi phần trăm", off=0.6), "0% 50%")
    t = c.at("04", "Trẻ sơ sinh")
    c.show(f"#{p}-mini", t)
    popl(c, f"#{p}-baby", t, "50% 100%")
    c.tl.ft(f"#{p}-baby-water", {"y": 600}, {"y": 0, "duration": 1.0, "ease": "power2.out"}, t + 0.2)
    c.blur_in(f"#{p}-l75", t + 0.6)
    c.blur_in(f"#{p}-n75", t + 0.6)
    t = c.at("04", "Người cao tuổi")
    popl(c, f"#{p}-old", t, "50% 100%")
    c.tl.ft(f"#{p}-old-water", {"y": 600}, {"y": 0, "duration": 1.0, "ease": "power2.out"}, t + 0.2)
    c.blur_in(f"#{p}-l55", t + 0.6)
    c.blur_in(f"#{p}-n55", t + 0.6)
    t = c.at("04", "Mỗi cơ quan")
    c.blur_out(f"#{p}-mini", t, 0.25)
    c.blur_out(f"#{p}-l60", t, 0.25)
    c.show(f"#{p}-org", t)
    popl(c, f"#{p}-o1", c.at("04", "não và tim"), "0% 50%")
    c.blur_in(f"#{p}-osrc", c.at("04", "não và tim"))
    popl(c, f"#{p}-o2", c.at("04", "Phổi"), "0% 50%")
    popl(c, f"#{p}-o3", c.at("04", "xương"), "0% 50%")
    t = c.at("04", "hai phần ba")
    for sel in (f"#{p}-me", f"#{p}-org"):
        c.blur_out(sel, t - 0.5, 0.25)
    c.show(f"#{p}-split", t - 0.3)
    c.hide(f"#{p}-in", f"#{p}-out")
    c.tl.ft(f"#{p}-in", {"autoAlpha": 1, "scaleX": 0, "transformOrigin": "0% 50%"},
            {"autoAlpha": 1, "scaleX": 1, "transformOrigin": "0% 50%", "duration": 0.7, "ease": "expo.out"}, t)
    c.sfx("whoosh", t)
    c.blur_in(f"#{p}-lin", t + 0.5)
    t = c.at("04", "Phần còn lại")
    c.tl.ft(f"#{p}-out", {"autoAlpha": 1, "scaleX": 0, "transformOrigin": "0% 50%"},
            {"autoAlpha": 1, "scaleX": 1, "transformOrigin": "0% 50%", "duration": 0.5, "ease": "expo.out"}, t)
    c.blur_in(f"#{p}-lout", t + 0.4)
    c.blur_in(f"#{p}-lout2", c.at("04", "trong máu"))
    t = c.at("04", "không hề đứng yên")
    c.show(f"#{p}-cyc", t)
    c.tl.ft(f"#{p}-ring", {"rotation": 0}, {"rotation": 360, "svgOrigin": "1280 820", "duration": 8, "ease": "none"}, t)
    for k2, w in enumerate(("chảy", "bốc hơi", "được lọc", "thay mới")):
        popl(c, f"#{p}-c{k2}", c.at("04", w), snd="pop")
    t = c.at("04", "một giọt nước")
    c.blur_out(f"#{p}-cyc", t - 0.3, 0.25)
    c.blur_out(f"#{p}-split", t - 0.3, 0.25)
    popl(c, f"#{p}-drop", t, "50% 100%")
    c.tl.to(f"#{p}-drop", {"x": -500, "duration": 1.6, "ease": "power2.inOut"}, c.at("04", "ba công việc chính"))
    c.hide(f"#{p}-l3")
    c.blur_in(f"#{p}-l3", c.at("04", "theo chân"))
    return c


# ---------------------------------------------------------------- 05 · Con sông vận chuyển
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
              label(f"{p}-lh", 940, 340, "HUYẾT TƯƠNG: CHỦ YẾU LÀ NƯỚC", 50, WHITE),
              label(f"{p}-ln", 1250, 700, "DINH DƯỠNG + OXY →", 48, YELLOW, "middle"),
              label(f"{p}-lw", 1250, 770, "← CHẤT THẢI", 48, GREY, "middle"),
              g(f"{p}-gut", f'<path d="M820 900 a70 70 0 1 1 0.1 0" fill="none" stroke="{WATER}" stroke-width="14" stroke-dasharray="36 22"/>'
                + label(f"{p}-g1", 940, 880, "RUỘT: ~8 LÍT DỊCH MỖI NGÀY", 50, WHITE)
                + label(f"{p}-g2", 940, 950, "→ HẤP THU LẠI GẦN HẾT", 46, WATER))]
    close()
    end = c.loc(SCENES["05"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 2)
    c.hide(f"#{p}-lh", f"#{p}-ln", f"#{p}-lw", f"#{p}-gut", f"#{p}-g1", f"#{p}-g2")
    c.pop(f"#{p}-riv", 0.1, 0.6, "0% 50%", "expo.out", 0.6)
    c.pop(f"#{p}-heart", 0.3, 0.5)
    t_dry = c.at("05", "Khi thiếu nước")
    t_fast = c.at("05", "Tim phải")
    beats = int((t_fast - 0.3) / 0.8)
    c.tl.ft(f"#{p}-heart", {"scale": 1}, {"scale": 1.12, "transformOrigin": "50% 60%", "duration": 0.4, "ease": "sine.inOut",
                                          "yoyo": True, "repeat": beats * 2 - 1}, 0.8)
    c.tl.ft(f"#{p}-heart", {"scale": 1}, {"scale": 1.14, "transformOrigin": "50% 60%", "duration": 0.22, "ease": "sine.inOut",
                                          "yoyo": True, "repeat": int((end - t_fast) / 0.44) * 2 - 1}, t_fast + 0.1)
    for k in range(8):
        c.tl.ft(f"#{p}-r{k}", {"x": 0}, {"x": 1400, "duration": 4.2, "ease": "none", "repeat": 5}, 0.1 + k * 0.52)
    t_n = c.at("05", "chất dinh dưỡng")
    for k in range(6):
        c.tl.ft(f"#{p}-y{k}", {"x": 0}, {"x": 1400, "duration": 4.6, "ease": "none", "repeat": 3}, t_n - 1.5 + k * 0.75)
    t_w = c.at("05", "chất thải")
    for k in range(6):
        c.tl.ft(f"#{p}-w{k}", {"x": 0}, {"x": -1400, "duration": 4.6, "ease": "none", "repeat": 3}, t_w - 1.2 + k * 0.75)
    popl(c, f"#{p}-lh", c.at("05", "huyết tương"), "0% 50%")
    popl(c, f"#{p}-ln", t_n)
    popl(c, f"#{p}-lw", t_w)
    t = c.at("05", "Trong ruột")
    c.show(f"#{p}-gut", t)
    popl(c, f"#{p}-g1", t, "0% 50%")
    c.blur_in(f"#{p}-g2", c.at("05", "Rồi gần như"))
    for sel in (f"#{p}-ln", f"#{p}-lw"):
        c.blur_out(sel, t - 0.2, 0.2)
    c.blur_out(f"#{p}-gut", t_dry - 0.2, 0.25)
    c.tl.to(f"#{p}-wt", {"y": 50, "duration": 1.2, "ease": "power2.inOut"}, t_dry + 0.3)
    c.tl.to(f"#{p}-wb", {"y": -50, "duration": 1.2, "ease": "power2.inOut"}, t_dry + 0.3)
    c.tl.to(f"#{p}-water", {"scaleY": 0.45, "transformOrigin": "50% 50%", "duration": 1.2, "ease": "power2.inOut"}, t_dry + 0.3)
    c.sfx("whoosh", t_dry + 0.3)
    return c


# ---------------------------------------------------------------- 06 · Máy điều hòa
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
    c.svg += [g(f"{p}-skin", skin + text(680, 880, "DA", 44, 900, "#9A5A3A")), g(f"{p}-drops", drops), g(f"{p}-vap", vapor + heat),
              thermometer(f"{p}-th", 1780, 400, 1.1, 0.85),
              sun(f"{p}-sun", 1520, 170, 0.9), pictogram(f"{p}-run", 1260, 230, 0.9, "run"),
              label(f"{p}-l2", 1150, 500, "≈ 2 LÍT / GIỜ", 100, YELLOW, "middle")]
    close()
    end = c.loc(SCENES["06"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 0)
    c.hide(f"#{p}-sun", f"#{p}-run", f"#{p}-l2", *[f"#{p}-d{k}" for k in range(7)], *[f"#{p}-h{k}" for k in range(0, 7, 2)])
    c.pop(f"#{p}-skin", 0.1, 0.6, "50% 100%", "expo.out", 0.7)
    c.pop(f"#{p}-th", 0.4, 0.5, "50% 100%")
    t = c.at("06", "da tiết mồ hôi")
    for k in range(7):
        c.pop(f"#{p}-d{k}", t + 0.08 * k, 0.4, "50% 100%")
    c.sfx("pop", t)
    t = c.at("06", "bay hơi")
    for k in range(7):
        c.draw(f"#{p}-v{k}", t + 0.07 * k, 0.8)
        c.tl.to(f"#{p}-d{k}", {"scale": 0.4, "opacity": 0.4, "transformOrigin": "50% 100%", "duration": 0.8}, t + 0.07 * k)
    for k in range(0, 7, 2):
        c.show(f"#{p}-h{k}", c.at("06", "một phần nhiệt"))
        c.tl.ft(f"#{p}-h{k}", {"y": 40}, {"y": -160, "duration": 1.6, "ease": "power1.out"}, c.at("06", "một phần nhiệt"))
        c.tl.to(f"#{p}-h{k}", {"opacity": 0, "duration": 0.4}, c.at("06", "một phần nhiệt", off=1.3))
    c.tl.to(f"#{p}-th-hg", {"scaleY": 0.6, "transformOrigin": "50% 100%", "duration": 1.4, "ease": "power2.inOut"}, c.at("06", "một phần nhiệt"))
    c.sfx("whoosh", c.at("06", "một phần nhiệt"))
    popl(c, f"#{p}-sun", c.at("06", "Trời càng nóng"))
    popl(c, f"#{p}-run", c.at("06", "vận động"))
    t = c.at("06", "hai lít mỗi giờ")
    c.blur_out(f"#{p}-vap", t - 0.3, 0.25)
    popl(c, f"#{p}-l2", t, snd="thump", dur=0.5)
    for k in range(7):
        c.tl.to(f"#{p}-d{k}", {"scale": 1.3, "opacity": 1, "transformOrigin": "50% 100%", "duration": 0.4, "ease": "back.out(2)"}, t + 0.05 * k)
    return c


# ---------------------------------------------------------------- 07 · Nhà máy lọc
def s07():
    c = comp("07")
    p = c.cid
    close = board(c)
    c.svg += [g(f"{p}-kid", kidney(f"{p}-k1", 1150, 470, 1.0) + kidney(f"{p}-k2", 1420, 470, 1.0, flip=True)),
              g(f"{p}-pipe", f'<path d="M680 470 H1020 M990 440 L1030 470 L990 500" fill="none" stroke="{RED}" stroke-width="22" '
                             f'stroke-linecap="round" stroke-linejoin="round"/>' + label(f"{p}-lm", 700, 430, "MÁU", 48, RED)),
              g(f"{p}-tub", bathtub(f"{p}-bt", 900, 830, 0.8) + label(f"{p}-l180", 900, 990, "≈ 180 LÍT / NGÀY", 54, WHITE, "middle")),
              g(f"{p}-loop", f'<path id="{p}-arc" d="M1100 340 C1150 180 1420 180 1470 340" pathLength="1" stroke-dasharray="1 1.2" '
                             f'stroke-dashoffset="1.1" fill="none" stroke="{TEAL}" stroke-width="16" stroke-linecap="round"/>'
                + label(f"{p}-l99", 1285, 170, "> 99% HẤP THU LẠI", 54, TEAL, "middle")),
              g(f"{p}-uri", glass(f"{p}-gl", 1450, 930, 0.6, 0.6) + label(f"{p}-l15", 1450, 1010, "NƯỚC TIỂU ≈ 1,5 LÍT", 44, WHITE, "middle")),
              g(f"{p}-adj", label(f"{p}-a1", 1700, 640, "THIẾU → GIỮ LẠI", 40, WATER, "middle")
                + label(f"{p}-a2", 1700, 700, "THỪA → THẢI BỚT", 40, YELLOW, "middle")),
              g(f"{p}-gau", gauge(f"{p}-gg", 1720, 340, 110, "TỐC ĐỘ THẢI"))]
    close()
    end = c.loc(SCENES["07"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 3)
    c.hide(f"#{p}-tub", f"#{p}-loop", f"#{p}-uri", f"#{p}-adj", f"#{p}-gau", f"#{p}-pipe", f"#{p}-l99", f"#{p}-a1", f"#{p}-a2")
    c.pop(f"#{p}-kid", 0.2, 0.6, "50% 50%", "back.out(1.4)", 0.4)
    t = c.at("07", "hai quả thận")
    c.pop(f"#{p}-pipe", t, 0.5, "0% 50%", "expo.out", 0.2)
    t = c.at("07", "một trăm tám mươi")
    popl(c, f"#{p}-tub", t, "50% 100%")
    t = c.at("07", "hơn chín mươi chín")
    c.show(f"#{p}-loop", t)
    c.draw(f"#{p}-arc", t, 0.7)
    c.pop(f"#{p}-l99", t + 0.3, 0.45)
    c.sfx("whoosh", t)
    t = c.at("07", "một lít rưỡi")
    popl(c, f"#{p}-uri", t, "50% 100%")
    t = c.at("07", "biết điều chỉnh")
    c.show(f"#{p}-adj", t)
    c.blur_in(f"#{p}-a1", c.at("07", "giữ lại"))
    c.blur_in(f"#{p}-a2", c.at("07", "thải bớt"))
    t = c.at("07", "giới hạn tốc độ")
    c.blur_out(f"#{p}-adj", t - 0.2, 0.2)
    popl(c, f"#{p}-gau", t, "50% 100%")
    c.tl.ft(f"#{p}-gg-n", {"rotation": -60}, {"rotation": 78, "svgOrigin": "1720 340", "duration": 1.2, "ease": "power2.inOut"}, t + 0.3)
    c.tl.ft(f"#{p}-gg-n", {"rotation": 78}, {"rotation": 84, "svgOrigin": "1720 340", "duration": 0.1, "yoyo": True, "repeat": 7,
                                             "ease": "none"}, t + 1.6)
    return c


# ---------------------------------------------------------------- 08 · Chiếc cân nước
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
              label(f"{p}-lo", 866, 230, "RA", 60, CORAL, "middle"), label(f"{p}-li", 1614, 230, "VÀO", 60, TEAL, "middle"),
              text(866, 620, "NƯỚC TIỂU · MỒ HÔI · HƠI THỞ", 30, 800, GREY, "middle", id_=f"{p}-lo2"),
              text(1614, 620, "ĐỒ UỐNG · THỨC ĂN", 30, 800, GREY, "middle", id_=f"{p}-li2"),
              label(f"{p}-lt", 1240, 960, "≈ 2–3 LÍT MỖI NGÀY (TÍNH CẢ THỨC ĂN)", 54, YELLOW, "middle"),
              label(f"{p}-lm", 1614, 700, "+ một ít từ chuyển hóa", 34, GREY, "middle", 800)]
    close()
    end = c.loc(SCENES["08"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 2)
    c.hide(*[f"#{p}-i{k}" for k in range(1, 7)], f"#{p}-lo", f"#{p}-li", f"#{p}-lo2", f"#{p}-li2", f"#{p}-lt", f"#{p}-lm")
    c.pop(f"#{p}-bal", 0.15, 0.6, "50% 100%", "back.out(1.4)", 0.5)
    BEAM = {"transformOrigin": "50% 5.7%"}
    popl(c, f"#{p}-lo", c.at("08", "Bên trái"))
    for k, w in ((1, "nước tiểu"), (2, "mồ hôi"), (3, "hơi thở")):
        popl(c, f"#{p}-i{k}", c.at("08", w), "50% 100%")
    c.blur_in(f"#{p}-lo2", c.at("08", "hơi thở"))
    t = c.at("08", "ngồi yên")
    c.tl.ft(f"#{p}-bal-beam", {"rotation": 0, **BEAM}, {"rotation": -5, **BEAM, "duration": 0.8, "ease": "power2.inOut"}, t)
    popl(c, f"#{p}-li", c.at("08", "Bên phải"))
    popl(c, f"#{p}-i4", c.at("08", "đồ uống"), "50% 100%")
    popl(c, f"#{p}-i5", c.at("08", "từ thức ăn"), "50% 100%")
    c.blur_in(f"#{p}-li2", c.at("08", "từ thức ăn"))
    c.tl.to(f"#{p}-bal-beam", {"rotation": 0, **BEAM, "duration": 0.8, "ease": "back.out(1.6)"}, c.at("08", "từ thức ăn", off=0.2))
    t = c.at("08", "tự tạo ra")
    popl(c, f"#{p}-i6", t, "50% 100%")
    c.blur_in(f"#{p}-lm", t + 0.3)
    popl(c, f"#{p}-lt", c.at("08", "hai đến ba lít"), dur=0.5)
    t = c.at("08", "lệch nhau")
    c.tl.to(f"#{p}-bal-beam", {"rotation": -8, **BEAM, "duration": 0.35, "ease": "power2.out"}, t)
    c.tl.to(f"#{p}-bal-beam", {"rotation": 0, **BEAM, "duration": 0.9, "ease": "elastic.out(1, 0.4)"}, t + 0.8)
    c.sfx("whoosh", t)
    return c


# ---------------------------------------------------------------- 09 · Bộ cảm biến
def s09():
    c = comp("09")
    p = c.cid
    close = board(c, ("suy-nghi", "vui"), look=(6, -6))
    GX, GY = 1420, 520
    c.svg += [brain(f"{p}-br", 960, 300, 1.1), gauge(f"{p}-gg", GX, GY, 150, "ĐỘ ĐẶC CỦA MÁU"),
              lamp(f"{p}-off", 1760, 300, "#4A5A68", 46), lamp(f"{p}-yel", 1760, 300, YELLOW, 46), lamp(f"{p}-red", 1760, 300, CORAL, 46),
              label(f"{p}-pct", GX, GY - 210, "+1–2%", 64, YELLOW, "middle"),
              g(f"{p}-adh", f'<rect x="-70" y="-40" width="140" height="80" rx="40" fill="{YELLOW}" stroke="{INK}" stroke-width="6"/>'
                + text(0, 18, "ADH", 48, 900, INK, "middle")),
              kidney(f"{p}-kid", 1180, 860, 0.7),
              f'<rect id="{p}-uri" x="1330" y="790" width="110" height="150" rx="22" fill="{URINE[1]}" stroke="{INK}" stroke-width="6"/>',
              text(1385, 990, "NƯỚC TIỂU", 32, 800, GREY, "middle", id_=f"{p}-urit"),
              bubble(f"{p}-thirst", 600, 380, 300, 120, "KHÁT!", YELLOW, INK, 64),
              glass(f"{p}-gl", 600, 960, 0.6, 0.85),
              pictogram(f"{p}-old", 1680, 850, 1.0, "elder"),
              label(f"{p}-lold", 1680, 1010, "KHÁT CHẬM, YẾU HƠN", 44, GREY, "middle")]
    close()
    end = c.loc(SCENES["09"]["end"])
    c.svg[-1:-1] = []
    c.hide(f"#{p}-yel", f"#{p}-red", f"#{p}-pct", f"#{p}-adh", f"#{p}-kid", f"#{p}-uri", f"#{p}-urit", f"#{p}-thirst",
           f"#{p}-gl", f"#{p}-old", f"#{p}-lold", f"#{p}-gg", f"#{p}-off")
    popl(c, f"#{p}-br", c.at("09", "bộ cảm biến"))
    t = c.at("09", "loãng hay đặc")
    c.pop(f"#{p}-gg", t - 0.4, 0.5, "50% 100%")
    c.pop(f"#{p}-off", t - 0.2, 0.4)
    N = f"#{p}-gg-n"
    O = {"svgOrigin": f"{GX} {GY}"}
    c.tl.ft(N, {"rotation": -10, **O}, {"rotation": 10, **O, "duration": 0.6, "ease": "sine.inOut", "yoyo": True, "repeat": 3}, t)
    t = c.at("09", "máu đặc lên")
    c.tl.to(N, {"rotation": 35, **O, "duration": 0.9, "ease": "power2.inOut"}, t)
    t = c.at("09", "một đến hai phần trăm")
    c.tl.to(N, {"rotation": 52, **O, "duration": 0.6, "ease": "power2.out"}, t)
    popl(c, f"#{p}-pct", t)
    c.show(f"#{p}-yel", c.at("09", "bật đèn báo"))
    c.sfx("pop", c.at("09", "bật đèn báo"))
    t = c.at("09", "hormone")
    c.show(f"#{p}-adh", t)
    c.tl.ft(f"#{p}-adh", {"x": 960, "y": 400, "scale": 0}, {"x": 960, "y": 400, "scale": 1, "duration": 0.4, "ease": "back.out(2)"}, t)
    c.sfx("pop", t)
    t = c.at("09", "ra lệnh cho thận")
    c.pop(f"#{p}-kid", t - 0.3, 0.45)
    c.show(f"#{p}-uri", t - 0.3)
    c.show(f"#{p}-urit", t - 0.3)
    c.tl.to(f"#{p}-adh", {"x": 1180, "y": 740, "duration": 1.0, "ease": "power2.inOut"}, t)
    c.sfx("whoosh", t)
    c.tl.to(f"#{p}-uri", {"attr": {"fill": URINE[4]}, "scaleY": 0.6, "transformOrigin": "50% 100%", "duration": 1.0},
            c.at("09", "sẫm màu hơn", off=-0.4))
    t = c.at("09", "cảm giác khát")
    c.show(f"#{p}-red", t)
    popl(c, f"#{p}-thirst", t, "20% 100%", snd="thump")
    t = c.at("09", "Bạn uống")
    popl(c, f"#{p}-gl", t, "50% 100%")
    c.tl.to(N, {"rotation": 0, **O, "duration": 1.0, "ease": "power2.inOut"}, t + 0.3)
    c.blur_out(f"#{p}-thirst", t + 0.3, 0.2)
    c.show(f"#{p}-red", c.at("09", "đèn báo tắt"), False)
    c.show(f"#{p}-yel", c.at("09", "đèn báo tắt"), False)
    c.tl.to(f"#{p}-uri", {"attr": {"fill": URINE[1]}, "scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.8}, t + 0.6)
    c.tl.to(f"#{p}-adh", {"opacity": 0, "duration": 0.3}, t + 0.3)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", t + 0.2)
    t = c.at("09", "người cao tuổi")
    for sel in (f"#{p}-kid", f"#{p}-uri", f"#{p}-urit", f"#{p}-gl"):
        c.blur_out(sel, t - 0.3, 0.2)
    popl(c, f"#{p}-old", t)
    c.blur_in(f"#{p}-lold", c.at("09", "chậm và yếu"))
    c.tl.to(N, {"rotation": 55, **O, "duration": 1.2, "ease": "power2.inOut"}, t + 0.4)
    c.show(f"#{p}-yel", c.at("09", "chậm và yếu", off=0.3))
    c.tl.ft(f"#{p}-yel", {"opacity": 0.25}, {"opacity": 0.6, "duration": 0.5, "yoyo": True, "repeat": 3}, c.at("09", "chậm và yếu", off=0.3))
    idle(c, f"{p}-suy-nghi", 0, c.at("09", "Bạn uống"), 1)
    idle(c, f"{p}-vui", c.at("09", "Bạn uống", off=0.8), end, 2)
    return c


# ---------------------------------------------------------------- 10 · Khi thiếu nước
def s10():
    c = comp("10")
    p = c.cid
    close = board(c, ("suy-nghi", "lo-lang"))

    def panel(id_, x, title, lines, icons):
        body = (f'<rect x="{x}" y="160" width="560" height="560" rx="30" fill="#1D4262" stroke="{INK}" stroke-width="6"/>'
                + text(x + 280, 240, title, 54, 900, YELLOW, "middle") + icons
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
    c.svg += [panel(f"{p}-pa", 680, "NỮ · MẤT ~1,4%", ["ĐAU ĐẦU · MỆT", "KHÓ TẬP TRUNG"], icons_f),
              panel(f"{p}-pb", 1300, "NAM · MẤT NƯỚC NHẸ", ["KÉM TỈNH TÁO", "TRÍ NHỚ TẠM THỜI GIẢM"], icons_m),
              f'<g transform="translate(1270 830) rotate(-3)"><g id="{p}-stamp"><rect x="-520" y="-56" width="1040" height="100" rx="14" '
              f'fill="{SLATE}" stroke="{YELLOW}" stroke-width="8"/>{text(0, 16, "KẾT QUẢ GIỮA CÁC NGHIÊN CỨU CHƯA THỐNG NHẤT", 42, 900, YELLOW, "middle")}</g></g>',
              text(1270, 990, "Armstrong 2012 · Ganio 2011", 28, 500, GREY, "middle", id_=f"{p}-src"),
              g(f"{p}-sport", sun(f"{p}-sun", 1600, 260, 0.9) + pictogram(f"{p}-run", 1000, 420, 1.6, "run")
                + label(f"{p}-l2", 1270, 760, "MẤT > 2% CÂN NẶNG → GIẢM SỨC BỀN", 54, YELLOW, "middle")
                + text(1270, 840, "nhất là khi trời nóng · ACSM 2007", 34, 600, GREY, "middle")),
              g(f"{p}-sev", place(1270, 330, g(f"{p}-cross", f'<circle r="110" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                                                              f'<path d="M-25 -65 H25 V-25 H65 V25 H25 V65 H-25 V25 H-65 V-25 H-25 Z" fill="#FFFFFF"/>'))
                + label(f"{p}-s1", 1270, 580, "TIÊU CHẢY, NÔN KÉO DÀI → NGUY HIỂM", 58, CORAL, "middle")
                + label(f"{p}-s2", 1270, 680, "BÙ NƯỚC + MUỐI (ORESOL) · ĐI KHÁM NGAY", 54, WHITE, "middle")),
              label(f"{p}-t3", 1270, 560, "15:00", 160, WHITE, "middle")]
    close()
    end = c.loc(SCENES["10"]["end"])
    c.hide(f"#{p}-pa", f"#{p}-pb", f"#{p}-stamp", f"#{p}-src", f"#{p}-sport", f"#{p}-sev", f"#{p}-s1", f"#{p}-s2", f"#{p}-t3")
    t = c.at("10", "Trong một thí nghiệm")
    popl(c, f"#{p}-pa", t, "50% 100%")
    c.blur_in(f"#{p}-src", t)
    t = c.at("10", "Một thí nghiệm khác")
    popl(c, f"#{p}-pb", t, "50% 100%")
    t = c.at("10", "Kết quả giữa")
    c.show(f"#{p}-stamp", t)
    c.tl.ft(f"#{p}-stamp", {"scale": 1.6, "transformOrigin": "50% 50%"}, {"scale": 1, "transformOrigin": "50% 50%", "duration": 0.3,
                                                                          "ease": "power4.in"}, t)
    c.sfx("thump", t + 0.3)
    t = c.at("10", "Nhưng với vận động")
    for sel in (f"#{p}-pa", f"#{p}-pb", f"#{p}-stamp", f"#{p}-src"):
        c.blur_out(sel, t, 0.25)
    c.show(f"#{p}-sport", t + 0.2)
    c.tl.ft(f"#{p}-run", {"x": -300}, {"x": 0, "duration": 0.8, "ease": "expo.out"}, t + 0.2)
    c.sfx("whoosh", t + 0.2)
    t = c.at("10", "mất nước nặng")
    c.blur_out(f"#{p}-sport", t - 0.3, 0.25)
    c.show(f"#{p}-sev", t)
    c.pop(f"#{p}-cross", t, 0.5)
    c.sfx("thump", t)
    c.blur_in(f"#{p}-s1", c.at("10", "rất nguy hiểm", off=-0.4))
    c.blur_in(f"#{p}-s2", c.at("10", "Lúc đó cần"))
    t = c.at("10", "Đau đầu, uể oải")
    c.blur_out(f"#{p}-sev", t - 0.3, 0.25)
    swap(c, f"{p}-suy-nghi", f"{p}-lo-lang", t)
    popl(c, f"#{p}-t3", c.at("10", "ba giờ chiều"), snd="thump")
    idle(c, f"{p}-suy-nghi", 0, t, 1)
    idle(c, f"{p}-lo-lang", t + 0.6, end, 2)
    return c


HAIR_C = "#1E2A3A"


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
    return (opt_row(f"{prefix}a", x, 300, "A", eight, "ĐÚNG 8 CỐC MỖI NGÀY")
            + opt_row(f"{prefix}b", x, 530, "B", check, "KHÁT THÌ UỐNG + KHI CẦN")
            + opt_row(f"{prefix}c", x, 760, "C", spill, "CÀNG NHIỀU CÀNG TỐT"))


# ---------------------------------------------------------------- 11 · Câu hỏi
def s11():
    c = comp("11")
    p = c.cid
    close = board(c)
    c.svg.append(options(f"{p}-o"))
    close()
    idle(c, f"{p}-suy-nghi", 0, c.loc(SCENES["11"]["end"]), 2)
    for L in "abc":
        t = c.at("11", L.upper())
        c.hide(f"#{p}-o{L}")
        c.tl.ft(f"#{p}-o{L}", {"autoAlpha": 0, "x": 60, "filter": "blur(8px)"},
                {"autoAlpha": 1, "x": 0, "filter": "blur(0px)", "duration": 0.45, "ease": "expo.out"}, t)
        c.sfx("pop", t)
        c.tl.to(f"#{p}-suy-nghi .mat", {"y": {"a": -6, "b": 0, "c": 6}[L], "duration": 0.2}, t)
    return c


# ---------------------------------------------------------------- 12 · Thử đoán
def s12():
    c = comp("12")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>',
              f'<circle cx="1590" cy="560" r="220" fill="{WATER}" stroke="{INK}" stroke-width="10"/>',
              text(1590, 300, "TẠM DỪNG VIDEO", 44, 900, INK, "middle"),
              g("s12-n", "".join(text(1590, 660, str(n), 300, 900, INK, "middle", id_=f"s12-n{n}") for n in (3, 2, 1)))]
    lines = [("h", "Thử đoán trước nhé!"),
             ("f", "1. Cơ thể mất nước liên tục, kể cả khi ngồi yên."),
             ("f", "2. Máu đặc lên → não tiết ADH giữ nước, rồi gây khát."),
             ("f", "3. Nhu cầu đổi theo thời tiết, vận động, tuổi tác."),
             ("f", "4. Thận có giới hạn tốc độ thải nước."),
             ("o", "A. Đúng 8 cốc mỗi ngày"), ("o", "B. Khát thì uống, uống thêm khi cần, nhìn màu nước tiểu"),
             ("o", "C. Càng nhiều càng tốt")]
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


# ---------------------------------------------------------------- 13 · Chìa khóa
def s13():
    c = comp("13")
    p = c.cid
    close = board(c, look=(6, -6))
    c.svg.append(g(f"{p}-bub", f"""<circle cx="560" cy="560" r="18" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>
<circle cx="640" cy="500" r="28" fill="{PAPER}" stroke="{INK}" stroke-width="6"/>
<path d="M760 420 C700 300 820 170 980 210 C1060 120 1300 110 1380 190 C1520 120 1760 190 1740 320 C1830 380 1790 560 1640 560 C1580 650 1340 650 1260 590 C1140 660 900 650 860 560 C720 590 650 470 760 420 Z" fill="{PAPER}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
{balance(f"{p}-bal", 1010, 300, 0.3)}
{text(1200, 340, "CON SỐ CỐ ĐỊNH", 50, 900, INK)}
<line id="{p}-strike" x1="1190" y1="322" x2="1610" y2="322" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>
{text(1220, 470, "CÂN BẰNG", 96, 900, WATER_DARK, id_=f"{p}-cb")}"""))
    close()
    c.css.append(f"#{p}-qs {{ left: 700px; top: 770px; width: 1120px; font-size: 76px; font-weight: 800; color: {WHITE}; "
                 f"line-height: 1.15; }} #{p}-qs b {{ color: {YELLOW}; font-weight: 900; }}")
    c.html.append(f'<div id="{p}-qs" class="txt">Con số <b>8 cốc</b> từ đâu ra?</div>')
    idle(c, f"{p}-suy-nghi", 0, c.loc(SCENES["13"]["end"]), 0)
    c.pop(f"#{p}-bub", 0.15, 0.6, "0% 100%", "back.out(1.3)", 0.3)
    c.sfx("pop", 0.15)
    c.draw(f"#{p}-strike", c.at("13", "con số cố định", which="end", off=-0.3), 0.4)
    c.sfx("pop", c.at("13", "con số cố định", which="end"))
    c.blur_in(f"#{p}-cb", c.at("13", "Nó cần cân bằng"), 0.2)
    c.blur_in(f"#{p}-qs", c.at("13", "Vậy con số"), 0.2)
    return c


# ---------------------------------------------------------------- 14 · Con số tám cốc
def s14():
    c = comp("14")
    p = c.cid
    close = board(c, look=(7, -2))
    glasses8 = "".join(glass(f"{p}-g{k}", 740 + k * 145, 600, 0.5, 0.75) for k in range(8))
    cols = [(820, "NỮ", "2,0 L", 0.62), (1060, "NAM", "2,5 L", 0.78), (1420, "NỮ", "2,7 L", 0.84), (1660, "NAM", "3,7 L", 1.0)]
    tall = "".join(g(f"{p}-t{k}", glass(f"{p}-tg{k}", x, 690, 0.8, lv) + label(f"{p}-tl{k}", x, 760, sx, 42, GREY, "middle") + label(f"{p}-tv{k}", x, 820, v, 52, WHITE, "middle"))
                   for k, (x, sx, v, lv) in enumerate(cols))
    c.svg += [g(f"{p}-eight", glasses8), label(f"{p}-l2", 1250, 760, "8 × 250 ML ≈ 2 LÍT", 70, YELLOW, "middle"),
              report1945(f"{p}-rep", 760, 250), magnifier(f"{p}-mag", 1500, 470, 1.2),
              label(f"{p}-lv", 1580, 720, "HEINZ VALTIN · 2002", 52, WHITE, "middle"),
              label(f"{p}-lno", 1560, 830, "8 CỐC: KHÔNG CÓ CƠ SỞ CỐ ĐỊNH", 42, CORAL, "middle"),
              tall, label(f"{p}-heu", 940, 420, "CHÂU ÂU · EFSA 2010", 46, TEAL, "middle"),
              label(f"{p}-hus", 1540, 420, "MỸ · 2004", 46, TEAL, "middle"),
              label(f"{p}-food", 1250, 900, "TỔNG LƯỢNG NƯỚC, TÍNH CẢ NƯỚC TRONG THỨC ĂN", 40, YELLOW, "middle"),
              text(1250, 980, "Dựa trên lượng nước người khỏe mạnh thường nạp vào", 34, 600, GREY, "middle", id_=f"{p}-why")]
    close()
    end = c.loc(SCENES["14"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 3)
    c.hide(f"#{p}-l2", f"#{p}-rep", f"#{p}-mag", f"#{p}-lv", f"#{p}-lno", f"#{p}-heu", f"#{p}-hus", f"#{p}-food", f"#{p}-why",
           *[f"#{p}-g{k}" for k in range(8)], *[f"#{p}-t{k}" for k in range(4)])
    t = c.at("14", "Tám cốc")
    for k in range(8):
        c.pop(f"#{p}-g{k}", t + 0.08 * k, 0.35, "50% 100%")
    c.sfx("pop", t)
    popl(c, f"#{p}-l2", c.at("14", "khoảng hai lít", 0), snd="thump")
    t = c.at("14", "Năm 1945")
    c.blur_out(f"#{p}-eight", t - 0.2, 0.25)
    c.blur_out(f"#{p}-l2", t - 0.2, 0.25)
    c.pop(f"#{p}-rep", t, 0.6, "50% 100%", "back.out(1.4)", 0.6)
    c.sfx("whoosh", t)
    c.tl.to(f"#{p}-rep-hl1", {"opacity": 1, "duration": 0.3}, c.at("14", "hai lít rưỡi"))
    c.tl.to(f"#{p}-rep-hl2", {"opacity": 1, "duration": 0.3}, c.at("14", "sẵn trong thức ăn"))
    t = c.at("14", "Năm 2002")
    popl(c, f"#{p}-mag", t)
    c.blur_in(f"#{p}-lv", t + 0.2)
    t = c.at("14", "bị bỏ quên")
    c.tl.to(f"#{p}-mag", {"x": -500, "y": 190, "duration": 0.8, "ease": "power2.inOut"}, t - 0.6)
    c.tl.ft(f"#{p}-rep-hl2", {"opacity": 1}, {"opacity": 0.2, "duration": 0.2, "yoyo": True, "repeat": 5}, t)
    popl(c, f"#{p}-lno", c.at("14", "không tìm thấy bằng chứng"), snd="thump")
    t = c.at("14", "Ngày nay")
    for sel in (f"#{p}-rep", f"#{p}-mag", f"#{p}-lv", f"#{p}-lno"):
        c.blur_out(sel, t - 0.2, 0.25)
    c.blur_in(f"#{p}-heu", c.at("14", "châu Âu"))
    popl(c, f"#{p}-t0", c.at("14", "hai lít mỗi ngày cho nữ"), "50% 100%")
    popl(c, f"#{p}-t1", c.at("14", "Với nam"), "50% 100%")
    c.blur_in(f"#{p}-food", c.at("14", "tính cả nước trong thức ăn"))
    c.blur_in(f"#{p}-hus", c.at("14", "Ở Mỹ", 1))
    t = c.at("14", "Khoảng hai phẩy bảy")
    popl(c, f"#{p}-t2", t, "50% 100%")
    popl(c, f"#{p}-t3", c.at("14", "ba phẩy bảy"), "50% 100%")
    c.blur_out(f"#{p}-food", c.at("14", "Con số khác nhau"), 0.2)
    c.blur_in(f"#{p}-why", c.at("14", "Họ dựa vào"))
    return c


# ---------------------------------------------------------------- 15 · Nước đến từ đâu
def s15():
    c = comp("15")
    p = c.cid
    close = board(c, look=(7, 0))
    can = place(1640, 430, g(f"{p}-can", f'<rect x="-50" y="-100" width="100" height="190" rx="16" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
                                          f'<rect x="-36" y="-118" width="72" height="22" rx="8" fill="{GREY}" stroke="{INK}" stroke-width="5"/>'
                                          f'<path d="M-50 -20 H50" stroke="#FFFFFF" stroke-width="10"/>'))
    c.svg += [watermelon(f"{p}-wm", 790, 470, 1.0), bowl(f"{p}-soup", 1020, 470, 0.85), bowl(f"{p}-rice", 1240, 470, 0.85, rice=True, steam=False),
              label(f"{p}-lf", 1000, 640, "≈ 1/5 – 1/3 TỪ THỨC ĂN", 44, YELLOW, "middle"),
              label(f"{p}-l90", 790, 330, "> 90% NƯỚC", 48, WHITE, "middle"),
              coffee_cup(f"{p}-cof", 1460, 470, 1.0), can, glass(f"{p}-gl", 1790, 540, 0.65, 0.8),
              label(f"{p}-lc", 1470, 640, "✓ 4 CỐC/NGÀY", 40, TEAL, "middle"),
              text(1470, 700, "≈ nước lọc · nam, quen uống · 2014", 30, 600, GREY, "middle", id_=f"{p}-lc2"),
              label(f"{p}-ls", 1640, 260, "+ ĐƯỜNG", 46, CORAL, "middle"),
              label(f"{p}-lg", 1790, 330, "TỐT NHẤT", 40, WATER, "middle"),
              urine_scale(f"{p}-us", 760, 440, 160, 200, 24),
              label(f"{p}-u1", 930, 400, "ĐỦ NƯỚC ✓", 52, TEAL, "middle"),
              label(f"{p}-u2", 1430, 400, "UỐNG THÊM", 52, CORAL, "middle"),
              text(1220, 760, "THUỐC, VITAMIN CŨNG LÀM ĐỔI MÀU · CHỈ LÀ GỢI Ý", 38, 800, GREY, "middle", id_=f"{p}-u3"),
              text(1220, 820, "Armstrong và cộng sự, 1994", 28, 500, GREY, "middle", id_=f"{p}-u4")]
    close()
    end = c.loc(SCENES["15"]["end"])
    idle(c, f"{p}-suy-nghi", 0, end, 1)
    food = (f"#{p}-wm", f"#{p}-soup", f"#{p}-rice", f"#{p}-lf", f"#{p}-l90", f"#{p}-cof", f"#{p}-can", f"#{p}-gl", f"#{p}-lc",
            f"#{p}-lc2", f"#{p}-ls", f"#{p}-lg")
    c.hide(*food, f"#{p}-us", f"#{p}-u1", f"#{p}-u2", f"#{p}-u3", f"#{p}-u4", *[f"#{p}-us-{k}" for k in range(5)])
    t = c.at("15", "từ thức ăn")
    for k, sel in enumerate((f"#{p}-wm", f"#{p}-soup", f"#{p}-rice")):
        popl(c, sel, t + 0.4 * k, "50% 100%", snd="pop" if k == 0 else None)
    popl(c, f"#{p}-lf", c.at("15", "một phần năm"), snd=None)
    t = c.at("15", "Dưa hấu")
    c.tl.ft(f"#{p}-wm", {"scale": 1}, {"scale": 1.15, "transformOrigin": "50% 100%", "duration": 0.25, "yoyo": True, "repeat": 1}, t)
    popl(c, f"#{p}-l90", c.at("15", "hơn chín mươi"))
    popl(c, f"#{p}-cof", c.at("15", "Trà và cà phê"), "50% 100%")
    c.blur_in(f"#{p}-lc", c.at("15", "Với bốn cốc"))
    c.blur_in(f"#{p}-lc2", c.at("15", "Với bốn cốc", off=0.4))
    popl(c, f"#{p}-can", c.at("15", "Nước ngọt"), "50% 100%")
    popl(c, f"#{p}-ls", c.at("15", "nhiều đường"))
    popl(c, f"#{p}-gl", c.at("15", "nước lọc vẫn"), "50% 100%")
    c.blur_in(f"#{p}-lg", c.at("15", "lựa chọn tốt nhất"))
    t = c.at("15", "nhìn màu nước tiểu", off=-0.35)
    for sel in food:
        c.blur_out(sel, t, 0.25)
    t = c.at("15", "nhìn màu nước tiểu")
    c.show(f"#{p}-us", t)
    for k in range(5):
        c.pop(f"#{p}-us-{k}", t + 0.08 * k, 0.35, "50% 100%")
    c.sfx("pop", t)
    popl(c, f"#{p}-u1", c.at("15", "vàng rơm nhạt"))
    popl(c, f"#{p}-u2", c.at("15", "vàng sẫm"))
    c.blur_in(f"#{p}-u3", c.at("15", "Một số thuốc"))
    c.blur_in(f"#{p}-u4", c.at("15", "Một số thuốc", off=0.3))
    return c


# ---------------------------------------------------------------- 16 · Khi nào cần chủ động
def s16():
    c = comp("16")
    p = c.cid
    close = board(c, ("suy-nghi", "lo-lang"))
    icons = [("sun", sun(f"{p}-i0", 760, 420, 0.8), "NÓNG", "trời nóng"),
             ("run", pictogram(f"{p}-i1", 1000, 420, 0.9, "run"), "VẬN ĐỘNG", "vận động mạnh"),
             ("th", thermometer(f"{p}-i2", 1240, 430, 0.9, 0.85), "ỐM, SỐT", "Khi sốt"),
             ("preg", pictogram(f"{p}-i3", 1480, 420, 0.9, "preg"), "MANG THAI", "Phụ nữ mang thai"),
             ("old", pictogram(f"{p}-i4", 1720, 420, 0.9, "elder"), "CAO TUỔI", "Người cao tuổi")]
    na = "".join(place(1300 + (k % 4) * 140, 450 + (k // 4) * 80, g(f"{p}-na{k}", f'<circle r="26" fill="{YELLOW}" stroke="{INK}" stroke-width="5"/>'
                                                                               + text(0, 10, "Na", 26, 900, INK, "middle")))
                 for k in range(8))
    medal_svg = place(1000, 520, g(f"{p}-med", f'<path d="M-60 -220 L-14 -40 L14 -40 L60 -220 Z" fill="{TEAL}" stroke="{INK}" stroke-width="6"/>'
                                                f'<circle cy="40" r="100" fill="{YELLOW}" stroke="{INK}" stroke-width="6"/>'
                                                + text(0, 28, "BOSTON", 34, 900, INK, "middle") + text(0, 76, "2002", 44, 900, INK, "middle")))
    c.svg += ["".join(icon for _, icon, _, _ in icons),
              "".join(text(x, 620, lb, 40, 900, WHITE, "middle", id_=f"{p}-il{k}")
                      for k, (x, (_, _, lb, _)) in enumerate(zip((760, 1000, 1240, 1480, 1720), icons))),
              g(f"{p}-gau", gauge(f"{p}-gg", 900, 560, 150, "THẬN CÓ GIỚI HẠN")),
              g(f"{p}-blood", f'<rect x="1220" y="370" width="620" height="200" rx="30" fill="{WATER}" stroke="{INK}" stroke-width="6"/>{na}'),
              label(f"{p}-hypo", 1530, 680, "HẠ NATRI MÁU", 70, CORAL, "middle"),
              label(f"{p}-more", 1270, 560, "NHIỀU HƠN ≠ TỐT HƠN", 96, CORAL, "middle"),
              medal_svg, label(f"{p}-l13", 1450, 520, "≈ 13%", 140, CORAL, "middle"),
              text(1450, 600, "người chạy được xét nghiệm", 36, 700, WHITE, "middle", id_=f"{p}-l13b"),
              text(1270, 760, "Nguy cơ cao nhất: tăng cân khi chạy = uống nhiều hơn lượng mồ hôi mất", 30, 700, GREY, "middle", id_=f"{p}-lw"),
              f'<g id="{p}-warn"><rect x="660" y="880" width="1220" height="110" rx="20" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>'
              + text(1270, 952, "BỆNH TIM, BỆNH THẬN: UỐNG THEO CHỈ DẪN BÁC SĨ", 46, 900, "#FFFFFF", "middle") + "</g>"]
    close()
    end = c.loc(SCENES["16"]["end"])
    c.hide(*[f"#{p}-i{k}" for k in range(5)], *[f"#{p}-il{k}" for k in range(5)], f"#{p}-gau", f"#{p}-blood", f"#{p}-hypo",
           f"#{p}-med", f"#{p}-l13", f"#{p}-l13b", f"#{p}-lw", f"#{p}-warn", f"#{p}-more")
    for k, (_, _, _, w) in enumerate(icons):
        t = c.at("16", w)
        popl(c, f"#{p}-i{k}", t, "50% 100%")
        c.blur_in(f"#{p}-il{k}", t + 0.2)
    t = c.at("16", "nhiều hơn không có nghĩa")
    for k in range(5):
        c.blur_out(f"#{p}-i{k}", t - 0.2, 0.2)
        c.blur_out(f"#{p}-il{k}", t - 0.2, 0.2)
    swap(c, f"{p}-suy-nghi", f"{p}-lo-lang", t)
    popl(c, f"#{p}-more", t + 0.3, snd="thump")
    c.blur_out(f"#{p}-more", c.at("16", "giới hạn tốc độ", off=-0.6), 0.2)
    t = c.at("16", "giới hạn tốc độ")
    popl(c, f"#{p}-gau", t - 0.4, "50% 100%")
    c.tl.ft(f"#{p}-gg-n", {"rotation": -40}, {"rotation": 80, "svgOrigin": "900 560", "duration": 1.0, "ease": "power2.in"}, t)
    t = c.at("16", "làm loãng natri")
    c.pop(f"#{p}-blood", t - 0.5, 0.5, "0% 50%", "expo.out", 0.4)
    for k in range(8):
        c.tl.to(f"#{p}-na{k}", {"x": (k % 4 - 1.5) * 18, "y": (k // 4 - 0.5) * 30, "scale": 0.7, "opacity": 0.55, "duration": 1.2,
                                "ease": "power2.inOut"}, t + 0.2)
    c.tl.to(f"#{p}-blood", {"scaleX": 1.0, "duration": 0.1}, t)
    popl(c, f"#{p}-hypo", c.at("16", "hạ natri máu", 0), snd="thump")
    t = c.at("16", "giải marathon")
    for sel in (f"#{p}-gau", f"#{p}-blood", f"#{p}-hypo"):
        c.blur_out(sel, t - 0.2, 0.25)
    c.show(f"#{p}-med", t)
    c.tl.ft(f"#{p}-med", {"rotation": -25, "y": -200}, {"rotation": 0, "y": 0, "transformOrigin": "50% 0%", "duration": 1.4,
                                                       "ease": "elastic.out(1, 0.4)"}, t)
    c.sfx("whoosh", t)
    popl(c, f"#{p}-l13", c.at("16", "mười ba phần trăm"), snd="thump")
    c.blur_in(f"#{p}-l13b", c.at("16", "mười ba phần trăm", off=0.3))
    c.blur_in(f"#{p}-lw", c.at("16", "Nguy cơ cao nhất"))
    t = c.at("16", "bệnh tim")
    c.show(f"#{p}-warn", t)
    c.tl.ft(f"#{p}-warn", {"y": 160}, {"y": 0, "duration": 0.5, "ease": "expo.out"}, t)
    c.sfx("whoosh", t)
    idle(c, f"{p}-suy-nghi", 0, c.at("16", "nhiều hơn không có nghĩa"), 1)
    idle(c, f"{p}-lo-lang", c.at("16", "nhiều hơn không có nghĩa", off=0.6), end, 3)
    return c


# ---------------------------------------------------------------- 17 · Loại trừ
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
    for L, nth in (("a", 1), ("c", 2)):
        tp = c.at("17", f"Phương án {L.upper()}")
        c.tl.ft(f"#{p}-o{L}-box", {"opacity": 0}, {"opacity": 1, "duration": 0.2}, tp)
        tlo = c.at("17", "Loại", nth)
        c.draw(f"#{p}-o{L}-strike", tlo, 0.3, "power3.out")
        c.sfx("pop", tlo)
        c.tl.to(f"#{p}-o{L}-box", {"opacity": 0, "duration": 0.2}, tlo + 0.5)
        c.tl.to(f"#{p}-o{L}", {"opacity": 0.5, "duration": 0.3}, tlo + 0.6)
    t = c.at("17", "phương án B")
    c.draw(f"#{p}-ring", t, 0.6)
    c.sfx("pop", t)
    swap(c, f"{p}-suy-nghi", f"{p}-vui", c.at("17", "Còn lại"))
    idle(c, f"{p}-suy-nghi", 0, c.at("17", "Còn lại"), 3)
    idle(c, f"{p}-vui", c.at("17", "Còn lại", off=0.6), end, 1)
    return c


# ---------------------------------------------------------------- 18 · Đáp án
def s18():
    c = comp("18")
    p = c.cid
    poses = ["vui", "dung"]
    hand = to_point(TO_X, TO_Y, TO_H, 322, 216)
    extra = (glass(f"{p}-hg", hand[0] + 16, hand[1] + 40, 0.5, 0.8)
             + place(1190, 280, g(f"{p}-chip", f'<rect x="-50" y="-50" width="100" height="100" rx="18" fill="{URINE[1]}" stroke="{INK}" stroke-width="6"/>'
                                               f'<path d="M-22 0 L-4 20 L28 -22" fill="none" stroke="{TEAL}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')))
    world_svg = office_world(p, 15, 0, poses) + extra
    c.svg += [f'<g id="{p}-k"><g id="{p}-settle"><g id="{p}-cam">{world_svg}</g></g></g>',
              label(f"{p}-no", 960, 950, "KHÔNG CẦN ÉP UỐNG CẢ LÍT", 70, CORAL, "middle"),
              g(f"{p}-b", f'<rect width="1920" height="1080" fill="{SLATE}"/>'
                + text(960, 720, "B", 560, 900, YELLOW, "middle", extra=" " + OUTLINE)
                + f'<circle id="{p}-ring" cx="960" cy="530" r="300" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" '
                  f'fill="none" stroke="{YELLOW}" stroke-width="16"/>' + slate_border())]
    c.hide(f"#{p}-dung-w", f"#{p}-no", f"#{p}-chip")
    end = c.loc(SCENES["18"]["end"])
    tq = c.at("18", "Quay lại")
    c.tl.ft(f"#{p}-b", {"scale": 1.3, "svgOrigin": "960 540", "filter": "blur(10px)", "opacity": 0},
            {"scale": 1, "svgOrigin": "960 540", "filter": "blur(0px)", "opacity": 1, "duration": 0.35, "ease": "power3.out"}, 0.05)
    c.draw(f"#{p}-ring", 0.4, 0.5)
    c.sfx("riser", 0.3)
    c.sfx("thump", 0.3)
    c.show(f"#{p}-b", tq, False)
    frame(c, tq, 1150, 430, 1.5, f"#{p}-cam", f"#{p}-settle")
    c.tl.ft(f"#{p}-hg", {"rotation": 0}, {"rotation": -25, "transformOrigin": "50% 100%", "duration": 0.5, "yoyo": True, "repeat": 1,
                                         "ease": "sine.inOut"}, c.at("18", "vài ngụm"))
    c.tl.ft(f"#{p}-hg-water", {"scaleY": 0.3, "transformOrigin": "50% 100%"}, {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.8},
            c.at("18", "thêm một ly"))
    c.sfx("pop", c.at("18", "thêm một ly"))
    t = c.at("18", "Không cần ép")
    popl(c, f"#{p}-no", t, snd="thump")
    c.show(f"#{p}-no", c.at("18", "Từ mai"), False)
    t = c.at("18", "Từ mai")
    frame(c, t, 1250, 500, 1.3, f"#{p}-cam", f"#{p}-settle")
    show_pose(c, poses, "dung", t)
    c.show(f"#{p}-hg", t, False)
    c.tl.to(f"#{p}-bot", {"x": -170, "duration": 0.8, "ease": "power2.inOut"}, c.at("18", "trong tầm mắt", off=-0.3))
    c.sfx("whoosh", c.at("18", "trong tầm mắt", off=-0.2))
    popl(c, f"#{p}-chip", c.at("18", "vàng rơm nhạt"))
    idle(c, f"{p}-vui", tq, t, 2)
    idle(c, f"{p}-dung", t, end, 0)
    return c


# ---------------------------------------------------------------- 19 · Bất ngờ: sỏi thận
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
    c.svg += [stone(f"{p}-st", 820, 330, 1.4), label(f"{p}-lst", 820, 520, "SỎI THẬN", 54, WHITE, "middle"),
              label(f"{p}-hd", 1450, 200, "Ý · 1996 · ~200 NGƯỜI · 5 NĂM", 50, YELLOW, "middle"),
              bar(f"{p}-b1", 1250, 12, WATER, "UỐNG ĐỦ (TIỂU ≥ 2 L)"), bar(f"{p}-b2", 1650, 27, CORAL, "NHÓM CÒN LẠI"),
              text(1450, 980, "tỉ lệ sỏi tái phát · Borghi và cộng sự", 30, 600, GREY, "middle", id_=f"{p}-src"),
              f'<g id="{p}-aua"><rect x="680" y="590" width="1180" height="160" rx="24" fill="#1D4262" stroke="{TEAL}" stroke-width="6"/>'
              + text(1270, 660, "HƯỚNG DẪN AUA 2014 CHO NGƯỜI TỪNG BỊ SỎI:", 38, 900, TEAL, "middle")
              + text(1270, 722, "UỐNG ĐỦ ĐỂ TIỂU ≥ 2,5 LÍT MỖI NGÀY", 48, 900, WHITE, "middle") + "</g>"]
    close()
    end = c.loc(SCENES["19"]["end"])
    c.hide(f"#{p}-st", f"#{p}-lst", f"#{p}-hd", f"#{p}-b1", f"#{p}-b2", f"#{p}-src", f"#{p}-aua", f"#{p}-b1-v", f"#{p}-b2-v")
    t = c.at("19", "lợi ích bất ngờ")
    swap(c, f"{p}-suy-nghi", f"{p}-ngac-nhien", t)
    t = c.at("19", "Năm 1996")
    popl(c, f"#{p}-st", t)
    c.blur_in(f"#{p}-lst", t + 0.3)
    c.blur_in(f"#{p}-hd", c.at("19", "gần hai trăm"))
    t = c.at("19", "Một nhóm")
    c.show(f"#{p}-b1", t)
    c.tl.ft(f"#{p}-b1-r", {"scaleY": 0, "transformOrigin": "50% 100%"}, {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.01}, t)
    c.tl.set(f"#{p}-b1-r", {"scaleY": 0.05, "transformOrigin": "50% 100%"}, t)
    c.blur_in(f"#{p}-src", t)
    t = c.at("19", "mười hai phần trăm")
    c.tl.to(f"#{p}-b1-r", {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.8, "ease": "expo.out"}, t)
    popl(c, f"#{p}-b1-v", t + 0.5)
    t = c.at("19", "Ở nhóm còn lại")
    c.show(f"#{p}-b2", t)
    c.tl.ft(f"#{p}-b2-r", {"scaleY": 0.05, "transformOrigin": "50% 100%"}, {"scaleY": 0.05, "transformOrigin": "50% 100%", "duration": 0.01}, t)
    t = c.at("19", "hai mươi bảy")
    c.tl.to(f"#{p}-b2-r", {"scaleY": 1, "transformOrigin": "50% 100%", "duration": 0.9, "ease": "expo.out"}, t)
    popl(c, f"#{p}-b2-v", t + 0.5, snd="thump")
    t = c.at("19", "Hướng dẫn năm 2014")
    for sel in (f"#{p}-b1", f"#{p}-b2", f"#{p}-src", f"#{p}-hd"):
        c.blur_out(sel, t - 0.2, 0.25)
    c.show(f"#{p}-aua", t)
    c.tl.ft(f"#{p}-aua", {"y": 120}, {"y": 0, "duration": 0.6, "ease": "expo.out"}, t)
    c.sfx("whoosh", t)
    idle(c, f"{p}-suy-nghi", 0, c.at("19", "lợi ích bất ngờ"), 1)
    idle(c, f"{p}-ngac-nhien", c.at("19", "lợi ích bất ngờ", off=0.6), end, 2)
    return c


# ---------------------------------------------------------------- 20 · Kết: phòng họp
def s20():
    c = comp("20")
    p = c.cid
    heads = "".join(place(x, 1010 + (k % 2) * 20, g(f"{p}-a{k}", f'<path d="M-80 120 Q-80 20 0 20 Q80 20 80 120 Z" fill="{col}" stroke="{INK}" stroke-width="6"/>'
                                                                   f'<circle cy="-30" r="58" fill="{sk}" stroke="{INK}" stroke-width="6"/>'
                                                                   f'<path d="M-58 -40 Q0 -110 58 -40 Q20 -70 -58 -40 Z" fill="{hr}"/>'))
                    for k, (x, col, sk, hr) in enumerate(((180, TEAL, "#F2C29B", HAIR_C), (430, CORAL, "#C98E6B", "#2A1C14"),
                                                          (680, "#7E6BD6", "#F2C29B", "#5A3A1E"), (1260, "#2F9E6E", "#E9B48A", HAIR_C),
                                                          (1520, YELLOW, "#C98E6B", "#2A1C14"), (1780, GREY, "#F2C29B", "#5A3A1E"))))
    room = (f'<rect width="1920" height="1080" fill="#2A5674"/><rect y="820" width="1920" height="260" fill="#244B66"/>'
            f'<rect x="420" y="100" width="760" height="460" rx="14" fill="#F5F7FA" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M500 460 L640 380 L760 410 L900 280 L1080 320" fill="none" stroke="{WATER}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
            + text(800, 180, "NƯỚC & CƠ THỂ", 50, 900, INK, "middle")
            + f'<g id="{p}-ok">{text(800, 520, "CÂN BẰNG ✓", 54, 900, TEAL, "middle")}</g>'
            + wc_door(f"{p}-door", 1560, 290))
    c.svg += [room, f'<g id="{p}-tw">{to(f"{p}-vui", "vui", 1150, 150, 780)}</g>', heads]
    c.hide(f"#{p}-ok")
    end = c.loc(SCENES["20"]["end"])
    t = c.at("20", "vỗ tay")
    for k in range(6):
        c.tl.ft(f"#{p}-a{k}", {"y": 0}, {"y": -16, "duration": 0.14 + 0.02 * (k % 3), "yoyo": True, "repeat": 7, "ease": "sine.inOut"}, t + 0.05 * k)
    t = c.at("20", "cúi chào")
    c.tl.to(f"#{p}-vui", {"rotation": 14, "transformOrigin": "50% 100%", "duration": 0.35, "ease": "power2.out", "yoyo": True, "repeat": 1}, t)
    t = c.at("20", "lao thẳng")
    c.tl.to(f"#{p}-tw", {"x": 560, "duration": 0.5, "ease": "power3.in"}, t)
    c.tl.to(f"#{p}-tw", {"opacity": 0, "duration": 0.1}, t + 0.48)
    c.sfx("whoosh", t + 0.1)
    c.tl.ft(f"#{p}-door", {"rotation": 0}, {"rotation": 1.5, "transformOrigin": "0% 50%", "duration": 0.06, "yoyo": True, "repeat": 7}, t + 0.55)
    c.sfx("thump", t + 0.55)
    popl(c, f"#{p}-ok", c.at("20", "cân bằng"))
    idle(c, f"{p}-vui", 0, c.at("20", "lao thẳng"), 2)
    return c


# ---------------------------------------------------------------- 21 · Thẻ cuối
def s21():
    c = comp("21")
    c.svg += [f'<rect width="1920" height="1080" fill="{PAPER}"/>', to("s21-to", "vui", 1400, 330, 680)]
    lines = [("big", "Khát thì uống.<br>Nóng, vận động, ốm: uống thêm.<br>Đừng ép."),
             ("lab", "Nguồn chính"),
             ("src", "Popkin và cộng sự, <i>Nutrition Reviews</i> (2010) · EFSA (2010) · Viện Hàn lâm Quốc gia Hoa Kỳ (2004)"),
             ("src", "Valtin, <i>Am J Physiol</i> (2002) · Almond và cộng sự, <i>NEJM</i> (2005) · Borghi và cộng sự, <i>J Urol</i> (1996)"),
             ("src", "Danh sách đầy đủ trong phần mô tả."),
             ("safe", "Video chỉ nhằm phổ biến kiến thức, không thay thế tư vấn y tế.<br>Người bệnh tim, thận: uống theo chỉ dẫn bác sĩ.")]
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
    c.tl.ft("#s21-to .tay-phai", {"rotation": 0}, {"rotation": -14, "transformOrigin": "20% 90%", "duration": 0.35, "ease": "sine.inOut",
                                                    "yoyo": True, "repeat": 5}, 1.0)
    idle(c, "s21-to", 0.3, c.loc(SCENES["21"]["end"]), 2)
    return c


BUILDERS = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21]

TRACKS = {"piz": 65.0, "mar": 46.0, "kal": 30.0, "lofi": 30.0, "doc": 39.0}


def music():
    """Nhạc: pizzicato (truyện) → tài liệu/marimba xoay vòng (giải thích 1) → lofi/kalimba/tài liệu/marimba
    (đố + giải thích 2) → pizzicato (đáp án → hết). Mức 0,14 dưới lời; 0,35 ở tiêu đề, đếm ngược, thẻ cuối."""
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
    core.run(BUILDERS, music)
