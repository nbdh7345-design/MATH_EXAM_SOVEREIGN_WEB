# Nhật ký cài đặt hệ thống sinh đề có chứng nhận Lean

Thiết kế đang dùng: **`thiet-ke-v2.1.md`** (câu trắc nghiệm, mọi dạng bài; từ 26/11). Các bản cũ v1.1, v1.2, v2.0 giữ lại để đối chiếu. Mã nguồn: thư mục `sinh-de-gt1/` của repo này.

**Nơi làm việc** (từ 25/11): bản clone trong Ubuntu `~/MATH_EXAM_SOVEREIGN_WEB`, mở từ Windows tại `\\wsl.localhost\Ubuntu-24.04\home\duc_huy\MATH_EXAM_SOVEREIGN_WEB`. Cache Mathlib và môi trường Python chỉ có ở bản này. Bản ở ổ D: dùng để xem tài liệu; trước khi sửa ở đó, chạy `git pull` để lấy thay đổi mới nhất.

Trạng thái: **xong M0, M1 theo v2.1** (lõi M0–M8, mở rộng M9–M15). Chưa sinh được câu hỏi nào; câu trắc nghiệm đầu tiên có chứng nhận sẽ có ở M4.

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

## 26/11/2026 — Mốc M1: nền tảng N1 (mục 6)

| Thành phần | Tệp trong `sinh-de-gt1/` | Nội dung |
|---|---|---|
| Văn phạm | `sinhde/nen_tang/van_pham.lark` | Biểu thức, ràng buộc tham số, điểm giới hạn; LALR strict, không xung đột |
| Bộ đọc | `sinhde/nen_tang/van_pham.py` | `doc_bieu_thuc`, `doc_dieu_kien`, `doc_diem`; lỗi `LoiVanPham` kèm dòng, cột |
| Cây biểu thức | `sinhde/nen_tang/cay.py` | 11 loại nút, ràng buộc; `to_sexpr` khớp `BT.toSExpr` của Lean; JSON hai chiều; tiện ích (độ sâu, số nút, thay tham số…) |
| Bộ in chuỗi | `sinhde/nen_tang/in_chuoi.py` | Theo bảng mức ưu tiên đã sửa ở v1.2 (`So` phân số mức 2, `So` âm mức 3) |
| Chuẩn hóa | `sinhde/nen_tang/chuan_hoa.py` | Đúng bảng 6.5, giống từng dòng `chuanHoa` của Lean |
| Đa thức theo tham số | `sinhde/nen_tang/da_thuc_tham_so.py` | Kiểm dạng đa thức; tính chính xác bằng `Fraction`; đánh giá ràng buộc |
| Tính giá trị | `sinhde/nen_tang/danh_gia.py` | Giá trị và điều kiện xác định theo `XacDinh` (Fraction + mpmath); dùng cho kiểm thử và sau này cho phép thử T2 |
| Công cụ | `tools/kiem_van_pham.py` | Kiểm văn phạm không xung đột LALR, không va chạm token |

Nghiệm thu (mục 6.7): **đạt**, 97 kiểm thử N1:
- chuỗi hợp lệ cho đúng cây; chuỗi bị cấm (`sin x`, `2x`, `log(x)`, `x^1.5`, `e*x`…) bị từ chối;
- 12 tên hàm, từ khóa và 20 chữ cái tham số được tách đúng;
- theo tính chất: khứ hồi chuỗi trên 5000 cây, chuẩn hóa lũy đẳng (2000 cây), chuẩn hóa giữ giá trị và điều kiện xác định tại điểm hữu tỉ (2000 cây), JSON hai chiều, khứ hồi ràng buộc.

Toàn bộ 103 kiểm thử không cần Lean đều đạt. Thêm phụ thuộc `interegular` (Lark cần để kiểm va chạm token ở chế độ strict).

---

## 26/11/2026 — Chuyển sang thiết kế v2.1 và mở rộng M1

