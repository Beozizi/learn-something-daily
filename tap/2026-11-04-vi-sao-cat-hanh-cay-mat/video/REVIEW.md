# REVIEW — Vì sao cắt hành lại cay mắt? (bản dựng 1)

## Lựa chọn sáng tạo

- Hai thế giới tách bạch: **bếp** (truyện, đáp án, kết) và **bảng đá phiến** (dữ kiện, chìa khóa, giải thích, bất ngờ); thẻ giấy cho tiêu đề, thử đoán, thẻ cuối. Không hòa trộn hai thế giới — cắt cứng giữa các cảnh.
- Màu = thông tin: khí cay luôn xanh chanh `#CDEB6E`, lưu huỳnh xanh ngọc, enzyme 2 vàng, vỡ/loại đỏ san hô.
- Cảnh 03 là một bảng dài 3 khu, máy quay lia ngang theo "Một / Hai / Ba".
- Cảnh 07–09 là **một khung liên tục 72 giây** (tế bào → mắt → não → tuyến lệ; hai mũi dao; loại trừ A/B/C), đổi phần bằng mờ-đổi trên cùng nền.
- Tò không mấp máy miệng (Tò là "bạn", không phải người kể).
- Không làm 3 hướng kể chuyện như quy trình HyperFrames gợi ý: cốt truyện đã chốt trong kịch bản đã kiểm chứng.

## Đã đo / đã xem

- `hyperframes check`: 0 lỗi. Cảnh báo giữ lại có chủ ý:
  - `composition_file_too_large` (s07 ~440 dòng): cảnh bảng liền mạch nên để chung một file; mã nguồn thật là `build.py`.
  - `text_below_floor` cho chữ "S" trên phân tử ở khoảnh khắc đang phóng to/thu nhỏ — chữ trang trí, đọc đủ khi đứng yên.
- Đã xem: các trang `snapshot --review` và ảnh chụp ở mọi mốc QA trong SPEC.md (15, 31, 40, 48, 53, 95, 104, 128, 137, 141, 146, 152, 159, 166, 177, 190, 194, 200, 218 s).
- **Chưa ai xem chuyển động ở tốc độ thật** — chỉ xem khung tĩnh. Cần xem bản xem trước một lượt.
- **Âm thanh (bản dựng 2):** lời đọc chuẩn hóa -16 LUFS; 46 hiệu ứng âm đặt điểm nổ 1 khung sau hình; nhạc pizzicato (truyện, kết) + marimba nối 3 lần chồng mờ 1,2 s (phần bảng), mức 0,14 dưới lời, 0,35 khi không lời.
  Đo bản render `xuat/vi-sao-cat-hanh-cay-mat.mp4`: -14,5 LUFS, true peak -2,6 dB. **Chỉ đo, chưa ai nghe** — cần nghe các mối nối marimba (≈69 s, ≈112 s) và độ to tiếng dao chặt.

## Cảnh yếu nhất và việc nên làm thêm

- Cảnh 11 đoạn 174–178 s: sau khi tủ lạnh mờ đi, bảng chỉ còn Tò ngạc nhiên ~3 s trước khi "2002" hiện → nên thêm một nhịp hình (VD: dấu "!" lớn hoặc lật trang bảng).
- Cảnh 10: con dao lắc lư trên củ hành nhưng bàn tay Tò khuất sau mặt bếp — đọc được là "đang thái" nhưng chưa có cảm giác tay cầm dao.
- Các cảnh bếp dùng chung một bối cảnh nên đổi khung bằng phóng to/cắt; có thể thêm cận tay cầm dao, góc nhìn từ trên thớt.

## BANNED đã gặp và đã sửa

- Đồ vật lơ lửng không có tay cầm (dao ở cảnh toàn 02) → ẩn đến khi cận.
- Nhãn sát/tràn mép khung (×40, 40 m/s, TUYẾN LỆ, vòng khoanh B) → đặt lại.
- Đĩa che mặt nhân vật (12) → đặt sau người.
