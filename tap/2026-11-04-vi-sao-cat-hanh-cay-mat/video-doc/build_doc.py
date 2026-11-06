"""Bản dọc 9:16 (1080×1920) cắt từ bản chính đã render (assets/full.mp4).

Chạy:  py build_doc.py      (trong thư mục video-doc\\)
Mỗi đoạn = một khoảng câu trong words.json + vùng cắt ngang trong khung 16:9.
Bố cục theo vùng an toàn của TikTok/Reels/Shorts: chữ nằm trong dải 168–1330 px, chừa 120 px bên phải.
"""
import json
import subprocess
import sys
from pathlib import Path

DOC = Path(__file__).resolve().parent
EP = DOC.parent
sys.path.insert(0, str(EP / "video"))
from ve import INK, SLATE, WOOD, YELLOW, CORAL, WHITE, GREY, to, onion  # noqa: E402

FFMPEG = r"C:\ffmpeg\ffmpeg-9.0.2-essentials_build\bin\ffmpeg.exe"
WORDS = json.loads((EP / "audio" / "words.json").read_text(encoding="utf-8"))
FONT_CSS = "".join(
    f"@font-face {{ font-family: 'Be Vietnam Pro'; font-weight: {w}; src: url('assets/fonts/BeVietnamPro-{n}.ttf'); }}\n"
    for w, n in ((500, "Medium"), (700, "Bold"), (800, "ExtraBold"), (900, "Black")))

# (cảnh, câu đầu, câu cuối — tiền tố chữ, vùng cắt (x, rộng) trong bản 1920×1080, ảnh tĩnh phủ đầu đoạn)
# Vùng cắt tỉ lệ 4:3, căn giữa theo chiều dọc. Ảnh tĩnh: (giây trong bản chính) — hiện từ đầu đoạn tới khi video tới đúng khung đó.
KITCHEN, BOARD = (240, 1440), (620, 1300)
SEGMENTS = [
    ("02", "Chỉ vài giây sau", "Rồi nước mắt", KITCHEN, None),
    ("06", "Khí cay không có sẵn", "Nó chỉ được tạo ra", BOARD, None),
    ("08", "Lưỡi dao sắc có mũi", "Nó phải đè mạnh hơn", BOARD, None),
    ("08", "Lưỡi dao cùn nhất", "Lưỡi dao cùn nhất", BOARD, None),
    ("08", "Còn tốc độ cắt", "Cắt càng nhanh", BOARD, None),
    ("10", "Bạn chọn con dao sắc", "Rổ hành vơi dần", KITCHEN, None),
    ("11", "Còn mẹo quen thuộc", "Nghĩa là mẹo này", BOARD, 164.3),
]
PAD_IN, PAD_OUT = 0.15, 0.3
END_CARD = 3.2
WIN_Y, WIN_H = 400, 810          # khung hình 1080×810 (cắt 1440×1080 của bản chính, thu 0,75)
CAP_Y = 1232                      # dải phụ đề, kết thúc trước 1330
CAP_MAX_WORDS, CAP_MAX_CHARS = 5, 24


def sentence(scene, prefix):
    for s in WORDS["sentences"]:
        if s["scene"] == scene and s["text"].startswith(prefix):
            return s
    raise SystemExit(f"Không thấy câu '{prefix}' trong cảnh {scene}")


def plan():
    """Trả về các đoạn đã đặt lên dòng thời gian mới: (t0, media_start, dur, crop_x, words)."""
    out, t = [], 0.0
    for scene, first, last, crop, still in SEGMENTS:
        a, b = sentence(scene, first), sentence(scene, last)
        ms, me = a["start"] - PAD_IN, b["end"] + PAD_OUT
        ws = [dict(w, t=round(t + w["start"] - ms, 3), e=round(t + w["end"] - ms, 3))
              for w in WORDS["words"] if a["start"] - 0.01 <= w["start"] <= b["end"] + 0.01]
        out.append((round(t, 3), round(ms, 3), round(me - ms, 3), (crop, still), ws))
        t += me - ms
    return out, round(t, 3)


