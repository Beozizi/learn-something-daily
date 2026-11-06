"""Sinh bộ tư thế SVG của nhân vật Tò từ chung một bộ phận.

Cách dùng (Python bất kỳ, không cần thư viện ngoài):
    py assets\\nhan-vat\\to\\tao-tu-the.py

Sửa màu, tay, nét mặt ở đây rồi chạy lại — đừng sửa tay các file .svg.
Đầu ra cạnh script: <tư-thế>.svg và xem-truoc.html (bảng xem tất cả tư thế).

Các class trong mỗi SVG (gốc có id="to-<tư-thế>") (dùng để diễn hoạt trong HyperFrames):
    .to          cả nhân vật          .dau        đầu (nghiêng, gật)
    .than        thân + chân          .tay-trai / .tay-phai   hai tay (trái/phải theo người xem)
    .mat         hai mắt (chớp: scaleY)            .long-may   lông mày
    .mieng       miệng của tư thế     .mieng-noi  miệng há khi nói (mặc định ẩn)
    .them        chi tiết phụ của biểu cảm (giọt mồ hôi, dấu chấm than…)
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent

INK = "#081420"
SKIN = "#F2C29B"
HAIR = "#1E2A3A"
SWEATER = "#FFC145"
SWEATER_DARK = "#E5A024"
PANTS = "#1E3A56"
SHOE = "#F5F7FA"
CHEEK = "#FF8A7A"
CARD = "#F5F1E8"
BADGE = "#19C3B1"
W = 6  # độ dày nét viền
ARM_W = 30  # độ dày tay áo (chibi: tay ngắn, mập)
HAND_R = 18

# Dáng chibi: đầu giữ nguyên (tâm 180,180), thân thấp tròn, chân ngắn, mặt đất y = 502.
LEFT_SHOULDER = (130, 312)
RIGHT_SHOULDER = (230, 312)
LEFT_EYE = (145, 199)
RIGHT_EYE = (215, 199)


def arm(id_, points, finger=None):
    """Tay là một đường gấp khúc vai → khuỷu → cổ tay, viền đậm, ống tay áo len, bàn tay tròn."""
    d = "M" + " L".join(f"{x} {y}" for x, y in points)
    hx, hy = points[-1]
    cuff_from = points[-2]
    # đoạn cổ tay áo ngay trước bàn tay
    dx, dy = hx - cuff_from[0], hy - cuff_from[1]
    length = (dx * dx + dy * dy) ** 0.5 or 1
    cx, cy = hx - dx / length * 12, hy - dy / length * 12
    cx2, cy2 = hx - dx / length * 26, hy - dy / length * 26
    parts = [
        f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{ARM_W + 2 * W}" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{SWEATER}" stroke-width="{ARM_W}" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M{cx2:.1f} {cy2:.1f} L{cx:.1f} {cy:.1f}" stroke="{SWEATER_DARK}" stroke-width="{ARM_W}" stroke-linecap="butt"/>',
    ]
    if finger:
        fx, fy = finger
        parts += [
            f'<path d="M{hx} {hy} L{fx} {fy}" stroke="{INK}" stroke-width="{12 + 2 * W}" stroke-linecap="round"/>',
            f'<path d="M{hx} {hy} L{fx} {fy}" stroke="{SKIN}" stroke-width="12" stroke-linecap="round"/>',
        ]
    parts.append(f'<circle cx="{hx}" cy="{hy}" r="{HAND_R}" fill="{SKIN}" stroke="{INK}" stroke-width="{W}"/>')
    return f'<g class="{id_}">' + "".join(parts) + "</g>"


def body():
    return f"""<g class="than" stroke="{INK}" stroke-width="{W}" stroke-linejoin="round" stroke-linecap="round">
  <rect x="142" y="414" width="36" height="72" rx="17" fill="{PANTS}"/>
  <rect x="182" y="414" width="36" height="72" rx="17" fill="{PANTS}"/>
  <path d="M116 502 Q114 476 140 476 L168 476 Q182 476 182 492 L182 502 Z" fill="{SHOE}"/>
  <path d="M178 492 Q178 476 192 476 L220 476 Q246 476 244 502 L178 502 Z" fill="{SHOE}"/>
  <path d="M116 502 H182 M178 502 H244" stroke-width="{W + 2}"/>
  <rect x="168" y="266" width="24" height="32" fill="{SKIN}"/>
  <path d="M130 300 Q180 284 230 300 Q252 360 256 428 Q180 446 104 428 Q108 360 130 300 Z" fill="{SWEATER}"/>
  <path d="M106 410 Q180 428 254 410 L256 428 Q180 446 104 428 Z" fill="{SWEATER_DARK}"/>
  <path d="M156 294 Q180 322 204 294" fill="{CARD}"/>
  <circle cx="210" cy="362" r="14" fill="{BADGE}"/>
  <path d="M205 357 q5 -7 10 0 q0 5 -5 7 v3" fill="none" stroke-width="3.5"/>
  <circle cx="210" cy="371.5" r="1.6" fill="{INK}" stroke="none"/>
