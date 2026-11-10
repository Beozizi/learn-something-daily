r"""Lõi dựng video HyperFrames dùng chung cho mọi tập.

Cách dùng trong build.py của một tập (thư mục video\ của tập):
    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
    from hf import core
    core.init(__file__)
    from hf.core import *          # Comp, TL, idle, swap, frame, burst, word_time, ...
    ... định nghĩa các hàm cảnh trả về Comp ...
    core.run([s01, s02, ...], music_fn)

Mốc thời gian lấy từ audio/timeline.json + audio/words.json của tập.
"""
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from .ve import *  # noqa: F401,F403
from .ve2 import *  # noqa: F401,F403
from .ve import SLATE, to_point
from cau_hinh import FFMPEG, ROOT

VID = EP = None
TIMELINE = WORDS = None
SCENES = {}
DURATION = 0.0
SFX_DIR = Path(__file__).resolve().parent / "sfx"


def init(build_file):
    """Nạp timeline và lời đọc của tập chứa build_file (…/tap/<tập>/video/build.py)."""
    global VID, EP, TIMELINE, WORDS, SCENES, DURATION
    VID = Path(build_file).resolve().parent
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




def board_to(c, uid, pose="suy-nghi", hidden=False):
    c.svg.append(to(uid, pose, B_X, B_Y, B_H))
    if hidden:
        c.hide(f"#{uid}-w")


def burst(c, prefix, n, t, spread=(-160, -20), dist=(140, 320), dur=0.7):
    """Giọt nước bắn ra theo hình quạt, hướng và độ xa cố định (không ngẫu nhiên)."""
    for k in range(n):
        a = math.radians(spread[0] + (spread[1] - spread[0]) * ((k * 7) % n) / max(n - 1, 1))
        d = dist[0] + (dist[1] - dist[0]) * ((k * 5) % n) / max(n - 1, 1)
        c.tl.ft(f"#{prefix}-{k}", {"x": 0, "y": 0, "opacity": 1},
                {"x": d * math.cos(a), "y": d * math.sin(a) + 40, "duration": dur, "ease": "power2.out"}, t + 0.015 * k)
        c.tl.to(f"#{prefix}-{k}", {"opacity": 0, "duration": 0.25, "ease": "power1.in"}, t + 0.015 * k + dur)




def lane(points):
    pts = ",".join(f'{{"t":{t:.2f},"v":{v}}}' for t, v in points)
    return f"data-automation='{{\"version\":1,\"lanes\":[{{\"target\":\"volume\",\"points\":[{pts}]}}]}}'"


def audio_tag(id_, src, start, dur, track, fade_in=0.0, fade_out=0.0, points=None, media_start=0.0, volume=1):
    ln = lane(points) if points else ""
    return (f'      <audio id="{id_}" class="clip" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{track}" '
            f'data-volume="{volume}" data-media-start="{media_start}" data-fade-in="{fade_in}" data-fade-out="{fade_out}" {ln} '
            f'src="assets/{src}"></audio>')


def prep_audio(bgm_files=()):
    """Chuẩn hóa lời đọc về -16 LUFS (đỉnh -1,5 dB); chép hiệu ứng âm dùng chung và nhạc nền vào assets/."""
    src, dst = EP / "audio" / "loi-doc.wav", VID / "assets" / "loi-doc.wav"
    if not src.exists():
        sys.exit(f"Thiếu {src} — chạy lồng tiếng (long-tieng.py) trước. Tập cũ lấy từ repo không kèm âm thanh.")
    dst.parent.mkdir(exist_ok=True)
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(src), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", "48000", str(dst)], check=True)
    (VID / "assets" / "sfx").mkdir(exist_ok=True)
    for f in SFX_DIR.glob("*.mp3"):
        if not (VID / "assets" / "sfx" / f.name).exists():
            shutil.copy(f, VID / "assets" / "sfx" / f.name)
    (VID / "assets" / "bgm").mkdir(exist_ok=True)
    for m in bgm_files:
        if not (VID / "assets" / "bgm" / m).exists():
            shutil.copy(VID / ".media" / "audio" / "bgm" / m, VID / "assets" / "bgm" / m)


