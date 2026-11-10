# Giấy phép hình ảnh và âm thanh — Why are you tired after a day of doing nothing?

## Hình (ảnh minh họa AI — ghi "AI-generated illustrations" trong mô tả)

| File (trong `video\assets\`) | Nguồn | Ghi chú |
|------|-------|---------|
| `char\*.png` (tư thế cậu bé) | ChatGPT tạo ảnh, 2026-11-05/06 | gốc ở `assets\nhan-vat\cau-be-kinh\`; tap-moi.py chép sẵn |
| `bg\phong-khach.jpg` | OpenAI Images API (gpt-image-2), 2026-11-09, `scripts\tao-hinh.py --boi-canh`, mẫu `phong-ngu.png` | Ảnh minh họa; gốc + `.json` ở `assets\boi-canh\phong-khach.*` |
| `bg\lop-hoc-bang.jpg` | ChatGPT tạo ảnh, 2026-11-06 | Ảnh minh họa |
| Hình bảng (pin, não, xe đạp tập, nút chích điện, nhịp tim, đường áp lực ngủ, đèn báo…) | tự vẽ SVG (`scripts\hf\ve.py`, `ve2.py`, `ve3.py`) | |

Mọi ảnh đã đẩy màu bằng `scripts\hf\day_mau.py` (gốc ở `video\assets\_goc\`). Kiểm tra điều khoản sử dụng ảnh của OpenAI trước khi bật kiếm tiền.

## Giọng đọc
GenMax (genmax.io) → ElevenLabs, giọng "Chris" (voice_id iP95p4xoKVk53GoZ742B), model eleven_v3, tốc độ 0,98.

## Hiệu ứng âm, nhạc nền
Hiệu ứng `scripts\hf\sfx\` (whoosh, pop, thump, riser). Nhạc nền `assets\nhac-nen\` (thư viện HeyGen).

## Thumbnail
| File (trong `xuat\`) | Nguồn | Ghi chú |
|------|-------|---------|
| `thumbnail-1..3.png/.jpg` | OpenAI Images API (gpt-image-2), 2026-11-09, `scripts\tao-hinh.py` (Chrome trên máy chưa kết nối nên không dùng ChatGPT web) | Ảnh minh họa AI; mẫu `goc-chatgpt.png` + `phong-khach.png`; gốc + `.json` ở `xuat\_goc\`; đã đẩy màu |
