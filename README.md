# Quy trình sản xuất video Khoa học đời sống

Video hoạt hình giải thích khoa học trong đời sống hằng ngày, theo lối **kể chuyện → đố người xem → giải thích trên một bảng sơ đồ** (phân tích mẫu: `tham-khao\ted-ed-billy-bonka\phan-tich.md`).

- **Bản chính:** ngang 16:9 · 1920×1080 · 24 fps · 4–6 phút · YouTube
- **Bản cắt ngắn:** dọc 9:16 · 1080×1920 · 45–60 giây · Shorts / TikTok / Reels
- Lồng tiếng tiếng Việt bằng AI (VieNeu-TTS), dựng bằng HyperFrames.

```
Ý tưởng → Brief & nghiên cứu → Kịch bản → KIỂM CHỨNG (cổng) → Lồng tiếng → Căn thời gian
       → Nhân vật & hình → Dựng HyperFrames → Render & QC → Xuất bản → Cắt bản dọc
```

## Cấu trúc thư mục

```
E:\science and technology\
├─ README.md            quy trình (file này)
├─ CLAUDE.md            hướng dẫn cho Claude khi làm việc trong dự án
├─ y-tuong.md           kho ý tưởng, chấm điểm, chọn chủ đề
├─ tham-khao\           video mẫu đã phân tích
├─ templates\           mẫu brief, kịch bản, kiểm chứng, xuất bản
├─ scripts\             tap-moi.py · long-tieng.py · can-phu-de.py
├─ assets\              brand.md · phat-am.txt · fonts\ · nhan-vat\
└─ tap\                 mỗi tập một thư mục
   └─ 2026-11-04-vi-sao-cat-hanh-cay-mat\
      ├─ 01-brief.md  02-kich-ban.md  03-kiem-chung.md  04-xuat-ban.md
      ├─ nguon\        PDF / ảnh chụp nguồn đã dùng
      ├─ audio\        canh-01.wav… · loi-doc.wav · timeline.json · words.json · phu-de.srt
      ├─ hinh\         hình, icon, sơ đồ + giay-phep.md
      ├─ video\        dự án HyperFrames bản 16:9
      ├─ video-doc\    dự án HyperFrames bản 9:16
      └─ xuat\         MP4 cuối cùng
```

## Cấu trúc một tập (theo video mẫu)

| Phần | Tỷ lệ | Mục đích | Hình |
|------|------:|----------|------|
| Đề từ | ~2 % | Đặt không khí | Thẻ chữ, không lời |
| Mở truyện | ~15 % | "Bạn" + tình huống đời thường + cược | Nhân vật, cắt cảnh 2–4 s mỗi câu |
| Dữ kiện | ~12 % | Đủ thông tin để người xem tự suy luận | Biểu tượng + nhãn ngắn |
| Câu hỏi + Thử đoán | ~5 % | Mời tạm dừng, đếm ngược 3‑2‑1 | Thẻ tóm tắt dữ kiện |
| Chìa khóa | ~7 % | Nêu nguyên tắc cốt lõi trước | Sơ đồ đơn giản |
| Giải thích | ~50 % | Đi từng bước, lặp một thao tác | **Một bảng liên tục**, không cắt cảnh |
| Đáp án + Kết | ~4 % | Đáp án bằng hình, một cú kết vui | Nhân vật |
| Thẻ cuối | ~5 % | Nguồn, ê-kíp, tập khác | Thẻ tĩnh |

Nhịp đọc ~170 tiếng/phút → video 5 phút ≈ 850 tiếng kịch bản.

## Các bước

