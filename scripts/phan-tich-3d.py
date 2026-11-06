"""Phân tích cấu trúc 3D của ảnh để dựng chuyển động tốt hơn.

Chạy (cần venv-3d đầy đủ: torch, transformers, rtmlib — không có trong cai-dat.ps1):
  py scripts\\chay.py chung scripts\\phan-tich-3d.py <ảnh...> --out <thư mục>

Ảnh bối cảnh (không có kênh trong suốt):
  - Depth Anything V2 → bản đồ độ sâu (depth.png, 16 bit, sáng = gần) và pháp tuyến (normal.png)
  - tách thành N lớp theo độ sâu (lop-0 = xa nhất ... lop-N-1 = gần nhất), lớp xa được vá lỗ
    để camera trượt (parallax) không lộ chỗ trống
  - 3d.json: mỗi lớp có hệ số parallax gợi ý, khung bao, tâm; điểm nhìn chính (vùng gần nhất có nhiều chi tiết)
Ảnh nhân vật (PNG nền trong):
  - rtmlib (RTMPose) → khung xương 17 điểm; tính trục xoay (vai, khuỷu, cổ, hông) cho từng bộ phận
  - độ sâu của nhân vật → bóng nổi (shade.png) để phủ ánh sáng giả 3D
  - nhanvat.json: khớp, trục xoay, góc tay, hướng mặt
Kèm xem-truoc.jpg ghép các bản đồ để kiểm tra bằng mắt.
"""
import argparse, json, os, sys
from pathlib import Path

import cau_hinh

cau_hinh.setup_env()
os.environ.setdefault("HF_HOME", str(cau_hinh.MODELS / "huggingface"))  # Depth Anything nằm ở thư mục model

import numpy as np
import cv2
from PIL import Image

DEPTH_MODEL = "depth-anything/Depth-Anything-V2-Base-hf"
COCO = ["mui", "mat-trai", "mat-phai", "tai-trai", "tai-phai", "vai-trai", "vai-phai",
        "khuyu-trai", "khuyu-phai", "co-tay-trai", "co-tay-phai", "hong-trai", "hong-phai",
        "goi-trai", "goi-phai", "co-chan-trai", "co-chan-phai"]
_depth = None


def depth_of(rgb):
    """Độ sâu tương đối 0..1, 1 = gần camera."""
    global _depth
    if _depth is None:
        import torch
        from transformers import pipeline
        _depth = pipeline("depth-estimation", model=DEPTH_MODEL,
                          device=0 if torch.cuda.is_available() else -1)
    d = np.asarray(_depth(Image.fromarray(rgb))["predicted_depth"].squeeze().cpu().numpy(), np.float32)
    d = cv2.resize(d, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_CUBIC)
    lo, hi = np.percentile(d, [1, 99])
    return np.clip((d - lo) / (hi - lo + 1e-6), 0, 1).astype(np.float32)


