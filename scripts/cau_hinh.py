r"""Cấu hình theo máy — mọi đường dẫn công cụ đọc từ `cau-hinh.json` ở gốc dự án.

File này không đưa lên repo (mỗi máy một bản). `scripts\cai-dat.ps1` tạo nó; mẫu ở `cau-hinh.mau.json`.
Thiếu file → mặc định công cụ nằm trong `<dự án>\.tools`.

    {
      "tools":      "D:\\lsd-tools",                     thư mục chứa venv và model
      "models":     "D:\\lsd-tools\\models",              (tùy chọn) model HuggingFace / torch / nltk / rembg
      "ffmpeg_bin": "C:\\ffmpeg\\bin",                    (tùy chọn) để trống nếu ffmpeg đã có trong PATH
      "venv": {"tts": "...", "align": "...", "media": "...", "chung": "..."},  (tùy chọn) ghi đè từng môi trường
      "env":  {"HF_HOME": ""}                             (tùy chọn) ghi đè biến model; "" = chỗ mặc định
    }

Vai trò môi trường: tts (lồng tiếng), align (WhisperX căn chữ), media (rembg tách nền),
chung (dò bảng trống, xử lý ảnh). Máy mới: tts/media/chung dùng chung một venv.
"""
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "cau-hinh.json"
CFG = json.loads(FILE.read_text(encoding="utf-8")) if FILE.exists() else {}
TOOLS = Path(CFG.get("tools") or ROOT / ".tools")
MODELS = Path(CFG.get("models") or TOOLS / "models")
FFMPEG_BIN = CFG.get("ffmpeg_bin") or ""
ROLES = ("tts", "align", "media", "chung")


def tool(name):
    """Đường dẫn ffmpeg / ffprobe."""
    if FFMPEG_BIN and (Path(FFMPEG_BIN) / f"{name}.exe").exists():
        return str(Path(FFMPEG_BIN) / f"{name}.exe")
    return shutil.which(name) or name


FFMPEG = tool("ffmpeg")
FFPROBE = tool("ffprobe")


def venv_python(role):
    # mặc định giống cai-dat.ps1: WhisperX riêng một venv, còn lại dùng chung venv-chung
    path = CFG.get("venv", {}).get(role) or TOOLS / ("venv-align" if role == "align" else "venv-chung")
    return Path(path) / "Scripts" / "python.exe"


def setup_env(env=None):
    """Thêm ffmpeg vào PATH và chỉ chỗ lưu model (để model nặng không rơi vào ổ C)."""
    env = os.environ if env is None else env
    if FFMPEG_BIN and FFMPEG_BIN not in env.get("PATH", ""):
        env["PATH"] = FFMPEG_BIN + os.pathsep + env.get("PATH", "")
    over = CFG.get("env", {})  # ghi đè; "" = để thư viện dùng chỗ mặc định
    for key, sub in (("HF_HOME", "huggingface"), ("TORCH_HOME", "torch"), ("NLTK_DATA", "nltk"),
                     ("U2NET_HOME", "rembg")):
        value = over.get(key, str(MODELS / sub))
        if value:
            env.setdefault(key, value)
    env.setdefault("PYTHONUTF8", "1")
    return env
