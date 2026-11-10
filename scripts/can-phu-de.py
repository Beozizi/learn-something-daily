"""Căn thời gian từng chữ, từng câu của lời đọc bằng WhisperX.

Căn theo đúng văn bản kịch bản (không nhận dạng lại), nên chữ luôn khớp kịch bản.
Từ được thay cách đọc qua assets\\phat-am.txt vẫn hiện chữ gốc.

Cách dùng (sau long-tieng.py):
    py scripts\\chay.py align scripts\\can-phu-de.py <thư mục tập> [--lang en]

Đầu ra trong <tập>\\audio\\:
    words.json    {"words": [...], "sentences": [...]}, mỗi mục có text, start, end, scene
    phu-de.srt    phụ đề để tải lên YouTube / dùng cho bản dọc
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

import cau_hinh  # noqa: E402

# ffmpeg vào PATH; nltk + mô hình căn (torchaudio) lưu ở thư mục model của máy, không rơi vào ổ C
cau_hinh.setup_env()

import torch  # noqa: E402
import whisperx  # noqa: E402

# Mô hình mặc định của WhisperX cho tiếng Việt (wav2vec2-base-vi-vlsp2020) nạp sai trọng số
# với bản transformers hiện tại và căn ra toàn rác, nên dùng mô hình 250h này.
ALIGN_MODEL = "nguyenvulebinh/wav2vec2-base-vietnamese-250h"
LOW_SCORE = 0.4
SENTENCE_END = (".", "!", "?", "…")
MAX_CUE_WORDS = 8
MAX_CUE_CHARS = 42


def fill_missing(items: list[dict], lo: float, hi: float) -> None:
    """Chữ WhisperX không căn được (số, ký hiệu) được chia đều vào khoảng trống quanh nó."""
    i = 0
    while i < len(items):
        if "start" in items[i]:
            i += 1
            continue
        j = i
        while j < len(items) and "start" not in items[j]:
            j += 1
        left = items[i - 1]["end"] if i > 0 else lo
        right = items[j]["start"] if j < len(items) else hi
        step = max(right - left, 0.0) / (j - i)
        for k in range(i, j):
            items[k]["start"] = left + step * (k - i)
            items[k]["end"] = left + step * (k - i + 1)
        i = j


def align_scene(scene: dict, model, metadata, audio, device: str) -> list[dict]:
    segment = {"text": scene["say_text"], "start": scene["start"], "end": scene["speech_end"]}
    result = whisperx.align([segment], model, metadata, audio, device)
    spoken = [{k: w[k] for k in ("word", "start", "end", "score") if k in w}
              for seg in result["segments"] for w in seg.get("words", [])]
    expected = sum(len(t["say"].split()) for t in scene["tokens"])
    if len(spoken) != expected:
        print(f"Cảnh {scene['id']}: căn được {len(spoken)}/{expected} chữ, chia đều theo độ dài")
        spoken = [{} for _ in range(expected)]
    unclear = [f"{w['word']}@{w['start']:.1f}s" for w in spoken if w.get("score", 1) < LOW_SCORE]
    if unclear:
        print(f"Cảnh {scene['id']}: nghe lại các chữ có thể đọc sai: {', '.join(unclear)}")
    fill_missing(spoken, scene["start"], scene["speech_end"])

    words, i = [], 0
    for token in scene["tokens"]:
        n = len(token["say"].split())
        words.append({"text": token["show"], "start": round(spoken[i]["start"], 3),
                      "end": round(spoken[i + n - 1]["end"], 3), "scene": scene["id"]})
        i += n
    return words


def group(words: list[dict], is_break) -> list[dict]:
    groups, current = [], []
    for k, word in enumerate(words):
        current.append(word)
        last = k == len(words) - 1 or words[k + 1]["scene"] != word["scene"]
        if last or is_break(current, word):
            groups.append({"text": " ".join(w["text"] for w in current), "start": current[0]["start"],
                           "end": current[-1]["end"], "scene": word["scene"]})
            current = []
    return groups


def het_cau(text: str) -> bool:
    """Chữ kết thúc câu. Chữ viết tắt một chữ cái ("E." trong "E. coli") không tính."""
    return text.endswith(SENTENCE_END) and not (len(text) == 2 and text[0].isupper())


def cue_break(current: list[dict], word: dict) -> bool:
    chars = sum(len(w["text"]) + 1 for w in current)
    return (het_cau(word["text"]) or len(current) >= MAX_CUE_WORDS
            or chars >= MAX_CUE_CHARS or (word["text"].endswith((",", ";", ":")) and len(current) >= 4))


def srt_time(seconds: float) -> str:
    ms = round(seconds * 1000)
    return f"{ms // 3_600_000:02d}:{ms // 60_000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Căn thời gian từng chữ")
    parser.add_argument("episode", type=Path)
    parser.add_argument("--lang", default="vi", help="vi (mặc định) hoặc en cho bản tiếng Anh")
    args = parser.parse_args()

    audio_dir = args.episode / "audio"
    timeline_path = audio_dir / "timeline.json"
    if not timeline_path.exists():
        sys.exit(f"Chưa có {timeline_path} — chạy long-tieng.py trước")
    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))

    device = "cuda" if torch.cuda.is_available() else "cpu"
    audio = whisperx.load_audio(str(audio_dir / "loi-doc.wav"))
    model, metadata = whisperx.load_align_model(language_code=args.lang, device=device,
                                                model_name=ALIGN_MODEL if args.lang == "vi" else None)

    words = []
    for scene in timeline["scenes"]:
        if scene["text"]:
            words += align_scene(scene, model, metadata, audio, device)

    sentences = group(words, lambda cur, w: het_cau(w["text"]))
    (audio_dir / "words.json").write_text(
        json.dumps({"words": words, "sentences": sentences}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    cues = group(words, cue_break)
    srt = "\n".join(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text']}\n"
                    for i, c in enumerate(cues, 1))
    (audio_dir / "phu-de.srt").write_text(srt, encoding="utf-8")
    print(f"{len(words)} chữ · {len(sentences)} câu · {len(cues)} dòng phụ đề → {audio_dir}")


if __name__ == "__main__":
    main()