def write_index(comps, music_html=""):
    sfx_tags = "\n".join(
        f'      <audio id="sfx{k:02d}" class="clip" data-start="{max(t, 0):.3f}" data-duration="{dur:.3f}" '
        f'data-track-index="{31 + k % 3}" data-volume="{v}"'
        + (f' data-media-start="{ms}"' if ms else "") + f' data-fade-out="0.08" src="assets/sfx/{f}"></audio>'
        for k, (t, f, dur, v, ms) in enumerate(sorted(SFX_EVENTS)))
    hosts = "\n".join(
        f'      <div id="{c.cid}" data-composition-id="{c.cid}" data-composition-src="compositions/{c.cid}.html" '
        f'data-start="{c.start:.3f}" data-duration="{c.end - c.start:.3f}" data-track-index="{k + 1}" '
        f'data-track-kind="{getattr(c, "kind", "graphics")}" data-width="1920" data-height="1080"'
        + (' style="z-index: 50"' if getattr(c, "kind", "") == "captions" else "") + '></div>'
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
{music_html}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")


def _srt(path):
    """Đọc phu-de.srt → [(giây đầu, giây cuối, chữ)]."""
    import re
    ts = lambda h, m, s, ms: int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    out = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
        lines = block.strip().splitlines()
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", lines[1] if len(lines) > 1 else "")
        if m:
            out.append((ts(*m.groups()[:4]), ts(*m.groups()[4:]), " ".join(lines[2:]).strip()))
    return out


def subtitles(srt=None, bottom=46, size=42):
    """Phụ đề in cứng từ audio/phu-de.srt: một dòng mỗi lúc, chữ trắng trên nền tối bo tròn, sát đáy khung.
    Trả về Comp (kind="captions") phủ cả phim; run() tự thêm khi subs=True."""
    from html import escape
    lines = _srt(srt or EP / "audio" / "phu-de.srt")
    c = Comp("subs", 0.0, DURATION)
    c.kind = "captions"
    c.css.append(f"#subs-box .cap {{ position: absolute; left: 0; right: 0; bottom: {bottom}px; text-align: center; overflow: visible; }}"
                 f"#subs-box .cap span {{ display: inline-block; max-width: 1500px; padding: 8px 26px 10px; border-radius: 14px; "
                 f"background: rgba(8, 20, 32, 0.78); color: #F5F7FA; font-size: {size}px; font-weight: 700; line-height: 1.25; }}")
    items = []
    for k, (a, b, tx) in enumerate(lines):
        nxt = lines[k + 1][0] if k + 1 < len(lines) else DURATION
        b = nxt if nxt - b < 0.45 else b + 0.15  # nối liền các dòng sát nhau để phụ đề không nhấp nháy
        gid = f"subs-{k}"
        items.append(f'<div id="{gid}" class="cap"><span>{escape(tx)}</span></div>')
        c.hide(f"#{gid}")
        c.tl.set(f"#{gid}", {"autoAlpha": 1}, max(a - 0.05, 0.1))
        c.tl.set(f"#{gid}", {"autoAlpha": 0}, min(b, DURATION - 0.01))
    c.html.append(f'<div id="subs-box" class="txt" style="left:0; top:0; width:1920px; height:1080px;">{"".join(items)}</div>')
    return c


def run(builders, music_fn=None, bgm_files=(), subs=False, mau=False):
    """mau=True: đẩy mọi mã màu theo day_mau (nền tối hơn, màu đậm hơn); ảnh chạy riêng scripts/hf/day_mau.py."""
    sys.stdout.reconfigure(encoding="utf-8")
    (VID / "compositions").mkdir(exist_ok=True)
    fonts = VID / "assets" / "fonts"
    if not fonts.exists():
        shutil.copytree(ROOT / "assets" / "fonts" / "BeVietnamPro", fonts)
    comps = [b() for b in builders] + ([subtitles()] if subs else [])
    for c in comps:
        c.write()
    prep_audio(bgm_files)
    write_index(comps, music_fn() if music_fn else "")
    if mau:
        from .day_mau import day_html
        for f in [VID / "index.html"] + [VID / "compositions" / f"{c.cid}.html" for c in comps]:
            f.write_text(day_html(f.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"{len(comps)} cảnh · {DURATION:.1f} giây → {VID}")
