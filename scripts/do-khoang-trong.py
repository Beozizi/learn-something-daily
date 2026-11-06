r"""Dò các đoạn bảng trống trong lúc giọng đang đọc (hình chậm hơn lời) trên file MP4 đã render.

  py scripts\chay.py chung scripts\do-khoang-trong.py tap\<tập> [--min 1.0]

Lấy 2 khung/giây, xét vùng bảng bên phải nhân vật: nền xanh bảng gần như không có nét nào mà
words.json đang có câu → in ra khoảng thời gian, cảnh, câu. Ảnh nền truyện không bị tính.
"""
import argparse
import glob
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

from cau_hinh import FFMPEG



def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("tap")
    ap.add_argument("--video", help="mặc định xuat\\<file mp4 lớn nhất>")
    ap.add_argument("--min", type=float, default=1.0, help="chỉ báo khoảng trống dài hơn (giây)")
    a = ap.parse_args()
    ep = Path(a.tap)
    video = Path(a.video) if a.video else max((ep / "xuat").glob("*.mp4"), key=lambda f: f.stat().st_size)
    w = json.loads((ep / "audio" / "words.json").read_text(encoding="utf-8"))
    sents = w["sentences"]

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(video), "-vf", "fps=2,scale=192:108",
                        f"{tmp}/%05d.png"], check=True)
        blank = []
        for k, f in enumerate(sorted(glob.glob(f"{tmp}/*.png"))):
            t = (k + 0.5) / 2
            if not any(s["start"] - 0.2 <= t <= s["end"] + 0.3 for s in sents):
                continue
            reg = cv2.imread(f).astype(int)[8:88, 55:185]  # bỏ dải phụ đề ở đáy
            med = np.median(reg.reshape(-1, 3), 0)
            slate = med[0] >= 55 and med[2] < 40  # nền bảng xanh đậm
            if slate and (np.abs(reg - med).sum(2) > 60).mean() < 0.02:
                blank.append(t)

    runs = []
    for t in blank:
        if runs and t - runs[-1][1] <= 0.6:
            runs[-1][1] = t
        else:
            runs.append([t, t])
    total = 0
    for s0, s1 in runs:
        if s1 - s0 >= a.min:
            total += s1 - s0 + 0.5
            hit = [s for s in sents if s["start"] <= s1 and s["end"] >= s0]
            print(f"{int(s0 // 60)}:{s0 % 60:04.1f}–{int(s1 // 60)}:{s1 % 60:04.1f} ({s1 - s0 + 0.5:.1f}s) "
                  f"cảnh {hit[0]['scene'] if hit else '?'} | " + " / ".join(s["text"][:50] for s in hit))
    print(f"Tổng khoảng trống: {total:.1f}s" if total else "Không có khoảng trống.")


if __name__ == "__main__":
    main()
