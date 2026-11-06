# Nhận diện hình ảnh

Tên kênh: **Learn Something Daily** — khẩu hiệu "Everyday science, explained".
Avatar và ảnh bìa: `assets\kenh\` (xem README trong đó).
Phong cách: hoạt hình 2D phẳng, nét viền đậm, nhân vật biểu cảm; giải thích trên một "bảng" sơ đồ hé lộ dần.
Tham khảo cấu trúc: `tham-khao\ted-ed-billy-bonka\phan-tich.md` (chỉ học cách kể, không sao chép hình).

## Màu

Nguyên tắc: **màu = thông tin.** Nền và nhân vật dùng tông trầm; chỉ các yếu tố đang được giải thích mới có màu mạnh.

| Vai trò | Mã | Dùng cho |
|---------|----|----------|
| Nền | `#0B1D2E` | nền chính (xanh đêm) |
| Nền bảng | `#13304A` | nền phần giải thích, thẻ |
| Thẻ chữ | `#F5F1E8` | nền thẻ đề từ / thẻ dữ kiện (chữ `#0B1D2E`) |
| Chính | `#19C3B1` | đường nét sơ đồ, nhấn mạnh khoa học |
| Điểm nhấn | `#FFC145` | yếu tố đang xét, phát sáng, số liệu |
| Loại bỏ / Hiểu lầm | `#FF6B5A` | khoanh tròn, gạch bỏ, "SAI", khuyến cáo |
| Chữ | `#F5F7FA` | chữ chính |
| Chữ phụ | `#9FB3C8` | chú thích, nguồn trên màn hình |
| Viền nét | `#081420` | viền nhân vật, biểu tượng (4–6 px) |

## Chữ

- Font: **Be Vietnam Pro** (`assets\fonts\BeVietnamPro`)
- Nhãn trên sơ đồ: ExtraBold 44–64 px, viết hoa, ≤ 3 từ
- Thẻ đề từ / thẻ dữ kiện: SemiBold 40–48 px, căn trái, đánh số
- Số đếm ngược: Black 220 px
- Nguồn trên màn hình: Medium 26 px, `#9FB3C8`, góc dưới trái

## Bố cục 1920×1080 · 24 fps

- Lề an toàn 96 px mọi phía.
- **Cảnh truyện:** nhân vật chiếm 1/3–1/2 khung, cắt cảnh mỗi 2–4 giây đúng đầu câu (mốc trong `words.json`).
- **Cảnh bảng:** nhân vật neo cố định ở 1/3 trái (x 0–640) tư thế suy nghĩ; sơ đồ ở 2/3 phải (x 700–1824). Không cắt cảnh — chỉ thêm/bớt lớp.
- **Thẻ chữ:** nền `#F5F1E8`, khối chữ căn trái trong vùng x 160–1500.
- Phụ đề: **không in cứng** lên bản 16:9 — tải `audio\phu-de.srt` lên YouTube làm CC.

## Chuyển động trên bảng

| Thao tác | Ý nghĩa | Cách làm |
|----------|---------|----------|
| Vẽ dần nét | đang giới thiệu | stroke-dashoffset 0,4–0,8 s |
| Hiện nhãn | gọi tên | trượt lên 12 px + mờ dần, sau nét 0,2 s |
| Phát sáng | đang xét yếu tố này | quầng `#FFC145` mờ, 0,3 s |
| Khoanh tròn | chú ý nhóm này | nét `#FF6B5A` tự vẽ quanh nhóm |
| Gạch ngang | loại bỏ | nét `#FF6B5A` chạy ngang, phần tử mờ còn 35 % |
| Mũi tên | quan hệ nhân quả | vẽ dần từ gốc tới ngọn |

Mọi thao tác hẹn giờ theo từ khóa trong `audio\words.json`.

## Nhân vật

Nhân vật chính: **Tò** — `assets\nhan-vat\to\` (6 tư thế SVG tách lớp, hướng dẫn diễn hoạt trong `README.md` ở đó).
Màu riêng của Tò: da `#F2C29B`, tóc `#1E2A3A`, áo `#FFC145` / viền áo `#E5A024`, huy hiệu `#19C3B1`, quần `#1E3A56`, má `#FF8A7A`.
Áo Tò trùng màu điểm nhấn: trên bảng, khi Tò đứng cạnh sơ đồ, đánh dấu yếu tố đang xét bằng quầng sáng hoặc khung — không tô kín màu vàng trùng mảng áo.

## Âm thanh

- Nhạc nền nhẹ, không lời, thấp hơn lời đọc ~18–20 dB; đổi nhạc giữa phần truyện và phần bảng.
- Hiệu ứng âm ngắn cho: khoanh tròn, gạch bỏ, đếm ngược, đáp án.

## Bản dọc 9:16 (cắt ngắn từ bản chính)

1080×1920 · 45–60 giây: Mở truyện (rút gọn) → Câu hỏi → Chìa khóa → Đáp án. In cứng phụ đề (Bold 64 px, từ đang đọc màu `#FFC145`, tâm y ≈ 1350 px), chừa trên 180 px, dưới 360 px, phải 120 px. Cuối video: "Xem bản đầy đủ trên YouTube".