def caption_groups(words):
    groups, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        nxt = words[k + 1] if k + 1 < len(words) else None
        chars = sum(len(x["text"]) + 1 for x in cur)
        end_sentence = w["text"].endswith((".", "?", "!", "…"))
        too_long = nxt is not None and chars + len(nxt["text"]) > CAP_MAX_CHARS
        if nxt is None or end_sentence or len(cur) >= CAP_MAX_WORDS or too_long or nxt["t"] - w["e"] > 0.6:
            groups.append(cur)
            cur = []
    return groups


def comp(cid, css, body, js):
    return f"""<template>
<style>
{FONT_CSS}
#root {{ position: absolute; inset: 0; overflow: hidden; font-family: 'Be Vietnam Pro', sans-serif; }}
{css}
</style>
<div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["{cid}"] = tl;
</script>
</template>
"""


def write_frame(total):
    """Nền bảng, câu hỏi cố định ở trên, viền khung hình, trang trí dưới vùng chữ."""
    svg = f"""<svg class="stage" viewBox="0 0 1080 1920" width="1080" height="1920">
<rect width="1080" height="1920" fill="{SLATE}"/>
<rect x="14" y="{WIN_Y - 16}" width="1052" height="{WIN_H + 32}" rx="22" fill="{WOOD}" stroke="{INK}" stroke-width="6"/>
<path d="M120 1560 q40 -8 80 0 M760 1700 q50 -8 100 0 M300 1800 q40 -6 80 0" stroke="#1D4262" stroke-width="10" stroke-linecap="round"/>
{onion("fr-onion", 880, 1560, 1.1)}
</svg>"""
    css = (f"#root .stage {{ position: absolute; left: 0; top: 0; }}"
           f"#fr-q {{ position: absolute; left: 60px; top: 196px; width: 900px; font-size: 76px; font-weight: 800; "
           f"line-height: 1.1; color: {WHITE}; letter-spacing: -0.01em; }} #fr-q b {{ color: {CORAL}; font-weight: 800; }}")
    body = svg + '<div id="fr-q">Vì sao cắt hành<br>lại <b>cay</b> mắt?</div>'
    reps = int(total / 1.6) | 1
    js = ('tl.fromTo("#fr-onion", {rotation: -4}, {rotation: 4, transformOrigin: "50% 100%", duration: 1.6, '
          f'ease: "sine.inOut", yoyo: true, repeat: {reps}, immediateRender: false}}, 0);')
    (DOC / "compositions" / "frame.html").write_text(comp("frame", css, body, js), encoding="utf-8")


def write_captions(segs):
    words = [w for *_, ws in segs for w in ws]
    groups = caption_groups(words)
    css = (f".cap {{ position: absolute; left: 50px; width: 860px; top: {CAP_Y}px; text-align: center; font-size: 58px; "
           f"font-weight: 800; color: {WHITE}; line-height: 1.15; "
           f"text-shadow: 0 0 2px {INK}, 3px 3px 0 {INK}, -3px 3px 0 {INK}, 3px -3px 0 {INK}, -3px -3px 0 {INK}; }}")
    body, js = [], []
    for g, grp in enumerate(groups):
        t0, t1 = grp[0]["t"], grp[-1]["e"] + 0.12
        spans = " ".join(f'<span id="cw{g}-{k}">{w["text"]}</span>' for k, w in enumerate(grp))
        body.append(f'<div id="cg{g}" class="cap clip" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}">{spans}</div>')
        for k, w in enumerate(grp):
            js.append(f'tl.set("#cw{g}-{k}", {{color: "{YELLOW}"}}, {w["t"]:.3f});')
            js.append(f'tl.set("#cw{g}-{k}", {{color: "{WHITE}"}}, {w["e"]:.3f});')
    (DOC / "compositions" / "captions.html").write_text(comp("captions", css, "\n".join(body), "\n".join(js)), encoding="utf-8")


