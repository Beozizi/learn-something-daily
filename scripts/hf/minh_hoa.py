r"""Bộ dựng cho các tập dùng hình minh họa (nhân vật cậu bé đeo kính PNG + bối cảnh AI) — rút từ tập
tap\2026-11-05-why-drink-water. Dùng trong build.py của tập:

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
    from hf import core
    core.init(__file__)
    from hf.core import *            # noqa
    from hf.minh_hoa import *        # noqa  (char, to, idle, S, comp, label, popl, board, chip, scene_comp, frame, music_plan)
    ...
    run(BUILDERS, music_plan(plan, lifts))

Ảnh nhân vật đọc từ video/assets/char/*.png (tap-moi.py --en chép sẵn); kích thước lấy từ header PNG.
"""
import struct
from pathlib import Path

from . import core
from .core import Comp, OUTLINE, text, g, audio_tag, subtitles  # noqa: F401
from .ve import WHITE, INK, YELLOW

# tên tư thế cũ của Tò → file ảnh mới (tên file cũng dùng trực tiếp được)
POSE_ALIAS = {"dung": "goc-chatgpt", "chi-tay": "goc-chatgpt", "lo-lang": "dau-dau", "uong": "uong-nuoc"}
LEAD = 0.2  # hình hiện sớm hơn tiếng một nhịp, để chữ không đuổi theo giọng đọc
_SIZE = {}


def pose_size(f):
    if f not in _SIZE:
        with open(core.VID / "assets" / "char" / f"{f}.png", "rb") as fh:
            fh.read(16)
            _SIZE[f] = struct.unpack(">II", fh.read(8))
    return _SIZE[f]


def char(uid, pose, cx, feet, h):
    """Nhân vật cao h px, chân chạm y = feet, giữa x = cx. #uid-w để ẩn/hiện, #uid để nhún/thở."""
    f = POSE_ALIAS.get(pose, pose)
    w0, h0 = pose_size(f)
    w = h * w0 / h0
    return (f'<g id="{uid}-w"><g id="{uid}"><image href="assets/char/{f}.png" x="{cx - w / 2:.1f}" y="{feet - h:.1f}" '
            f'width="{w:.1f}" height="{h:.1f}"/></g></g>')


def to(uid, pose, x, y, h):
    """Cùng chữ ký với Tò (khung 440×540 tại x, y, cao h) để board_to() của core dùng được."""
    k = h / 540
    return char(uid, pose, x + 220 * k, y + 505 * k, 470 * k)


core.to = to


def idle(c, uid, t0, t1, seed=0):
    """Đứng yên vẫn sống: thở nhẹ và lắc rất khẽ quanh chân."""
    n = int((t1 - t0) / 1.3)
    if n >= 2:
        reps = n - 1 if (n - 1) % 2 else n - 2
        c.tl.ft(f"#{uid}", {"scaleY": 1, "rotation": 0}, {"scaleY": 1.015, "rotation": 0.6 if seed % 2 else -0.6,
                                                         "transformOrigin": "50% 100%", "duration": 1.3, "ease": "sine.inOut",
                                                         "yoyo": True, "repeat": reps}, t0 + 0.1 * (seed % 3))


_at = Comp.at
Comp.at = lambda self, scene, phrase, nth=0, which="start", off=0.0: max(_at(self, scene, phrase, nth, which, off - LEAD), 0)


def S(c, scene, prefix):
    """Mốc (giây trong cảnh, đã trừ LEAD) của câu bắt đầu bằng `prefix`."""
    for s in core.WORDS["sentences"]:
        if s["scene"] == scene and s["text"].startswith(prefix):
            return round(max(s["start"] - c.start - LEAD, 0), 3)
    raise SystemExit(f"Không thấy câu '{prefix}' trong cảnh {scene}")


def comp(sid, last=None):
    a, b = core.SCENES[sid], core.SCENES[last or sid]
    return Comp(f"s{sid}", a["start"], b["end"])


def label(id_, x, y, s, size=52, fill=WHITE, anchor="start", weight=900):
    return text(x, y, s, size, weight, fill, anchor, id_=id_, extra=" " + OUTLINE)


