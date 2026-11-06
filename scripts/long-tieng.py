"""Lồng tiếng từng cảnh trong 02-kich-ban.md bằng VieNeu-TTS (GPU).

Cách dùng (chạy bằng venv-tts):
    python scripts\\long-tieng.py <thư mục tập> [--voice "Thiện Minh"] [--gap 0.4] [--only 03 07]

Đầu ra trong <tập>\\audio\\:
    canh-NN.wav     lời đọc từng cảnh (--only chỉ đọc lại các cảnh này, cảnh khác dùng file cũ)
    loi-doc.wav     cả tập ghép lại, có khoảng lặng giữa các cảnh và theo "Thời lượng:"
    timeline.json   mốc thời gian từng cảnh cho bước căn chữ và dựng video
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

import cau_hinh

cau_hinh.setup_env()

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_RATE = 48_000
SCENE_RE = re.compile(r"^##\s+Cảnh\s+(\d+)\s*[·:\-–—]?\s*(.*)$")
EDGE_PUNCT = "\"'“”‘’()[]{}.,;:!?…«»"


def load_lexicon(path: Path) -> dict[str, str]:
    lexicon = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                lexicon[key.strip()] = value.strip()
    return lexicon


def parse_script(path: Path) -> list[dict]:
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    scenes = []
    for line in text.splitlines():
        line = line.strip()
        if m := SCENE_RE.match(line):
            scenes.append({"id": f"{int(m.group(1)):02d}", "title": m.group(2).strip(),
                           "visual": [], "min_duration": None, "lines": []})
        elif not scenes:
            continue
        elif line.startswith(">"):
            if spoken := line.lstrip(">").strip():
                scenes[-1]["lines"].append(spoken)
        elif line.lower().startswith("hình:"):
            if visual := line.split(":", 1)[1].strip():
                scenes[-1]["visual"].append(visual)
        elif line.lower().startswith("thời lượng:"):
            scenes[-1]["min_duration"] = float(re.findall(r"[\d.,]+", line)[0].replace(",", "."))
    for scene in scenes:
        scene["text"] = " ".join(scene.pop("lines"))
    return scenes


def tokenize(text: str, lexicon: dict[str, str]) -> list[dict]:
    """Tách từ, thay cách đọc theo từ điển; "show" là chữ hiển thị, "say" là chữ đưa vào TTS."""
    tokens = []
    for word in text.split():
        core = word.strip(EDGE_PUNCT)
        say = word.replace(core, lexicon[core], 1) if core in lexicon else word
        tokens.append({"show": word, "say": say})
    return tokens


def genmax_tts(text: str, args) -> np.ndarray:
    """Đọc một đoạn bằng GenMax API (ElevenLabs/MiniMax/CapCut), trả về mono 48 kHz.

    Key đọc từ .genmax_key.txt ở gốc dự án (hoặc GENMAX_API_KEY) — không in ra.
    """
    import os
    import subprocess
    import tempfile
    import time
    import requests

    key = os.environ.get("GENMAX_API_KEY") or (ROOT / ".genmax_key.txt").read_text(encoding="utf-8").strip()
    headers = {"xi-api-key": key, "Content-Type": "application/json"}
    body = {"text": text, "model_id": args.model, "provider": args.provider, "language_code": args.lang,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": args.speed}}
    r = requests.post(f"https://api.genmax.io/v1/text-to-speech/{args.voice}", headers=headers,
                      json=body, timeout=60)
    r.raise_for_status()
    task = r.json()["id"]
    for _ in range(240):
        time.sleep(3)
        d = requests.get(f"https://api.genmax.io/v1/history/{task}", headers=headers, timeout=30).json()
        if d["status"] == "completed":
            break
        if d["status"] == "failed":
            sys.exit(f"GenMax lỗi: {d.get('error')}")
    else:
        sys.exit("GenMax quá thời gian chờ")
    mp3 = requests.get(d["result"]["audio_url"], timeout=120).content
    with tempfile.TemporaryDirectory() as tmp:
        src, dst = Path(tmp) / "a.mp3", Path(tmp) / "a.wav"
        src.write_bytes(mp3)
        subprocess.run([cau_hinh.FFMPEG, "-v", "error", "-y", "-i", str(src), "-ac", "1", "-ar", str(SAMPLE_RATE),
                        str(dst)], check=True)
        audio, _ = sf.read(dst, dtype="float32")
    return audio


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Lồng tiếng kịch bản")
    parser.add_argument("episode", type=Path)
    parser.add_argument("--voice", default="Thiện Minh", help="VieNeu: tên giọng; GenMax: voice_id")
    parser.add_argument("--engine", choices=["vieneu", "genmax"], default="vieneu")
    parser.add_argument("--provider", default="elevenlabs", help="GenMax: elevenlabs / minimax / capcut")
    parser.add_argument("--model", default="eleven_v3", help="GenMax: model_id")
    parser.add_argument("--lang", default="en", help="GenMax: language_code")
    parser.add_argument("--speed", type=float, default=0.98, help="GenMax: tốc độ đọc")
    parser.add_argument("--gap", type=float, default=0.4, help="giây lặng giữa các cảnh")
    parser.add_argument("--only", nargs="+", help="chỉ đọc lại các cảnh này, VD: 03 07")
    args = parser.parse_args()

    script = args.episode / "02-kich-ban.md"
    if not script.exists():
        sys.exit(f"Không thấy {script}")
    scenes = parse_script(script)
    if not scenes:
        sys.exit("Kịch bản không có cảnh nào (cần dòng '## Cảnh NN · Tên')")
    only = {f"{int(s):02d}" for s in args.only} if args.only else None
    # phat-am.txt là cách đọc tiếng Việt — bỏ qua khi đọc bằng GenMax (tiếng Anh)
    lexicon = {} if args.engine == "genmax" else load_lexicon(ROOT / "assets" / "phat-am.txt")
    audio_dir = args.episode / "audio"
    audio_dir.mkdir(exist_ok=True)

    tts = None
    clips = []
    for scene in scenes:
        scene["tokens"] = tokenize(scene["text"], lexicon)
        scene["say_text"] = " ".join(t["say"] for t in scene["tokens"])
        wav = audio_dir / f"canh-{scene['id']}.wav"
        if not scene["text"]:
            clips.append(np.zeros(0, dtype=np.float32))
            continue
        if wav.exists() and only is not None and scene["id"] not in only:
            audio, _ = sf.read(wav, dtype="float32")
        else:
            print(f"Cảnh {scene['id']} · {scene['title']}")
            if args.engine == "genmax":
                audio = genmax_tts(scene["say_text"], args)
            else:
                if tts is None:
                    from vieneu import Vieneu
                    tts = Vieneu(device="cuda")
                audio = np.asarray(tts.infer(scene["say_text"], voice=args.voice), dtype=np.float32)
            sf.write(wav, audio, SAMPLE_RATE)
        clips.append(audio)

    # Ghép: mỗi cảnh kéo dài tới đầu cảnh sau, để các clip video phủ kín dòng thời gian.
    parts, t = [], 0.0
    for i, (scene, audio) in enumerate(zip(scenes, clips)):
        speech = len(audio) / SAMPLE_RATE
        length = max(speech, scene["min_duration"] or 0.0)
        if length == 0:
            print(f"Cảnh {scene['id']} không có lời và không có 'Thời lượng:', dùng 2 giây")
            length = 2.0
        if i < len(scenes) - 1:
            length += args.gap
        pad = round(length * SAMPLE_RATE) - len(audio)
        parts.append(np.concatenate([audio, np.zeros(pad, dtype=np.float32)]))
        scene.update(start=round(t, 3), speech_end=round(t + speech, 3), end=round(t + length, 3))
        t += length

    sf.write(audio_dir / "loi-doc.wav", np.concatenate(parts), SAMPLE_RATE)
    timeline = {"voice": args.voice, "sample_rate": SAMPLE_RATE, "duration": round(t, 3),
                "scenes": [{k: s[k] for k in ("id", "title", "start", "end", "speech_end",
                                             "min_duration", "visual", "text", "say_text", "tokens")}
                           for s in scenes]}
    (audio_dir / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2),
                                             encoding="utf-8")
    print(f"Tổng {t:.1f} giây · {len(scenes)} cảnh → {audio_dir / 'loi-doc.wav'}")


if __name__ == "__main__":
    main()