| # | Bước | Làm gì | Đầu ra | Xong khi |
|---|------|--------|--------|----------|
| 0 | Chọn chủ đề | Chấm điểm trong `y-tuong.md` | 1 chủ đề | ≥ 14/18 điểm |
| 1 | Tạo tập | `py scripts\tap-moi.py <slug> "<Tiêu đề>"` | Thư mục tập | — |
| 2 | Brief & nghiên cứu | Câu hỏi trung tâm, dữ kiện, câu đố, nguồn | `01-brief.md` | ≥ 2 nguồn uy tín cho mỗi ý chính |
| 3 | Kịch bản | Theo khung 12 cảnh trong mẫu | `02-kich-ban.md` | Đọc to 4–6 phút; dữ kiện đủ để tự giải |
| 4 | **Kiểm chứng** | Mỗi khẳng định có nguồn, đúng mức chắc chắn | `03-kiem-chung.md` | Không còn ❌ / ❓ — **chưa qua thì không lồng tiếng** |
| 5 | Lồng tiếng | `long-tieng.py` đọc từng cảnh | `audio\loi-doc.wav`, `timeline.json` | Nghe lại không lỗi phát âm |
| 6 | Căn thời gian | `can-phu-de.py` căn từng chữ, từng câu | `words.json`, `phu-de.srt` | — |
| 7 | Nhân vật & hình | Tư thế nhân vật, sơ đồ, biểu tượng | `hinh\` + `giay-phep.md` | Mọi file có nguồn & giấy phép |
| 8 | Dựng | HyperFrames: cảnh theo `timeline.json`, thao tác bảng theo `words.json` | `video\` | `hyperframes check` sạch |
| 9 | Render & QC | `hyperframes render`, xem hết một lượt | `xuat\<slug>.mp4` | Qua checklist `04-xuat-ban.md` |
| 10 | Thumbnail | ChatGPT tạo 3 phương án ảnh bìa (nhân vật + đồ vật nút thắt + chữ ≤ 5 từ) | `xuat\thumbnail-N.jpg` 1280×720 | Chữ đúng chính tả, đọc được ở 320×180 |
| 10b | Xuất bản | Tiêu đề, mô tả có nguồn, CC từ `phu-de.srt`, thumbnail đã chọn | Bài đăng YouTube | — |
| 11 | Bản dọc | Cắt 45–60 s, in cứng phụ đề | `video-doc\`, `xuat\<slug>-doc.mp4` | — |

## Lệnh

Đường dẫn công cụ của từng máy ở `cau-hinh.json`; máy mới cài bằng `scripts\cai-dat.ps1` (xem `BAN-GIAO.md`). Script Python chạy qua `scripts\chay.py <vai>`.

```powershell
# 1. Tạo tập mới (bản tiếng Anh: thêm --en)
py scripts\tap-moi.py vi-sao-cat-hanh-cay-mat "Vì sao cắt hành lại cay mắt?"

# 5. Lồng tiếng (cả tập; làm lại một cảnh: --only 03). Bản tiếng Anh: xem skill video-khoa-hoc bước 6
py scripts\chay.py tts scripts\long-tieng.py tap\2026-11-04-vi-sao-cat-hanh-cay-mat --voice "Thiện Minh"

# 6. Căn thời gian từng chữ, từng câu + xuất phụ đề SRT
py scripts\chay.py align scripts\can-phu-de.py tap\2026-11-04-vi-sao-cat-hanh-cay-mat

# 8–9. Dựng và render — nên giao cho Claude: "Dựng video cho tập tap\…"
hyperframes preview
hyperframes check
hyperframes render
```

## Giọng đọc gợi ý (VieNeu-TTS)

| Giọng | Mô tả | Dùng cho |
|-------|-------|----------|
| **Thiện Minh** (mặc định) | Nam · Bắc · kể chuyện | Kể chuyện, giải thích |
| Ngọc Linh | Nữ · Bắc · kể chuyện | Chủ đề sức khỏe, gia đình |
| Thanh Bình | Nam · Bắc · kể chuyện | Chủ đề nghiêm túc |
| Trúc Ly | Nữ · Bắc · tự nhiên | Tập vui, nhịp nhanh |
| Thục Đoan / Thái Sơn | Nữ / Nam · Nam · kể chuyện | Khán giả phía Nam |

Từ khó đọc (DNA, CO2, B12…) thêm vào `assets\phat-am.txt`; phụ đề vẫn hiện chữ gốc.

## Nguyên tắc nội dung

1. **Đúng trước, hay sau.** Mỗi khẳng định phải truy được về nguồn trong `03-kiem-chung.md`.
2. **Thứ tự ưu tiên nguồn:** tổng quan hệ thống / meta-analysis → nghiên cứu gốc trên tạp chí bình duyệt → WHO, CDC, NIH, Bộ Y tế → sách giáo khoa đại học → báo khoa học uy tín. Không dùng blog, báo lá cải, video khác làm nguồn chính.
3. **Nói đúng mức chắc chắn:** "có liên quan" ≠ "gây ra"; nghiên cứu trên chuột/tế bào phải nói rõ. Câu đố không được đánh đố bằng dữ kiện sai hoặc mập mờ.
4. **Sức khỏe:** không chỉ định thuốc, liều lượng, không thay lời khuyên bác sĩ; có khuyến cáo ở thẻ cuối và mô tả.
5. **Hình ảnh:** sơ đồ phải đúng khoa học; ảnh AI chỉ dùng cho minh họa không mang thông tin và ghi "Ảnh minh họa".
6. **Nguyên bản:** học cấu trúc từ video mẫu, không sao chép nhân vật, hình vẽ, nhạc, tên gọi của kênh khác.
