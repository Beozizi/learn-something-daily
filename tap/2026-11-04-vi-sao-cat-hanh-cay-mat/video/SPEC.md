# SPEC — Vì sao cắt hành lại cay mắt?

GOAL:    Người xem hiểu khí cay chỉ sinh ra khi tế bào vỡ, và nhớ một câu: dao sắc, cắt chậm.
OUTPUT:  HyperFrames, 1920 × 1080, 24 fps. Sinh bằng `build.py` từ `../audio/timeline.json` + `../audio/words.json` — sửa build.py rồi chạy lại, không sửa tay HTML.
TIME:    218,2 s × 24 = 5237 khung. Lời đọc là đồng hồ: mọi hình hiện đúng chữ nêu nó (mốc lấy từ words.json).

LOOK:
- Hai thế giới, không hòa vào nhau:
  - **Bếp** (cảnh 02, 04, 10, 12): tường `#1E4A63`, gạch ốp `#245A78` kẻ `#2C6788` 4 px, cửa sổ trời chiều `#FF9F5A`, mặt bếp gỗ `#B7834F`, thân tủ `#7A5233`. Phẳng, không gradient.
  - **Bảng đá phiến** (cảnh 03, 06, 07–09, 11): nền `#13304A`, khung gỗ `#7A5233` dày 28 px ở mép khung hình, nét sơ đồ màu theo vai trò bên dưới.
  - **Thẻ giấy** (cảnh 01, 05, 13): nền `#F5F1E8`, chữ `#0B1D2E`.
- Màu = thông tin: phân tử lưu huỳnh `#19C3B1`, enzyme cắt `#9FB3C8`, enzyme thứ hai `#FFC145`, **khí cay `#CDEB6E`** (chỉ khí cay dùng màu này), nước mắt `#9FD8F5`, vỡ / loại / sai `#FF6B5A`. Viền nét mọi vật `#081420` 6 px.
- Chữ: Be Vietnam Pro. Câu lớn ExtraBold 84 px, tracking −1 %; nhãn sơ đồ ExtraBold 52 px viết hoa; chú thích Medium 30 px `#9FB3C8`; số liệu Black 160–220 px.
- Môi trường hoạt hình 2D phẳng nét đậm (như nhân vật Tò). Không bóng đổ, không glow, không grain.

OBJECTS (vẽ đủ chi tiết để nhận ra không cần nhãn):
- Củ hành tây: hình giọt ngược, vỏ vàng nâu `#E8B36A` sọc `#C98A3E`, ngọn khô trên đỉnh, rễ tua dưới đáy.
- Dao: cán gỗ `#6B4529` 3 đinh tán; lưỡi sắc `#DDE6EE` có đường mài sáng và tia lấp lánh; lưỡi cùn `#A7B2BC` xỉn, 3 vết mẻ ở lưỡi.
- Đồng hồ treo tường mặt kem, kim giờ/phút; nồi cơm điện có đèn; chuông cửa; tủ lạnh; huy chương có dải; công tắc gạt.
- Tế bào hành: hình chữ nhật bo góc 40 px, màng `#081420`, bên trong hai ngăn ngăn bởi màng nét đứt.
- Mắt nhìn nghiêng: nhãn cầu trắng, mống mắt `#19C3B1`, giác mạc lồi; dây thần kinh là đường vẽ dần tới não hồng `#F7A8B8`; tuyến lệ hạnh nhân hồng phía trên.
- Mũi dao phóng đại: mũi sắc là nêm hẹp nhọn; mũi cùn là nêm rộng đầu tròn bán kính 40 px.

MOTION:
- Vào: `expo.out` 0,5–0,7 s; di chuyển máy quay: `power2.inOut` 0,8–1,2 s; ra: `power3.in` bằng 50 % thời gian vào.
- Đồ vật "nảy" khi đặt xuống: `back.out(1.6)` trên scale/vị trí, không bao giờ trên opacity.
- Nét sơ đồ vẽ dần (stroke-dashoffset) 0,5–0,8 s; nhãn hiện sau nét 0,15 s, mờ 8 px → 0 trong 0,15 s.
- Tò: thở + chớp mắt không đều 2–4 s; đổi tư thế qua nhún lấy đà; mắt liếc về thứ đang được nói.
- Cắt cảnh truyện ở đầu mỗi câu (`sentences[].start`), khung mới vào lớn 104 % rồi lắng về 100 % trong 0,4 s `expo.out`.

