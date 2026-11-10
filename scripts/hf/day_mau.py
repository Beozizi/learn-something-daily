"""Nền tối hơn, dải màu rộng hơn — cùng nguyên tắc với kênh Kurzgesagt (scripts\\kg\\mau.py):
tính trong OKLCH, giữ sắc độ H; vùng tối hạ độ sáng L về gần đen; độ đậm C nhân lên rồi ép vào sRGB
ở đúng L, H (không cắt kênh RGB nên không lệch màu). Không thêm vignette, đường cong hay hiệu ứng.

Áp cho cả mã màu SVG/CSS (core.Comp.write tự gọi day_html khi core.DAY_MAU) và ảnh nền/nhân vật:
    py scripts\\chay.py chung scripts\\hf\\day_mau.py tap\\<tập>
(ảnh gốc giữ ở video\\assets\\_goc\\, chạy lại bao nhiêu lần cũng tính từ gốc).
"""
import math
import re
import sys
from pathlib import Path

DAM = 1.45                # hệ số độ đậm C
TOI_TU, TOI_DEN = .12, .62  # khoảng độ sáng L được hạ dần (dưới TOI_DEN mới bị hạ)
TOI_MIN = .5              # L thấp nhất bị nhân với hệ số này


def _ss(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3 - 2 * t)


def _lin(c):
    return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= .0031308 else 1.055 * c ** (1 / 2.4) - .055


def _to_lab(r, g, b):
    r, g, b = _lin(r), _lin(g), _lin(b)
    l = (.4122214708 * r + .5363325363 * g + .0514459929 * b) ** (1 / 3)
    m = (.2119034982 * r + .6806995451 * g + .1073969566 * b) ** (1 / 3)
    s = (.0883024619 * r + .2817188376 * g + .6299787005 * b) ** (1 / 3)
    return (.2104542553 * l + .7936177850 * m - .0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + .4505937099 * s,
            .0259040371 * l + .7827717662 * m - .8086757660 * s)


def _to_rgb(L, a, b):
    l = (L + .3963377774 * a + .2158037573 * b) ** 3
    m = (L - .1055613458 * a - .0638541728 * b) ** 3
    s = (L - .0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + .2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - .3413193965 * s,
            -.0041960863 * l - .7034186147 * m + 1.7076147010 * s)


def _ok(rgb):
    return all(-1e-4 <= v <= 1 + 1e-4 for v in rgb)


def day(hexs):
    """Một mã #RRGGBB → mã đã đẩy (nền tối hơn, màu đậm hơn, cùng sắc độ)."""
    h = hexs.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    L, A, B = _to_lab(r, g, b)
    L2 = L * (TOI_MIN + (1 - TOI_MIN) * _ss(TOI_TU, TOI_DEN, L))
    lo, hi = 0.0, DAM
    if _ok(_to_rgb(L2, A * hi, B * hi)):
        lo = hi
    else:
        for _ in range(24):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if _ok(_to_rgb(L2, A * mid, B * mid)) else (lo, mid)
    out = [_gam(min(max(v, 0.0), 1.0)) for v in _to_rgb(L2, A * lo, B * lo)]
    return "#" + "".join(f"{round(v * 255):02X}" for v in out)


_HEX = re.compile(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b")
_RGBA = re.compile(r"rgba?\((\d+),\s*(\d+),\s*(\d+)")


def day_html(text):
    """Đẩy mọi mã màu trong HTML/SVG/CSS (#hex và rgb()/rgba())."""
    cache = {}

    def hx(m):
        k = m.group(0).upper()
        if k not in cache:
            cache[k] = day(k)
        return cache[k]

    def rg(m):
        v = day("#" + "".join(f"{int(x):02X}" for x in m.groups()))
        return f"rgba({int(v[1:3], 16)}, {int(v[3:5], 16)}, {int(v[5:7], 16)}" if m.group(0).startswith("rgba") \
            else f"rgb({int(v[1:3], 16)}, {int(v[3:5], 16)}, {int(v[5:7], 16)}"
    return _RGBA.sub(rg, _HEX.sub(hx, text))


def day_anh(src, dst):
    """Cùng phép biến đổi cho từng điểm ảnh (giữ kênh alpha)."""
    import numpy as np
    from PIL import Image
    im = Image.open(src)
    has_a = im.mode in ("RGBA", "LA") or "transparency" in im.info
    im = im.convert("RGBA" if has_a else "RGB")
    arr = np.asarray(im).astype(np.float64) / 255
    rgb = arr[..., :3]
    lin = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
    M1 = np.array([[.4122214708, .5363325363, .0514459929], [.2119034982, .6806995451, .1073969566],
                   [.0883024619, .2817188376, .6299787005]])
    M2 = np.array([[.2104542553, .7936177850, -.0040720468], [1.9779984951, -2.4285922050, .4505937099],
                   [.0259040371, .7827717662, -.8086757660]])
    lab = np.cbrt(lin @ M1.T) @ M2.T
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    t = np.clip((L - TOI_TU) / (TOI_DEN - TOI_TU), 0, 1)
    L2 = L * (TOI_MIN + (1 - TOI_MIN) * t * t * (3 - 2 * t))
    N1 = np.linalg.inv(M2)
    N2 = np.linalg.inv(M1)

    def back(k):
        lab2 = np.stack([L2, A * k, B * k], -1)
        return (lab2 @ N1.T) ** 3 @ N2.T

    def inside(k):
        v = back(k)
        return np.all((v >= -1e-4) & (v <= 1 + 1e-4), -1)
    lo = np.zeros_like(L)
    hi = np.full_like(L, DAM)
    full = inside(hi)
    for _ in range(14):
        mid = (lo + hi) / 2
        ok = inside(mid)
        lo = np.where(ok, mid, lo)
        hi = np.where(ok, hi, mid)
    k = np.where(full, DAM, lo)
    out = np.clip(back(k), 0, 1)
    out = np.where(out <= .0031308, 12.92 * out, 1.055 * np.power(out, 1 / 2.4) - .055)
    arr[..., :3] = out
    res = Image.fromarray((arr * 255 + .5).clip(0, 255).astype(np.uint8), im.mode)
    res.save(dst, quality=95) if str(dst).lower().endswith((".jpg", ".jpeg")) else res.save(dst)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    vid = Path(sys.argv[1]) / "video" / "assets"
    goc = vid / "_goc"
    n = 0
    for sub in ("bg", "char"):
        for p in sorted((vid / sub).glob("*.*")):
            if p.suffix.lower() not in (".jpg", ".jpeg", ".png"):
                continue
            g = goc / sub / p.name
            if not g.exists():
                g.parent.mkdir(parents=True, exist_ok=True)
                p.replace(g)
            day_anh(g, p)
            n += 1
    print(f"Đã đẩy màu {n} ảnh (gốc ở {goc})")


if __name__ == "__main__":
    main()