def normals_of(d, strength=6.0):
    d = d.astype(np.float32)
    gx = cv2.Sobel(d, cv2.CV_32F, 1, 0, ksize=5)
    gy = cv2.Sobel(d, cv2.CV_32F, 0, 1, ksize=5)
    n = np.dstack([-gx * strength, -gy * strength, np.ones_like(d)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return n


def save_gray16(path, a):
    cv2.imwrite(str(path), (np.clip(a, 0, 1) * 65535).astype(np.uint16))


def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


def analyse_scene(path, out, n_layers, max_shift):
    bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]
    d = depth_of(rgb)
    save_gray16(out / "depth.png", d)
    n = normals_of(d)
    cv2.imwrite(str(out / "normal.png"), ((n[..., ::-1] * 0.5 + 0.5) * 255).astype(np.uint8))

    # gom lớp theo cụm độ sâu tự nhiên (k-means), để một bức tường phẳng không bị xé làm hai lớp
    ds = cv2.GaussianBlur(d, (0, 0), 3)
    _, lab, centers = cv2.kmeans(ds.reshape(-1, 1), n_layers, None,
                                 (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-3),
                                 3, cv2.KMEANS_PP_CENTERS)
    rank = np.argsort(np.argsort(centers.ravel()))  # 0 = xa nhất
    idx = cv2.medianBlur(rank[lab.ravel()].reshape(d.shape).astype(np.uint8), 15).astype(int)
    band = int(max_shift * 1.5) | 1
    layers = []
    for i in range(n_layers):
        own = (idx == i).astype(np.uint8)
        nearer = (idx > i).astype(np.uint8)
        src = bgr
        # lớp i = vùng của nó + một dải vá sau vật gần hơn, rộng hơn độ dịch tối đa → trượt không lộ lỗ
        if nearer.any():
            src = cv2.inpaint(bgr, cv2.dilate(nearer, np.ones((7, 7), np.uint8)), 9, cv2.INPAINT_TELEA)
        cover = own | (cv2.dilate(own, np.ones((band, band), np.uint8)) & nearer)
        alpha = cv2.GaussianBlur(cover.astype(np.float32), (0, 0), 1.5)
        if i == 0:
            alpha[:] = 1  # lớp xa nhất phủ kín khung
        rgba = np.dstack([src, (alpha * 255).astype(np.uint8)])
        cv2.imwrite(str(out / f"lop-{i}.png"), rgba)
        mean_d = float(d[idx == i].mean()) if (idx == i).any() else 0.0
        bb = bbox(idx == i)
        layers.append({
            "file": f"lop-{i}.png", "do-sau-tb": round(mean_d, 3),
            "parallax": round(mean_d, 3),
            "dich-toi-da-px": round(mean_d * max_shift, 1),
            "khung": bb, "dien-tich": round(float((idx == i).mean()), 3),
        })

    # điểm nhìn chính: vùng gần (top 15%) có nhiều cạnh
    near = d > np.percentile(d, 85)
    edges = cv2.Canny(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), 80, 160) > 0
    score = cv2.GaussianBlur((near & edges).astype(np.float32), (0, 0), w / 40)
    bx, by = w // 8, h // 8  # bỏ mép khung: vật cắt ngang mép không phải tâm điểm
    score[:by] = score[-by:] = 0
    score[:, :bx] = score[:, -bx:] = 0
    fy, fx = np.unravel_index(score.argmax(), score.shape)
    # chân trời ước lượng: hàng có độ sâu đổi nhanh nhất theo chiều dọc ở nửa trên
    row = d.mean(axis=1)
    horizon = int(np.argmax(np.abs(np.gradient(cv2.GaussianBlur(row.reshape(-1, 1), (1, 31), 0).ravel()))[: h * 2 // 3]))

    info = {
        "anh": str(path), "loai": "boi-canh", "kich-thuoc": [w, h], "model": DEPTH_MODEL,
        "lop": layers,
        "diem-nhin": {"x": int(fx), "y": int(fy), "ty-le": [round(fx / w, 3), round(fy / h, 3)]},
        "chan-troi-y": horizon,
        # lưới độ sâu 32×18 (ô = w/32 × h/18) để file dựng tra độ sâu tại chân nhân vật mà không cần numpy
        "luoi-do-sau": np.round(cv2.resize(d, (32, 18), interpolation=cv2.INTER_AREA), 2).tolist(),
        "goi-y": [
            f"Camera trượt ngang: lớp i dịch = hướng × parallax × {max_shift}px (gần dịch nhiều, xa gần như đứng yên).",
            f"Đẩy vào (push-in) hướng về điểm nhìn ({fx}, {fy}); lớp gần phóng nhanh hơn lớp xa.",
            "Đặt nhân vật lên mặt sàn: chân ở độ sâu gần bằng lớp gần nhất chứa vị trí đó; nhân vật ở xa thì thu nhỏ theo độ sâu.",
        ],
    }
    preview(out, [bgr, colorize(d), (n[..., ::-1] * 127 + 128).astype(np.uint8),
                  layer_map(idx, n_layers, bgr)], (fx, fy), horizon)
    return info


def colorize(d):
    return cv2.applyColorMap((d * 255).astype(np.uint8), cv2.COLORMAP_INFERNO)


def layer_map(idx, n, bgr):
    pal = cv2.applyColorMap(np.uint8(np.linspace(30, 230, n)).reshape(-1, 1), cv2.COLORMAP_VIRIDIS).reshape(-1, 3)
    return cv2.addWeighted(bgr, 0.45, pal[idx], 0.55, 0)


def preview(out, tiles, focus=None, horizon=None, joints=None):
    th = 360
    row = []
    for t in tiles:
        s = th / t.shape[0]
        t = cv2.resize(t, (int(t.shape[1] * s), th))
        if focus is not None:
            cv2.circle(t, (int(focus[0] * s), int(focus[1] * s)), 10, (0, 255, 255), 2)
        if horizon is not None:
            cv2.line(t, (0, int(horizon * s)), (t.shape[1], int(horizon * s)), (255, 200, 0), 1)
        if joints:
            for a, b in SKELETON:
                pa, pb = joints.get(a), joints.get(b)
                if pa and pb:
                    cv2.line(t, (int(pa[0] * s), int(pa[1] * s)), (int(pb[0] * s), int(pb[1] * s)), (0, 220, 255), 2)
            for p in joints.values():
                cv2.circle(t, (int(p[0] * s), int(p[1] * s)), 4, (0, 0, 255), -1)
        row.append(t)
    cv2.imwrite(str(out / "xem-truoc.jpg"), np.hstack(row), [cv2.IMWRITE_JPEG_QUALITY, 88])


SKELETON = [("vai-trai", "vai-phai"), ("vai-trai", "khuyu-trai"), ("khuyu-trai", "co-tay-trai"),
            ("vai-phai", "khuyu-phai"), ("khuyu-phai", "co-tay-phai"), ("vai-trai", "hong-trai"),
            ("vai-phai", "hong-phai"), ("hong-trai", "hong-phai"), ("hong-trai", "goi-trai"),
            ("goi-trai", "co-chan-trai"), ("hong-phai", "goi-phai"), ("goi-phai", "co-chan-phai"),
            ("mui", "mat-trai"), ("mui", "mat-phai")]
_pose = None


def pose_of(bgr, box):
    global _pose
    if _pose is None:
        from rtmlib import RTMPose
        dev = "cpu"  # onnxruntime-gpu cần CUDA 13; RTMPose trên CPU vẫn nhanh
        _pose = RTMPose(
            "https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/onnx_sdk/"
            "rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.zip",
            model_input_size=(192, 256), backend="onnxruntime", device=dev)
    kp, sc = _pose(bgr, bboxes=[box])
    return kp[0], sc[0]


def angle(a, b):
    return round(float(np.degrees(np.arctan2(b[1] - a[1], b[0] - a[0]))), 1)


def analyse_character(path, out, min_score):
    rgba = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    alpha = rgba[..., 3].astype(np.float32) / 255
    bgr = rgba[..., :3].copy()
    # nền xám trung tính cho model (nền trong suốt dễ làm sai)
    comp = (bgr * alpha[..., None] + 200 * (1 - alpha[..., None])).astype(np.uint8)
    h, w = alpha.shape
    bb = bbox(alpha > 0.5)
    kp, sc = pose_of(comp, bb)
    joints, conf = {}, {}
    for name, p, s in zip(COCO, kp, sc):
        conf[name] = round(float(s), 3)
        if s >= min_score:
            joints[name] = [round(float(p[0]), 1), round(float(p[1]), 1)]

    def mid(a, b):
        return [round((joints[a][0] + joints[b][0]) / 2, 1), round((joints[a][1] + joints[b][1]) / 2, 1)] \
            if a in joints and b in joints else None

    pivots = {
        "dau (xoay quanh cổ)": mid("vai-trai", "vai-phai"),
        "tay-trai-tren (vai)": joints.get("vai-trai"), "tay-trai-duoi (khuỷu)": joints.get("khuyu-trai"),
        "tay-phai-tren (vai)": joints.get("vai-phai"), "tay-phai-duoi (khuỷu)": joints.get("khuyu-phai"),
        "than (hông)": mid("hong-trai", "hong-phai"),
    }
    ang = {}
    for seg, (a, b) in {"canh-tay-trai": ("vai-trai", "khuyu-trai"), "cang-tay-trai": ("khuyu-trai", "co-tay-trai"),
                        "canh-tay-phai": ("vai-phai", "khuyu-phai"), "cang-tay-phai": ("khuyu-phai", "co-tay-phai"),
                        "vai": ("vai-trai", "vai-phai")}.items():
        if a in joints and b in joints:
            ang[seg] = angle(joints[a], joints[b])
    face = None
    if {"mui", "mat-trai", "mat-phai"} <= joints.keys():
        eye_mid = (joints["mat-trai"][0] + joints["mat-phai"][0]) / 2
        span = abs(joints["mat-trai"][0] - joints["mat-phai"][0]) + 1e-6
        face = round((joints["mui"][0] - eye_mid) / span, 2)  # <0 quay sang trái ảnh, >0 sang phải

    d = (depth_of(comp) * (alpha > 0.5)).astype(np.float32)
    n = normals_of(d, 10)
    light = np.array([-0.5, -0.6, 0.62]); light /= np.linalg.norm(light)
    shade = np.clip((n @ light), 0, 1)
    shade_rgba = np.dstack([np.full_like(alpha, 255), np.full_like(alpha, 255), np.full_like(alpha, 255),
                            alpha * np.clip(shade - 0.55, 0, 1) * 255 * 1.6]).astype(np.uint8)
    cv2.imwrite(str(out / "shade.png"), shade_rgba)
    save_gray16(out / "depth.png", d)

    info = {
        "anh": str(path), "loai": "nhan-vat", "kich-thuoc": [w, h], "khung": bb,
        "khop": joints, "do-tin-cay": conf, "truc-xoay": pivots, "goc-do": ang,
        "huong-mat": face,
        "goi-y": [
            "Xoay đầu quanh trục cổ ±4°, tay quanh vai/khuỷu theo góc đo được; cần tách lớp bộ phận (SAM/rembg) nếu muốn cử động tay thật.",
            "shade.png phủ chế độ screen/soft-light để tạo khối sáng giả 3D khi nhân vật quay về phía nguồn sáng.",
            "Điểm có độ tin cậy < ngưỡng bị bỏ — nhân vật hoạt hình đầu to có thể làm lệch mặt/vai, kiểm tra xem-truoc.jpg.",
        ],
    }
    preview(out, [comp, colorize(d), (n[..., ::-1] * 127 + 128).astype(np.uint8)], joints=joints)
    return info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("anh", nargs="+")
    ap.add_argument("--out", required=True, help="thư mục gốc; mỗi ảnh một thư mục con")
    ap.add_argument("--lop", type=int, default=4, help="số lớp độ sâu cho bối cảnh")
    ap.add_argument("--dich", type=float, default=60, help="độ dịch tối đa (px) của lớp gần nhất")
    ap.add_argument("--nguong", type=float, default=0.3, help="độ tin cậy tối thiểu của khớp")
    a = ap.parse_args()
    for p in map(Path, a.anh):
        out = Path(a.out) / p.stem
        out.mkdir(parents=True, exist_ok=True)
        im = Image.open(p)
        has_alpha = im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 128
        info = analyse_character(p, out, a.nguong) if has_alpha else analyse_scene(p, out, a.lop, a.dich)
        (out / "3d.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{p.name}: {info['loai']} → {out}")


if __name__ == "__main__":
    main()