def write_endcard():
    svg = f"""<svg class="stage" viewBox="0 0 1080 1920" width="1080" height="1920">
<rect width="1080" height="1920" fill="{SLATE}"/>
{to("ec-to", "vui", 300, 760, 560)}
</svg>"""
    css = (f"#root .stage {{ position: absolute; left: 0; top: 0; }}"
           f"#ec-t {{ position: absolute; left: 60px; top: 230px; width: 900px; font-size: 92px; font-weight: 900; line-height: 1.08; color: {WHITE}; }}"
           f"#ec-t b {{ color: {YELLOW}; }}"
           f"#ec-s {{ position: absolute; left: 60px; top: 560px; width: 880px; font-size: 48px; font-weight: 700; color: {GREY}; }}")
    body = (svg + '<div id="ec-t">Dao <b>sắc</b>,<br>cắt <b>chậm</b>.</div>'
            '<div id="ec-s">Xem bản đầy đủ trên YouTube</div>')
    js = "\n".join([
        'tl.fromTo("#ec-t", {opacity: 0, filter: "blur(8px)"}, {opacity: 1, filter: "blur(0px)", duration: 0.2, immediateRender: false}, 0.05);',
        'tl.fromTo("#ec-s", {opacity: 0, filter: "blur(8px)"}, {opacity: 1, filter: "blur(0px)", duration: 0.2, immediateRender: false}, 0.35);',
        'tl.fromTo("#ec-to-w", {y: 80, opacity: 0}, {y: 0, opacity: 1, duration: 0.6, ease: "expo.out", immediateRender: false}, 0.15);',
    ])
    css += "#ec-t, #ec-s { opacity: 0; }"
    (DOC / "compositions" / "endcard.html").write_text(comp("endcard", css, body, js), encoding="utf-8")


def write_index(segs, speech_end):
    total = round(speech_end + END_CARD, 3)
    videos, vo = [], []
    for k, (t0, ms, dur, (crop, still), _) in enumerate(segs):
        (cx, cw), k_ = crop, 1080 / crop[1]
        cy = (1080 - cw * 0.75) / 2
        pos = (f"left: {-cx * k_:.1f}px; top: {-cy * k_:.1f}px; width: {1920 * k_:.1f}px; height: {1080 * k_:.1f}px")
        videos.append(f'<video id="v{k}" class="clip" data-start="{t0:.3f}" data-duration="{dur:.3f}" data-media-start="{ms:.3f}" '
                      f'data-track-index="2" muted playsinline src="assets/full.mp4" style="{pos}"></video>')
        if still:
            img = f"still{k}.png"
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", f"{still:.3f}", "-i", str(DOC / "assets" / "full.mp4"),
                            "-frames:v", "1", str(DOC / "assets" / img)], check=True)
            videos.append(f'<img id="st{k}" class="clip" data-start="{t0:.3f}" data-duration="{still - ms:.3f}" data-track-index="3" '
                          f'src="assets/{img}" style="{pos}; z-index: 1" alt="">')
        vo.append(f'<audio id="vo{k}" class="clip" data-start="{t0:.3f}" data-duration="{dur:.3f}" data-media-start="{ms:.3f}" '
                  f'data-track-index="10" data-volume="1" data-fade-in="0.04" data-fade-out="0.08" src="assets/loi-doc.wav"></audio>')
    lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0.14}, {"t": round(speech_end, 2), "v": 0.14}, {"t": round(speech_end + 0.6, 2), "v": 0.35}]}]},
        separators=(",", ":"))
    (DOC / "index.html").write_text(f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {SLATE}; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      #win {{ position: absolute; left: 0; top: {WIN_Y}px; width: 1080px; height: {WIN_H}px; overflow: hidden; z-index: 2; }}
      #win video, #win img {{ position: absolute; }}
      #frame {{ z-index: 1; }} #captions {{ z-index: 3; }} #endcard {{ z-index: 4; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="1080" data-height="1920">
      <div id="frame" data-composition-id="frame" data-composition-src="compositions/frame.html" data-start="0" data-duration="{speech_end:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="win" data-layout-allow-overflow>
        {chr(10).join("        " + v for v in videos).strip()}
      </div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{speech_end:.3f}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920"></div>
      <div id="endcard" data-composition-id="endcard" data-composition-src="compositions/endcard.html" data-start="{speech_end:.3f}" data-duration="{END_CARD:.3f}" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      {chr(10).join("      " + a for a in vo).strip()}
      <audio id="bgm" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="11" data-volume="1" data-fade-out="1.5" data-automation='{lane}' src="assets/bgm_001.wav"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")
    return total


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    segs, speech_end = plan()
    write_frame(speech_end + END_CARD)
    write_captions(segs)
    write_endcard()
    total = write_index(segs, speech_end)
    print(f"{len(segs)} đoạn · {total:.1f} giây → {DOC}")


if __name__ == "__main__":
    main()
