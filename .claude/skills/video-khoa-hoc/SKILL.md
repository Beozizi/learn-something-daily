---
name: video-khoa-hoc
description: Làm trọn một tập video Khoa học đời sống (TED-Ed style) trong E:\science and technology — từ chủ đề tới MP4 và thumbnail (ChatGPT) — đặc biệt bản tiếng Anh dùng nhân vật cậu bé đeo kính, giọng GenMax và HyperFrames. Dùng khi người dùng bảo "làm video mới về …", "làm tập …", "làm lại bản tiếng Anh", hoặc nhắc tới một bước trong quy trình (kịch bản, kiểm chứng, lồng tiếng, dựng, render, thumbnail/ảnh bìa).
---

# Quy trình một tập video (đóng gói từ tập "Why drink water" và "Why we sleep")

Mọi đường dẫn dưới đây tính từ gốc dự án (thư mục chứa `CLAUDE.md`; chạy lệnh từ đó). Đường dẫn công cụ của từng máy nằm trong `cau-hinh.json` — chạy script Python qua `py scripts\chay.py <vai> <script>`, không gõ đường dẫn venv. Máy mới: `scripts\cai-dat.ps1`, rồi `py scripts\kiem-tra-may.py` phải 0 lỗi (xem `BAN-GIAO.md`). Đọc `CLAUDE.md` và `README.md` trước. Mọi trao đổi bằng tiếng Việt; lời đọc bản EN viết tiếng Anh.

