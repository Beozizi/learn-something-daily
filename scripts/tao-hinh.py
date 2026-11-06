"""Tạo hình minh họa bằng OpenAI Images API (cùng phong cách nhân vật/bối cảnh của kênh).

Key đọc từ `.chatgpt_key.txt` ở gốc dự án (hoặc biến môi trường OPENAI_API_KEY) — không in key ra.

Ví dụ:
  python scripts/tao-hinh.py "a cozy bathroom..." -o assets/boi-canh/phong-tam.png
  python scripts/tao-hinh.py "same boy, thinking pose" -o assets/nhan-vat/cau-be-kinh/suy-nghi.png \
      --ref assets/nhan-vat/cau-be-kinh/goc-chatgpt.png --size 1024x1024 --nen-trong
  python scripts/tao-hinh.py --boi-canh "a park with trees and a water fountain" -o assets/boi-canh/cong-vien.png

Có --ref → dùng /images/edits (ảnh mẫu giữ đúng nét vẽ); không có → /images/generations.
Mỗi ảnh ghi kèm file .json cạnh nó (lệnh tạo, mẫu, kích thước, model, ngày) để ghi giấy phép.
"""
import argparse
import base64
import datetime
import json
import os
import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.openai.com/v1/images"

# Phần mô tả phong cách chung — giữ mọi hình cùng một "nét"
STYLE = (
    "Style: clean modern children's book illustration, soft flat colors with gentle shading, "
    "clean warm-brown outlines, warm and friendly. Palette: off-white #F5F1E8, slate blue #13304A, "
    "mustard yellow #FFC145, water blue #4FB3E8, coral red #E8604C used sparingly, light wood. "
    "No text, no logo, no watermark."
)
BOI_CANH = (
    "Background for a 16:9 explainer video, wide landscape. Keep the right third mostly empty "
    "floor space where a character will stand. No people, no characters. "
)


def read_key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        for name in (".chatgpt_key.txt", ".chatgpt_key"):
            p = ROOT / name
            if p.exists():
                k = p.read_text(encoding="utf-8").strip()
                break
    if not k:
        sys.exit("Không tìm thấy API key (.chatgpt_key.txt ở gốc dự án hoặc OPENAI_API_KEY).")
    return k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", help="mô tả hình (tiếng Anh cho kết quả tốt nhất)")
    ap.add_argument("-o", "--out", required=True, help="file PNG đầu ra")
    ap.add_argument("--ref", action="append", default=[], help="ảnh mẫu (dùng nhiều lần được)")
    ap.add_argument("--size", default="1536x1024", help="VD 1536x1024, 1024x1024, 1024x1536, auto")
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high", "auto"])
    ap.add_argument("--model", default="gpt-image-2")
    ap.add_argument("--nen-trong", action="store_true", help="nền trong suốt (nhân vật, đồ vật)")
    ap.add_argument("--boi-canh", action="store_true", help="thêm quy tắc khung bối cảnh 16:9")
    ap.add_argument("--khong-style", action="store_true", help="không thêm đoạn phong cách chung")
    a = ap.parse_args()

    prompt = a.prompt
    if a.boi_canh:
        prompt = BOI_CANH + prompt
    if not a.khong_style:
        prompt = prompt + " " + STYLE

    fields = {"model": a.model, "prompt": prompt, "size": a.size, "quality": a.quality, "n": "1"}
    if a.nen_trong:
        fields["background"] = "transparent"
        fields["output_format"] = "png"
    headers = {"Authorization": "Bearer " + read_key()}

    if a.ref:
        files = [("image[]", (Path(r).name, open(ROOT / r if not Path(r).is_absolute() else r, "rb"), "image/png"))
                 for r in a.ref]
        res = requests.post(f"{API}/edits", headers=headers, data=fields, files=files, timeout=600)
    else:
        res = requests.post(f"{API}/generations", headers=headers, json={**fields, "n": 1}, timeout=600)

    if res.status_code != 200:
        try:
            msg = res.json()["error"]["message"]
        except Exception:
            msg = res.text[:500]
        sys.exit(f"Lỗi API {res.status_code}: {msg}")

    data = res.json()
    out = Path(a.out)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))

    meta = {
        "nguon": f"OpenAI Images API ({a.model}) — ảnh do AI tạo, ghi 'Ảnh minh họa' khi dùng",
        "ngay": datetime.date.today().isoformat(),
        "prompt": prompt,
        "ref": a.ref,
        "size": a.size,
        "quality": a.quality,
        "usage": data.get("usage"),
    }
    out.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã lưu {out}")
    if data.get("usage"):
        print("usage:", data["usage"])


if __name__ == "__main__":
    main()
