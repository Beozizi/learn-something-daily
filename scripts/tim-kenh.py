r"""Tìm kênh mới cho khảo sát thị trường: tìm video gần đây theo từ khóa rồi gom về kênh.

    py scripts\tim-kenh.py "từ khóa 1" "từ khóa 2" … [--ngay 90] [--moi-tu-khoa 50] [--out tim-kenh.csv]

Mỗi từ khóa gọi search.list (video đăng trong N ngày, xếp theo lượt xem, tiếng Anh) —
tốn 100 đơn vị hạn mức/lần, nên 10 từ khóa ≈ 1 000 trên 10 000 đơn vị/ngày.
Kết quả: mỗi kênh một dòng, kèm sub, tổng view, số lần xuất hiện và vài tiêu đề mẫu
để lọc tay trước khi đưa vào danh sách khảo sát (khao-sat-kenh.py).
"""
import argparse
import csv
import datetime as dt
import importlib.util
from collections import defaultdict
from pathlib import Path

_spec = importlib.util.spec_from_file_location("khao_sat", Path(__file__).with_name("khao-sat-kenh.py"))
ks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ks)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tu_khoa", nargs="+")
    ap.add_argument("--ngay", type=int, default=90)
    ap.add_argument("--moi-tu-khoa", type=int, default=50, help="số video lấy mỗi từ khóa (tối đa 50)")
    ap.add_argument("--out", default=str(ks.GOC / "nghien-cuu-thi-truong" / "tim-kenh.csv"))
    a = ap.parse_args()
    key = ks.doc_key()

    tu = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.ngay)).strftime("%Y-%m-%dT%H:%M:%SZ")
    gap = defaultdict(lambda: {"lan": 0, "tu_khoa": set(), "tieu_de": []})
    for q in a.tu_khoa:
        r = ks.goi(key, "search", part="snippet", q=q, type="video", order="viewCount",
                   publishedAfter=tu, relevanceLanguage="en", maxResults=min(a.moi_tu_khoa, 50))
        print(f"{q}: {len(r.get('items', []))} video")
        for it in r.get("items", []):
            g = gap[it["snippet"]["channelId"]]
            g["lan"] += 1
            g["tu_khoa"].add(q)
            if len(g["tieu_de"]) < 3:
                g["tieu_de"].append(it["snippet"]["title"])

    dong = []
    for k in ks.lay_kenh(key, list(gap)):
        sn, st = k["snippet"], k["statistics"]
        g = gap[k["id"]]
        dong.append({
            "ten": sn["title"],
            "channel_id": k["id"],
            "link": f"https://www.youtube.com/channel/{k['id']}",
            "ngay_lap": sn["publishedAt"][:10],
            "quoc_gia": sn.get("country", ""),
            "sub": "" if st.get("hiddenSubscriberCount") else ks.so(st.get("subscriberCount")),
            "tong_view": ks.so(st.get("viewCount")),
            "tong_so_video": ks.so(st.get("videoCount")),
            "so_lan_xuat_hien": g["lan"],
            "tu_khoa": "; ".join(sorted(g["tu_khoa"])),
            "tieu_de_mau": " | ".join(g["tieu_de"]),
        })
    dong.sort(key=lambda d: (-d["so_lan_xuat_hien"], -(d["tong_view"] or 0)))
    ks.ghi_csv(a.out, dong)
    print(f"\n{len(dong)} kênh → {a.out}")


if __name__ == "__main__":
    main()