</g>"""


def head(face):
    return f"""<g class="dau">
 <g stroke="{INK}" stroke-width="{W}" stroke-linejoin="round" stroke-linecap="round">
  <circle cx="82" cy="200" r="19" fill="{SKIN}"/>
  <circle cx="278" cy="200" r="19" fill="{SKIN}"/>
  <ellipse cx="180" cy="180" rx="100" ry="104" fill="{SKIN}"/>
  <path d="M78 198 C64 98 134 62 180 62 C228 62 296 98 282 198 C276 168 262 148 244 140 C232 150 214 146 206 134 C192 146 168 146 156 132 C144 146 124 150 112 140 C96 152 82 172 78 198 Z" fill="{HAIR}"/>
  <path d="M176 68 C168 44 182 26 204 28 C226 30 230 54 210 60" fill="none" stroke="{HAIR}" stroke-width="13"/>
 </g>
 <g fill="{CHEEK}" opacity=".55"><ellipse cx="116" cy="240" rx="15" ry="9"/><ellipse cx="244" cy="240" rx="15" ry="9"/></g>
 <path d="M181 214 q6 10 -3 15" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
 <g class="mat">{face["eyes"]}</g>
 <g fill="#FFFFFF" fill-opacity=".28" stroke="{INK}" stroke-width="{W}">
  <circle cx="142" cy="196" r="33"/><circle cx="218" cy="196" r="33"/>
 </g>
 <path d="M175 193 Q180 186 185 193" fill="none" stroke="{INK}" stroke-width="{W}" stroke-linecap="round"/>
 <g class="long-may" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round">{face["brows"]}</g>
 <g class="mieng" stroke="{INK}" stroke-width="{W}" stroke-linecap="round" stroke-linejoin="round">{face["mouth"]}</g>
 <g class="mieng-noi" opacity="0" stroke="{INK}" stroke-width="{W}" stroke-linejoin="round">
  <path d="M164 246 Q180 244 196 246 Q194 270 180 270 Q166 270 164 246 Z" fill="#7A2E2E"/>
 </g>
 <g class="them">{face.get("extra", "")}</g>
