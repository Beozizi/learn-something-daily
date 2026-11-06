# Bàn giao — làm video cho kênh Learn Something Daily

Tài liệu cho người mới nhận dự án trên **máy của mình**. Làm phần A một lần; sau đó mỗi tập chỉ là phần B.
Claude (trong ứng dụng Claude desktop, tab Code) làm gần hết việc theo skill `video-khoa-hoc`; bạn giao chủ đề, duyệt ở các điểm kiểm tra và đăng bài.

---

## A. Chuẩn bị (một lần, khoảng 1 giờ)

### 1. Cần có

| Thứ | Ghi chú |
|-----|---------|
| Máy Windows 10/11 | còn ≥ 20 GB trống (công cụ ~10 GB, mỗi tập ~400 MB) |
| Card NVIDIA (khuyến nghị) | không có vẫn làm được, căn phụ đề và tách nền chạy CPU chậm hơn |
| Tài khoản **Claude** có Claude Code | cài ứng dụng Claude desktop |
| Tài khoản **ChatGPT** có tạo ảnh (Plus trở lên) | vẽ nhân vật, bối cảnh, thumbnail |
| **GenMax** API key | lồng tiếng tiếng Anh (khoảng 10 000 credit / tập 8 phút) |
| Google **Chrome** + tiện ích **Claude in Chrome** | để Claude điều khiển ChatGPT web |
| Quyền truy cập repo dự án | chủ kênh mời vào repo GitHub riêng tư |

Dùng tài khoản và key **của chính bạn** — không xin, không gửi key qua chat/email.

### 2. Lấy dự án và cài công cụ

Mở PowerShell:

```powershell
winget install --id Git.Git -e
git clone <địa chỉ repo chủ kênh gửi> "D:\learn-something-daily"
cd "D:\learn-something-daily"
powershell -ExecutionPolicy Bypass -File scripts\cai-dat.ps1 -Tools "D:\lsd-tools"
```

- Không có card NVIDIA: thêm `-CPU` vào lệnh cuối.
- Script cài Python, uv, ffmpeg, Node.js, Git; tạo hai môi trường (`venv-chung`, `venv-align`); ghi `cau-hinh.json`; rồi chạy kiểm tra máy. Lần đầu mất 15–30 phút (tải torch ~2,5 GB).

### 3. Đặt key

Mở Notepad, dán GenMax API key (một dòng), lưu thành `.genmax_key.txt` ở gốc dự án (cạnh `CLAUDE.md`).
Nếu chủ kênh cho dùng OpenAI API để vẽ bằng script: làm tương tự với `.chatgpt_key.txt` (không bắt buộc).
Hai file này đã bị `.gitignore` chặn, không bao giờ lên repo.

### 4. Kiểm tra máy

```powershell
py scripts\kiem-tra-may.py
```

Phải ra **0 lỗi** (⚠️ được phép). Dòng ❌ nào cũng có hướng dẫn sửa ngay bên cạnh.

### 5. Claude và trình duyệt

1. Mở Claude desktop → tab **Code** → chọn thư mục dự án. Claude tự đọc `CLAUDE.md` và skill trong `.claude\skills\`.
2. Cài tiện ích **Claude in Chrome**, đăng nhập cùng tài khoản Claude.
3. Trong Chrome, đăng nhập **chatgpt.com**.

### 6. Tập thử (nghiệm thu)

Gõ cho Claude:

> Làm tập thử khoảng 1 phút về "Why do onions make you cry?" theo đúng quy trình (có thumbnail), để kiểm tra máy mới.

Xong khi có `tap\<ngày>-…\xuat\<slug>.mp4` có tiếng, phụ đề, `do-khoang-trong` báo "Không có khoảng trống." và 3 thumbnail. Gửi bản xem thử cho chủ kênh.

---

## B. Làm một tập (mỗi lần)

Gõ cho Claude:

> Làm video mới về: <chủ đề>

Claude tự chạy hết 10 bước của skill `video-khoa-hoc`: nghiên cứu → kịch bản → kiểm chứng → hình → lồng tiếng → căn chữ → dựng → render → thumbnail → tài liệu xuất bản. Khoảng 2–4 giờ máy chạy.

**Bạn phải tự làm ở 5 điểm** (Claude không thay được):

| Khi | Bạn làm |
|-----|---------|
| Sau bước kiểm chứng | đọc `03-kiem-chung.md`: mọi dòng ✅/✏️, nguồn mở được. Thấy nghi ngờ thì hỏi lại Claude |
| Sau lồng tiếng | nghe `audio\loi-doc.wav` — số, năm, tên riêng đọc đúng chưa |
| Sau render | xem **hết** video ở tốc độ thật, có tiếng: chữ không chồng, không che phụ đề, không đoạn trống |
| Thumbnail | chọn 1 trong 3 bản (hoặc cả 3 cho "Test & compare"); đánh dấu cột "Chọn" trong `04-xuat-ban.md` |
| Đăng | dùng tiêu đề, mô tả, hashtag trong `04-xuat-ban.md`; tải `audio\phu-de.srt` làm CC |

Quy ước của kênh (Claude đã biết, bạn để ý khi duyệt): chữ theo kịp giọng, không parallax, số liệu từ bài gốc, chủ đề sức khỏe có khuyến cáo, ảnh AI có ghi công. Chi tiết ở đầu `.claude\skills\video-khoa-hoc\SKILL.md`.

---

## C. Giữ quy trình đồng bộ

- Đầu mỗi ngày: `git pull` để nhận cập nhật quy trình từ chủ kênh.
- Bạn (hoặc Claude) sửa script, skill, mẫu → commit và báo chủ kênh xem. Kịch bản, kiểm chứng, `build.py` của tập cũng nên commit; video, âm thanh thì không (đã chặn sẵn).
- Tập cũ trong repo chỉ có kịch bản và `build.py` để tham khảo; muốn render lại phải lồng tiếng lại.

## D. Gặp lỗi

| Hiện tượng | Cách xử lý |
|------------|-----------|
| "Chưa có môi trường '…'" | chạy lại `scripts\cai-dat.ps1`, hoặc sửa đường dẫn trong `cau-hinh.json` |
| WhisperX báo CUDA / chạy rất chậm | `py scripts\kiem-tra-may.py` xem dòng GPU; không có GPU vẫn chạy, chỉ chậm |
| Claude không điều khiển được ChatGPT | kiểm tra tiện ích Claude in Chrome đã kết nối, chatgpt.com đã đăng nhập |
| GenMax báo lỗi key/credit | kiểm tra `.genmax_key.txt`, số credit trên genmax.io |
| Render lỗi | bảo Claude: "chạy hyperframes check và sửa lỗi cho tập …" |

Không tự xử lý được: chụp màn hình lỗi, gửi chủ kênh kèm tên tập.
