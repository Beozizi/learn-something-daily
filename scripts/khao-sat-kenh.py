r"""Khảo sát thị trường: lấy số liệu các kênh YouTube qua YouTube Data API v3.

    py scripts\khao-sat-kenh.py <file danh sách kênh> [--ngay 90] [--nguong 3]
                               [--so-sanh <kenh.csv lần trước>] [--out <thư mục>]

File danh sách: CSV xuất từ Google Sheet (File → Tải xuống → CSV) hoặc file chữ bất kỳ
có link kênh — script tự nhặt mã `UC…` và `@handle`.
Key: `.youtube_key.txt` ở gốc dự án (không đưa lên repo) hoặc biến môi trường YOUTUBE_API_KEY.

Ghi ra `nghien-cuu-thi-truong\<ngày>\` (UTF-8, mở được bằng Excel / dán vào Sheet):
  kenh.csv     mỗi kênh một dòng: sub, tổng view, nhịp đăng, view trung bình/trung vị
               của video trong N ngày, video top; có --so-sanh thì thêm mức tăng/ngày.
  video.csv    mọi video trong N ngày, kèm hệ số = view / trung vị của kênh.
  outlier.csv  video có hệ số ≥ ngưỡng (mặc định 3×) — nguyên liệu chọn chủ đề.

Video đăng chưa đủ 7 ngày không tính vào trung vị và outlier (chưa kịp lên view).
Hạn mức API: ~3–5 đơn vị/kênh, 49 kênh tốn khoảng 250 trên 10 000 đơn vị/ngày miễn phí.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
API = "https://www.googleapis.com/youtube/v3/"
TUOI_TOI_THIEU = 7  # ngày


def doc_key():
    key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    f = GOC / ".youtube_key.txt"
    if not key and f.exists():
        key = f.read_text(encoding="utf-8").strip()
    if not key:
        sys.exit("Thiếu key: tạo .youtube_key.txt ở gốc dự án (YouTube Data API v3) "
                 "hoặc đặt biến YOUTUBE_API_KEY.")
    return key


def goi(key, endpoint, **params):
    params["key"] = key
    url = API + endpoint + "?" + urllib.parse.urlencode(params)
    for lan in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            loi = e.read().decode("utf-8", "replace")
            try:
                loi = json.loads(loi)["error"]["message"]
            except (ValueError, KeyError):
                pass
            if e.code in (500, 503) and lan < 2:
                time.sleep(2 * (lan + 1))
                continue
            sys.exit(f"Lỗi API {e.code} ({endpoint}): {loi}")
        except urllib.error.URLError as e:
            if lan < 2:
                time.sleep(2 * (lan + 1))
                continue
            sys.exit(f"Không kết nối được API: {e.reason}")


def nhat_kenh(path):
    """Nhặt mã kênh UC… và @handle theo thứ tự xuất hiện, bỏ trùng."""
    chu = Path(path).read_text(encoding="utf-8-sig")
    thay = re.findall(r"(UC[0-9A-Za-z_-]{22})|youtube\.com/(@[\w.\-]+)", chu)
    ra, da = [], set()
    for uc, handle in thay:
        k = uc or handle
        if k not in da:
            da.add(k)
            ra.append(k)
    return ra


def theo_lo(ds, n=50):
    for i in range(0, len(ds), n):
        yield ds[i:i + n]


def thoi_luong(iso):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, p, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + p * 60 + s


def ngay(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def so(x):
    return int(x) if x not in (None, "") else None


def lay_kenh(key, ds):
    uc = [k for k in ds if k.startswith("UC")]
    for h in (k for k in ds if k.startswith("@")):
        r = goi(key, "channels", part="id", forHandle=h)
        if r.get("items"):
            uc.append(r["items"][0]["id"])
        else:
            print(f"  ! không tìm thấy {h}")
    kenh = {}
    for lo in theo_lo(uc):
        r = goi(key, "channels", part="snippet,statistics,contentDetails", id=",".join(lo))
        for it in r.get("items", []):
            kenh[it["id"]] = it
    for k in uc:
        if k not in kenh:
            print(f"  ! kênh {k} không còn hoặc bị ẩn")
    return [kenh[k] for k in uc if k in kenh]


def lay_video(key, uploads, moc, toi_da):
    """Video của kênh đăng sau mốc `moc` (danh sách uploads xếp mới → cũ)."""
    ids, trang = [], None
    while len(ids) < toi_da:
        r = goi(key, "playlistItems", part="contentDetails", playlistId=uploads,
                maxResults=50, **({"pageToken": trang} if trang else {}))
        het = False
        for it in r.get("items", []):
            cd = it["contentDetails"]
            if "videoPublishedAt" not in cd:
                continue  # video riêng tư / đã xóa
            if ngay(cd["videoPublishedAt"]) < moc:
                het = True
                break
            ids.append(cd["videoId"])
        trang = r.get("nextPageToken")
        if het or not trang:
            break
    video = []
    for lo in theo_lo(ids[:toi_da]):
        r = goi(key, "videos", part="snippet,statistics,contentDetails", id=",".join(lo))
        video += [v for v in r.get("items", []) if "viewCount" in v.get("statistics", {})]
    return video


def ghi_csv(path, dong):
    if not dong:
        return
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(dong[0]))
        w.writeheader()
        w.writerows(dong)


def doc_lan_truoc(path):
    with open(path, encoding="utf-8-sig") as f:
        return {d["channel_id"]: d for d in csv.DictReader(f)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vao", help="file chứa link kênh (CSV từ Sheet, txt…)")
    ap.add_argument("--ngay", type=int, default=90, help="cửa sổ video gần đây (mặc định 90)")
    ap.add_argument("--nguong", type=float, default=3.0, help="hệ số outlier (mặc định 3)")
    ap.add_argument("--toi-da", type=int, default=300, help="số video tối đa mỗi kênh")
    ap.add_argument("--so-sanh", help="kenh.csv của lần lấy trước để tính mức tăng")
    ap.add_argument("--out", help="thư mục ghi kết quả")
    a = ap.parse_args()

    ds = nhat_kenh(a.vao)
    print(f"Đọc được {len(ds)} kênh từ {a.vao}")
    if not ds:
        sys.exit("Không thấy link kênh nào (cần dạng /channel/UC… hoặc /@handle).")
    key = doc_key()

    bay_gio = dt.datetime.now(dt.timezone.utc)
    moc = bay_gio - dt.timedelta(days=a.ngay)
    hom_nay = bay_gio.astimezone().date().isoformat()
    out = Path(a.out) if a.out else GOC / "nghien-cuu-thi-truong" / hom_nay
    out.mkdir(parents=True, exist_ok=True)
    truoc = doc_lan_truoc(a.so_sanh) if a.so_sanh else {}

    dong_kenh, dong_video = [], []
    for i, k in enumerate(lay_kenh(key, ds), 1):
        sn, st = k["snippet"], k["statistics"]
        sub = None if st.get("hiddenSubscriberCount") else so(st.get("subscriberCount"))
        print(f"[{i}] {sn['title']}")
        video = lay_video(key, k["contentDetails"]["relatedPlaylists"]["uploads"], moc, a.toi_da)

        vd = []
        for v in video:
            dang = ngay(v["snippet"]["publishedAt"])
            tuoi = max((bay_gio - dang).total_seconds() / 86400, 0.1)
            view = int(v["statistics"]["viewCount"])
            giay = thoi_luong(v["contentDetails"].get("duration"))
            vd.append({
                "kenh": sn["title"],
                "channel_id": k["id"],
                "tieu_de": v["snippet"]["title"],
                "link": f"https://www.youtube.com/watch?v={v['id']}",
                "ngay_dang": dang.date().isoformat(),
                "so_ngay": round(tuoi),
                "view": view,
                "like": so(v["statistics"].get("likeCount")),
                "comment": so(v["statistics"].get("commentCount")),
                "thoi_luong_phut": round(giay / 60, 1),
                "video_ngan": "có" if giay <= 180 else "",
                "view_moi_ngay": round(view / tuoi),
                "view_tren_sub": round(view / sub, 2) if sub else "",
                "he_so": "",
            })

        du_tuoi = [d for d in vd if d["so_ngay"] >= TUOI_TOI_THIEU]
        trung_vi = statistics.median(d["view"] for d in du_tuoi) if du_tuoi else 0
        for d in du_tuoi:
            d["he_so"] = round(d["view"] / trung_vi, 1) if trung_vi else ""
        dong_video += vd

        top = max(vd, key=lambda d: d["view"], default=None)
        dai = [d["thoi_luong_phut"] for d in vd if not d["video_ngan"]]
        dong = {
            "ten": sn["title"],
            "channel_id": k["id"],
            "link": f"https://www.youtube.com/channel/{k['id']}",
            "ngay_lap": sn["publishedAt"][:10],
            "quoc_gia": sn.get("country", ""),
            "sub": sub if sub is not None else "",
            "tong_view": so(st.get("viewCount")),
            "tong_so_video": so(st.get("videoCount")),
            f"video_{a.ngay}n": len(vd),
            f"video_ngan_{a.ngay}n": sum(1 for d in vd if d["video_ngan"]),
            "video_moi_tuan": round(len(vd) / (a.ngay / 7), 1),
            f"view_{a.ngay}n": sum(d["view"] for d in vd),
            "view_tb_video": round(statistics.mean(d["view"] for d in du_tuoi)) if du_tuoi else "",
            "view_trung_vi_video": round(trung_vi) if du_tuoi else "",
            "thoi_luong_trung_vi_phut": round(statistics.median(dai), 1) if dai else "",
            "video_top": top["tieu_de"] if top else "",
            "video_top_view": top["view"] if top else "",
            "video_top_link": top["link"] if top else "",
            "ngay_lay": hom_nay,
        }
        cu = truoc.get(k["id"])
        if cu:
            so_ngay = (dt.date.fromisoformat(hom_nay) - dt.date.fromisoformat(cu["ngay_lay"])).days
            tang_view = (dong["tong_view"] or 0) - int(cu["tong_view"] or 0)
            dong["so_ngay_tu_lan_truoc"] = so_ngay
            dong["view_tang"] = tang_view
            dong["sub_tang"] = (sub - int(cu["sub"])) if sub is not None and cu["sub"] else ""
            dong["view_tang_moi_ngay"] = round(tang_view / so_ngay) if so_ngay > 0 else ""
        dong_kenh.append(dong)

    # cột so sánh chỉ có ở một số kênh → điền trống cho đủ cột
    cot = list(dict.fromkeys(c for d in dong_kenh for c in d))
    dong_kenh = [{c: d.get(c, "") for c in cot} for d in dong_kenh]
    dong_kenh.sort(key=lambda d: d[f"view_{a.ngay}n"], reverse=True)
    outlier = sorted((d for d in dong_video if d["he_so"] != "" and d["he_so"] >= a.nguong),
                     key=lambda d: d["he_so"], reverse=True)

    ghi_csv(out / "kenh.csv", dong_kenh)
    ghi_csv(out / "video.csv", dong_video)
    ghi_csv(out / "outlier.csv", outlier)
    print(f"\nXong: {len(dong_kenh)} kênh, {len(dong_video)} video, {len(outlier)} outlier "
          f"(≥ {a.nguong:g}× trung vị) → {out}")


if __name__ == "__main__":
    main()
