r"""Kiểm tra máy đã đủ công cụ để làm một tập video chưa.

    py scripts\kiem-tra-may.py

In từng mục ✅ / ⚠️ / ❌. ❌ là phải sửa trước khi làm tập; ⚠️ là chạy được nhưng chậm hoặc thiếu tùy chọn.
Không in nội dung API key — chỉ xem file có hay không.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cau_hinh  # noqa: E402

ROOT = cau_hinh.ROOT
loi = canh_bao = 0


def dong(trang_thai, ten, ghi_chu=""):
    global loi, canh_bao
    loi += trang_thai == "❌"
    canh_bao += trang_thai == "⚠️"
    print(f"{trang_thai} {ten}" + (f" — {ghi_chu}" if ghi_chu else ""))


def chay(cmd, timeout=120, **kw):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, **kw)
        return r.returncode, (r.stdout + r.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


print(f"Dự án: {ROOT}\n")

# Cấu hình
if cau_hinh.FILE.exists():
    dong("✅", "cau-hinh.json", f"công cụ ở {cau_hinh.TOOLS}")
else:
    dong("❌", "cau-hinh.json", "chưa có — chạy scripts\\cai-dat.ps1 (hoặc chép cau-hinh.mau.json rồi sửa)")

# Python hệ thống (chạy build.py, tap-moi.py)
dong("✅" if sys.version_info >= (3, 10) else "❌", f"Python {sys.version.split()[0]}", "dùng cho build.py, tap-moi.py")

# ffmpeg
for name in ("ffmpeg", "ffprobe"):
    code, out = chay([cau_hinh.tool(name), "-version"])
    dong("✅" if code == 0 else "❌", name, out.splitlines()[0][:60] if code == 0 else "không chạy được")

# Node + HyperFrames
code, out = chay(["node", "--version"])
if code == 0 and int(out.lstrip("v").split(".")[0]) >= 18:
    dong("✅", f"Node {out}")
else:
    dong("❌", "Node.js ≥ 18", "cài Node.js LTS")
npx = shutil.which("npx") or shutil.which("npx.cmd")
mau = ROOT / "tap" / "2026-11-06-why-cant-you-focus" / "video"
if npx:
    code, out = chay([npx, "--yes", "hyperframes@0.9.10", "--version"], timeout=300, cwd=mau)
    dong("✅" if code == 0 else "❌", "HyperFrames 0.9.10", out.splitlines()[-1] if out else "")
    if code == 0:
        code, out = chay([npx, "--yes", "hyperframes@0.9.10", "doctor", "--json"], timeout=300, cwd=mau)
        try:
            khong_dung = ("whisper", "tts", "bgm", "kokoro", "musicgen")  # quy trình không dùng
            bad = [c for c in json.loads(out[out.index("{"):]).get("checks", []) if not c.get("ok", True)
                   and not any(k in c.get("name", "").lower() for k in khong_dung)]
            dong("⚠️" if bad else "✅", "hyperframes doctor", ", ".join(c.get("name", "?") for c in bad))
        except ValueError:
            dong("⚠️" if code else "✅", "hyperframes doctor", "" if code == 0 else "xem: npx hyperframes@0.9.10 doctor")
else:
    dong("❌", "npx", "không thấy — cài Node.js LTS")

# Môi trường Python cho từng vai
CAN = {
    "tts": "numpy, soundfile, requests",
    "align": "torch, whisperx",
    "media": "rembg, onnxruntime, PIL",
    "chung": "cv2, numpy, PIL",
}
for vai, mods in CAN.items():
    py = cau_hinh.venv_python(vai)
    if not py.exists():
        dong("❌", f"môi trường '{vai}'", f"không có {py}")
        continue
    code, out = chay([str(py), "-c", f"import {mods}"], env=cau_hinh.setup_env(dict(__import__('os').environ)))
    dong("✅" if code == 0 else "❌", f"môi trường '{vai}' ({mods})", "" if code == 0 else out.splitlines()[-1][:90])

# GPU
code, out = chay(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"])
if code == 0:
    py = cau_hinh.venv_python("align")
    c2, o2 = chay([str(py), "-c", "import torch;print(torch.cuda.is_available())"]) if py.exists() else (1, "")
    dong("✅" if o2.strip().endswith("True") else "⚠️", f"GPU {out.splitlines()[0]}",
         "" if o2.strip().endswith("True") else "torch không thấy CUDA — WhisperX sẽ chạy CPU")
else:
    dong("⚠️", "GPU NVIDIA", "không có — WhisperX và rembg chạy CPU (chậm hơn, vẫn được)")

# Key (chỉ xem có hay không)
for f, bat_buoc, dung in ((".genmax_key.txt", True, "lồng tiếng tiếng Anh (GenMax)"),
                          (".chatgpt_key.txt", False, "tao-hinh.py qua OpenAI API (không bắt buộc nếu vẽ trên ChatGPT web)")):
    p = ROOT / f
    ok = p.exists() and p.stat().st_size > 10
    dong("✅" if ok else ("❌" if bat_buoc else "⚠️"), f, dung if ok else f"chưa có — {dung}")

# Ổ đĩa
free = shutil.disk_usage(cau_hinh.TOOLS if cau_hinh.TOOLS.exists() else ROOT).free / 2**30
dong("✅" if free > 15 else "⚠️", f"Ổ chứa công cụ còn {free:.0f} GB", "" if free > 15 else "nên còn ≥ 15 GB (mỗi tập ~400 MB)")

print("\nTự kiểm tra bằng tay (script không xem được):")
print("  • Claude desktop đã mở thư mục dự án; tiện ích Claude in Chrome đã cài và kết nối")
print("  • Trong Chrome đã đăng nhập chatgpt.com (tài khoản có tạo ảnh)")
print(f"\nKết quả: {loi} lỗi, {canh_bao} cảnh báo." + (" Sẵn sàng làm tập mới." if not loi else " Sửa các dòng ❌ trước."))
sys.exit(1 if loi else 0)