## Quy ước của kênh Learn Something Daily (chủ kênh đã chốt — làm theo, không hỏi lại)
- Kênh tiếng Anh, khẩu hiệu "Everyday science, explained"; nhận diện ở `assets\brand.md`, avatar/ảnh bìa/mô tả ở `assets\kenh\`.
- Nhân vật: cậu bé đeo kính tròn, áo len vàng (`assets\nhan-vat\cau-be-kinh\`). Không chép nhân vật/hình của kênh khác (kể cả TED-Ed).
- Video 8–10 phút, 16:9, 24 fps, giọng GenMax "Chris", **phụ đề tiếng Anh in cứng**.
- **Chữ/hình phải theo kịp giọng đọc**: mỗi câu có hình hoặc chữ mới, không để bảng trống (chủ kênh từng bắt lỗi ở phút 5:26).
- **Không dùng parallax nhiều lớp** — nền phẳng như các tập đã làm.
- Số liệu lấy từ bài gốc, nói rõ khi nghiên cứu trên động vật hoặc còn tranh cãi; chủ đề sức khỏe có khuyến cáo.
- Video xong là **làm luôn 3 thumbnail** (bước 9), không đợi nhắc. Tập chỉ xong khi có MP4 + thumbnail + `04-xuat-ban.md`.
- Trước khi đăng, người làm phải tự nghe/xem hết ở tốc độ thật (Claude chưa nghe được giọng).

## 0. Hỏi một lần (nếu người dùng chưa nói)
Ngôn ngữ (EN: GenMax / VI: VieNeu) và thời lượng (8–10 phút ≈ 1 350–1 450 từ EN, vì giọng ElevenLabs đọc ~165 từ/phút).

## 1. Tạo tập
```
py scripts\tap-moi.py <slug> "<Title>" --en
```
Tạo `tap\<ngày>-<slug>\` + `video\` dựng sẵn (cấu hình HyperFrames, `assets\char` 8 tư thế, `assets\bg` bối cảnh 1920×1080, `assets\bgm`, `build.py` khung).

## 2. Nghiên cứu → `01-brief.md`
- Sách/nguồn phổ thông chỉ để định hướng. **Mọi số liệu phải lấy từ bài gốc** (DOI/PMC). Ví dụ: Walker nói "40%" trí nhớ, bài gốc Yoo 2007 ghi 19% → dùng 19%.
- Nghiên cứu trên động vật nói rõ ("in mice"); kết quả đang tranh cãi nói thẳng ("still debated").
- Tìm bằng WebSearch song song; đọc toàn văn PDF khi cần bằng pypdf (`py scripts\chay.py chung -c "…"`).

## 3. Kịch bản → `02-kich-ban.md`
Định dạng `templates\kich-ban.md`. Khung đã chạy tốt: Title · Truyện mở (bối cảnh minh họa, đổi hình mỗi câu) · Câu đố/manh mối trên bảng · Câu hỏi A/B/C · Thử đoán 10 s · Chìa khóa · 5–8 cảnh giải thích (bảng) · Đáp án · Lời khuyên · Quay lại truyện · Thẻ cuối 16 s. Số viết bằng chữ ("nineteen percent").

## 4. Kiểm chứng → `03-kiem-chung.md` (cổng)
Mỗi khẳng định một dòng, nguồn, mức chắc chắn, ✅/✏️. Còn ❓/❌ thì không lồng tiếng.

## 5. Hình mới (nếu cần) — ChatGPT web qua Claude in Chrome
- Chọn trình duyệt Windows (`list_connected_browsers`), mở chatgpt.com, `file_upload` ảnh mẫu (`assets\boi-canh\van-phong.png` + `assets\nhan-vat\cau-be-kinh\goc-chatgpt.png`) để giữ nét.
- Prompt: "same art style… 16:9… no people/no text" cho bối cảnh; "exact same character… plain pure white background" cho tư thế.
- Lưu: bấm "Copy image" rồi `powershell -NoProfile -STA -File scripts\save-clip.ps1 -Out <đường dẫn>` (đọc ảnh từ clipboard). Không tải bằng hộp thoại Save As.
- Tư thế: `py scripts\chay.py media scripts\tach-nen.py <ảnh> --out tach-nen` → cắt sát viền vào `tach-nen\cat\` → chép vào `video\assets\char\`. Bối cảnh: ffmpeg scale 1920:1080 → `video\assets\bg\*.jpg`.
- Ghi `hinh\giay-phep.md`.

## 6. Lồng tiếng + căn chữ
```
py scripts\chay.py tts scripts\long-tieng.py tap\<tập> --engine genmax --voice iP95p4xoKVk53GoZ742B --provider elevenlabs --model eleven_v3 --lang en --speed 0.98
py scripts\chay.py align scripts\can-phu-de.py tap\<tập> --lang en
```
(`chay.py` chọn đúng venv và đưa ffmpeg vào PATH theo `cau-hinh.json` của máy.)
Chạy nền. Thêm/sửa cảnh: đổi số file `audio\canh-NN.wav` cho khớp rồi `--only NN`. Thiếu thời lượng → thêm cảnh có nguồn, đừng kéo chậm giọng.

## 7. Dựng `video\build.py`
- `from hf.minh_hoa import *` (char, board, S, comp, label, chip, popl, scene_comp, frame, show_pose, music_plan) + `from hf.ve3 import *` (trăng, sóng não, bình, biểu đồ…). Đồ vật mới thêm vào `ve3.py`.
- Hình đi trước giọng 0,2 s (LEAD, đã cài trong minh_hoa). **Mỗi câu phải có hình/chữ mới**: câu hỏi tu từ → nhãn lớn; câu nối → nhãn tiêu đề. Neo theo đầu câu `S(c, cảnh, "tiền tố")`, chỉ dùng `c.at()` cho từ chắc chắn có.
- Mẫu đầy đủ: `tap\2026-11-06-why-we-sleep\video\build.py` (cảnh truyện 2 bối cảnh, bảng, đếm ngược, thẻ cuối).
- **Phụ đề tiếng Anh in cứng (bắt buộc):** `run(BUILDERS, music)` của minh_hoa tự thêm phụ đề từ `audio\phu-de.srt` (dải đáy, nền tối, chữ trắng 42 px, cách đáy 46 px). Tập dùng thẳng core: `core.run(BUILDERS, music, subs=True)`. Vì vậy **giữ mọi chữ/hình của bảng trên y ≈ 950**; ghi chú nguồn đặt ≤ 948 hoặc dưới tiêu đề (y ≈ 230). `check` báo `content_overlap … #subs-N` là chữ cảnh đang nằm dưới phụ đề → dời lên.
- `py build.py` → `npx hyperframes check` (0 lỗi) → `npx hyperframes snapshot --at …` ~40 khung, đọc contact sheet, sửa chữ tràn/chồng.