SHOTS (thời gian tuyệt đối, theo timeline.json):
- 0,0–4,4 · 01 Tiêu đề: thẻ giấy, tiêu đề hiện từng chữ, củ hành bốc một làn khí cay.
- 4,4–26,4 · 02 Mở truyện: 8 khung theo 8 câu — bếp toàn cảnh (đồng hồ 6:00) → cận dao chạm hành → cận mặt Tò cay → nước mắt chảy → rổ hành "20" → ngăn kéo hai dao → Tò phân vân "NHANH? / CHẬM?" → mắt đỏ, đồng hồ nhảy 7:00.
- 26,4–55,9 · 03 Dữ kiện: bảng dài 3 khu, máy quay lia ngang; khu 1 tế bào hai ngăn → vỡ → khí; khu 2 khí bay tới mắt, dây thần kinh lóe; khu 3 lưỡi dao ấn lõm vỏ rồi đứt, giọt bắn.
- 55,9–63,2 · 04 Câu hỏi: bảng, Tò bên trái, ba hàng A/B/C xếp dọc hiện đúng chữ "A", "B", "C".
- 63,2–73,6 · 05 Thử đoán: thẻ giấy tóm tắt 3 dữ kiện + A/B/C, đếm ngược 3‑2‑1 cỡ 220 px.
- 73,6–83,0 · 06 Chìa khóa: bong bóng suy nghĩ; "CÓ SẴN" bị gạch, "TẾ BÀO VỠ → KHÍ CAY" in đè; câu hỏi lớn "Cách nào làm vỡ ÍT tế bào nhất?".
- 83,0–155,3 · 07–09 Bảng giải thích (một khung liên tục): tế bào → chuỗi phản ứng → mắt → não → tuyến lệ; tế bào thu vào góc, hai mũi dao ấn hàng tế bào, "×40", "40 m/s", "NHANH ×4"; ba hàng A/B/C, gạch A, gạch C, khoanh B.
- 155,3–161,3 · 10 Đáp án: chữ "B" lớn đóng xuống → bếp, Tò vui cắt chậm, rổ vơi.
- 161,3–196,5 · 11 Bất ngờ: bảng; tủ lạnh có hành + dấu "?" đỏ + "CHƯA ĐƯỢC CHỨNG MINH"; "2002", enzyme vàng, huy chương Ig Nobel 2013, công tắc tắt gen → làn khí teo lại.
- 196,5–203,2 · 12 Kết: bếp, đồng hồ 7:00, chuông cửa, Tò bưng đĩa tự hào → liếc nồi cơm tắt đèn → ngạc nhiên.
- 203,2–218,2 · 13 Thẻ cuối: một câu chốt + nguồn + nhắc an toàn, giữ yên.

SOUND: lời đọc `assets/loi-doc.wav` (1.0). Nhạc nền và hiệu ứng âm chờ đăng nhập HeyGen — chưa có thì giao bản không nhạc và ghi rõ.

BANNED: nền tối trống với vật nhỏ trôi giữa khung; glow, bloom, hạt bay trang trí; gradient tím/xanh, thẻ kính; mọi thứ căn giữa và cùng mờ dần trượt lên; chữ chuyển động khi đang đọc; ba thẻ nằm ngang một hàng; nhãn góc, khung viền trang trí; tiêu đề đang đứng còn trôi/phóng chậm; nhân vật mấp máy miệng (Tò không phải người kể).

QA: 2,0 (tiêu đề đọc được) · 9,0 (cận dao + hành) · 14,0 (nước mắt) · 21,0 (hai dao phân biệt được sắc/cùn) · 35, 44, 52 (ba khu dữ kiện) · 68 (thẻ thử đoán đọc được) · 95 (chuỗi phản ứng) · 128 (×40) · 150 (B được khoanh) · 165 (tủ lạnh + "?") · 185 (huy chương) · 201 (nồi cơm) · 210 (thẻ cuối).
