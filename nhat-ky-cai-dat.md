# Nhật ký cài đặt hệ thống sinh đề có chứng nhận Lean

Thiết kế: `thiet-ke-pipeline-sinh-de-v1.2.md`. Mã nguồn: thư mục `sinh-de-gt1/` của repo này.

**Nơi làm việc** (từ 25/11): bản clone trong Ubuntu `~/MATH_EXAM_SOVEREIGN_WEB`, mở từ Windows tại `\\wsl.localhost\Ubuntu-24.04\home\duc_huy\MATH_EXAM_SOVEREIGN_WEB`. Cache Mathlib và môi trường Python chỉ có ở bản này. Bản ở ổ D: dùng để xem tài liệu; trước khi sửa ở đó, chạy `git pull` để lấy thay đổi mới nhất.

Trạng thái: **xong M0** (1/9 mốc). Chưa sinh được câu hỏi nào; câu đầu tiên có chứng nhận sẽ có ở M4.

---

## 23/11/2026 — Thiết kế và chuẩn bị máy

**Thiết kế**
- Cập nhật thiết kế từ v1.1 lên v1.2 (Phụ lục B): cổng kiểm cuối so ở mức `Expr` bằng tiện ích `kiem_khop`; thêm công cụ đạo hàm và chiến lược L'Hospital; sửa bảng ưu tiên của `in_chuoi`; hướng dẫn chạy trên WSL2; tách mẫu ngẫu nhiên khi tính cận trên.
- Commit `ee5295a` và push lên GitHub (repo `MATH_EXAM_SOVEREIGN_WEB`).

**Chuẩn bị máy**
- Chuyển ổ ảo Ubuntu-24.04 từ ổ C: sang `D:\WSL\Ubuntu-24.04` (ổ C: chỉ còn 9,6 GB).
- Tạo `C:\Users\DUC HUY\.wslconfig`: giới hạn RAM cho WSL, swap 8 GB đặt ở `D:\WSL\swap.vhdx`.
- Cài Docker Engine (`docker.io`) trong Ubuntu, thêm tài khoản `duc_huy` vào nhóm `docker`.
- Cài elan 4.4.0, Claude Code 2.1.330 và `uv` trong Ubuntu.
- Tạo repo `~/sinh-de-gt1`, chép tài liệu thiết kế vào `docs/`.

## 24/11/2026 — Mốc M0 và ba thử nghiệm rủi ro

**M0: khung dự án** (commit `0c24105`)
| Thành phần | Nội dung |
|---|---|
| Phiên bản cố định | Lean 4.36.0, Mathlib tag v4.36.0; cache Mathlib đã tải sẵn (khoảng 7,3 GB) |
| Python | Môi trường ảo bằng `uv`; `pyproject.toml`; `config.yaml` có kiểm kiểu (`sinhde/cau_hinh.py`) |
| Lệnh `sinhde` | `cau-hinh`, `nen-tang kiem`, `nen-tang lam-nong` |
| Sandbox | Ảnh Docker `sinhde-lean`, `sandbox/chay_lean.sh`: không mạng, dự án chỉ đọc, giới hạn RAM và thời gian |
| `LeanRunner` | `sinhde/lean/chay_lean.py`: ba chế độ `kiem_tep_tam`, `build_module`, `kiem_khop`; mọi lần chạy ghi vào CSDL |
| CSDL | `sinhde/luu_tru/schema.sql`: 8 bảng theo mục 10 của thiết kế |
| Lean | Dự án `lean/`: `ThuVienGT` còn rỗng, đã import phần Mathlib cần dùng |

Nghiệm thu M0 (mục 17): `lake build` chạy trong sandbox, `pytest` chạy được, Lean truy cập mạng bị chặn. **Đạt.**

**Sửa ba thử nghiệm rủi ro** (commit `ccc2a26`; chi tiết trong `docs/ket_qua_M0.md` của repo mới)
| Thử nghiệm | Kết quả |
|---|---|
| 1. Tốc độ Lean trong container | Nạp toàn bộ Mathlib: lần lạnh 351 s. Chỉ import phần cần (1,45 GB): **lần lạnh 21 s, các lần sau 2–3 s**. `ThuVienGT` đã chuyển sang import cụ thể |
| 2. `decide` trên `chuanHoa` (mục 7.9, 12.6) | `decide` thường không chạy; **`decide +kernel` đạt 50/50 cây**, trung bình 69 ms mỗi cây (giới hạn 10 s) |
| 3. Tiện ích `kiem_khop` (mục 12.7) | Chạy thành chương trình Lean có đầu vào và đầu ra JSON; 8/8 kiểm thử đạt. Module tấn công dùng `macro_rules` đổi "2 + 2 = 4" thành `True`: **cổng kiểm văn bản kiểu v1.1 bị lừa, `kiem_khop` chặn đúng** |

Kiểm thử: 6 kiểm thử thường và 16 kiểm thử sandbox, đều đạt.

**Sự cố bộ nhớ Windows**
- Khi Lean nạp Mathlib, Windows cạn bộ nhớ commit và tắt máy ảo Ubuntu (3 lần). Đã khởi động lại Windows.
- Nguyên nhân chính: tiến trình `fczf` (do `fclauncher.exe` khởi chạy) chiếm khoảng 4,8 GB từ lúc mở máy, cộng với WSL.
- Đã hạ RAM cho WSL từ 10 GB xuống 8 GB.

## 25/11/2026 — Rà hệ thống cũ, chuẩn bị M1

- Đọc hệ thống cũ trong repo này. Các câu hỏi cũ do LLM sinh, chưa kiểm chứng, nên **không dùng làm dữ liệu**. Một số phần code để dành cho các mốc sau: `lean_prover.py` (M6–M7), `llm_generator.py` và `lean_retrieval.py` (M7), các script benchmark (M7–M8), giao diện `app.py`, `static/` (sau M8, bỏ phần sinh câu bằng LLM, randomize và phòng thí nghiệm chạy mã).
- Bắt đầu M1 rồi dừng theo yêu cầu; đã xóa phần làm dở. Repo mới sạch ở commit `ccc2a26`.
- **Gộp vào repo chung:** đưa code M0 vào thư mục `sinh-de-gt1/` của repo `MATH_EXAM_SOVEREIGN_WEB` bằng `git subtree`, giữ lịch sử 2 commit; push lên GitHub (commit `0b01f0c`).
- **Một chỗ làm việc duy nhất:** clone repo chung vào Ubuntu (`~/MATH_EXAM_SOVEREIGN_WEB`); chuyển cache Mathlib (7,5 GB) sang, tạo lại `.venv`; git trong Ubuntu dùng chung đăng nhập GitHub của Windows (Git Credential Manager). Kiểm thử chạy lại ở chỗ mới đều đạt. Đã xóa bản cũ `~/sinh-de-gt1`.

---

## Việc tiếp theo
- **M1**: văn phạm N1, cây biểu thức, bộ in chuỗi, chuẩn hóa (Python, mục 6).

## Còn treo
- Nên tắt `fclauncher` trước khi chạy Lean nhiều; có thể thêm pagefile trên ổ D: để Windows không cạn bộ nhớ.