</g>"""


def dot_eyes(dx=0, dy=0, r=8.5):
    out = ""
    for ex, ey in (LEFT_EYE, RIGHT_EYE):
        out += f'<circle cx="{ex + dx}" cy="{ey + dy}" r="{r}" fill="{INK}"/>'
        out += f'<circle cx="{ex + dx + 3}" cy="{ey + dy - 3}" r="2.6" fill="#FFFFFF"/>'
    return out


FACES = {
    "binh-thuong": {
        "eyes": dot_eyes(),
        "brows": "<path d='M122 148 Q140 140 158 148'/><path d='M202 148 Q220 140 238 148'/>",
        "mouth": "<path d='M162 248 Q180 264 198 248' fill='none'/>",
    },
    "suy-nghi": {
        "eyes": dot_eyes(dx=7, dy=-8),
        "brows": "<path d='M122 152 Q140 148 158 152'/><path d='M202 138 Q220 128 238 140'/>",
        "mouth": "<path d='M170 254 Q182 250 194 256' fill='none'/>",
    },
    "ngac-nhien": {
        "eyes": dot_eyes(r=6.5),
        "brows": "<path d='M122 136 Q140 124 158 136'/><path d='M202 136 Q220 124 238 136'/>",
        "mouth": f"<ellipse cx='180' cy='258' rx='11' ry='15' fill='#7A2E2E'/>",
        "extra": f"<g stroke='{INK}' stroke-width='5' stroke-linecap='round'>"
                 "<path d='M86 96 l-16 -14'/><path d='M100 78 l-8 -20'/><path d='M274 96 l16 -14'/><path d='M260 78 l8 -20'/></g>",
    },
    "vui": {
        "eyes": "".join(f"<path d='M{ex - 11} {ey + 3} Q{ex} {ey - 11} {ex + 11} {ey + 3}' fill='none' stroke='{INK}' stroke-width='6' stroke-linecap='round'/>"
                        for ex, ey in (LEFT_EYE, RIGHT_EYE)),
        "brows": "<path d='M122 144 Q140 134 158 144'/><path d='M202 144 Q220 134 238 144'/>",
        "mouth": "<path d='M156 242 Q180 244 204 242 Q200 276 180 276 Q160 276 156 242 Z' fill='#7A2E2E'/>"
                 "<path d='M166 264 Q180 256 194 264 Q188 274 180 274 Q172 274 166 264 Z' fill='#E86A6A' stroke='none'/>",
    },
    "lo-lang": {
        "eyes": dot_eyes(dy=3),
        "brows": "<path d='M122 150 Q142 146 158 136'/><path d='M202 136 Q218 146 238 150'/>",
        "mouth": "<path d='M162 258 Q168 250 174 258 Q180 266 186 258 Q192 250 198 258' fill='none'/>",
        "extra": f"<path d='M268 132 Q258 150 262 158 A9 9 0 0 0 278 156 Q280 148 268 132 Z' fill='#9FD8F5' stroke='{INK}' stroke-width='4'/>",
    },
    "tu-tin": {
        "eyes": dot_eyes(dx=8, dy=1),
        "brows": "<path d='M122 146 Q140 140 158 146'/><path d='M202 144 Q220 136 238 142'/>",
        "mouth": "<path d='M160 246 Q184 270 204 244' fill='none'/>",
    },
}

ARMS = {
    "dung": [arm("tay-trai", [LEFT_SHOULDER, (108, 356), (96, 394)]),
             arm("tay-phai", [RIGHT_SHOULDER, (252, 356), (264, 394)])],
    "suy-nghi": [arm("tay-trai", [LEFT_SHOULDER, (114, 368), (132, 394), (196, 390)]),
                 arm("tay-phai", [RIGHT_SHOULDER, (244, 376), (208, 294)])],
    "ngac-nhien": [arm("tay-trai", [LEFT_SHOULDER, (90, 300), (78, 252)]),
                   arm("tay-phai", [RIGHT_SHOULDER, (270, 300), (282, 252)])],
    "vui": [arm("tay-trai", [LEFT_SHOULDER, (108, 356), (96, 394)]),
            arm("tay-phai", [RIGHT_SHOULDER, (272, 270), (282, 216)])],
    "lo-lang": [arm("tay-trai", [LEFT_SHOULDER, (122, 374), (168, 350)]),
                arm("tay-phai", [RIGHT_SHOULDER, (238, 374), (192, 350)])],
    "chi-tay": [arm("tay-trai", [LEFT_SHOULDER, (94, 358), (120, 396)]),
                arm("tay-phai", [RIGHT_SHOULDER, (282, 300), (330, 280)], finger=(356, 270))],
}

# tư thế: (tay, nét mặt, tay nào vẽ đè lên thân)
POSES = {
    "dung": ("dung", "binh-thuong", set()),
    "suy-nghi": ("suy-nghi", "suy-nghi", {"tay-trai", "tay-phai"}),
    "ngac-nhien": ("ngac-nhien", "ngac-nhien", set()),
    "vui": ("vui", "vui", set()),
    "lo-lang": ("lo-lang", "lo-lang", {"tay-trai", "tay-phai"}),
    "chi-tay": ("chi-tay", "tu-tin", set()),
}
LABELS = {
    "dung": "Đứng — mặc định, kể chuyện",
    "suy-nghi": "Suy nghĩ — neo bên trái bảng giải thích",
    "ngac-nhien": "Ngạc nhiên — khoảnh khắc “à há”",
    "vui": "Vui — đáp án, kết",
    "lo-lang": "Lo lắng — đặt cược, vấn đề",
    "chi-tay": "Chỉ tay — giới thiệu sơ đồ bên phải",
}


def build(pose):
    arm_key, face_key, front = POSES[pose]
    arms = ARMS[arm_key]
    behind = [a for a in arms if a.split('"')[1] not in front]
    in_front = [a for a in arms if a.split('"')[1] in front]
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 540" width="440" height="540">\n'
        f'<title>Tò — {LABELS[pose]}</title>\n'
        f'<g id="to-{pose}" class="to" transform="translate(40 0)">\n'
        + "\n".join(behind) + "\n" + body() + "\n" + head(FACES[face_key]) + "\n" + "\n".join(in_front)
        + "\n</g>\n</svg>\n"
    )


def main():
    cards = []
    for pose in POSES:
        (OUT / f"{pose}.svg").write_text(build(pose), encoding="utf-8")
        cards.append(f'<figure><img src="{pose}.svg" alt="{pose}"><figcaption><b>{pose}.svg</b><br>{LABELS[pose]}</figcaption></figure>')
    (OUT / "xem-truoc.html").write_text(f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><title>Tò — bộ tư thế</title>
<style>
@font-face {{ font-family: "Be Vietnam Pro"; font-weight: 500; src: url("../../fonts/BeVietnamPro/BeVietnamPro-Medium.ttf"); }}
@font-face {{ font-family: "Be Vietnam Pro"; font-weight: 800; src: url("../../fonts/BeVietnamPro/BeVietnamPro-ExtraBold.ttf"); }}
body {{ margin: 0; background: #0B1D2E; font-family: "Be Vietnam Pro", sans-serif; color: #9FB3C8; }}
.grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; padding: 24px; }}
figure {{ margin: 0; background: #13304A; border-radius: 16px; padding: 12px; text-align: center; }}
img {{ width: 100%; }}
figcaption {{ font-size: 14px; line-height: 1.4; }}
b {{ color: #F5F7FA; font-weight: 800; }}
</style></head><body><div class="grid">{"".join(cards)}</div></body></html>
""", encoding="utf-8")
    print(f"{len(POSES)} tư thế → {OUT}")


if __name__ == "__main__":
    main()