def chip(id_, cx, cy, s, size=56, fill=YELLOW, color=INK):
    w = len(s) * size * 0.62 + 60
    return g(id_, f'<rect x="{cx - w / 2:.0f}" y="{cy - size * 0.95:.0f}" width="{w:.0f}" height="{size * 1.5:.0f}" rx="{size * 0.75:.0f}" '
                  f'fill="{fill}" stroke="{INK}" stroke-width="6"/>' + text(cx, cy + size * 0.3, s, size, 900, color, "middle"))


def popl(c, sel, t, origin="50% 50%", snd="pop", dur=0.45):
    c.pop(sel, t, dur, origin)
    if snd:
        c.sfx(snd, t)


def board(c, poses=("suy-nghi",)):
    """Nền bảng + nhân vật bên trái (tư thế đầu hiện, các tư thế khác ẩn). Gọi close() sau khi thêm hình."""
    c.svg.append(core.slate_frame())
    for k, pose in enumerate(poses):
        core.board_to(c, f"{c.cid}-{pose}", pose, hidden=k > 0)
    return lambda: c.svg.append(core.slate_border())


def frame(c, t, px, py, z, cam, settle):
    """Như core.frame nhưng giữ khung nhìn trong ảnh nền 1920×1080 (không lộ mép)."""
    px = min(max(px, 960 / z), 1920 - 960 / z)
    py = min(max(py, 540 / z), 1080 - 540 / z)
    core.frame(c, t, px, py, z, cam, settle)


def scene_comp(c, bg, poses, cx, feet, h, extra=""):
    """Cảnh truyện trên ảnh nền assets/bg/<bg>.jpg: nhân vật (nhiều tư thế, tư thế đầu hiện) + lớp phủ.
    Trả về (cam, settle) để dùng với frame()."""
    p = c.cid
    figs = "".join(char(f"{p}-{pose}", pose, cx, feet, h) for pose in poses)
    c.svg.append(f'<g id="{p}-settle"><g id="{p}-cam"><image href="assets/bg/{bg}.jpg" width="1920" height="1080"/>'
                 f'{figs}{extra}</g></g>')
    for pose in poses[1:]:
        c.hide(f"#{p}-{pose}-w")
    return f"#{p}-cam", f"#{p}-settle"


def show_pose(c, poses, which, t):
    for pose in poses:
        c.show(f"#{c.cid}-{pose}-w", t, pose == which)


TRACKS = {"piz": 65.0, "mar": 46.0, "kal": 30.0, "lofi": 30.0, "doc": 39.0}


def music_plan(plan, lifts, lo=0.14, hi=0.35, xf=1.2):
    """plan: [(giây đầu, giây cuối, ["piz", ...])] — xoay vòng các bản nhạc trong assets/bgm.
    lifts: [(a, b)] — các khoảng nhạc nâng lên mức hi (tiêu đề, đếm ngược, thẻ cuối)."""
    def build():
        D = core.DURATION
        tags, n = [], 0
        for a, b, cycle in plan:
            t, k = a, 0
            while t < b - 2:
                name = cycle[k % len(cycle)]
                dur = min(TRACKS[name], b + 0.6 - t, D - t)
                pts = [(0, lo)]
                for la, lb in lifts:
                    if la < t + dur and lb > t:
                        pts += [(max(la + 0.3 - t, 0.01), lo), (max(la + 1.0 - t, 0.02), hi), (max(lb - 0.6 - t, 0.03), hi),
                                (max(lb - t, 0.04), lo)]
                pts = sorted({round(x, 2): v for x, v in pts}.items())
                if pts[0][0] > 0:
                    pts = [(0, lo)] + pts
                last_seg = t + dur >= D - 0.1
                tags.append(audio_tag(f"bgm{n:02d}", f"bgm/{name}.wav", t, dur, 40 + n % 4, 0.6 if k else 0.4,
                                      2.0 if last_seg else xf, pts))
                t += dur - xf
                k += 1
                n += 1
        return "\n".join(tags)
    return build


def run(builders, music_fn=None, subs=True, mau=False):
    """subs=True: in cứng phụ đề tiếng Anh (audio/phu-de.srt) lên trên mọi cảnh.
    mau=True: nền tối hơn, dải màu rộng hơn (day_mau) — nhớ chạy day_mau.py cho ảnh."""
    core.run(builders, music_fn, subs=subs, mau=mau)
