r"""Tạo thư mục cho một tập mới từ các mẫu trong templates\.

Cách dùng:
    py scripts\tap-moi.py <slug> "<Tiêu đề>" [--en]

Ví dụ:
    py scripts\tap-moi.py vi-sao-cat-hanh-cay-mat "Vì sao cắt hành lại cay mắt?"
    py scripts\tap-moi.py why-we-sleep "Why do we sleep?" --en

--en: tập tiếng Anh dùng hình minh họa. Dựng sẵn thư mục video (cấu hình HyperFrames, ảnh nhân vật
cậu bé đeo kính, bối cảnh 1920x1080, nhạc nền) và build.py khung dùng scripts\hf\minh_hoa.py.
"""
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = [
    ("brief.md", "01-brief.md"),
    ("kich-ban.md", "02-kich-ban.md"),
    ("kiem-chung.md", "03-kiem-chung.md"),
    ("xuat-ban.md", "04-xuat-ban.md"),
]
SUBDIRS = ["nguon", "audio", "hinh", "video", "video-doc", "xuat"]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cau_hinh import FFMPEG  # noqa: E402
MAU_VIDEO = ROOT / "tap" / "2026-11-05-why-drink-water" / "video"  # chỉ chép file cấu hình, không chép cảnh

BUILD_KHUNG = r'''"""{title} — dựng HyperFrames từ audio/timeline.json + audio/words.json.
Chạy:  py build.py      (trong thư mục video\)
Mẫu đầy đủ: tap\2026-11-05-why-drink-water\video\build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from hf import core  # noqa: E402

core.init(__file__)
from hf.core import *  # noqa: E402,F401,F403
from hf.core import SCENES, WORDS, DURATION  # noqa: E402,F401
from hf.minh_hoa import *  # noqa: E402,F401,F403


# ---------------------------------------------------------------- 01 · Title
def s01():
    c = comp("01")
    c.svg += [f'<rect width="1920" height="1080" fill="{{PAPER}}"/>', char("s01-boy", "vui", 1600, 1000, 760),
              label("s01-t", 130, 520, "{title}", 110, INK)]
    c.blur_in("#s01-t", 0.3)
    return c


BUILDERS = [s01]

if __name__ == "__main__":
    run(BUILDERS, music_plan([(0, 9999, ["piz", "doc", "mar"])], [(0, SCENES["01"]["end"])]))
'''


def video_en(episode, title):
    vid = episode / "video"
    for f in ("hyperframes.json", "package.json", "CLAUDE.md", "AGENTS.md"):
        shutil.copy(MAU_VIDEO / f, vid / f)
    (vid / "meta.json").write_text(json.dumps({"id": episode.name, "name": title}, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
    for sub, src in (("char", ROOT / "assets" / "nhan-vat" / "cau-be-kinh" / "tach-nen" / "cat"),
                     ("bgm", ROOT / "assets" / "nhac-nen")):
        shutil.copytree(src, vid / "assets" / sub)
    (vid / "assets" / "bg").mkdir(parents=True)
    for png in (ROOT / "assets" / "boi-canh").glob("*.png"):
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(png), "-vf", "scale=1920:1080:flags=lanczos",
                        "-q:v", "2", str(vid / "assets" / "bg" / f"{png.stem}.jpg")], check=True)
    (vid / "build.py").write_text(BUILD_KHUNG.format(title=title), encoding="utf-8")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Tạo tập mới")
    parser.add_argument("slug", help="tên ngắn không dấu, nối bằng gạch ngang")
    parser.add_argument("title", help="tiêu đề tập")
    parser.add_argument("--en", action="store_true", help="tập tiếng Anh, dựng sẵn thư mục video dùng hình minh họa")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        sys.exit("slug chỉ gồm chữ thường không dấu, số và gạch ngang, VD: vi-sao-ngap")

    today = datetime.date.today().isoformat()
    episode = ROOT / "tap" / f"{today}-{args.slug}"
    if episode.exists():
        sys.exit(f"Đã có thư mục {episode}")

    for sub in SUBDIRS:
        (episode / sub).mkdir(parents=True)
    for src, dst in TEMPLATES:
        text = (ROOT / "templates" / src).read_text(encoding="utf-8")
        text = text.replace("{{TIEU_DE}}", args.title).replace("{{NGAY}}", today)
        (episode / dst).write_text(text, encoding="utf-8")
    (episode / "hinh" / "giay-phep.md").write_text(
        "# Giấy phép hình ảnh\n\n"
        "| File | Nguồn (URL) | Tác giả | Giấy phép | Ghi chú |\n"
        "|------|-------------|---------|-----------|---------|\n",
        encoding="utf-8",
    )
    if args.en:
        video_en(episode, args.title)
    print(episode)


if __name__ == "__main__":
    main()