## 8. Render + QC
```
npx --yes hyperframes@0.9.10 render --fps 24 --output ..\xuat\<slug>.mp4      (chạy nền, ~8 phút)
py scripts\chay.py chung scripts\do-khoang-trong.py tap\<tập>   (phải: "Không có khoảng trống.")
```
Xem vài khung có phụ đề trên cảnh truyện và cảnh bảng. Đo âm lượng (ebur128, mục tiêu ≈ -14 LUFS, đỉnh < -1 dB). Bản xem thử 480p (`scale=854:480`, 260k/64k mono) để gửi qua SendUserFile (giới hạn 30 MB). Viết `04-xuat-ban.md` (ghi chú video đã có phụ đề in cứng; vẫn tải `phu-de.srt` lên YouTube làm CC; tiêu đề, chữ ảnh bìa, mô tả có nguồn, khuyến cáo, ghi công AI), cập nhật `y-tuong.md`.

## 9. Thumbnail bằng ChatGPT (bắt buộc, làm ngay sau khi video xong)
Một tập chỉ coi là xong khi có thumbnail. Không cần người dùng nhắc.
- **Đầu vào:** tiêu đề số 1 và "Chữ trên ảnh bìa" (≤ 5 từ) trong `04-xuat-ban.md`; cảm xúc chính của truyện mở; một đồ vật/ý tưởng nút thắt của tập (VD bể cá vàng, điện thoại rung, đồng hồ cát).
- **ChatGPT web qua Claude in Chrome** (như bước 5): trình duyệt Windows, mở cuộc trò chuyện mới, `file_upload` `assets\nhan-vat\cau-be-kinh\goc-chatgpt.png` + một tư thế/bối cảnh của tập để giữ nét. Prompt mẫu:
  > YouTube thumbnail, 16:9 (1280×720), same art style and the exact same boy with glasses as the reference. Close-up, head and shoulders large on one side, exaggerated <emotion> expression. One key object: <object>, big and clear. Simple bold background, strong color contrast, no clutter. Large bold text "<TEXT>" on the other side, white with thick dark outline, spelled exactly. Keep the bottom-right corner empty (YouTube timestamp). No logos, no other text.
- Làm **3 phương án** khác nhau (đổi cảm xúc/bố cục/màu nền) để người dùng chọn hoặc chạy YouTube "Test & compare".
- **Lưu:** bấm "Copy image" → `powershell -NoProfile -STA -File scripts\save-clip.ps1 -Out tap\<tập>\xuat\thumbnail-N.png`.
- **Kiểm:** zoom đọc từng chữ — ChatGPT hay viết sai chính tả; sai thì bảo sửa đúng chữ hoặc tạo lại. Thu nhỏ 320×180 xem còn đọc được chữ và nhận ra mặt nhân vật. Thumbnail không hứa điều video không có.
- **Xuất:** `py scripts\xuat-thumbnail.py tap\<tập>` → `thumbnail-N.jpg` 1280×720 ≤ 2 MB (giới hạn YouTube) + `thumbnail-nho.jpg` (3 bản 320×180 cạnh nhau, đọc để kiểm chữ).
- ChatGPT đếm đồ vật kém (yêu cầu 8 ly vẫn vẽ 7, sửa lại vẫn sai) — đừng đặt con số vào hình; để số trong chữ. Dặn "no app icons that look like real brands".
- Ghi vào `hinh\giay-phep.md` (ảnh minh họa AI, ngày, cuộc trò chuyện) và mục "Thumbnail" của `04-xuat-ban.md`; gửi 3 bản bằng SendUserFile để người dùng chọn.

## Bẫy đã gặp
- Render mặc định 30 fps → luôn `--fps 24`.
- Trong cảnh có camera (`scene_comp` + `frame`), **không** tween `rotation` kèm `svgOrigin` trên phần tử con của nhóm camera — GSAP làm lệch cả khung (ảnh nền trôi ra ngoài). Rung/lắc đồ vật bằng `x`/`y`.
- `scripts\tap-moi.py` và file Python có đường dẫn Windows: dùng chuỗi `r"..."`, đừng sửa bằng heredoc có `\b \f`.
- Không đọc/chép API key từ trang web; key do người dùng tạo ở `.chatgpt_key.txt`, `.genmax_key.txt`.
- Parallax nhiều lớp (`scripts\phan-tich-3d.py`) có sẵn nhưng người dùng chọn giữ nền phẳng — chỉ dùng khi được yêu cầu.
