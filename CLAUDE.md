# Dự án video Khoa học đời sống — hướng dẫn cho Claude

Đọc `README.md` để nắm quy trình. Phong cách kể và dựng theo `tham-khao\ted-ed-billy-bonka\phan-tich.md` và `assets\brand.md`. Mọi trao đổi và nội dung bằng tiếng Việt.

## Đường dẫn

- Dự án: thư mục chứa file này — mỗi tập ở `tap\<yyyy-mm-dd>-<slug>\`. Kênh: **Learn Something Daily**; quy ước kênh ở đầu skill `video-khoa-hoc`.
- **Đường dẫn công cụ theo máy** nằm trong `cau-hinh.json` (không đưa lên repo; mẫu `cau-hinh.mau.json`). Chạy script Python qua `py scripts\chay.py <vai> <script> …` — vai: `tts` (long-tieng.py), `align` (can-phu-de.py, WhisperX), `media` (tach-nen.py, rembg), `chung` (do-khoang-trong.py, xử lý ảnh). Không gõ đường dẫn venv/ffmpeg cố định vào script; script lấy `FFMPEG` từ `scripts\cau_hinh.py`.
- Máy mới: `powershell -ExecutionPolicy Bypass -File scripts\cai-dat.ps1`, rồi `py scripts\kiem-tra-may.py` (phải 0 lỗi). Hướng dẫn người mới: `BAN-GIAO.md`.
- Máy gốc (chủ kênh): công cụ ở `F:\News Football\tools` (dùng chung dự án bóng đá, đừng cài lại); ổ C gần đầy — model/gói nặng đặt trên F: hoặc E:.

## Quy tắc bắt buộc

1. **Cổng kiểm chứng:** không chạy lồng tiếng khi `03-kiem-chung.md` còn dòng ❌ hoặc ❓. Nếu người dùng yêu cầu bỏ qua, nhắc một lần rồi làm theo.
2. Khi nghiên cứu, ghi nguồn thật (DOI/URL) vào brief và bảng kiểm chứng. Không bịa nguồn, số liệu, tên nhà khoa học. Không tìm được nguồn → ghi ❓ và nói rõ.
3. Kịch bản dùng đúng định dạng của `templates\kich-ban.md` (`## Cảnh NN · Tên`, dòng `Hình:`, `Thời lượng:`, lời đọc bắt đầu bằng `> `) — script lồng tiếng đọc theo định dạng này.
4. Lời đọc viết cho tai nghe: ngôi "bạn", thì hiện tại, câu ≤ 20 tiếng, tránh viết tắt (hoặc thêm vào `assets\phat-am.txt`). Phần dữ kiện phải đủ để người xem tự giải câu đố.
5. Chủ đề sức khỏe: khuyến cáo ở thẻ cuối và trong mô tả.
6. Mọi hình ảnh lấy về ghi vào `hinh\giay-phep.md` (file, nguồn, tác giả, giấy phép). Không sao chép nhân vật/hình của kênh khác.

## Dựng video (bước 8)