**Thiết kế:** người dùng viết bản v2.0 (câu trắc nghiệm 4 phương án, mệnh đề chung `TracNghiemDung`, kiểu đáp án T1–T4, toàn bộ dạng bài trắc nghiệm, lộ trình M0–M15). Sau rà soát, tạo bản v2.1 với 10 sửa đổi (Phụ lục B.3), quan trọng nhất là khôi phục cổng kiểm cuối ở mức `Expr` (`kiem_khop`). Commit `cefe378`.

**M1 theo v2.1** (mục 6): mở rộng từ N1 của bản 1.2, giữ lõi và thêm:
| Phần | Thay đổi |
|---|---|
| Văn phạm `van_pham.lark` | Biến `x, y, t, n`; ẩn `m`; `pi`, `e`; `luythua`; `tp(f, a, b)`; tập (`rong`, `{…}`, khoảng `kmo/kdong/ktrai/kphai`, hợp `U`, vô cùng `vc`, `-vc`); điểm ℝ²; phương án đặc biệt. Điểm bắt đầu: `bieu_thuc`, `dieu_kien`, `tap`, `diem2`, `dac_biet`. Vẫn LALR strict, không xung đột |
| Bộ đọc `van_pham.py` | Thêm `doc_tap`, `doc_diem2`, `doc_dac_biet`, `doc_phuong_an(chuoi, kieu)`; kiểm chung `E_LUYTHUA_NGUYEN` và `E_BIEN_T`; lỗi mang mã |
| Cây `cay.py` | Nút `Bien(ten)`, `An`, `Pi`, `TichPhanT`; phương án `DacBiet`, `Khoang`, `VoCung`, `TapHuuHan`, `HopKhoang`, `TapRong`, `Diem2`, `KhangDinh`; `bien_dung`, `bien_tu_do`, `chi_chua_tham_so`; `to_sexpr` cho mọi nút (biến thành `(bien x)`); JSON tổng quát |
| `in_chuoi.py` | In mọi nút mới và phương án; `exp(1)` in là `e` |
| `chuan_hoa.py` | Thêm quy tắc v2.1: `e^n → exp(n)`, `luythua(e, b) → exp(b)`; tích phân chuẩn hóa các con; `chuan_hoa_pa` không sắp xếp, không bỏ phần tử trùng |
| `bieu_thuc_tham_so.py` (thay `da_thuc_tham_so.py`) | Ràng buộc là phân thức hữu tỉ, tự thêm điều kiện "mẫu ≠ 0"; `danh_gia_rang_buoc`, `mien_hop_le`, `la_hang_theo_tham_so` |
| `danh_gia.py` | Tính giá trị với nhiều biến, ẩn m, π |

Kiểm thử: 124 kiểm thử N1, gồm khứ hồi 5000 cây có đủ nút mới, lũy đẳng, giữ giá trị (nhiều biến, π, m), khứ hồi tập và khoảng (3000), ràng buộc, phương án đặc biệt. Toàn bộ 130 kiểm thử không cần Lean đều đạt.

Ghi lại cho các mốc sau: văn phạm v2.1 chưa có cú pháp cho **hàm từng khúc** (cần ở M12) và **tập điểm trong ℝ²** (cần ở M15).

---

## Việc tiếp theo
- **M2** (theo v2.1): thư viện Lean lõi `ThuVienGT`: `BT` tổng quát, `GanBien`, `XacDinh`, `chuanHoa`, kiểu giá trị đáp án, `TracNghiemDung`, Q và định nghĩa của giới hạn, kẹp số. Đây là mốc lớn nhất; cần thông tin giáo trình đối chiếu (câu hỏi mở 1) trước khi kết thúc M2.

## Còn treo
- Nên tắt `fclauncher` trước khi chạy Lean nhiều; có thể thêm pagefile trên ổ D: để Windows không cạn bộ nhớ.
