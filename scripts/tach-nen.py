"""Tách nền ảnh người bằng BiRefNet-portrait trên GPU.

Cách dùng:
    py scripts\\chay.py media scripts\\tach-nen.py <ảnh vào> [<ảnh vào> ...] [--out <thư mục>] [--model birefnet-portrait]

Chép từ F:\\News Football\\tools\\scripts\\cutout.py để dự án tự đủ. Không có GPU thì chạy CPU (chậm hơn).

Ảnh PNG nền trong suốt được lưu cạnh ảnh gốc (hoặc vào --out) với đuôi "-cutout.png".
"""
import argparse
import os
from pathlib import Path

import cau_hinh

cau_hinh.setup_env()  # model rembg lưu ở thư mục model của máy

import onnxruntime  # noqa: E402

# rembg không tự nạp thư viện CUDA/cuDNN cài qua pip, thiếu bước này sẽ chạy CPU.
if hasattr(onnxruntime, "preload_dlls"):
    onnxruntime.preload_dlls()

from PIL import Image  # noqa: E402
from rembg import new_session, remove  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Tách nền ảnh người")
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, help="thư mục lưu kết quả")
    parser.add_argument("--model", default="birefnet-portrait")
    args = parser.parse_args()

    session = new_session(args.model, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    for src in args.images:
        out_dir = args.out or src.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        dst = out_dir / f"{src.stem}-cutout.png"
        remove(Image.open(src), session=session).save(dst)
        print(dst)


if __name__ == "__main__":
    main()
