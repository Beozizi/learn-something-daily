"""Xuất thumbnail YouTube từ ảnh ChatGPT.

    py scripts\\xuat-thumbnail.py tap\\<tập>

Đọc `xuat\\thumbnail-N.png`, ghi `xuat\\thumbnail-N.jpg` (1280×720, ≤ 2 MB) và
`xuat\\thumbnail-nho.jpg`: các bản thu về 320×180 đặt cạnh nhau để kiểm chữ còn đọc được.
"""
import glob
import os
import subprocess
import sys

from cau_hinh import FFMPEG

LIMIT = 2 * 1024 * 1024


def run(*args):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *args], check=True)


def main(tap):
    xuat = os.path.join(tap, "xuat")
    pngs = sorted(glob.glob(os.path.join(xuat, "thumbnail-[0-9].png")))
    if not pngs:
        sys.exit(f"Không thấy thumbnail-N.png trong {xuat}")
    fit = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720"
    for png in pngs:
        jpg = png[:-4] + ".jpg"
        for q in (2, 3, 4, 6):
            run("-i", png, "-vf", fit, "-q:v", str(q), jpg)
            if os.path.getsize(jpg) <= LIMIT:
                break
        print(f"{os.path.basename(jpg)}  {os.path.getsize(jpg) // 1024} KB")
    ins = []
    for p in pngs:
        ins += ["-i", p]
    small = ";".join(f"[{i}]{fit},scale=320:180[s{i}]" for i in range(len(pngs)))
    stack = "".join(f"[s{i}]" for i in range(len(pngs)))
    graph = small + f";{stack}hstack=inputs={len(pngs)}" if len(pngs) > 1 else f"[0]{fit},scale=320:180"
    run(*ins, "-filter_complex", graph, "-q:v", "3", os.path.join(xuat, "thumbnail-nho.jpg"))
    print("thumbnail-nho.jpg (bản 320×180 để kiểm chữ)")


if __name__ == "__main__":
    main(sys.argv[1])