- Thư viện dựng dùng chung: `scripts\hf\` — `core.py` (Comp, TL, idle, swap, frame, burst, sfx, nhạc, index), `ve.py` + `ve2.py` (đồ vật SVG), `sfx\` (hiệu ứng âm). `build.py` của mỗi tập: `core.init(__file__)`, viết các hàm cảnh, `core.run(BUILDERS, music)`. Xem mẫu ở `tap\2026-11-04-vi-sao-can-uong-nuoc\video\build.py`. Đồ vật mới thêm vào `ve2.py` (hoặc `ve3.py`) để tập sau dùng lại.
- Lấy mốc câu theo chữ đầu câu (`S(c, cảnh, "tiền tố")`), không theo chỉ số; khi dùng `c.at(...)` với từ lặp lại (VD "Loại", "Mỹ", "hai", "ba") phải chỉ rõ `nth`.

- Hình minh họa (nhân vật cậu bé đeo kính `assets\nhan-vat\cau-be-kinh\`, bối cảnh `assets\boi-canh\`): tạo bằng `scripts\tao-hinh.py` (OpenAI Images API, key ở `.chatgpt_key.txt` — không in, không chép key ra đâu). Giữ đúng nét: `--ref` ảnh nhân vật/bối cảnh có sẵn; `--boi-canh` cho khung 16:9 chừa 1/3 phải; `--nen-trong` cho nhân vật/đồ vật. Mỗi ảnh có file `.json` đi kèm — chép vào `hinh\giay-phep.md` và ghi "Ảnh minh họa".
- Quy trình trọn gói đã đóng thành skill `video-khoa-hoc` (`.claude\skills\video-khoa-hoc\SKILL.md`). Tập EN mới: `py scripts\tap-moi.py <slug> "<Title>" --en`; dựng bằng `scripts\hf\minh_hoa.py` + `ve3.py`; sau render chạy `py scripts\chay.py chung scripts\do-khoang-trong.py tap\<tập>` để chắc không còn đoạn bảng trống. Video EN luôn có phụ đề tiếng Anh in cứng (`subs=True`, từ `audio\phu-de.srt`) — giữ nội dung bảng trên y ≈ 950. Video xong thì làm luôn thumbnail bằng ChatGPT (skill bước 9: 3 phương án, `xuat\thumbnail-N.jpg` 1280×720, lưu ảnh bằng `scripts\save-clip.ps1`) — tập chưa có thumbnail là chưa xong.
- Bản tiếng Anh: lồng tiếng bằng GenMax (`long-tieng.py --engine genmax --voice <voice_id>`, key ở `.genmax_key.txt`), căn chữ `can-phu-de.py --lang en`. Mẫu dựng dùng ảnh nhân vật PNG thay Tò: `tap\2026-11-05-why-drink-water\video\build.py`.
- Tải skill `hyperframes` (và `hyperframes-registry` trước khi tự dựng hiệu ứng có sẵn, `media-use` khi cần nhạc/hình/hiệu ứng âm) trước khi viết composition.
- Bản 16:9 trong `tap\…\video\` (1920×1080, 24 fps); bản dọc trong `tap\…\video-doc\` (1080×1920). Track lời đọc: `audio\loi-doc.wav`.
- `audio\timeline.json` → `scenes[]`: `id`, `title`, `start`, `end` (giây), `text`, `visual` (các dòng `Hình:`). Mỗi cảnh là một clip đúng khoảng thời gian đó.
- `audio\words.json` → `words[]` (`text`, `start`, `end`, `scene`) và `sentences[]` (`text`, `start`, `end`, `scene`):
  - Cảnh truyện: đổi hình ở đầu mỗi câu (`sentences[].start`).
  - Cảnh bảng: hẹn giờ vẽ / khoanh / gạch / phát sáng theo từ khóa trong `words[]`; các cảnh bảng liên tiếp dùng chung một khung, không cắt.
- Nhân vật chính là Tò: đọc `assets\nhan-vat\to\README.md`, nhúng thẳng SVG tư thế vào HTML để diễn hoạt từng bộ phận. Cần tư thế mới thì thêm vào `tao-tu-the.py` rồi chạy lại, không sửa tay file SVG.
- Phân tích 3D ảnh (chỉ máy gốc có venv-3d đủ gói; chủ kênh đã bỏ parallax — chỉ dùng khi được yêu cầu): `py scripts\chay.py chung scripts\phan-tich-3d.py <ảnh...> --out assets\phan-tich-3d` (Depth Anything V2 + RTMPose).
  - Bối cảnh: tách lớp theo độ sâu (`lop-0` xa → gần, đã vá lỗ), `3d.json` có hệ số parallax từng lớp, điểm nhìn, chân trời → camera trượt/đẩy vào có chiều sâu thay cho phóng ảnh phẳng.
  - Nhân vật PNG nền trong: khớp xương, trục xoay vai/khuỷu/cổ, góc tay, `shade.png` (khối sáng). Mặt nhân vật đầu to dễ lệch — xem `xem-truoc.jpg`.
- Trước khi render: `hyperframes check`, rồi `hyperframes snapshot` để xem vài khung hình. Xuất ra `tap\…\xuat\<slug>.mp4`.
