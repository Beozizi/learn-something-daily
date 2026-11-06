# REVIEW — Vì sao cần uống nước? (bản dựng 1)

## Lựa chọn sáng tạo

- 8 phút 18 giây, 21 cảnh: văn phòng (truyện, đặt vấn đề, đáp án), bảng đá phiến (giải thích, đố), thẻ giấy (tiêu đề, thử đoán, thẻ cuối), phòng họp (cú kết).
- Màu = thông tin: nước luôn xanh `#4FB3E8`; thang màu nước tiểu 5 mức; cảnh báo/loại bỏ đỏ san hô.
- Hình người "đổ đầy nước" tới 60%; cân nước vào/ra; bộ cảm biến có kim đo và đèn báo — mỗi đồ vật hiện đúng chữ nêu nó (mốc lấy từ words.json).
- Dựng bằng thư viện chung `scripts/hf` (tách từ tập 1) — `build.py` chỉ chứa phần riêng của tập.
- Nhạc: thư viện chỉ có bản 30–65 s, nên xoay vòng 5 bản theo từng phần thay vì lặp một bản.

## Đã đo / đã xem

- `hyperframes check`: 0 lỗi. Cảnh báo giữ lại: `text_below_floor` (chữ đang trong hiệu ứng phóng to, < 1 s), `composition_file_too_large` (mã nguồn thật là build.py).
- Đã xem ảnh chụp ở hơn 70 mốc trong 21 cảnh; đã sửa: khung vượt mép bối cảnh, nhãn chồng nhau, nhãn tràn mép, vài khoảng bảng trống 3–4 s, các mốc chữ khớp nhầm ("Mỹ" ở câu 1945).
- Bản render `xuat/vi-sao-can-uong-nuoc.mp4`: 1920×1080, 24 fps, H.264 + AAC, 8:17.7, 72,8 MB.
- Âm thanh (`hyperframes audio`): -14,2 LUFS, đỉnh thật -2,7 dB, không vỡ tiếng; khoảng lặng dài nhất < 0,5 s.
- **Chưa ai xem chuyển động ở tốc độ thật; âm thanh chỉ đo, chưa nghe.**

## Cảnh yếu nhất

- Cảnh 05 (con sông): hạt trôi đều, ít điểm nhấn; có thể thêm cận một tế bào nhận "kiện hàng".
- Cảnh 16: chấm "Na" nhỏ, chủ yếu trang trí.
- Văn phòng dùng chung một bối cảnh; có thể thêm góc máy khác (cận tay cầm ly).
